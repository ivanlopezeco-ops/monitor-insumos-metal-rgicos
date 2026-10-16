"""Descarga de fuentes. Cada función recibe el contexto de la corrida (ctx) y devuelve un DataFrame largo:
fecha | id | valor | unidad | fuente | marca     (marca: "" o "provisorio")

Los ids son los del catálogo (config/catalogo.yaml). Algunas fuentes también guardan series auxiliares
(tipos de cambio, stocks de otros metales) con ids propios.
"""
import datetime as dt
import io
import json
import re
import time
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

import pandas as pd
import requests
import urllib3

urllib3.disable_warnings()
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36",
      "Accept-Language": "es-AR,es;q=0.9,en;q=0.8"}
SEC_UA = {"User-Agent": "ADIMRA Estudios Economicos estudios@adimra.org.ar"}
HOY = dt.datetime.now(ZoneInfo("America/Argentina/Buenos_Aires")).date()
COLS = ["fecha", "id", "valor", "unidad", "fuente", "marca"]


def _get(url, intentos=3, metodo="GET", **kw):
    """GET/POST con reintentos ante errores transitorios (5xx, 429, cortes)."""
    kw.setdefault("headers", UA)
    kw.setdefault("timeout", 90)
    kw.setdefault("verify", False)
    for i in range(intentos):
        try:
            r = requests.request(metodo, url, **kw)
            if (r.status_code >= 500 or r.status_code == 429) and i < intentos - 1:
                time.sleep(12 if r.status_code == 429 else 4 * (i + 1))
                continue
            r.raise_for_status()
            return r
        except (requests.ConnectionError, requests.Timeout):
            if i == intentos - 1:
                raise
            time.sleep(4 * (i + 1))
    r.raise_for_status()
    return r


def _df(filas):
    df = pd.DataFrame(filas, columns=COLS)
    if df.empty:
        return df
    df["fecha"] = pd.to_datetime(df["fecha"]).dt.date
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce")
    df["marca"] = df["marca"].fillna("")
    return df.dropna(subset=["valor"])


def _num(x):
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip().replace(",", "")
    try:
        return float(s)
    except ValueError:
        return None


def accesos(ctx, prefijo):
    """{código: id} a partir del campo 'acceso' del catálogo (ej. 'API BOJ, PRCG20_...')."""
    out = {}
    for s in ctx.series_catalogo:
        a = (s.get("fuente") or {}).get("acceso", "")
        if a.startswith(prefijo):
            out[a.split(",", 1)[1].strip()] = s["id"]
    return out


# ================================================================ BCRA: A3500 y tipos de pase
def bcra_a3500(ctx):
    filas, offset, total = [], 0, 1
    ini = dt.date(2008, 1, 1) if ctx.completo("tc_a3500") else HOY - dt.timedelta(days=60)
    while offset < total:
        j = _get(f"https://api.bcra.gob.ar/estadisticas/v4.0/monetarias/5?desde={ini}&hasta={HOY}&limit=3000&offset={offset}").json()
        total = j.get("metadata", {}).get("resultset", {}).get("count", 0)
        for r in j["results"]:
            for d in r["detalle"]:
                filas.append((d["fecha"], "tc_a3500", d["valor"], "ARS/USD", "BCRA (A3500)", ""))
        offset += 3000
    return _df(filas)


def bcra_monedas(ctx):
    """USD por yuan y por euro (tipo de pase del BCRA), en ventanas de 90 días."""
    filas, errores = [], []
    for mon, vid in [("CNY", "usd_por_cny"), ("EUR", "usd_por_eur")]:
        ini = dt.date(2008, 1, 1) if ctx.completo(vid) else HOY - dt.timedelta(days=30)
        while ini <= HOY:
            fin = min(ini + dt.timedelta(days=89), HOY)
            try:
                url = f"https://api.bcra.gob.ar/estadisticascambiarias/v1.0/Cotizaciones/{mon}?fechadesde={ini}&fechahasta={fin}"
                for r in _get(url).json().get("results", []):
                    for d in r["detalle"]:
                        if d.get("tipoPase"):
                            filas.append((r["fecha"], vid, d["tipoPase"], f"USD/{mon}", "BCRA (tipo de pase)", ""))
            except Exception as e:  # noqa: BLE001
                errores.append(f"{mon} {ini}: {e}"[:120])
            ini = fin + dt.timedelta(days=1)
    df = _df(filas)
    df.attrs["errores"] = errores[:5]
    if df.empty:
        raise RuntimeError("; ".join(errores[:3]))
    return df


# ================================================================ Yahoo (futuros CME / COMEX)
def yahoo(ctx):
    filas, errores = [], []
    p1 = int(dt.datetime(2000, 1, 1).timestamp())
    for ticker, sid in accesos(ctx, "Yahoo chart API").items():
        try:
            j = _get(f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}",
                     params={"period1": p1, "period2": int(time.time()), "interval": "1d"}).json()["chart"]["result"][0]
            q = j.get("indicators", {}).get("quote", [{}])[0]
            for ts, c in zip(j.get("timestamp") or [], q.get("close") or []):
                if c is not None:
                    f = dt.datetime.utcfromtimestamp(ts).date()
                    filas.append((f, sid, c, "", f"CME vía Yahoo Finance ({ticker})", "provisorio" if f >= HOY else ""))
        except Exception as e:  # noqa: BLE001
            errores.append(f"{ticker}: {e}"[:120])
    df = _df(filas)
    df.attrs["errores"] = errores
    return df


# ================================================================ Westmetall (LME y cotizaciones alemanas)
WESTMETALL = {  # campo: [(columna, id), ...]  columna 1 = contado, 3 = stock
    "LME_Cu_cash": [(1, "cobre_lme"), (3, "cobre_lme_stock")],
    "LME_Al_cash": [(1, "aluminio_lme"), (3, "aluminio_lme_stock")],
    "LME_Ni_cash": [(1, "niquel_lme"), (3, "niquel_lme_stock")],
    "LME_Zn_cash": [(1, "zinc_lme"), (3, "zinc_lme_stock")],
    "LME_Sn_cash": [(1, "estano_lme"), (3, "estano_lme_stock")],
    "LME_Pb_cash": [(1, "plomo_lme"), (3, "plomo_lme_stock")],
    "WM_Cu_low": [(1, "cobre_alemania")],
    "MB_MS_58_1": [(1, "laton_alemania")],
}


def westmetall(ctx):
    filas, errores = [], []
    for campo, cols in WESTMETALL.items():
        completo = ctx.completo(cols[0][1])
        anios = [None] + (list(range(HOY.year - 1, 2007, -1)) if completo else ([HOY.year - 1] if HOY.month == 1 else []))
        for anio in anios:
            try:
                p = {"action": "table", "field": campo}
                if anio:
                    p["year"] = anio
                t = pd.read_html(io.StringIO(_get("https://www.westmetall.com/en/markdaten.php", params=p).text))[0]
                fechas = pd.to_datetime(t.iloc[:, 0], format="%d. %B %Y", errors="coerce")
                for i, sid in cols:
                    if i >= t.shape[1]:
                        continue
                    for f, v in zip(fechas, t.iloc[:, i]):
                        if pd.notna(f):
                            filas.append((f.date(), sid, _num(v), "", "LME vía Westmetall" if campo.startswith("LME") else "Westmetall", ""))
            except Exception as e:  # noqa: BLE001
                errores.append(f"{campo} {anio}: {e}"[:120])
    df = _df(filas)
    df.attrs["errores"] = errores[:6]
    return df


# ================================================================ Banco Mundial (Pink Sheet)
PINK = {"iron ore, cfr spot": "mineral_banco_mundial", "copper": "cobre_banco_mundial", "aluminum": "aluminio_banco_mundial",
        "nickel": "niquel_banco_mundial", "zinc": "zinc_banco_mundial", "tin": "estano_banco_mundial", "lead": "plomo_banco_mundial"}


def pink_sheet(ctx):
    pag = _get("https://www.worldbank.org/en/research/commodity-markets").text
    link = re.findall(r'https://thedocs\.worldbank\.org/[^"\']+CMO-Historical-Data-Monthly\.xlsx', pag)[0]
    x = pd.read_excel(io.BytesIO(_get(link, timeout=180).content), sheet_name="Monthly Prices", header=None)
    fila = x.index[x.iloc[:, 1].astype(str).str.contains("Crude oil", na=False)][0]
    nombres = [str(c).strip().lower() for c in x.iloc[fila]]
    datos = x.iloc[fila + 2:]
    filas = []
    for col, sid in PINK.items():
        if col not in nombres:
            continue
        j = nombres.index(col)
        for p, v in zip(datos.iloc[:, 0], datos.iloc[:, j]):
            m = re.match(r"(\d{4})M(\d{2})", str(p))
            if m:
                filas.append((dt.date(int(m[1]), int(m[2]), 1), sid, _num(v), "", "Banco Mundial (Pink Sheet)", ""))
    return _df(filas)


# ================================================================ Bolsas chinas (SHFE y ZCE)
SHFE = {"hc": "hrc_china_futuro", "rb": "barra_china_futuro", "wr": "alambron_china_futuro", "ss": "inox_china_futuro",
        "cu": "cobre_shfe", "al": "aluminio_shfe", "ni": "niquel_shfe", "zn": "zinc_shfe", "sn": "estano_shfe", "pb": "plomo_shfe"}
ZCE = {"SF": "ferrosilicio_china_futuro", "SM": "silicomanganeso_china_futuro"}


def _dias_a_pedir(ctx, clave, primero, tope_backfill=250, recientes=8):
    """Días recientes + un tramo hacia atrás del relleno histórico (cursor guardado en el estado)."""
    dias = [HOY - dt.timedelta(days=i) for i in range(recientes)]
    cur = ctx.cursor.get(clave)
    cur = dt.date.fromisoformat(cur) if cur else HOY - dt.timedelta(days=recientes)
    n = 0
    while cur > primero and n < tope_backfill:
        if cur.weekday() < 5:
            dias.append(cur)
            n += 1
        cur -= dt.timedelta(days=1)
    ctx.cursor[clave] = str(max(cur, primero))
    return [d for d in dias if d.weekday() < 5]


def shfe(ctx):
    filas, errores, vistos = [], [], 0
    for d in _dias_a_pedir(ctx, "shfe", dt.date(2010, 1, 4)):
        try:
            r = requests.get(f"https://www.shfe.com.cn/data/tradedata/future/dailydata/kx{d:%Y%m%d}.dat",
                             headers={**UA, "Referer": "https://www.shfe.com.cn/"}, timeout=40, verify=False)
            if r.status_code != 200 or not r.text.lstrip().startswith("{"):
                continue
            vistos += 1
            mejor = {}
            for x in r.json().get("o_curinstrument", []):
                prod = re.sub(r"_f$", "", (x.get("PRODUCTID") or "").strip())
                mes = str(x.get("DELIVERYMONTH") or "").strip()
                if prod not in SHFE or not mes.isdigit():
                    continue
                oi, pr = _num(x.get("OPENINTEREST")) or 0, _num(x.get("SETTLEMENTPRICE")) or _num(x.get("CLOSEPRICE"))
                if pr and (prod not in mejor or oi > mejor[prod][0]):
                    mejor[prod] = (oi, pr, mes)
            for prod, (_, pr, mes) in mejor.items():
                filas.append((d, SHFE[prod], pr, "CNY/t con IVA", f"SHFE (contrato más negociado, {prod}{mes})", ""))
            time.sleep(0.15)
        except Exception as e:  # noqa: BLE001
            errores.append(f"{d}: {e}"[:100])
    df = _df(filas)
    df.attrs["errores"] = errores[:5]
    df.attrs["detalle"] = f"{vistos} días con archivo; relleno hasta {ctx.cursor.get('shfe')}"
    return df


def zce(ctx):
    filas, errores, vistos = [], [], 0
    for d in _dias_a_pedir(ctx, "zce", dt.date(2016, 1, 4)):
        try:
            r = requests.get(f"http://www.czce.com.cn/cn/DFSStaticFiles/Future/{d:%Y}/{d:%Y%m%d}/FutureDataDaily.txt",
                             headers=UA, timeout=40)
            if r.status_code != 200 or len(r.content) < 500:
                continue
            vistos += 1
            r.encoding = r.apparent_encoding
            mejor = {}
            for linea in r.text.splitlines():
                p = [c.strip() for c in linea.split("|")]
                m = re.match(r"^([A-Z]{2})(\d{3,4})$", p[0]) if p else None
                if not m or m[1] not in ZCE or len(p) < 11:
                    continue
                pr, oi = _num(p[6]), _num(p[10]) or 0
                if pr and (m[1] not in mejor or oi > mejor[m[1]][0]):
                    mejor[m[1]] = (oi, pr, p[0])
            for prod, (_, pr, c) in mejor.items():
                filas.append((d, ZCE[prod], pr, "CNY/t con IVA", f"ZCE (contrato más negociado, {c})", ""))
            time.sleep(0.15)
        except Exception as e:  # noqa: BLE001
            errores.append(f"{d}: {e}"[:100])
    df = _df(filas)
    df.attrs["errores"] = errores[:5]
    df.attrs["detalle"] = f"{vistos} días con archivo; relleno hasta {ctx.cursor.get('zce')}"
    return df


# ================================================================ NBS China (precios cada 10 días)
NBS = [("螺纹钢", "barra_china_spot"), ("线材", "alambron_china_spot"), ("普通中板", "chapa_gruesa_china_spot"),
       ("热轧普通板卷", "hrc_china_spot"), ("无缝钢管", "tubo_sin_costura_china_spot"), ("角钢", "angulo_china_spot"),
       ("焦煤", "carbon_coque_china_spot"), ("焦炭", "coque_china_spot"), ("电解铜", "cobre_china_spot"),
       ("铝锭", "aluminio_china_spot"), ("锌锭", "zinc_china_spot")]
NBS_LISTA = "https://www.stats.gov.cn/sj/zxfb/"


def _fecha_decada(anio, mes, dec):
    if dec == "上":
        return dt.date(anio, mes, 10)
    if dec == "中":
        return dt.date(anio, mes, 20)
    return (dt.date(anio + (mes == 12), mes % 12 + 1, 1) - dt.timedelta(days=1))


def nbs(ctx):
    ya = set(ctx.fechas("hrc_china_spot"))
    pagina_bf = int(ctx.cursor.get("nbs_pagina", 3))
    paginas = list(range(0, 3)) + list(range(pagina_bf, pagina_bf + 12))
    filas, errores, informes, sin = [], [], 0, 0
    for p in paginas:
        url = NBS_LISTA + ("index.html" if p == 0 else f"index_{p}.html")
        try:
            r = _get(url, intentos=2)
        except Exception as e:  # noqa: BLE001
            errores.append(f"pág {p}: {e}"[:100])
            if p >= pagina_bf:
                sin += 1
            continue
        r.encoding = "utf-8"
        links = re.findall(r'href="([^"]+)"[^>]*>\s*([^<]*?(\d{4})年(\d{1,2})月([上中下])旬流通领域重要生产资料市场价格变动情况)', r.text)
        if p >= pagina_bf and not links:
            sin += 1
        for href, _, a, m, dcd in dict.fromkeys(links):
            f = _fecha_decada(int(a), int(m), dcd)
            if f in ya:
                continue
            try:
                inf = _get(urljoin(url, href), intentos=2)
                inf.encoding = "utf-8"
                t = pd.read_html(io.StringIO(inf.text))[0]
                for fila in t.fillna("").astype(str).values.tolist():
                    nombre = fila[0].strip()
                    for clave, sid in NBS:
                        if nombre.startswith(clave):
                            filas.append((f, sid, _num(fila[2]), "CNY/t con IVA", "NBS China", ""))
                            break
                ya.add(f)
                informes += 1
            except Exception as e:  # noqa: BLE001
                errores.append(f"{f}: {e}"[:100])
    ctx.cursor["nbs_pagina"] = pagina_bf + 12 if sin < 6 else pagina_bf   # cuando se acaban las páginas, deja de retroceder
    df = _df(filas)
    df.attrs["errores"] = errores[:5]
    df.attrs["detalle"] = f"{informes} informes nuevos; próxima página de relleno {ctx.cursor['nbs_pagina']}"
    return df


# ================================================================ BLS (índices de productor de EE.UU.)
def bls(ctx):
    series = accesos(ctx, "API BLS v2")
    completo = any(ctx.completo(s) for s in series.values())
    tramos = [(a, min(a + 9, HOY.year)) for a in range(1980, HOY.year + 1, 10)] if completo else [(HOY.year - 1, HOY.year)]
    filas, mensajes = [], []
    for a, b in tramos:
        j = _get("https://api.bls.gov/publicAPI/v2/timeseries/data/", metodo="POST",
                 json={"seriesid": list(series), "startyear": str(a), "endyear": str(b)},
                 headers={**UA, "Content-type": "application/json"}).json()
        if j.get("status") != "REQUEST_SUCCEEDED":
            raise RuntimeError(f"BLS: {j.get('status')} {j.get('message')}")
        mensajes += [m for m in j.get("message", []) if "does not exist" in m]
        for s in j["Results"]["series"]:
            for d in s["data"]:
                if not d["period"].startswith("M") or d["period"] == "M13":
                    continue
                prov = any(fn.get("code") == "P" for fn in d.get("footnotes", []) if fn)
                filas.append((dt.date(int(d["year"]), int(d["period"][1:]), 1), series[s["seriesID"]], _num(d["value"]), "",
                              f"BLS ({s['seriesID']})", "provisorio" if prov else ""))
    df = _df(filas)
    df.attrs["errores"] = mensajes
    return df


# ================================================================ Comex Stat (Brasil)
COMEX = [  # (id, flujo, prefijos NCM, métrica)
    ("hrc_brasil_export", "export", ["7208"], "metricFOB"),
    ("frio_brasil_export", "export", ["7209"], "metricFOB"),
    ("galv_brasil_export", "export", ["7210"], "metricFOB"),
    ("barra_brasil_export", "export", ["7214"], "metricFOB"),
    ("semis_brasil_export", "export", ["7207"], "metricFOB"),
    ("mineral_brasil_export", "export", ["26011100"], "metricFOB"),
    ("arrabio_brasil_export", "export", ["72011000"], "metricFOB"),
    ("carbon_coque_brasil_import", "import", ["27011200"], "metricCIF"),
]


def comexstat(ctx):
    lista = _get("https://api-comexstat.mdic.gov.br/general/filters/ncm?language=pt", timeout=120).text
    ncms = sorted(set(re.findall(r'"(\d{8})"', lista)))
    filas, errores = [], []
    for sid, flujo, pref, met in COMEX:
        codigos = [n for n in ncms if any(n.startswith(p) for p in pref)] or pref
        ini = "1997-01" if ctx.completo(sid) else f"{HOY.year - 1}-01"
        body = {"flow": flujo, "monthDetail": True, "period": {"from": ini, "to": f"{HOY.year}-12"},
                "filters": [{"filter": "ncm", "values": codigos}], "details": ["ncm"], "metrics": ["metricFOB", "metricKG"] + (["metricCIF"] if flujo == "import" else [])}
        try:
            time.sleep(11)
            j = _get("https://api-comexstat.mdic.gov.br/general", metodo="POST", json=body, timeout=240).json()
            d = pd.DataFrame(j["data"]["list"])
            if d.empty:
                continue
            for c in [met, "metricKG"]:
                d[c] = pd.to_numeric(d[c], errors="coerce")
            g = d.groupby(["year", "monthNumber"])[[met, "metricKG"]].sum()
            for (a, m), x in g.iterrows():
                if x["metricKG"] > 0:
                    filas.append((dt.date(int(a), int(m), 1), sid, x[met] / x["metricKG"] * 1000, "USD/t", "Comex Stat (Brasil)", ""))
                    filas.append((dt.date(int(a), int(m), 1), sid + "_toneladas", x["metricKG"] / 1000, "t", "Comex Stat (Brasil)", ""))
        except Exception as e:  # noqa: BLE001
            errores.append(f"{sid}: {e}"[:120])
    df = _df(filas)
    df.attrs["errores"] = errores
    if df.empty and errores:
        raise RuntimeError("; ".join(errores[:3]))
    return df


# ================================================================ Eurostat Comext (comercio de la UE)
COMEXT = [("hrc_ue_import_china", "7208", "CN", "1"), ("barra_turquia_ue", "7214", "TR", "1"), ("chatarra_ue_turquia", "7204", "TR", "2")]


def comext(ctx):
    base = "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-045409"
    filas, errores = [], []
    for sid, prod, socio, flujo in COMEXT:
        desde = "2002-01" if ctx.completo(sid) else f"{HOY.year - 2}-01"
        val = {}
        try:
            for ind in ["VALUE_IN_EUROS", "QUANTITY_IN_100KG"]:
                j = _get(base, params={"freq": "M", "reporter": "EU", "partner": socio, "product": prod, "flow": flujo,
                                       "indicators": ind, "sinceTimePeriod": desde, "format": "JSON"}, timeout=180).json()
                inv = {v: k for k, v in j["dimension"]["time"]["category"]["index"].items()}
                val[ind] = {inv[int(k)]: v for k, v in j.get("value", {}).items()}
            for per, eur in val["VALUE_IN_EUROS"].items():
                q = val["QUANTITY_IN_100KG"].get(per)
                if q:
                    f = dt.date(int(per[:4]), int(per[5:7]), 1)
                    filas.append((f, sid, eur / (q / 10), "EUR/t", "Eurostat Comext", ""))
                    filas.append((f, sid + "_toneladas", q / 10, "t", "Eurostat Comext", ""))
        except Exception as e:  # noqa: BLE001
            errores.append(f"{sid}: {e}"[:120])
    df = _df(filas)
    df.attrs["errores"] = errores
    return df


# ================================================================ Eurostat (índices de productor)
def eurostat_ppi(ctx):
    filas = []
    for geo in ["EU27_2020", "DE", "IT", "ES", "FR"]:
        j = _get("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_inppd_m",
                 params={"geo": geo, "nace_r2": "C241", "unit": "I21", "s_adj": "NSA"}).json()
        inv = {v: k for k, v in j["dimension"]["time"]["category"]["index"].items()}
        sid = "acero_ue_indice" if geo == "EU27_2020" else f"acero_ue_indice_{geo.lower()}"
        for k, v in j.get("value", {}).items():
            per = inv[int(k)]
            filas.append((dt.date(int(per[:4]), int(per[5:7]), 1), sid, v, "índice 2021=100", f"Eurostat sts_inppd_m ({geo})", ""))
    return _df(filas)


# ================================================================ Banco de Japón
def boj(ctx):
    codigos = accesos(ctx, "API BOJ")
    inicio = "198001" if any(ctx.completo(s) for s in codigos.values()) else f"{HOY.year - 2}01"
    filas, pos = [], None
    for _ in range(20):
        p = {"format": "json", "lang": "en", "db": "PR01", "code": ",".join(codigos), "startDate": inicio}
        if pos:
            p["startPosition"] = pos
        j = _get("https://www.stat-search.boj.or.jp/api/v1/getDataCode", params=p, timeout=120).json()
        for s in j.get("RESULTSET", []):
            sid = codigos.get(s.get("SERIES_CODE"))
            v = s.get("VALUES") or {}
            fechas, valores = v.get("SURVEY_DATES") or [], v.get("VALUES") or []
            for f, x in zip(fechas, valores):
                f = str(f)
                if sid and len(f) >= 6 and x not in (None, ""):
                    filas.append((dt.date(int(f[:4]), int(f[4:6]), 1), sid, x, "índice 2020=100", f"Banco de Japón ({s['SERIES_CODE']})", ""))
        pos = j.get("NEXTPOSITION")
        if not pos:
            break
    df = _df(filas)
    if df.empty:
        raise RuntimeError(f"Sin datos; respuesta: {json.dumps(j)[:300]}")
    return df


# ================================================================ IBGE (IPP Brasil, metalurgia)
def ibge(ctx):
    j = _get("https://apisidra.ibge.gov.br/values/t/6903/n1/all/v/all/p/all/c842/46641", timeout=180).json()
    filas = [x for x in j[1:]]
    variables = {x["D2C"]: x["D2N"] for x in filas}
    vind = next((c for c, n in variables.items() if "índice" in n.lower() and "varia" not in n.lower()), None)
    out = []
    if vind:
        for x in filas:
            if x["D2C"] == vind:
                out.append((dt.date(int(x["D3C"][:4]), int(x["D3C"][4:]), 1), "metalurgia_brasil_indice", _num(x["V"]), "índice dic-2018=100", "IBGE (tabla 6903)", ""))
    else:   # se reconstruye el índice encadenando la variación mensual
        vmm = next(c for c, n in variables.items() if "M/M-1" in n)
        nivel = 100.0
        for x in sorted([x for x in filas if x["D2C"] == vmm], key=lambda x: x["D3C"]):
            v = _num(x["V"])
            if v is None:
                continue
            nivel *= 1 + v / 100
            out.append((dt.date(int(x["D3C"][:4]), int(x["D3C"][4:]), 1), "metalurgia_brasil_indice", nivel, "índice", "IBGE (tabla 6903, encadenado)", ""))
    df = _df(out)
    df.attrs["detalle"] = f"variables: {variables}"
    return df


# ================================================================ India (índice mayorista por ítem)
INDIA = {"1314010014": "barras_india_indice", "1201010100": "carbon_coque_india_indice",
         "1314010003": "arrabio_india_indice", "1314010001": "dri_india_indice"}


def india(ctx):
    pag = _get("https://eaindustry.nic.in/download_data_2223.asp").text
    link = sorted(re.findall(r'(indx_download_2223/wpi_monthly_index_\d+\.xlsx)', pag))[-1]
    x = pd.read_excel(io.BytesIO(_get("https://eaindustry.nic.in/" + link, timeout=120).content), header=None)
    enc = [str(c) for c in x.iloc[0]]
    col_cod = enc.index("Commodity Code")
    fechas = {i: pd.to_datetime(c, format="%b-%y", errors="coerce") for i, c in enumerate(enc)}
    filas = []
    for _, r in x.iloc[1:].iterrows():
        cod = str(r.iloc[col_cod]).split(".")[0].strip()
        if cod in INDIA:
            for i, f in fechas.items():
                if pd.notna(f):
                    filas.append((f.date(), INDIA[cod], _num(r.iloc[i]), "índice 2022-23=100", "Office of the Economic Adviser (India)", ""))
    return _df(filas)


# ================================================================ INDEC
MESES = {"ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8, "sep": 9, "oct": 10, "nov": 11, "dic": 12}
IPIM = {"27": "ipim_metalicos_basicos", "271": "ipim_hierro_acero", "272": "ipim_no_ferrosos", "273": "ipim_fundicion",
        "28": "ipim_productos_metalicos", "281": "ipim_281", "2811": "ipim_2811", "289": "ipim_289", "2899": "ipim_2899", "29": "ipim_maquinaria"}


def _fechas_columnas(h, max_filas=15):
    """Busca en las primeras filas la fila de meses y la de años; devuelve {columna: (fecha, provisorio)}."""
    for i in range(min(max_filas, len(h))):
        celdas = [str(c).strip().lower() for c in h.iloc[i]]
        meses = [MESES.get(re.sub(r"[^a-záéíóú]", "", c)[:3]) for c in celdas]
        if sum(m is not None for m in meses) >= 6:
            anio, out = None, {}
            # años: en la fila de arriba (celdas combinadas, rellenar hacia la derecha) o en la misma celda
            fila_anios = [re.search(r"(19|20)\d{2}", str(c)) for c in h.iloc[i - 1]] if i else [None] * len(celdas)
            for j, m in enumerate(meses):
                a = fila_anios[j] or re.search(r"(19|20)\d{2}", celdas[j])
                if a:
                    anio = int(a.group(0))
                if m and anio:
                    out[j] = (dt.date(anio, m, 1), "*" in celdas[j])
            # si falta el año, se infiere hacia atrás desde el último dato
            return out
        fechas = {j: pd.to_datetime(c, errors="coerce") for j, c in enumerate(h.iloc[i]) if isinstance(c, (dt.datetime, pd.Timestamp))}
        if len(fechas) >= 6:
            return {j: (f.date().replace(day=1), False) for j, f in fechas.items()}
    return {}


def indec_sipm(ctx):
    r = _get("https://www.indec.gob.ar/ftp/cuadros/economia/series_sipm_dic2015.xls", timeout=180)
    h = pd.read_excel(io.BytesIO(r.content), sheet_name="IPIM", header=None)
    cols = _fechas_columnas(h)
    if not cols:
        raise RuntimeError("no encontré la fila de fechas en la hoja IPIM")
    filas = []
    for _, fila in h.iterrows():
        cod = str(fila.iloc[0]).strip()
        if cod in IPIM:
            for j, (f, prov) in cols.items():
                filas.append((f, IPIM[cod], _num(fila.iloc[j]), "índice dic-2015=100", "INDEC (SIPM)", "provisorio" if prov else ""))
    return _df(filas)


INDEC_PRODUCTOS = [  # (archivo, hoja (texto contenido en el nombre), texto a buscar en la fila, id)
    ("op_icc_sipm_2016.xls", "IPIB apertura", "41261-1", "ipib_barras_acero"),
    ("op_icc_sipm_2016.xls", "IPIB apertura", "41241-1", "ipib_alambron"),
    ("op_icc_sipm_2016.xls", "IPIB apertura", "41263-1", "ipib_alambre_acero"),
    ("op_icc_sipm_2016.xls", "IPIB apertura", "42999-2", "ipib_chapas"),
    ("op_icc_sipm_2016.xls", "Cap. Mat", "Acero aletado conformado, en barra", "icc_acero_aletado"),
    ("icc_variaciones_indices_item_2016.xls", "índices", "Carpintería metálica", "icc_carpinteria_metalica"),
]


def indec_productos(ctx):
    libros, filas, errores = {}, [], []
    for archivo, hoja, texto, sid in INDEC_PRODUCTOS:
        try:
            if archivo not in libros:
                libros[archivo] = pd.read_excel(io.BytesIO(_get(f"https://www.indec.gob.ar/ftp/cuadros/economia/{archivo}", timeout=180).content),
                                                sheet_name=None, header=None)
            nombre = next(n for n in libros[archivo] if hoja.lower() in n.lower())
            h = libros[archivo][nombre]
            cols = _fechas_columnas(h, 25)
            if not cols:
                raise RuntimeError(f"sin fila de fechas en '{nombre}'")
            plano = h.fillna("").astype(str)
            m = plano.apply(lambda c: c.str.contains(texto, regex=False)).any(axis=1)
            if not m.any():
                raise RuntimeError(f"no está '{texto}' en '{nombre}'")
            fila = h[m].iloc[0]
            for j, (f, prov) in cols.items():
                filas.append((f, sid, _num(fila.iloc[j]), "índice", f"INDEC ({archivo})", "provisorio" if prov else ""))
        except Exception as e:  # noqa: BLE001
            errores.append(f"{sid}: {e}"[:140])
    df = _df(filas)
    df.attrs["errores"] = errores
    return df


# ================================================================ Precio realizado de la siderúrgica local (SEC)
def precio_realizado(ctx):
    from bs4 import BeautifulSoup
    j = _get("https://data.sec.gov/submissions/CIK0001342874.json", headers=SEC_UA).json()
    rec = j["filings"]["recent"]
    ya = {str(f) for f in ctx.fechas("acero_region_sur_usd_t")}
    filas, errores = [], []
    for i, doc in enumerate(rec["primaryDocument"]):
        m = re.match(r"prternium([1-4])q(\d{4})\.htm", doc or "")
        if not m:
            continue
        f = dt.date(int(m[2]), 3 * int(m[1]) - 2, 1)
        if str(f) in ya:
            continue
        try:
            acc = rec["accessionNumber"][i].replace("-", "")
            html = _get(f"https://www.sec.gov/Archives/edgar/data/1342874/{acc}/{doc}", headers=SEC_UA).text
            time.sleep(0.3)
            soup = BeautifulSoup(html, "html.parser")
            for tr in soup.find_all("tr"):
                celdas = [c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"])]
                if not celdas or not celdas[0].lower().startswith("southern region"):
                    continue
                nums = [_num(c.replace("(", "-").replace(")", "")) for c in celdas[1:]]
                nums = [n for n in nums if n is not None]
                if len(nums) >= 11:
                    ventas, tons, rpt = nums[0], nums[5], nums[10]
                    calc = ventas / tons * 1000 if tons else None
                    valor = rpt if calc and abs(rpt / calc - 1) < 0.05 else calc
                    filas.append((f, "acero_region_sur_usd_t", valor, "USD/t", f"Comunicado trimestral 6-K ({doc})", ""))
                    break
        except Exception as e:  # noqa: BLE001
            errores.append(f"{doc}: {e}"[:100])
    df = _df(filas)
    df.attrs["errores"] = errores
    return df

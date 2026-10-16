"""Test de fuentes del monitor de costos metalúrgicos.

Cada caso es independiente: si uno falla, el resto sigue. Para cada fuente se informa
estado HTTP, tamaño, y si se pudo leer, la última fecha y el último valor de algunas series.
Salida: results/test_report.md y results/samples/ (crudos para inspección).
"""
import datetime as dt
import io
import json
import pathlib
import re
import time
import traceback

import pandas as pd
import requests
import urllib3

urllib3.disable_warnings()
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                    "(KHTML, like Gecko) Chrome/124 Safari/537.36",
      "Accept-Language": "es-AR,es;q=0.9,en;q=0.8"}
HOY = dt.date.today()
RES = pathlib.Path("results")
SAMPLES = RES / "samples"
SAMPLES.mkdir(parents=True, exist_ok=True)
out = [f"# Test de fuentes — {dt.datetime.utcnow():%Y-%m-%d %H:%M} UTC\n"]
resumen = []  # (bloque, caso, estado, detalle)


def get(url, **kw):
    kw.setdefault("headers", UA)
    kw.setdefault("timeout", 60)
    kw.setdefault("verify", False)
    return requests.get(url, **kw)


def guardar(nombre, contenido):
    p = SAMPLES / nombre
    if isinstance(contenido, (bytes, bytearray)):
        p.write_bytes(contenido[:3_000_000])
    else:
        p.write_text(str(contenido)[:500_000], encoding="utf-8")


def caso(bloque, nombre, f):
    out.append(f"\n## [{bloque}] {nombre}")
    t0 = time.time()
    try:
        texto = f()
        estado = "OK" if "SIN DATOS" not in str(texto) else "PARCIAL"
        out.append(str(texto)[:5000])
        resumen.append((bloque, nombre, estado, str(texto).splitlines()[0][:110] if texto else ""))
    except Exception as e:  # noqa: BLE001
        out.append("ERROR\n```\n" + traceback.format_exc()[-1200:] + "\n```")
        resumen.append((bloque, nombre, "ERROR", f"{type(e).__name__}: {str(e)[:100]}"))
    out.append(f"_({time.time() - t0:.1f} s)_")


def ultimos(s, n=3):
    s = s.dropna()
    return " | ".join(f"{i}: {v}" for i, v in s.tail(n).items())


# =============================================================== NO FERROSOS
def westmetall():
    res = []
    campos = ["LME_Cu_cash", "LME_Al_cash", "LME_Ni_cash", "LME_Zn_cash", "LME_Sn_cash", "LME_Pb_cash",
              "WM_Cu_low", "MB_MS_58_1"]
    for c in campos:
        r = get("https://www.westmetall.com/en/markdaten.php", params={"action": "table", "field": c})
        tablas = pd.read_html(io.StringIO(r.text))
        t = tablas[0]
        res.append(f"{c}: HTTP {r.status_code}, tablas {len(tablas)}, filas {len(t)}, columnas {list(t.columns)[:4]}")
        res.append("   primeras filas: " + " || ".join(" ; ".join(str(x) for x in fila) for fila in t.head(2).values.tolist()))
    # historia por año
    r = get("https://www.westmetall.com/en/markdaten.php", params={"action": "table", "field": "LME_Cu_cash", "year": 2010})
    t = pd.read_html(io.StringIO(r.text))
    res.append(f"Historia (year=2010): {len(t)} tablas, filas {[len(x) for x in t][:5]}, "
               f"muestra {t[0].head(1).values.tolist() if t else '-'}")
    guardar("westmetall_cu.html", get("https://www.westmetall.com/en/markdaten.php",
                                     params={"action": "table", "field": "LME_Cu_cash"}).text)
    return "\n".join(res)


YAHOO = ["HG=F", "ALI=F", "HRC=F", "TIO=F", "BUS=F", "TSR=F", "EHR=F", "NSF=F", "HMS=F",
         "AUP=F", "EDP=F", "ZNC=F", "NICKEL=F", "BDRY"]


def yahoo():
    res = []
    p1 = int(dt.datetime(2000, 1, 1).timestamp())
    for t in YAHOO:
        try:
            r = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}",
                    params={"period1": p1, "period2": int(time.time()), "interval": "1d"})
            j = r.json()
            if not j.get("chart", {}).get("result"):
                res.append(f"{t}: HTTP {r.status_code} sin resultado ({str(j)[:120]})")
                continue
            x = j["chart"]["result"][0]
            m = x.get("meta", {})
            ts, cl = x.get("timestamp") or [], x["indicators"]["quote"][0].get("close") or []
            pares = [(dt.datetime.utcfromtimestamp(a).date(), b) for a, b in zip(ts, cl) if b is not None]
            res.append(f"{t}: {m.get('shortName') or m.get('longName')} [{m.get('exchangeName')}, {m.get('currency')}] "
                       f"obs {len(pares)}, desde {pares[0][0] if pares else '-'}, último {pares[-1] if pares else '-'}")
        except Exception as e:  # noqa: BLE001
            res.append(f"{t}: ERROR {e}"[:200])
    return "\n".join(res)


def pink_sheet():
    r = get("https://www.worldbank.org/en/research/commodity-markets")
    links = re.findall(r'https://thedocs\.worldbank\.org/[^"\']+CMO-Historical-Data-Monthly\.xlsx', r.text)
    if not links:
        return f"SIN DATOS: no encontré el link (HTTP {r.status_code}, {len(r.text)} bytes)"
    x = get(links[0], timeout=120)
    guardar("pink_sheet.xlsx", x.content)
    df = pd.read_excel(io.BytesIO(x.content), sheet_name="Monthly Prices", header=None)
    fila_nombres = df.index[df.iloc[:, 1].astype(str).str.contains("Crude oil", na=False)][0]
    cols = df.iloc[fila_nombres].tolist()
    unid = df.iloc[fila_nombres + 1].tolist()
    datos = df.iloc[fila_nombres + 2:].copy()
    datos.columns = range(len(cols))
    res = [f"Link: {links[0]}", f"Filas: {len(datos)}, primera {datos.iloc[0, 0]}, última {datos.iloc[-1, 0]}"]
    for i, c in enumerate(cols):
        if any(k in str(c).lower() for k in ["iron ore", "copper", "aluminum", "nickel", "zinc", "tin", "lead", "coal"]):
            res.append(f"  {c} [{unid[i]}]: últimos {datos.iloc[-3:, i].tolist()}")
    return "\n".join(res)


def imf_pcps():
    res = []
    urls = [
        "https://api.imf.org/external/sdmx/2.1/data/IMF.RES,PCPS/M.G001.PCOPP.USD?startPeriod=2025-01",
        "https://api.imf.org/external/sdmx/2.1/data/PCPS/M.W00.PCOPP.USD?startPeriod=2025-01",
        "https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.RES/PCPS/+/M.*.PCOPP.USD?c[TIME_PERIOD]=ge:2025-01",
        "http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/PCPS/M.W00.PCOPP.USD?startPeriod=2025",
    ]
    for u in urls:
        try:
            r = get(u, headers={**UA, "Accept": "application/json, application/xml"})
            res.append(f"{u}\n   -> HTTP {r.status_code} {len(r.content)} bytes: {r.text[:200]!r}")
        except Exception as e:  # noqa: BLE001
            res.append(f"{u}\n   -> ERROR {e}"[:250])
    return "\n".join(res)


def fred_metales():
    res = []
    for sid in ["PCOPPUSDM", "PALUMUSDM", "PIORECRUSDM", "WPU101704"]:
        try:
            r = get(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}", timeout=40)
            res.append(f"{sid}: HTTP {r.status_code} últimas {r.text.strip().splitlines()[-2:]}")
        except Exception as e:  # noqa: BLE001
            res.append(f"{sid}: ERROR {type(e).__name__}")
    return "\n".join(res)


def _habiles(n=8):
    d, dias = HOY, []
    while len(dias) < n:
        d -= dt.timedelta(days=1)
        if d.weekday() < 5:
            dias.append(d)
    return dias


def shfe():
    res = []
    for d in _habiles(4):
        u = f"https://www.shfe.com.cn/data/tradedata/future/dailydata/kx{d:%Y%m%d}.dat"
        r = get(u, headers={**UA, "Referer": "https://www.shfe.com.cn/"})
        res.append(f"{u} -> HTTP {r.status_code} {len(r.content)} bytes {r.headers.get('content-type')}")
        if r.ok and r.text.strip().startswith("{"):
            j = r.json()
            filas = j.get("o_curinstrument", [])
            prods = sorted({(x.get("PRODUCTID") or "").strip() for x in filas})
            res.append(f"   productos: {prods}")
            for x in filas:
                if (x.get("PRODUCTID") or "").strip().startswith(("rb", "hc", "cu", "al")) and x.get("DELIVERYMONTH"):
                    res.append(f"   {x.get('PRODUCTID')} {x.get('DELIVERYMONTH')} cierre {x.get('CLOSEPRICE')} liq {x.get('SETTLEMENTPRICE')}")
                    break
            guardar("shfe.json", r.text)
            break
    return "\n".join(res)


def changjiang():
    res = []
    for u in ["https://www.ccmn.cn/", "https://www.ccmn.cn/historyprice/"]:
        r = get(u)
        r.encoding = r.apparent_encoding
        txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r.text))
        m = re.findall(r"(1#铜|A00铝|0#锌|1#铅|1#锡|1#镍)[^0-9]{0,30}([0-9]{4,6})", txt)
        res.append(f"{u} -> HTTP {r.status_code} {len(r.content)} bytes; coincidencias {m[:8]}")
        guardar("ccmn_" + ("home" if u.endswith("cn/") else "hist") + ".html", r.text)
    return "\n".join(res)


def mcx():
    r = get("https://www.mcxindia.com/market-data/bhavcopy")
    return f"HTTP {r.status_code} {len(r.content)} bytes; menciona 'bhavcopy' {('bhavcopy' in r.text.lower())}"


# =============================================================== MATERIAS PRIMAS SIDERÚRGICAS
def dce():
    res = []
    d = _habiles(1)[0]
    pruebas = [
        ("GET", "http://www.dce.com.cn/publicweb/quotesdata/dayQuotesCh.html", None),
        ("POST", "http://www.dce.com.cn/publicweb/quotesdata/dayQuotesCh.html",
         {"dayQuotes.variety": "i", "dayQuotes.trade_type": "0", "year": d.year, "month": d.month - 1, "day": d.day}),
        ("GET", "http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/rtj/rxq/index.html", None),
    ]
    for metodo, u, data in pruebas:
        r = requests.request(metodo, u, headers=UA, data=data, timeout=60, verify=False)
        r.encoding = r.apparent_encoding
        txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r.text))
        res.append(f"{metodo} {u} -> HTTP {r.status_code} {len(r.content)} bytes; "
                   f"铁矿石 {'铁矿石' in r.text};焦煤 {'焦煤' in r.text}; texto: {txt[:200]!r}")
    return "\n".join(res)


def zce():
    res = []
    for d in _habiles(4):
        u = f"http://www.czce.com.cn/cn/DFSStaticFiles/Future/{d:%Y}/{d:%Y%m%d}/FutureDataDaily.txt"
        r = get(u)
        res.append(f"{u} -> HTTP {r.status_code} {len(r.content)} bytes")
        if r.ok and len(r.content) > 1000:
            r.encoding = r.apparent_encoding
            lineas = [x for x in r.text.splitlines() if x[:2] in ("SF", "SM")]
            res.append("   " + "\n   ".join(lineas[:4]))
            break
    return "\n".join(res)


COMEX_NCM = {  # NCM: descripción
    "26011100": "Mineral de hierro no aglomerado",
    "26011200": "Mineral de hierro aglomerado (pellets)",
    "72011000": "Arrabio no aleado",
    "72071200": "Semis (planchones) de acero",
    "72083990": "Laminado en caliente, rollos <3mm (otros)",
    "72091800": "Laminado en frío <0,5mm",
    "72104910": "Galvanizado",
    "72142000": "Barras para hormigón",
    "72139100": "Alambrón",
}


def comexstat():
    res = []
    ini, fin = f"{HOY.year - 1}-01", f"{HOY.year}-12"
    for flujo, ncms, extra in [("export", list(COMEX_NCM), {}),
                               ("import", ["27011200", "27040010"], {}),
                               ("export", ["72083990", "72142000", "72104910"], {"country": ["063"]})]:
        body = {"flow": flujo, "monthDetail": True, "period": {"from": ini, "to": fin},
                "filters": [{"filter": "ncm", "values": ncms}] + ([{"filter": "country", "values": extra["country"]}] if extra else []),
                "details": ["ncm"], "metrics": ["metricFOB", "metricKG"]}
        r = requests.post("https://api-comexstat.mdic.gov.br/general", json=body, headers=UA, timeout=120, verify=False)
        etiqueta = f"{flujo}{' a Argentina' if extra else ''}"
        res.append(f"{etiqueta}: HTTP {r.status_code} {len(r.content)} bytes")
        if not r.ok:
            res.append("   " + r.text[:300])
            continue
        j = r.json()
        filas = j.get("data", {}).get("list", []) if isinstance(j.get("data"), dict) else j.get("data", [])
        df = pd.DataFrame(filas)
        if df.empty:
            res.append(f"   SIN DATOS {str(j)[:200]}")
            continue
        guardar(f"comexstat_{etiqueta.replace(' ', '_')}.json", json.dumps(filas)[:400000])
        for c in ["metricFOB", "metricKG"]:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df["usd_t"] = df["metricFOB"] / df["metricKG"] * 1000
        col_ncm = "coNcm" if "coNcm" in df else df.columns[0]
        for n, g in df.groupby(col_ncm):
            g = g.sort_values(["year", "monthNumber"])
            u = g.iloc[-1]
            res.append(f"   {n} {COMEX_NCM.get(str(n), '')}: último {u['year']}-{u['monthNumber']} "
                       f"{u['usd_t']:.0f} USD/t ({u['metricKG'] / 1e6:.1f} mil t)")
    return "\n".join(res)


def comext():
    res = []
    base = "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-045409"
    pruebas = {
        "Chatarra 7204 UE->Turquía": {"freq": "M", "reporter": "EU", "partner": "TR", "product": "7204", "flow": "2"},
        "Barra 7214 Turquía->UE": {"freq": "M", "reporter": "EU", "partner": "TR", "product": "7214", "flow": "1"},
        "HRC 7208 importado UE (total extra)": {"freq": "M", "reporter": "EU", "partner": "EXT_EU27_2020", "product": "7208", "flow": "1"},
    }
    for nombre, p in pruebas.items():
        q = {**p, "indicators": "VALUE_IN_EUROS", "sinceTimePeriod": f"{HOY.year - 1}M01", "format": "JSON"}
        r = get(base, params=q, timeout=120)
        res.append(f"{nombre}: HTTP {r.status_code} {len(r.content)} bytes {r.text[:150]!r}")
        if r.ok:
            j = r.json()
            vals = j.get("value", {})
            tiempos = list(j.get("dimension", {}).get("time", {}).get("category", {}).get("index", {}))
            res.append(f"   períodos {tiempos[-3:]}, valores {list(vals.values())[-3:]}")
            q["indicators"] = "QUANTITY_IN_100KG"
            r2 = get(base, params=q, timeout=120)
            res.append(f"   cantidad: HTTP {r2.status_code} {list(r2.json().get('value', {}).values())[-3:] if r2.ok else r2.text[:120]}")
    return "\n".join(res)


def boj():
    res = []
    for db in ["PR01", "PR02"]:
        u = "https://www.stat-search.boj.or.jp/api/v1/getMetadata"
        r = get(u, params={"format": "json", "lang": "en", "db": db})
        res.append(f"{db} metadata -> HTTP {r.status_code} {len(r.content)} bytes")
        if not r.ok:
            res.append("   " + r.text[:300])
            continue
        j = r.json()
        guardar(f"boj_{db}_meta.json", json.dumps(j)[:400000])
        filas = j.get("RESULTSET") or j.get("resultset") or []
        claves = ["iron ore", "coking coal", "steel scrap", "hot rolled", "cold rolled", "galvanized", "steel bars",
                  "pig iron", "copper", "aluminium", "nickel", "zinc"]
        hits = [f"{x.get('SERIES_CODE')}: {x.get('NAME_OF_TIME_SERIES')}" for x in filas
                if any(k in str(x.get("NAME_OF_TIME_SERIES", "")).lower() for k in claves)]
        res.append(f"   series: {len(filas)}, coincidencias {len(hits)}")
        res.extend("   " + h for h in hits[:40])
        codigos = [h.split(":")[0] for h in hits[:3]]
        if codigos:
            r2 = get("https://www.stat-search.boj.or.jp/api/v1/getDataCode",
                     params={"format": "json", "lang": "en", "db": db, "code": ",".join(codigos), "startDate": f"{HOY.year - 1}01"})
            res.append(f"   datos {codigos}: HTTP {r2.status_code} {r2.text[:400]!r}")
    return "\n".join(res)


# =============================================================== ACERO
BLS = {"WPU1017": "Laminados de acero", "WPU101704": "Barras, chapa gruesa y perfiles en caliente",
       "WPU101707": "Laminado en frío", "WPU101": "Hierro y acero", "WPU1012": "Chatarra hierro y acero",
       "WPU101211": "Chatarra de acero al carbono", "WPU101708": "Galvanizado (a confirmar)",
       "WPU10170811": "Galvanizado (otra variante)", "WPU1011": "Mineral de hierro (a confirmar)",
       "WPU101702": "Semis (a confirmar)"}


def bls():
    r = requests.post("https://api.bls.gov/publicAPI/v2/timeseries/data/",
                      json={"seriesid": list(BLS), "startyear": str(HOY.year - 1), "endyear": str(HOY.year)},
                      headers={**UA, "Content-type": "application/json"}, timeout=60)
    j = r.json()
    res = [f"HTTP {r.status_code} status {j.get('status')} {j.get('message')}"]
    for s in j.get("Results", {}).get("series", []):
        d = s.get("data", [])
        res.append(f"   {s['seriesID']} {BLS.get(s['seriesID'], '')}: "
                   + (f"último {d[0]['year']}-{d[0]['period']} = {d[0]['value']}" if d else "SIN DATOS"))
    return "\n".join(res)


def nbs():
    res = []
    u = "https://www.stats.gov.cn/xxgk/sjfb/zxfb2020/202610/t20261008_1965465.html"
    r = get(u)
    r.encoding = "utf-8"
    res.append(f"Página conocida -> HTTP {r.status_code} {len(r.content)} bytes")
    if r.ok:
        tablas = pd.read_html(io.StringIO(r.text))
        res.append(f"   tablas {len(tablas)}; filas {[len(t) for t in tablas]}")
        t = tablas[0]
        for fila in t.values.tolist():
            if any(k in " ".join(map(str, fila)) for k in ["螺纹钢", "热轧", "焦煤", "焦炭", "电解铜"]):
                res.append("   " + " | ".join(map(str, fila))[:150])
    for lista in ["https://www.stats.gov.cn/sj/zxfb/", "https://www.stats.gov.cn/xxgk/sjfb/zxfb2020/"]:
        r = get(lista)
        r.encoding = "utf-8"
        n = len(re.findall("流通领域重要生产资料", r.text))
        res.append(f"Listado {lista} -> HTTP {r.status_code}, menciones del informe: {n}")
        guardar("nbs_lista.html", r.text)
    return "\n".join(res)


def cisa():
    res = []
    for u in ["https://www.chinaisa.org.cn/", "http://www.chinaisa.org.cn/gxportal/xfgl/portal/index.html"]:
        r = get(u)
        r.encoding = r.apparent_encoding
        res.append(f"{u} -> HTTP {r.status_code} {len(r.content)} bytes; menciona 价格指数: {'价格指数' in r.text}")
    return "\n".join(res)


def aduana_china():
    res = []
    for u in ["http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/302277/index.html",
              "http://english.customs.gov.cn/statics/report/preliminary.html"]:
        r = get(u)
        r.encoding = r.apparent_encoding
        res.append(f"{u} -> HTTP {r.status_code} {len(r.content)} bytes; 钢材 {'钢材' in r.text}; steel {'steel' in r.text.lower()}")
    return "\n".join(res)


def eurostat():
    res = []
    for geo in ["EU27_2020", "DE", "IT", "ES", "FR"]:
        for nace in ["C241", "C2442", "C2444"]:
            r = get("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sts_inppd_m",
                    params={"geo": geo, "nace_r2": nace, "unit": "I21", "s_adj": "NSA", "lastTimePeriod": 2})
            if r.ok:
                j = r.json()
                t = list(j["dimension"]["time"]["category"]["index"])
                v = j.get("value", {})
                res.append(f"{geo} {nace}: {t} -> {list(v.values())}")
            else:
                res.append(f"{geo} {nace}: HTTP {r.status_code}")
    return "\n".join(res)


def destatis():
    res = []
    base = "https://www-genesis.destatis.de/genesisWS/rest/2020/"
    for metodo, ruta, params in [
        ("GET", "helloworld/logincheck", {"username": "GAST", "password": "GAST"}),
        ("GET", "data/tablefile", {"username": "GAST", "password": "GAST", "name": "61241-0004", "area": "all",
                                   "format": "ffcsv", "startyear": str(HOY.year)}),
        ("POST", "data/tablefile", {"name": "61241-0004", "area": "all", "format": "ffcsv", "startyear": str(HOY.year)}),
    ]:
        if metodo == "GET":
            r = get(base + ruta, params=params, timeout=120)
        else:
            r = requests.post(base + ruta, data=params, timeout=120, verify=False,
                              headers={**UA, "username": "GAST", "password": "GAST"})
        res.append(f"{metodo} {ruta} -> HTTP {r.status_code} {len(r.content)} bytes {r.headers.get('content-type')}")
        txt = r.content[:400].decode("utf-8", "ignore")
        res.append(f"   {txt!r}")
        if r.ok and len(r.content) > 2000:
            guardar("destatis_61241_0004.csv", r.content)
            t = r.content.decode("utf-8", "ignore")
            for k in ["Betonstahl", "Warmbreitband", "verzinkt", "Kaltgewalzt", "Walzdraht", "Stahlschrott"]:
                filas = [x for x in t.splitlines() if k.lower() in x.lower()]
                res.append(f"   '{k}': {len(filas)} filas; ej: {filas[-1][:200] if filas else '-'}")
            break
    return "\n".join(res)


def ibge():
    res = []
    for u in ["https://apisidra.ibge.gov.br/values/t/6903/n1/all/v/all/p/last%202/c842/all",
              "https://servicodados.ibge.gov.br/api/v3/agregados/6903/metadados"]:
        r = get(u, timeout=90)
        res.append(f"{u} -> HTTP {r.status_code} {len(r.content)} bytes")
        if r.ok:
            try:
                j = r.json()
            except ValueError:
                res.append("   " + r.text[:200])
                continue
            if isinstance(j, list):
                metal = [x for x in j if "metal" in json.dumps(x, ensure_ascii=False).lower()]
                res.append(f"   filas {len(j)}, con 'metal' {len(metal)}: {json.dumps(metal[:3], ensure_ascii=False)[:500]}")
            else:
                res.append(f"   nombre: {j.get('nome')}; periodicidad {j.get('periodicidade')}; "
                           f"clasificaciones {[c.get('nome') for c in j.get('classificacoes', [])]}")
    return "\n".join(res)


def india_wpi():
    r = get("https://eaindustry.nic.in/download_data_2223.asp")
    links = re.findall(r'href="([^"]+\.(?:xlsx?|csv|zip))"', r.text, flags=re.I)
    return f"HTTP {r.status_code} {len(r.content)} bytes; links {links[:15]}"


def ternium_sec():
    h = {"User-Agent": "ADIMRA Estudios Economicos estudios@adimra.org.ar"}
    j = requests.get("https://data.sec.gov/submissions/CIK0001342874.json", headers=h, timeout=60).json()
    rec = j["filings"]["recent"]
    filas = [f"{rec['filingDate'][i]} {rec['form'][i]} {rec['primaryDocument'][i]}"
             for i in range(len(rec["form"])) if rec["form"][i] in ("6-K", "20-F")][:12]
    pr = [f for f in filas if f.split()[-1].lower().startswith("pr")]
    return f"{j.get('name')}: {len(rec['form'])} presentaciones recientes\n   " + "\n   ".join(filas) + f"\n   comunicados: {pr[:4]}"


# =============================================================== LOCALES
def indec_sipm():
    res = []
    for u in ["https://www.indec.gob.ar/ftp/cuadros/economia/series_sipm_dic2015.xls",
              "https://www.indec.gob.ar/ftp/cuadros/economia/IPIM-dde1993.xls"]:
        r = get(u, timeout=120)
        res.append(f"{u} -> HTTP {r.status_code} {len(r.content)} bytes, modif. {r.headers.get('last-modified')}")
        if not r.ok:
            continue
        hojas = pd.read_excel(io.BytesIO(r.content), sheet_name=None, header=None)
        for nombre, h in list(hojas.items())[:6]:
            plano = h.astype(str)
            filas = plano[plano.apply(lambda x: x.str.contains("ierro y acero|etales|2710|2720|273", regex=True)).any(axis=1)]
            res.append(f"   hoja '{nombre}' {h.shape}: filas con hierro/acero/metales {len(filas)}")
            for _, f in filas.head(6).iterrows():
                res.append("      " + " | ".join(x for x in f.tolist()[:4] if x != "nan")[:140])
    return "\n".join(res)


def indec_icc():
    res = []
    for u in ["https://www.indec.gob.ar/ftp/cuadros/economia/icc_variaciones_indices_item_2016.xls",
              "https://www.indec.gob.ar/ftp/cuadros/economia/op_icc_sipm_2016.xls"]:
        r = get(u, timeout=120)
        res.append(f"{u} -> HTTP {r.status_code} {len(r.content)} bytes")
        if r.ok:
            hojas = pd.read_excel(io.BytesIO(r.content), sheet_name=None, header=None)
            for nombre, h in list(hojas.items())[:6]:
                plano = h.astype(str)
                filas = plano[plano.apply(lambda x: x.str.contains("ierro|cero|etál|hapa|años|erfil", regex=True)).any(axis=1)]
                res.append(f"   hoja '{nombre}' {h.shape}: {len(filas)} filas con acero")
                for _, f in filas.head(5).iterrows():
                    res.append("      " + " | ".join(x for x in f.tolist()[:3] if x != "nan")[:140])
    return "\n".join(res)


def rosario():
    res = []
    r = get("https://datos.rosario.gob.ar/api/3/action/package_search", params={"q": "materiales construccion", "rows": 10})
    res.append(f"CKAN -> HTTP {r.status_code} {len(r.content)} bytes")
    if r.ok and r.headers.get("content-type", "").startswith("application/json"):
        for p in r.json()["result"]["results"]:
            res.append(f"   {p['name']}: " + "; ".join(f"{x.get('format')} {x.get('url')}" for x in p.get("resources", [])[:4]))
    u = "https://datos.rosario.gob.ar/sites/default/files/2026-08/07_26%20Informe%20indices%20mat%20de%20la%20construccion.pdf"
    r = get(u)
    res.append(f"PDF jul-26 -> HTTP {r.status_code} {len(r.content)} bytes")
    return "\n".join(res)


def a3500():
    j = get("https://api.bcra.gob.ar/estadisticas/v4.0/monetarias/5", params={"limit": 3}).json()
    return f"A3500: {json.dumps(j.get('results'), ensure_ascii=False)[:300]}"


# =============================================================== CORRIDA
CASOS = [
    ("No ferrosos", "Westmetall (LME oficial y precios alemanes)", westmetall),
    ("No ferrosos", "Yahoo Finance (futuros CME/COMEX y BDRY)", yahoo),
    ("No ferrosos", "Banco Mundial Pink Sheet (mensual)", pink_sheet),
    ("No ferrosos", "FMI PCPS (API)", imf_pcps),
    ("No ferrosos", "FRED (respaldo)", fred_metales),
    ("No ferrosos", "SHFE futuros (Shanghái)", shfe),
    ("No ferrosos", "Changjiang spot (ccmn.cn)", changjiang),
    ("No ferrosos", "MCX India", mcx),
    ("Materias primas", "DCE (mineral, carbón coque, coque)", dce),
    ("Materias primas", "ZCE (ferroaleaciones)", zce),
    ("Materias primas", "Comex Stat Brasil (valores unitarios por NCM)", comexstat),
    ("Materias primas", "Eurostat Comext (chatarra y barra Turquía, HRC UE)", comext),
    ("Materias primas", "Banco de Japón (precios corporativos e importación)", boj),
    ("Acero", "BLS PPI (EE.UU.)", bls),
    ("Acero", "NBS China (precios cada 10 días)", nbs),
    ("Acero", "CISA (índice de precios del acero China)", cisa),
    ("Acero", "Aduana China", aduana_china),
    ("Acero", "Eurostat PPI por país", eurostat),
    ("Acero", "Destatis GENESIS (precios por producto Alemania)", destatis),
    ("Acero", "IBGE IPP Brasil", ibge),
    ("Acero", "India WPI por ítem", india_wpi),
    ("Local", "Ternium (SEC, precio realizado)", ternium_sec),
    ("Local", "INDEC SIPM (IPIM 4 dígitos)", indec_sipm),
    ("Local", "INDEC ICC (materiales)", indec_icc),
    ("Local", "DGE Rosario (materiales)", rosario),
    ("Local", "BCRA A3500", a3500),
]

for b, n, f in CASOS:
    caso(b, n, f)

tabla = ["\n# Resumen\n", "| Bloque | Fuente | Estado | Detalle |", "|---|---|---|---|"]
tabla += [f"| {b} | {n} | {e} | {d.replace('|', '/')} |" for b, n, e, d in resumen]
(RES / "test_report.md").write_text("\n".join(tabla + out), encoding="utf-8")
print("\n".join(tabla))

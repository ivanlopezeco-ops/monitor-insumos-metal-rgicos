"""Test 2: correcciones y fuentes que en el test 1 fallaron por formato, límite de pedidos o falta de detalle."""
import datetime as dt
import io
import json
import re
import time

import pandas as pd
import requests

import test_fuentes as T  # reutiliza get, guardar, caso, out, resumen

T.out.clear()
T.resumen.clear()
T.out.append(f"# Test 2 — {dt.datetime.utcnow():%Y-%m-%d %H:%M} UTC\n")
get, guardar, HOY = T.get, T.guardar, T.HOY


def filas_con(h, patron, n=8, ancho=5):
    plano = h.fillna("").astype(str)
    m = plano.apply(lambda c: c.str.contains(patron, regex=True, case=False)).any(axis=1)
    sal = []
    for _, f in plano[m].head(n).iterrows():
        sal.append("      " + " | ".join(x for x in f.tolist()[:ancho] if x.strip())[:160])
    return int(m.sum()), sal


def indec_sipm():
    res = []
    for u in ["https://www.indec.gob.ar/ftp/cuadros/economia/series_sipm_dic2015.xls",
              "https://www.indec.gob.ar/ftp/cuadros/economia/IPIM-dde1993.xls"]:
        r = get(u, timeout=120)
        res.append(f"{u} -> HTTP {r.status_code} {len(r.content)} bytes, modif. {r.headers.get('last-modified')}")
        if not r.ok:
            continue
        guardar(u.rsplit("/", 1)[-1], r.content)
        for nombre, h in pd.read_excel(io.BytesIO(r.content), sheet_name=None, header=None).items():
            n, ej = filas_con(h, r"hierro|acero|metales|metálic|2710|2720|273")
            res.append(f"   hoja '{nombre}' {h.shape}: {n} filas con metales")
            res.extend(ej)
            # última columna/fila con número para ver hasta dónde llega
            num = h.apply(pd.to_numeric, errors="coerce")
            res.append(f"      celdas numéricas {int(num.notna().sum().sum())}; primeras filas: "
                       + " || ".join(" ; ".join(str(x) for x in h.iloc[i, :6].tolist()) for i in range(min(6, len(h))))[:500])
    return "\n".join(res)


def indec_icc():
    res = []
    for u in ["https://www.indec.gob.ar/ftp/cuadros/economia/icc_variaciones_indices_item_2016.xls",
              "https://www.indec.gob.ar/ftp/cuadros/economia/op_icc_sipm_2016.xls"]:
        r = get(u, timeout=120)
        res.append(f"{u} -> HTTP {r.status_code} {len(r.content)} bytes")
        if r.ok:
            guardar(u.rsplit("/", 1)[-1], r.content)
            for nombre, h in pd.read_excel(io.BytesIO(r.content), sheet_name=None, header=None).items():
                n, ej = filas_con(h, r"hierro|acero|metál|chapa|caño|perfil|carpinter")
                res.append(f"   hoja '{nombre}' {h.shape}: {n} filas con acero")
                res.extend(ej)
    return "\n".join(res)


def comexstat():
    res = []
    ini, fin = f"{HOY.year - 1}-01", f"{HOY.year}-12"
    consultas = [
        ("import", ["27011200", "27040010", "72044900", "72031000"], [], "Brasil importa: carbón coque, coque, chatarra, DRI"),
        ("export", ["72083990", "72083910", "72085200", "72091800", "72104910", "72142000", "72139100", "72071200"], ["063"],
         "Brasil exporta a la Argentina"),
        ("export", ["26011100"], [], "Historia larga: mineral de hierro desde 1997"),
    ]
    for flujo, ncms, paises, nombre in consultas:
        time.sleep(15)
        filtros = [{"filter": "ncm", "values": ncms}] + ([{"filter": "country", "values": paises}] if paises else [])
        periodo = {"from": "1997-01", "to": fin} if "1997" in nombre else {"from": ini, "to": fin}
        metricas = ["metricFOB", "metricKG"] + (["metricCIF"] if flujo == "import" else [])
        body = {"flow": flujo, "monthDetail": True, "period": periodo, "filters": filtros,
                "details": ["ncm"], "metrics": metricas}
        r = requests.post("https://api-comexstat.mdic.gov.br/general", json=body, headers=T.UA, timeout=180, verify=False)
        res.append(f"{nombre}: HTTP {r.status_code} {len(r.content)} bytes")
        if not r.ok:
            res.append("   " + r.text[:200])
            continue
        j = r.json()
        df = pd.DataFrame(j["data"]["list"])
        for c in metricas:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        v = "metricCIF" if flujo == "import" else "metricFOB"
        df["usd_t"] = df[v] / df["metricKG"] * 1000
        res.append(f"   filas {len(df)}, desde {df['year'].min()}-{df.loc[df['year'] == df['year'].min(), 'monthNumber'].min()}")
        for n, g in df.groupby("coNcm"):
            g = g.sort_values(["year", "monthNumber"])
            u = g.iloc[-1]
            res.append(f"   {n} {str(u.get('ncm', ''))[:50]}: {u['year']}-{u['monthNumber']} {u['usd_t']:.0f} USD/t "
                       f"({'CIF' if flujo == 'import' else 'FOB'}), {u['metricKG'] / 1e6:.1f} mil t")
    return "\n".join(res)


def comext():
    res = []
    base = "https://ec.europa.eu/eurostat/api/comext/dissemination/statistics/1.0/data/DS-045409"
    variantes = [{"sinceTimePeriod": f"{HOY.year - 1}-01"}, {"sinceTimePeriod": f"{HOY.year - 1}M01"},
                 {"time": f"{HOY.year}-06"}, {"lastTimePeriod": "3"}]
    p = {"freq": "M", "reporter": "EU", "partner": "TR", "product": "7204", "flow": "2", "indicators": "VALUE_IN_EUROS"}
    ok = None
    for v in variantes:
        r = get(base, params={**p, **v}, timeout=120)
        res.append(f"variante {v}: HTTP {r.status_code} {r.text[:160]!r}")
        if r.ok:
            ok = v
            break
    if ok:
        for nombre, q in {"Chatarra UE->Turquía": {"partner": "TR", "product": "7204", "flow": "2"},
                          "Barra Turquía->UE": {"partner": "TR", "product": "7214", "flow": "1"},
                          "HRC UE desde China": {"partner": "CN", "product": "7208", "flow": "1"},
                          "HRC UE extra-UE": {"partner": "EXT_EU27_2020", "product": "7208", "flow": "1"}}.items():
            vals = {}
            for ind in ["VALUE_IN_EUROS", "QUANTITY_IN_100KG"]:
                r = get(base, params={**p, **q, **ok, "indicators": ind}, timeout=120)
                if r.ok:
                    j = r.json()
                    idx = j["dimension"]["time"]["category"]["index"]
                    inv = {v: k for k, v in idx.items()}
                    vals[ind] = {inv[int(k)]: v for k, v in j.get("value", {}).items()}
                else:
                    vals[ind] = r.text[:100]
            try:
                ult = sorted(vals["VALUE_IN_EUROS"])[-1]
                eur_t = vals["VALUE_IN_EUROS"][ult] / (vals["QUANTITY_IN_100KG"][ult] / 10)
                res.append(f"   {nombre}: {ult} {eur_t:.0f} EUR/t ({vals['QUANTITY_IN_100KG'][ult] / 1e4:.0f} mil t)")
            except Exception as e:  # noqa: BLE001
                res.append(f"   {nombre}: {str(vals)[:200]} {e}")
    return "\n".join(res)


def boj():
    res = []
    meta = json.loads((T.SAMPLES / "boj_PR01_meta.json").read_text()) if (T.SAMPLES / "boj_PR01_meta.json").exists() else None
    if meta is None:
        meta = get("https://www.stat-search.boj.or.jp/api/v1/getMetadata", params={"format": "json", "lang": "en", "db": "PR01"}).json()
    filas = meta.get("RESULTSET", [])
    claves = ["iron ore", "coking coal", "coal", "steel scrap", "iron scrap", "pig iron", "ferro-alloy", "aluminium ingot",
              "nickel", "zinc", "tin", "steel bars", "plates", "wire rods", "steel pipes"]
    hits = [x for x in filas if any(k in str(x.get("NAME_OF_TIME_SERIES", "")).lower() for k in claves)]
    res.append(f"coincidencias {len(hits)}")
    for x in hits[:60]:
        res.append(f"   {x.get('SERIES_CODE')}: {x.get('NAME_OF_TIME_SERIES')} [{x.get('UNIT')}] {x.get('FREQUENCY')} "
                   f"{x.get('START_OF_THE_TIME_SERIES')}-{x.get('END_OF_THE_TIME_SERIES')}")
    # prefijos: qué significa cada bloque (doméstico / exportación / importación, yen / contrato)
    pref = {}
    for x in filas:
        c = str(x.get("SERIES_CODE", ""))[:9]
        pref.setdefault(c, x.get("NAME_OF_TIME_SERIES"))
    res.append("Prefijos (primer nombre de cada bloque):")
    res.extend(f"   {k}: {v}" for k, v in list(pref.items())[:40])
    return "\n".join(res)


def yahoo_busqueda():
    res = []
    for q in ["scrap", "steel", "rebar", "coking coal", "iron ore", "cobalt", "lithium", "aluminum", "hot-rolled", "turkish"]:
        r = get("https://query2.finance.yahoo.com/v1/finance/search", params={"q": q, "quotesCount": 15, "newsCount": 0})
        try:
            qs = r.json().get("quotes", [])
            fut = [f"{x.get('symbol')} ({x.get('shortname') or x.get('longname')}, {x.get('exchange')})" for x in qs
                   if x.get("quoteType") == "FUTURE" or str(x.get("symbol", "")).endswith("=F")]
            res.append(f"'{q}': {fut}")
        except Exception as e:  # noqa: BLE001
            res.append(f"'{q}': HTTP {r.status_code} {e}")
    # detalle de los dudosos
    for t in ["BUS=F", "EHR=F", "TIO=F", "HRC=F"]:
        r = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}", params={"range": "1mo", "interval": "1d"})
        x = r.json()["chart"]["result"][0]
        cl = [c for c in x["indicators"]["quote"][0]["close"] if c is not None]
        res.append(f"{t} último mes: {len(cl)} obs, valores {cl[-5:]}; vencimiento {x['meta'].get('expireDate') or ''}")
    return "\n".join(res)


def changjiang():
    res = []
    for u in ["https://copper.ccmn.cn/copperprice/cjxh/", "https://alu.ccmn.cn/aluprice/cjxh/",
              "https://zinc.ccmn.cn/zincprice/cjxh/", "https://lead.ccmn.cn/leadprice/cjxh/",
              "https://tin.ccmn.cn/tinprice/cjxh/", "https://nickel.ccmn.cn/nickelprice/cjxh/"]:
        try:
            r = get(u)
            r.encoding = r.apparent_encoding
            tablas = []
            try:
                tablas = pd.read_html(io.StringIO(r.text))
            except ValueError:
                pass
            muestra = tablas[0].head(3).values.tolist() if tablas else re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r.text))[:200]
            res.append(f"{u} -> HTTP {r.status_code} {len(r.content)} bytes; tablas {len(tablas)}; muestra {str(muestra)[:300]}")
        except Exception as e:  # noqa: BLE001
            res.append(f"{u} -> ERROR {e}"[:200])
    return "\n".join(res)


def cisa():
    r = get("http://www.chinaisa.org.cn/gxportal/xfgl/portal/index.html")
    r.encoding = r.apparent_encoding
    guardar("cisa.html", r.text)
    i = r.text.find("价格指数")
    links = re.findall(r'href="([^"]+)"[^>]*>([^<]*价格[^<]*)<', r.text)
    return f"HTTP {r.status_code}; contexto: {re.sub(r'<[^>]+>', ' ', r.text[max(0, i - 300):i + 300])!r}\nlinks con 价格: {links[:10]}"


def nbs_lista():
    r = get("https://www.stats.gov.cn/sj/zxfb/")
    r.encoding = "utf-8"
    links = re.findall(r'href="([^"]+)"[^>]*title="([^"]*流通领域重要生产资料[^"]*)"', r.text) or \
        re.findall(r'href="([^"]+)"[^>]*>\s*([^<]*流通领域重要生产资料[^<]*)<', r.text)
    sal = [f"links: {len(links)}"] + [f"   {t} -> {h}" for h, t in links[:6]]
    # paginación hacia atrás (profundidad histórica)
    for pag in ["index_1.html", "index_10.html", "index_30.html"]:
        r2 = get("https://www.stats.gov.cn/sj/zxfb/" + pag)
        r2.encoding = "utf-8"
        fechas = re.findall(r"(\d{4}年\d{1,2}月[上中下]旬)流通领域", r2.text)
        sal.append(f"   {pag}: HTTP {r2.status_code}, informes {fechas[:3]}")
    return "\n".join(sal)


def destatis():
    res = []
    pruebas = [
        ("POST", "https://www-genesis.destatis.de/genesisWS/rest/2020/helloworld/logincheck", {}),
        ("POST", "https://www-genesis.destatis.de/genesisWS/rest/2020/data/tablefile",
         {"name": "61241-0004", "area": "all", "compress": "false", "format": "ffcsv", "startyear": str(HOY.year)}),
        ("GET", "https://www-genesis.destatis.de/genesisWS/rest/2020/data/tablefile",
         {"username": "GAST", "password": "GAST", "name": "61241-0004", "format": "ffcsv", "startyear": str(HOY.year), "language": "de"}),
        ("POST", "https://www-genesis.destatis.de/genesisWS/rest/2020/catalogue/tables",
         {"selection": "61241*", "area": "all", "pagelength": "50"}),
    ]
    for metodo, u, d in pruebas:
        h = {**T.UA, "username": "GAST", "password": "GAST", "Content-Type": "application/x-www-form-urlencoded"}
        r = requests.request(metodo, u, headers=h, data=d if metodo == "POST" else None,
                             params=d if metodo == "GET" else None, timeout=180)
        res.append(f"{metodo} {u.rsplit('/2020/', 1)[-1]} -> HTTP {r.status_code} {len(r.content)} bytes {r.headers.get('content-type')}")
        res.append(f"   {r.content[:300].decode('utf-8', 'ignore')!r}")
        if r.ok and len(r.content) > 5000 and "csv" in (r.headers.get("content-type") or "") + u:
            t = r.content.decode("utf-8", "ignore")
            guardar("destatis.csv", t)
            for k in ["Betonstahl", "Warmbreitband", "verzinkt", "kaltgewalzt", "Walzdraht", "Schrott", "Roheisen"]:
                f = [x for x in t.splitlines() if k.lower() in x.lower()]
                res.append(f"   '{k}': {len(f)} filas; ej: {f[-1][:220] if f else '-'}")
    return "\n".join(res)


def india():
    r = get("https://eaindustry.nic.in/indx_download_2223/wpi_monthly_index_202610.xlsx", timeout=120)
    res = [f"HTTP {r.status_code} {len(r.content)} bytes"]
    if r.ok:
        guardar("india_wpi.xlsx", r.content)
        for nombre, h in pd.read_excel(io.BytesIO(r.content), sheet_name=None, header=None).items():
            res.append(f"   hoja '{nombre}' {h.shape}; encabezado {h.iloc[0, :6].tolist()} ... {h.iloc[0, -3:].tolist()}")
            n, ej = filas_con(h, r"HR coil|CR coil|pig iron|sponge|coking coal|coke|bars|galvan|ferro|scrap|copper|alumin|zinc", n=25, ancho=3)
            res.append(f"   {n} filas de interés")
            res.extend(ej)
    return "\n".join(res)


def ternium():
    h = {"User-Agent": "ADIMRA Estudios Economicos estudios@adimra.org.ar"}
    res = []
    for doc in ["000134287426000044/prternium2q2026.htm"]:
        u = f"https://www.sec.gov/Archives/edgar/data/1342874/{doc}"
        r = requests.get(u, headers=h, timeout=60)
        res.append(f"{u} -> HTTP {r.status_code} {len(r.content)} bytes")
        tablas = pd.read_html(io.StringIO(r.text))
        for t in tablas:
            plano = t.fillna("").astype(str)
            if plano.apply(lambda c: c.str.contains("Southern Region", case=False)).any().any() and \
                    plano.apply(lambda c: c.str.contains("per ton|Revenue", case=False)).any().any():
                res.append("   tabla encontrada:\n" + "\n".join("      " + " | ".join(x for x in f if x.strip())[:160]
                                                          for f in plano.values.tolist()[:14]))
                break
    # índice de comunicados trimestrales para armar la historia
    j = requests.get("https://data.sec.gov/submissions/CIK0001342874.json", headers=h, timeout=60).json()
    rec = j["filings"]["recent"]
    q = [(rec["filingDate"][i], rec["primaryDocument"][i]) for i in range(len(rec["form"]))
         if re.match(r"prternium[1-4]q\d{4}", rec["primaryDocument"][i] or "")]
    res.append(f"comunicados trimestrales en 'recent': {len(q)}; primero {q[-1] if q else '-'}; files extra {len(j['filings'].get('files', []))}")
    return "\n".join(res)


def rosario_pdf():
    import subprocess
    subprocess.run(["pip", "install", "-q", "pdfplumber"], check=False)
    import pdfplumber
    u = "https://datos.rosario.gob.ar/sites/default/files/2026-08/07_26%20Informe%20indices%20mat%20de%20la%20construccion.pdf"
    r = get(u)
    res = [f"HTTP {r.status_code} {len(r.content)} bytes"]
    with pdfplumber.open(io.BytesIO(r.content)) as pdf:
        res.append(f"páginas {len(pdf.pages)}")
        for i, p in enumerate(pdf.pages):
            t = p.extract_text() or ""
            for linea in t.splitlines():
                if re.search(r"hierro|acero|chapa|tubo|perfil", linea, re.I):
                    res.append(f"   p{i + 1}: {linea[:150]}")
    return "\n".join(res[:40])


def imf():
    res = []
    for u in ["https://api.imf.org/external/sdmx/3.0/structure/dataflow/IMF.RES/PCPS/+?references=datastructure",
              "https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.RES/PCPS/+/*.PCOPP.*.M?c[TIME_PERIOD]=ge:2026-01",
              "https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.RES/PCPS/+/G001.PCOPP.USD.M"]:
        r = get(u, headers={**T.UA, "Accept": "application/json"})
        txt = r.text
        dims = re.findall(r'"id":"([A-Z_]+)","position"', txt)
        res.append(f"{u}\n   -> HTTP {r.status_code} {len(r.content)} bytes; dimensiones {dims[:8]}; {txt[:250]!r}")
    return "\n".join(res)


CASOS = [
    ("Local", "INDEC SIPM (IPIM 4 dígitos)", indec_sipm),
    ("Local", "INDEC ICC (materiales)", indec_icc),
    ("Local", "DGE Rosario (lectura del PDF)", rosario_pdf),
    ("Local", "Ternium (tabla de precio por tonelada)", ternium),
    ("Materias primas", "Comex Stat Brasil (con pausa)", comexstat),
    ("Materias primas", "Eurostat Comext (formato de período)", comext),
    ("Materias primas", "Banco de Japón (ítems de materias primas)", boj),
    ("No ferrosos", "Yahoo (búsqueda de futuros y chequeo)", yahoo_busqueda),
    ("No ferrosos", "Changjiang (páginas de precio)", changjiang),
    ("No ferrosos", "FMI (estructura de la API)", imf),
    ("Acero", "NBS (listado e historia)", nbs_lista),
    ("Acero", "CISA (índice de precios)", cisa),
    ("Acero", "Destatis (API nueva)", destatis),
    ("Acero", "India WPI (ítems)", india),
]
for b, n, f in CASOS:
    T.caso(b, n, f)

tabla = ["\n# Resumen\n", "| Bloque | Fuente | Estado | Detalle |", "|---|---|---|---|"]
tabla += [f"| {b} | {n} | {e} | {d.replace('|', '/')} |" for b, n, e, d in T.resumen]
(T.RES / "test_report_2.md").write_text("\n".join(tabla + T.out), encoding="utf-8")
print("\n".join(tabla))

"""Test 3: últimos detalles (BOJ, Yahoo, Changjiang, CISA, INDEC por código, profundidad histórica)."""
import datetime as dt
import io
import re

import pandas as pd

import test_fuentes as T

T.out.clear()
T.resumen.clear()
T.out.append(f"# Test 3 — {dt.datetime.utcnow():%Y-%m-%d %H:%M} UTC\n")
get, guardar = T.get, T.guardar


def indec_codigos():
    r = get("https://www.indec.gob.ar/ftp/cuadros/economia/series_sipm_dic2015.xls", timeout=120)
    h = pd.read_excel(io.BytesIO(r.content), sheet_name="IPIM", header=None)
    fila_fechas = None
    for i in range(12):
        if pd.to_datetime(h.iloc[i, 3:10], errors="coerce").notna().sum() > 3:
            fila_fechas = i
            break
    res = [f"fila de fechas: {fila_fechas}; últimas fechas {h.iloc[fila_fechas, -3:].tolist() if fila_fechas is not None else '-'}"]
    cod = h.iloc[:, 0].astype(str).str.strip()
    for c in ["27", "271", "2710", "272", "2720", "273", "28", "281", "289", "29", "2899", "2811"]:
        m = cod.eq(c)
        if m.any():
            f = h[m].iloc[0]
            res.append(f"   {c} {str(f.iloc[1]).strip()}: últimos {[round(float(x), 1) for x in f.iloc[-3:].tolist()]}")
        else:
            res.append(f"   {c}: no está")
    return "\n".join(res)


def boj():
    r = get("https://www.stat-search.boj.or.jp/api/v1/getMetadata", params={"format": "json", "lang": "en", "db": "PR01"}, timeout=120)
    filas = r.json().get("RESULTSET", [])
    claves = ["iron ore", "coking coal", "coal", "scrap", "pig iron", "ferro", "aluminium", "nickel", "zinc", "tin",
              "bars", "plates", "wire rods", "steel pipes", "galvan", "zinc-coated", "hot rolled", "cold rolled", "copper"]
    hits = [x for x in filas if any(k in str(x.get("NAME_OF_TIME_SERIES", "")).lower() for k in claves)
            and str(x.get("NAME_OF_TIME_SERIES", "")).startswith(("Commodity/", "Commodity class/"))]
    bloques = {}
    for x in filas:
        n = str(x.get("NAME_OF_TIME_SERIES", ""))
        if not n.startswith(("Commodity", "Subgroup", "Group")):
            bloques.setdefault(str(x.get("SERIES_CODE", ""))[:10], n)
    res = [f"series {len(filas)}; ítems de interés {len(hits)}", "Encabezados de bloque (para saber cuál es doméstico, export, import):"]
    res += [f"   {k}: {v}" for k, v in list(bloques.items())[:30]]
    vistos = set()
    for x in hits:
        clave = (str(x["SERIES_CODE"])[:10], x["NAME_OF_TIME_SERIES"])
        if clave in vistos:
            continue
        vistos.add(clave)
        res.append(f"   {x['SERIES_CODE']}: {x['NAME_OF_TIME_SERIES']} [{x.get('UNIT')}] {x.get('START_OF_THE_TIME_SERIES')}-{x.get('END_OF_THE_TIME_SERIES')}")
    return "\n".join(res[:140])


def yahoo():
    res = []
    for q in ["scrap", "steel", "rebar", "coking coal", "iron ore", "cobalt", "lithium", "hot-rolled", "turkish", "aluminium"]:
        r = get("https://query2.finance.yahoo.com/v1/finance/search", params={"q": q, "quotesCount": 20, "newsCount": 0})
        try:
            qs = r.json().get("quotes", [])
            fut = [f"{x.get('symbol')} ({x.get('shortname') or x.get('longname')})" for x in qs
                   if x.get("quoteType") == "FUTURE" or str(x.get("symbol", "")).endswith("=F")]
            res.append(f"'{q}': {fut}")
        except Exception as e:  # noqa: BLE001
            res.append(f"'{q}': HTTP {r.status_code} {e}")
    for t in ["BUS=F", "EHR=F", "TIO=F", "HRC=F", "ZNC=F"]:
        r = get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}", params={"range": "3mo", "interval": "1d"})
        x = r.json()["chart"]["result"][0]
        q = x.get("indicators", {}).get("quote", [{}])[0]
        cl = [c for c in (q.get("close") or []) if c is not None]
        res.append(f"{t}: {len(cl)} obs en 3 meses; últimos {cl[-4:]}; meta {x['meta'].get('regularMarketPrice')}")
    return "\n".join(res)


def changjiang():
    res = []
    for metal, u in [("cobre", "https://copper.ccmn.cn/copperprice/cjxh/"), ("aluminio", "https://alu.ccmn.cn/aluprice/cjxh/"),
                     ("zinc", "https://zinc.ccmn.cn/zincprice/cjxh/"), ("níquel", "https://nickel.ccmn.cn/nickelprice/cjxh/")]:
        r = get(u)
        r.encoding = r.apparent_encoding
        links = re.findall(r'href="([^"]+)"[^>]*>[^<]*\d{1,2}月\d{1,2}日长江[^<]*价格行情参考', r.text)
        if not links:
            res.append(f"{metal}: HTTP {r.status_code}, sin links")
            continue
        link = links[0] if links[0].startswith("http") else "https://www.ccmn.cn" + links[0]
        a = get(link)
        a.encoding = a.apparent_encoding
        guardar(f"ccmn_{metal}.html", a.text)
        tablas = []
        try:
            tablas = pd.read_html(io.StringIO(a.text))
        except ValueError:
            pass
        muestra = [t.head(4).values.tolist() for t in tablas[:2]]
        nums = re.findall(r"(\d{4,6})\s*[-—–]\s*(\d{4,6})", re.sub(r"<[^>]+>", " ", a.text))
        res.append(f"{metal}: {link} -> HTTP {a.status_code}; tablas {len(tablas)} {str(muestra)[:300]}; rangos {nums[:3]}")
        p2 = get(u + "index_2.html")
        res.append(f"   página 2 del listado: HTTP {p2.status_code}")
    return "\n".join(res)


def cisa():
    base = "http://www.chinaisa.org.cn/gxportal/xfgl/portal/"
    col = "17b6a9a214c94ccc28e56d4d1a2dbb5acef3e73da431ddc0a849a4dcfc487d04"
    r = get(base + f"list.html?columnId={col}")
    r.encoding = r.apparent_encoding
    guardar("cisa_lista.html", r.text)
    txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", r.text))
    links = re.findall(r'href="([^"]*content\.html[^"]*)"', r.text)
    res = [f"lista -> HTTP {r.status_code} {len(r.content)} bytes; links {links[:3]}; texto {txt[:300]!r}"]
    # la lista suele cargarse por AJAX: probar el endpoint
    for u, data in [(base + "getColumnList", {"columnId": col, "pageNumber": 1, "pageSize": 10}),
                    ("http://www.chinaisa.org.cn/gxportal/xfpt/portal/getColumnList", {"params": '{"columnId":"%s"}' % col})]:
        try:
            import requests
            x = requests.post(u, data=data, headers=T.UA, timeout=60)
            res.append(f"POST {u} -> HTTP {x.status_code} {x.text[:300]!r}")
        except Exception as e:  # noqa: BLE001
            res.append(f"POST {u} -> ERROR {e}"[:200])
    return "\n".join(res)


def profundidad():
    res = []
    r = get("https://www.shfe.com.cn/data/tradedata/future/dailydata/kx20100104.dat", headers={**T.UA, "Referer": "https://www.shfe.com.cn/"})
    res.append(f"SHFE 2010-01-04: HTTP {r.status_code} {len(r.content)} bytes")
    r = get("https://www.shfe.com.cn/data/tradedata/future/dailydata/kx20180102.dat", headers={**T.UA, "Referer": "https://www.shfe.com.cn/"})
    res.append(f"SHFE 2018-01-02: HTTP {r.status_code} {len(r.content)} bytes")
    r = get("http://www.czce.com.cn/cn/DFSStaticFiles/Future/2018/20180102/FutureDataDaily.txt")
    res.append(f"ZCE 2018-01-02: HTTP {r.status_code} {len(r.content)} bytes")
    r = get("https://www.stats.gov.cn/sj/zxfb/index_60.html")
    r.encoding = "utf-8"
    res.append(f"NBS listado pág. 60: informes {re.findall(r'(\d{4}年\d{1,2}月[上中下]旬)流通领域', r.text)[:2]}")
    return "\n".join(res)


CASOS = [("Local", "INDEC IPIM por código (2710, 2720, 28...)", indec_codigos),
         ("Materias primas", "Banco de Japón (ítems)", boj),
         ("No ferrosos", "Yahoo (búsqueda)", yahoo),
         ("No ferrosos", "Changjiang (valores del día)", changjiang),
         ("Acero", "CISA (lista del índice)", cisa),
         ("General", "Profundidad histórica SHFE / ZCE / NBS", profundidad)]
for b, n, f in CASOS:
    T.caso(b, n, f)
tabla = ["\n# Resumen\n", "| Bloque | Fuente | Estado | Detalle |", "|---|---|---|---|"]
tabla += [f"| {b} | {n} | {e} | {d.replace('|', '/')} |" for b, n, e, d in T.resumen]
(T.RES / "test_report_3.md").write_text("\n".join(tabla + T.out), encoding="utf-8")
print("\n".join(tabla))

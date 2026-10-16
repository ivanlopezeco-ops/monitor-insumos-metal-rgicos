"""Test 4: futuros encontrados por el buscador de Yahoo, índices de importación del BOJ y lista de CISA."""
import datetime as dt
import re
import time

import requests

import test_fuentes as T

T.out.clear()
T.resumen.clear()
T.out.append(f"# Test 4 — {dt.datetime.utcnow():%Y-%m-%d %H:%M} UTC\n")


def yahoo():
    res = []
    for t in ["FSF=F", "HDG=F", "EHR=F", "LTH=F", "TIO=F", "BUS=F"]:
        r = T.get(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}",
                  params={"period1": int(dt.datetime(2005, 1, 1).timestamp()), "period2": int(time.time()), "interval": "1d"})
        x = r.json()["chart"]["result"][0]
        q = x.get("indicators", {}).get("quote", [{}])[0]
        pares = [(dt.datetime.utcfromtimestamp(a).date(), b) for a, b in zip(x.get("timestamp") or [], q.get("close") or []) if b is not None]
        ult90 = [p for p in pares if p[0] >= dt.date.today() - dt.timedelta(days=90)]
        res.append(f"{t} {x['meta'].get('shortName')} [{x['meta'].get('currency')}]: obs {len(pares)}, desde {pares[0][0] if pares else '-'}, "
                   f"último {pares[-1] if pares else '-'}, obs últimos 90 días {len(ult90)}")
    return "\n".join(res)


def boj():
    filas = T.get("https://www.stat-search.boj.or.jp/api/v1/getMetadata", params={"format": "json", "lang": "en", "db": "PR01"},
                  timeout=120).json().get("RESULTSET", [])
    claves = ["iron ore", "coking", "coal", "scrap", "pig iron", "ferro", "aluminium", "nickel", "zinc", "copper", "steel"]
    res = []
    for pref, nombre in [("PRCG20_250", "Importación, moneda de contrato"), ("PRCG20_230", "Exportación, moneda de contrato")]:
        hits = [x for x in filas if str(x.get("SERIES_CODE", "")).startswith(pref)
                and str(x.get("NAME_OF_TIME_SERIES", "")).startswith("Commodity/")
                and any(k in str(x.get("NAME_OF_TIME_SERIES", "")).lower() for k in claves)]
        res.append(f"{nombre}: {len(hits)} ítems")
        res += [f"   {x['SERIES_CODE']}: {x['NAME_OF_TIME_SERIES']} {x.get('START_OF_THE_TIME_SERIES')}-{x.get('END_OF_THE_TIME_SERIES')}" for x in hits[:30]]
    return "\n".join(res)


def cisa():
    col = "17b6a9a214c94ccc28e56d4d1a2dbb5acef3e73da431ddc0a849a4dcfc487d04"
    r = requests.post("http://www.chinaisa.org.cn/gxportal/xfpt/portal/getColumnList", data={"params": '{"columnId":"%s"}' % col},
                      headers=T.UA, timeout=60)
    html = r.json().get("articleListHtml", "")
    items = re.findall(r"articleId=([0-9a-f]+)[^>]*>([^<]+)<.*?(\d{4}-\d{2}-\d{2})", html, flags=re.S)
    res = [f"HTTP {r.status_code}; artículos {len(items)}"] + [f"   {f} {t.strip()} ({a[:10]}...)" for a, t, f in items[:8]]
    if items:
        a = items[0][0]
        x = requests.post("http://www.chinaisa.org.cn/gxportal/xfpt/portal/viewArticleById", data={"params": '{"articleId":"%s","columnId":"%s"}' % (a, col)},
                          headers=T.UA, timeout=60)
        txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x.text))
        res.append(f"artículo -> HTTP {x.status_code}: {txt[:600]!r}")
    return "\n".join(res)


for b, n, f in [("Futuros", "Yahoo: chatarra Turquía, galvanizado, HRC Europa, litio", yahoo),
                ("Materias primas", "BOJ: índices de importación y exportación", boj),
                ("Acero", "CISA: artículos del índice", cisa)]:
    T.caso(b, n, f)
(T.RES / "test_report_4.md").write_text("\n".join(T.out), encoding="utf-8")

"""Arma site/data.json para el tablero: catálogo + series convertidas a la unidad del tablero (USD/t).

Para cada serie se exporta:
  d  datos en la unidad del tablero (USD/t o índice)
  o  datos en la unidad original (solo si es distinta)
Los pesos se calculan en el navegador con el A3500 (diario y promedio mensual), que va aparte.
"""
import datetime as dt
import json
import math
import pathlib

import pandas as pd
import yaml

BASE = pathlib.Path(__file__).resolve().parents[1]
DATA = BASE / "data"
SITE = BASE / "site"


def redondear(x, sig=6):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return None
    if x == 0:
        return 0
    return round(x, max(0, sig - 1 - int(math.floor(math.log10(abs(x))))))


def serie(base, sid):
    d = base[base["id"] == sid][["fecha", "valor", "marca"]].dropna(subset=["valor"])
    d = d.assign(fecha=pd.to_datetime(d["fecha"])).sort_values("fecha").drop_duplicates("fecha", keep="last")
    return d.set_index("fecha")


def cambio(base, sid, fechas, mensual):
    """Tipo de cambio para cada fecha: promedio del mes si la serie es mensual o trimestral; si no, último dato disponible."""
    tc = serie(base, sid)["valor"]
    if tc.empty:
        return pd.Series(index=fechas, dtype=float)
    if mensual:
        m = tc.groupby(tc.index.to_period("M")).mean()
        return pd.Series([m.get(f.to_period("M"), float("nan")) for f in fechas], index=fechas).ffill()
    return tc.reindex(tc.index.union(fechas)).ffill().reindex(fechas)


def convertir(base, s, d):
    u = (s.get("unidad_original") or "").lower()
    mensual = s.get("frecuencia") in ("mensual", "trimestral")
    v = d["valor"]
    if "tonelada corta" in u:
        return v / 0.907185
    if "libra" in u:
        return v * 2204.62
    if "cny" in u:
        return v / 1.13 * cambio(base, "usd_por_cny", d.index, mensual)
    if "eur/100 kg" in u:
        return v * 10 * cambio(base, "usd_por_eur", d.index, mensual)
    if "eur" in u:
        return v * cambio(base, "usd_por_eur", d.index, mensual)
    return v


def main():
    cat = yaml.safe_load((BASE / "config" / "catalogo.yaml").read_text(encoding="utf-8"))
    base = pd.read_csv(DATA / "series.csv", keep_default_na=False)
    base["valor"] = pd.to_numeric(base["valor"], errors="coerce")
    estado = json.loads((DATA / "estado.json").read_text()) if (DATA / "estado.json").exists() else {}
    val = estado.get("series", {})

    def calc_galv():   # galvanizado estimado = futuro HRC + prima
        a, b = serie(base, "hrc_eeuu_futuro")["valor"], serie(base, "galv_eeuu_prima")["valor"]
        x = (a + b.reindex(a.index)).dropna()
        return pd.DataFrame({"valor": x, "marca": ""})

    series, insumos = {}, []
    for ins in cat["insumos"]:
        ids = []
        for s in ins["series"]:
            if s.get("estado") == "pendiente":
                continue
            d = calc_galv() if s["id"] == "galv_eeuu_estimado" else serie(base, s["id"])
            if s["id"] == "galv_eeuu_estimado" and not d.empty:
                d = d.assign(valor=d["valor"] / 0.907185)  # ya en USD/t
                conv = d["valor"]
            else:
                conv = convertir(base, s, d) if not d.empty else d.get("valor", pd.Series(dtype=float))
            prov = d.index[d["marca"] == "provisorio"].min() if not d.empty and (d["marca"] == "provisorio").any() else None
            reg = {k: s.get(k) for k in ["nombre", "mercado", "tipo", "que_mide", "limitaciones", "frecuencia", "rezago", "desde",
                                        "unidad_original", "unidad_tablero", "conversion", "licencia", "estado"]}
            reg["fuente"] = s.get("fuente", {})
            reg["validacion"] = val.get(s["id"], {})
            reg["d"] = [[f.strftime("%Y-%m-%d"), redondear(x)] for f, x in conv.items() if x is not None and not math.isnan(x)]
            if not d.empty and any(k in (s.get("unidad_original") or "").lower() for k in ["cny", "eur", "libra", "corta"]) \
                    and s["id"] != "galv_eeuu_estimado":
                reg["o"] = [[f.strftime("%Y-%m-%d"), redondear(x)] for f, x in d["valor"].items()]
            reg["p"] = prov.strftime("%Y-%m-%d") if prov is not None else None
            series[s["id"]] = reg
            ids.append(s["id"])
        insumos.append({k: ins.get(k) for k in ["id", "grupo", "nombre", "que_es", "por_que_importa"]} | {"series": ids})
    a3 = serie(base, "tc_a3500")["valor"]
    salida = {
        "generado": estado.get("generado") or dt.datetime.utcnow().isoformat() + "Z",
        "tipos": cat["tipos"],
        "insumos": insumos,
        "series": series,
        "a3500": [[f.strftime("%Y-%m-%d"), round(x, 4)] for f, x in a3.items()],
        "fuentes": {k: {c: v.get(c) for c in ["estado", "filas", "ultimo_ok", "error", "detalle"]} for k, v in estado.get("fuentes", {}).items()},
    }
    SITE.mkdir(exist_ok=True)
    (SITE / "data.json").write_text(json.dumps(salida, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"data.json: {len(series)} series, {(SITE / 'data.json').stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()

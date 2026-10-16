"""Corrida del monitor: descarga, valida, guarda y exporta.

Salidas en data/ (viven en la rama "datos"):
  series.csv     base larga acumulada: fecha, id, valor, unidad, fuente, marca
  estado.json    estado de cada fuente, cursores del relleno histórico y hora de la última descarga
  validacion.md  controles por serie (dato viejo, salto raro, sin datos)
Al final llama a exportar.py, que arma site/data.json.
"""
import datetime as dt
import json
import pathlib
import time
import traceback

import pandas as pd
import yaml

import fuentes as F

BASE = pathlib.Path(__file__).resolve().parents[1]
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)
CAT = yaml.safe_load((BASE / "config" / "catalogo.yaml").read_text(encoding="utf-8"))
SERIES_CAT = [s for i in CAT["insumos"] for s in i["series"]]

# (nombre, función, horas mínimas entre descargas)
FUENTES = [
    ("BCRA A3500", F.bcra_a3500, 0),
    ("BCRA tipos de pase", F.bcra_monedas, 0),
    ("Yahoo (futuros CME)", F.yahoo, 0),
    ("Westmetall (LME)", F.westmetall, 0),
    ("SHFE (Shanghái)", F.shfe, 0),
    ("ZCE (Zhengzhou)", F.zce, 0),
    ("NBS China", F.nbs, 6),
    ("Banco Mundial", F.pink_sheet, 24),
    ("BLS (EE.UU.)", F.bls, 12),
    ("Comex Stat (Brasil)", F.comexstat, 24),
    ("Eurostat Comext", F.comext, 24),
    ("Eurostat PPI", F.eurostat_ppi, 24),
    ("Banco de Japón", F.boj, 24),
    ("IBGE", F.ibge, 24),
    ("India WPI", F.india, 24),
    ("INDEC SIPM", F.indec_sipm, 12),
    ("INDEC por producto", F.indec_productos, 12),
    ("Precio realizado (SEC)", F.precio_realizado, 24),
]
LIMITE_DIAS = {"diaria": 6, "semanal": 16, "decadal": 25, "mensual": 80, "trimestral": 240}   # para avisar "dato viejo"
SALTO = {"diaria": 0.12, "decadal": 0.15, "semanal": 0.15, "mensual": 0.30, "trimestral": 0.35}  # variación que se marca para revisar


class Ctx:
    def __init__(self, base, estado):
        self.base = base
        self.cursor = estado.setdefault("cursores", {})
        self.series_catalogo = SERIES_CAT
        self._ids = set(base["id"].unique()) if len(base) else set()

    def completo(self, sid):          # True si la serie todavía no está en la base: hay que bajar toda la historia
        return sid not in self._ids

    def fechas(self, sid):
        return list(self.base.loc[self.base["id"] == sid, "fecha"]) if len(self.base) else []


def cargar():
    p = DATA / "series.csv"
    if p.exists():
        b = pd.read_csv(p, dtype={"unidad": str, "fuente": str, "marca": str}, keep_default_na=False)
        b["fecha"] = pd.to_datetime(b["fecha"]).dt.date
        b["valor"] = pd.to_numeric(b["valor"], errors="coerce")
        return b
    return pd.DataFrame(columns=F.COLS)


def unir(base, nuevo):
    if nuevo is None or nuevo.empty:
        return base
    nuevo = nuevo.drop_duplicates(["fecha", "id"], keep="last")
    # un dato provisorio no pisa uno definitivo del mismo día que ya estaba
    if len(base):
        clave = base.set_index(["fecha", "id"])["marca"]
        k = list(zip(nuevo["fecha"], nuevo["id"]))
        pisa_def = [clave.get(x, "provisorio") == "" and m == "provisorio" for x, m in zip(k, nuevo["marca"])]
        nuevo = nuevo[[not p for p in pisa_def]]
    b = pd.concat([base, nuevo]).drop_duplicates(["fecha", "id"], keep="last")
    return b.sort_values(["id", "fecha"]).reset_index(drop=True)


def validar(base, estado):
    out, filas = {}, ["# Validación por serie\n", "| Serie | Último dato | Obs. | Estado | Detalle |", "|---|---|---|---|---|"]
    for s in SERIES_CAT:
        if s.get("estado") == "pendiente" or s["id"] == "galv_eeuu_estimado":
            continue
        d = base[base["id"] == s["id"]].sort_values("fecha")
        if d.empty:
            out[s["id"]] = {"estado": "sin_datos"}
            filas.append(f"| {s['id']} | - | 0 | SIN DATOS | |")
            continue
        ult, n = d.iloc[-1], len(d)
        dias = (F.HOY - ult["fecha"]).days
        fr = s.get("frecuencia", "mensual")
        notas, est = [], "ok"
        if dias > LIMITE_DIAS.get(fr, 80):
            est = "viejo"
            notas.append(f"último dato hace {dias} días")
        if n > 1:
            v0, v1 = d.iloc[-2]["valor"], ult["valor"]
            if v0 and abs(v1 / v0 - 1) > SALTO.get(fr, 0.3):
                notas.append(f"salto de {100 * (v1 / v0 - 1):+.1f}% en el último dato")
                est = "revisar" if est == "ok" else est
        if (d["valor"] <= 0).any() and not s["id"].endswith("prima"):
            notas.append("hay valores menores o iguales a cero")
        out[s["id"]] = {"estado": est, "ultimo": str(ult["fecha"]), "obs": n, "notas": notas}
        filas.append(f"| {s['id']} | {ult['fecha']} | {n} | {est} | {'; '.join(notas)} |")
    estado["series"] = out
    (DATA / "validacion.md").write_text("\n".join(filas), encoding="utf-8")


def main():
    estado = json.loads((DATA / "estado.json").read_text()) if (DATA / "estado.json").exists() else {}
    estado.setdefault("fuentes", {})
    base = cargar()
    ahora = dt.datetime.utcnow()
    for nombre, f, horas in FUENTES:
        prev = estado["fuentes"].get(nombre, {})
        ult_ok = prev.get("ultimo_ok")
        if horas and ult_ok and (ahora - dt.datetime.fromisoformat(ult_ok)).total_seconds() < horas * 3600:
            prev["estado"] = "al día (no se volvió a pedir)"
            estado["fuentes"][nombre] = prev
            continue
        t0 = time.time()
        ctx = Ctx(base, estado)
        try:
            df = f(ctx)
            base = unir(base, df)
            estado["fuentes"][nombre] = {"estado": "ok", "filas": int(len(df)), "ultimo_ok": ahora.isoformat(timespec="seconds"),
                                         "segundos": round(time.time() - t0, 1), "detalle": df.attrs.get("detalle", ""),
                                         "error": "; ".join(df.attrs.get("errores", []))[:400]}
        except Exception as e:  # noqa: BLE001
            estado["fuentes"][nombre] = {**prev, "estado": "error", "error": f"{type(e).__name__}: {e}"[:400],
                                         "traza": traceback.format_exc()[-800:], "segundos": round(time.time() - t0, 1)}
        print(f"{nombre}: {estado['fuentes'][nombre]['estado']} ({estado['fuentes'][nombre].get('filas', '-')} filas, "
              f"{estado['fuentes'][nombre].get('segundos')} s) {estado['fuentes'][nombre].get('error', '')[:150]}", flush=True)
    validar(base, estado)
    estado["generado"] = ahora.isoformat(timespec="seconds") + "Z"
    base.to_csv(DATA / "series.csv", index=False)
    (DATA / "estado.json").write_text(json.dumps(estado, ensure_ascii=False, indent=1), encoding="utf-8")
    import exportar
    exportar.main()


if __name__ == "__main__":
    main()

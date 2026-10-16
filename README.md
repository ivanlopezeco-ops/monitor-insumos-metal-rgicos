# Monitor de costos metalúrgicos

Tablero de precios de insumos para empresas metalúrgicas (ADIMRA, Departamento de Estudios Económicos).
Misma arquitectura que el tablero macroeconómico: pipeline en Python con GitHub Actions, base acumulada
en la rama `datos` y página en GitHub Pages.

## Etapa actual: prueba de fuentes

`tests/test_fuentes.py` consulta cada fuente candidata y deja el resultado en `results/test_report.md`
(con un resumen al principio) y los crudos en `results/samples/`. Corre solo al subir cambios en `tests/`
o a mano desde la pestaña Actions ("Run workflow").

Bloques en prueba: no ferrosos, materias primas siderúrgicas, acero por mercado y precios locales.

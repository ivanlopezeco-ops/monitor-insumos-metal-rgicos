
# Resumen

| Bloque | Fuente | Estado | Detalle |
|---|---|---|---|
| Local | INDEC SIPM (IPIM 4 dígitos) | OK | https://www.indec.gob.ar/ftp/cuadros/economia/series_sipm_dic2015.xls -> HTTP 200 1067520 bytes, modif. Fri, 1 |
| Local | INDEC ICC (materiales) | OK | https://www.indec.gob.ar/ftp/cuadros/economia/icc_variaciones_indices_item_2016.xls -> HTTP 200 90624 bytes |
| Local | DGE Rosario (lectura del PDF) | OK | HTTP 200 722174 bytes |
| Local | Ternium (tabla de precio por tonelada) | OK | https://www.sec.gov/Archives/edgar/data/1342874/000134287426000044/prternium2q2026.htm -> HTTP 200 592718 byte |
| Materias primas | Comex Stat Brasil (con pausa) | OK | Brasil importa: carbón coque, coque, chatarra, DRI: HTTP 200 8764 bytes |
| Materias primas | Eurostat Comext (formato de período) | OK | variante {'sinceTimePeriod': '2025-01'}: HTTP 200 '{"version":"2.0","class":"dataset","label":"EU trade since  |
| Materias primas | Banco de Japón (ítems de materias primas) | ERROR | JSONDecodeError: Unterminated string starting at: line 1 column 399992 (char 399991) |
| No ferrosos | Yahoo (búsqueda de futuros y chequeo) | ERROR | KeyError: 'close' |
| No ferrosos | Changjiang (páginas de precio) | OK | https://copper.ccmn.cn/copperprice/cjxh/ -> HTTP 200 41408 bytes; tablas 1; muestra [['【长江铜价格】', '10月16日长江铜价格行 |
| No ferrosos | FMI (estructura de la API) | OK | https://api.imf.org/external/sdmx/3.0/structure/dataflow/IMF.RES/PCPS/+?references=datastructure |
| Acero | NBS (listado e historia) | OK | links: 9 |
| Acero | CISA (índice de precios) | OK | HTTP 200; contexto: '                 \r\n             \r\n             \r\n                 \r\n              |
| Acero | Destatis (API nueva) | OK | POST helloworld/logincheck -> HTTP 200 165 bytes application/json;charset=UTF-8 |
| Acero | India WPI (ítems) | OK | HTTP 200 331956 bytes |
# Test 2 — 2026-10-16 23:02 UTC


## [Local] INDEC SIPM (IPIM 4 dígitos)
https://www.indec.gob.ar/ftp/cuadros/economia/series_sipm_dic2015.xls -> HTTP 200 1067520 bytes, modif. Fri, 16 Oct 2026 18:52:31 GMT
   hoja 'Índice' (7, 1): 0 filas con metales
      celdas numéricas 0; primeras filas: SISTEMA DE ÍNDICES DE PRECIOS MAYORISTAS (SIPM) || nan || Índice || nan || Cuadro 1. Índice de Precios Internos al por Mayor (IPIM), base año 1993, periodo de referencia diciembre 2015=100. || Cuadro 2. Índice de Precios Internos Básicos al por Mayor (IPIB), base año 1993, periodo de referencia diciembre 2015=100.
   hoja 'IPIM' (155, 132): 119 filas con metales
      NG | Nivel general | 100 | 108.78717907264219 | 114.17088428630503
      1 | Primarios | 100 | 109.22178107352131 | 114.72663147724357
      A |  Productos agropecuarios | 100 | 102.55410419205293 | 109.70959829607973
      0111 |  Cereales y oleaginosas | 100 | 113.75705349740785 | 121.00995512760296
      0112 |  Hortalizas y legumbres | 100 | 109.60990606329119 | 115.67420436975002
      0113 |  Frutas | 100 | 138.76662159775498 | 172.81574601952948
      012 |  Ganaderos | 100 | 96.9028321258066 | 102.07428769702926
      0121 |  Ganado vacuno y leche | 100 | 96.1492935818583 | 101.41463306643021
      celdas numéricas 18082; primeras filas: SISTEMA DE ÍNDICES DE PRECIOS MAYORISTAS (SIPM) ; nan ; nan ; nan ; nan ; nan || Índice de Precios Internos al por Mayor (IPIM), base año 1993, periodo de referencia diciembre 2015=100 ; nan ; nan ; nan ; nan ; nan || nan ; nan ; nan ; nan ; nan ; nan || Código ; Descripción ; 2015 ; 2016 ; nan ; nan || nan ; nan ; Dic ; Ene ; Feb ; Mar || nan ; nan ; Número índice ; nan ; nan ; nan
   hoja 'IPIB' (155, 132): 127 filas con metales
      NG | Nivel general | 100 | 109.01190453958323 | 114.55178790732718
      N | Productos nacionales | 100 | 108.35403678025716 | 113.5737571195419
      1 | Primarios | 100 | 109.12741478829737 | 115.28914439054091
      A |  Productos agropecuarios | 100 | 104.28347471507264 | 112.12223473903582
      011 |  Agrícolas | 100 | 113.5852829336208 | 124.63246473315986
      0111 |  Cereales y oleaginosas | 100 | 111.02394162916636 | 119.93114831857379
      0112 |  Hortalizas y legumbres | 100 | 109.60612658135727 | 115.66833366640523
      0113 |  Frutas | 100 | 138.74850318076486 | 172.78346720087015
      celdas numéricas 18082; primeras filas: SISTEMA DE ÍNDICES DE PRECIOS MAYORISTAS (SIPM) ; nan ; nan ; nan ; nan ; nan || Índice de Precios Internos Básicos al por Mayor (IPIB), base año 1993, periodo de referencia diciembre 2015=100 ; nan ; nan ; nan ; nan ; nan || nan ; nan ; nan ; nan ; nan ; nan || Código ; Descripción ; 2015 ; 2016 ; nan ; nan || nan ; nan ; Dic ; Ene ; Feb ; Mar || nan ; nan ; Número índice ; nan ; nan ; nan
   hoja 'IPP' (153, 132): 123 filas con metales
      NG | Nivel general | 100 | 109.10494620714626 | 114.57440926480469
      N | Productos nacionales | 100 | 109.10494620714626 | 114.57440926480469
      1 | Primarios | 100 | 110.05171098397683 | 116.7983218925156
      A |  Productos agropecuarios | 100 | 106.10351737472045 | 114.75690380058019
      011 |  Agrícolas | 100 | 114.12673967393026 | 125.71228031406488
      0111 |  Cereales y oleaginosas | 100 | 111.02394162916636 | 119.93114831857379
      0112 |  Hortalizas y legumbres | 100 | 109.60612658135727 | 115.66833366640523
      0113 |  Frutas | 100 | 138.74850318076486 | 172.78346720087015
      celdas numéricas 17952; primeras filas: SISTEMA DE ÍNDICES DE PRECIOS MAYORISTAS (SIPM) ; nan ; nan ; nan ; nan ; nan || Índice de Precios Básicos del Productor (IPP), base año 1993, periodo de referencia diciembre 2015=100. ; nan ; nan ; nan ; nan ; nan || nan ; nan ; nan ; nan ; nan ; nan || Código ; Descripción ; 2015 ; 2016 ; nan ; nan || nan ; nan ; Dic ; Ene ; Feb ; Mar || nan ; nan ; Número índice ; nan ; nan ; nan
https://www.indec.gob.ar/ftp/cuadros/economia/IPIM-dde1993.xls -> HTTP 200 1097216 bytes, modif. Tue, 14 Jun 2016 17:50:12 GMT
   hoja '1993' (207, 14): 15 filas con metales
      26 Productos de minerales no metálicos | 98.271 | 98.4396 | 98.9523
      269 Otros productos de minerales no metálicos | 97.922 | 97.9868 | 98.6555
      estructural | 97.7916 | 97.8385 | 99.2205
      27 Productos metálicos básicos | 99.9798 | 99.9901 | 100.1668
      273 Productos de fundición | 100 | 100 | 100
      28 Productos metálicos excepto máquinas y equipos | 100.0643 | 100.0489 | 100.1274
      281 Productos metálicos estructurales, recipientes y
      2811 Productos metálicos para uso estructural | 100.0333 | 100.0333 | 100.0333
      celdas numéricas 2089; primeras filas: SISTEMA DE INDICES DE PRECIOS MAYORISTAS (SIPM) ; nan ; nan ; nan ; nan ; nan || Series del SIPM base 1993 = 100 ; nan ; nan ; nan ; nan ; nan || nan ; nan ; nan ; nan ; nan ; nan || Indice de Precios Internos al por Mayor (IPIM) - Año 1993 ; nan ; nan ; nan ; nan ; nan || nan ; nan ; nan ; nan ; nan ; nan || Concepto ; nan ; nan ; nan ; nan ; nan
   hoja '1994' (201, 17): 11 filas con metales
     
_(6.0 s)_

## [Local] INDEC ICC (materiales)
https://www.indec.gob.ar/ftp/cuadros/economia/icc_variaciones_indices_item_2016.xls -> HTTP 200 90624 bytes
   hoja 'Ítem de obra_variaciones' (25, 144): 2 filas con acero
      8- | Carpintería metálica y herrería | 0.9303561935140925 | 6.715828285488534
      9- | Carpintería de madera | 1.279166173161217 | 5.461349549760253
   hoja 'Ítems de obra_índices' (24, 63): 2 filas con acero
      8- | Carpintería metálica y herrería | 100 | 105.61061404405004 | 107.49054923883058
      9- | Carpintería de madera | 100 | 104.34830158139943 | 109.42387191320896
https://www.indec.gob.ar/ftp/cuadros/economia/op_icc_sipm_2016.xls -> HTTP 200 1357824 bytes
   hoja '1, IPIB' (204, 145): 0 filas con acero
   hoja '2 y 3 IPIB apertura' (212, 145): 27 filas con acero
      (1) | 2811 | 42120-2 | Aberturas de chapa de hierro                                            | s
      (2) | 2710 | 41263-1 | Alambres de acero                                                       | 100
      (2) | 2710 | 41241-1 | Alambrones de hierro                                                    | s
      (2) | 2710 | 41261-1 | Barras de hierro y acero                                                | 100
      (10) | 2520 | 36320-3 | Caños y tubos de polietileno                                            | s
      (7) | 2520 | 36320-2 | Caños y tubos de polipropileno                                          | s
      2520 | 36320-1 | Caños y tubos de PVC                                                    | 100
      2899 | 42999-2 | Chapas metálicas                                                        | 100
   hoja '4, ICC cont.' (169, 13): 2 filas con acero
      c) Pisos y revestimientos
      m) Acero aletado conformado de dureza natural, tipo ADN 420 (IRAM-IAS U 500-528), tensión máxima admisible 2.400 kg/cm2,
   hoja '5, ICC' (28, 147): 2 filas con acero
      d) | Carpinterías | Cuadro 1.5 | Ítem Carpintería metálica y herrería | 100
      h) | Caños de PVC para instalaciones varias | Cuadro 1.9 | Caños de PVC | 100
   hoja '6, Servicios' (27, 147): 0 filas con acero
   hoja '7, y 8Cap. M. Obra' (57, 150): 0 filas con acero
   hoja '9, Equipos' (26, 147): 0 filas con acero
   hoja '10, Cap Gtos. Grales.' (39, 147): 0 filas con acero
   hoja '11 y 12Cap. Mat.' (257, 148): 44 filas con acero
      42911 | - | 81 | Accesorios metálicos para baño
      41242 | - | 11 | Acero aletado conformado, en barra
      42911 | - | 11 | Bañera de chapa porcelanizada
      46212 | - | 21 | Caja de chapa con tablero trifásico
      42999 | - | 23 | Caja de chapa para tablero
      42999 | - | 21 | Caja octogonal de chapa para instalación eléctrica
      42999 | - | 22 | Caja rectangular de chapa para instalación eléctrica
      41277 | - | 21 | Caño de acero para instalaciones eléctricas
_(4.2 s)_

## [Local] DGE Rosario (lectura del PDF)
HTTP 200 722174 bytes
páginas 8
   p2: Chapas galvanizadas 2,0 9,1 -0,9
   p2: Hierro fundido 0,9 5,5 0,7
   p2: Hierro redondo y acero para construcción 0,0 7,9 -1,0
   p2: Tubos estructurales 3,1 23,8 6,7
   p3: Chapas galvanizadas 2,0
   p3: Hierro fundido 0,9
   p3: Hierro redondo y acero para construcción 0,0
   p3: Tubos estructurales 3,1
   p4: CHAPAS GALVANIZADAS CONDUCTORES DE COBRE
   p5: HIERRO FUNDIDO HIERRO RED. Y ACERO PARA LA CONSTRUCCIÓN
   p6: SANITARIOS DE CERÁMICA TUBOS ESTRUCTURALES
   p7: Tubos PVC 10 atmosférico diámetro 75 mm (incluído aro de caucho)
   p7: Tubos PVC 10 atmosférico diámetro 110 mm (incluído aro de caucho)
   p7: Chapas galvanizadas Chapa ondulada galvanizada nº 27, ancho 1,10m
   p7: Chapa Galvanizada n° 14
   p7: Hierro fundido Caño de F F de 4mm x 100mm x 3000mm
   p7: Hierro redondo y acero para construcción Acero alto límite de fluyen. 2400 Kg/cm2 diam. 10 mm (e/b)
   p8: Tubos estructurales Tubo de acero estructural 100x60x3,2 mm barra 6 m
   p8: Tubo acero estructural recto 30x30mm e:2mm barra 6 m
   p8: Tubo acero estructural recto 40x40mm e:2mm barra 6 m
_(3.9 s)_

## [Local] Ternium (tabla de precio por tonelada)
https://www.sec.gov/Archives/edgar/data/1342874/000134287426000044/prternium2q2026.htm -> HTTP 200 592718 bytes
   tabla encontrada:
      
      STEEL SEGMENT | STEEL SEGMENT | STEEL SEGMENT | NET SALES ($ MILLION) | NET SALES ($ MILLION) | NET SALES ($ MILLION) | NET SALES ($ MILLION) | NET SALES ($ MIL
      
      2Q26 | 2Q26 | 2Q26 | 1Q26 | 1Q26 | 1Q26 | DIF | DIF | DIF | 2Q25 | 2Q25 | 2Q25 | DIF | DIF | DIF | 2Q26 | 2Q26 | 2Q26 | 1Q26 | 1Q26 | 1Q26 | DIF | DIF | DIF | 2
      
      Mexico | Mexico | Mexico | 2219 | 2219 | 1985 | 1985 | 12 | 12 | % | 1780 | 1780 | 25 | 25 | % | 2082 | 2082 | 1983 | 1983 | 5 | 5 | % | 1784 | 1784 | 17 | 17 |
      Brazil | Brazil | Brazil | 989 | 989 | 919 | 919 | 8 | 8 | % | 928 | 928 | 7 | 7 | % | 937 | 937 | 945 | 945 | -1 | -1 | % | 980 | 980 | -4 | -4 | % | 1055 | 10
      Southern Region | Southern Region | Southern Region | 551 | 551 | 481 | 481 | 15 | 15 | % | 606 | 606 | -9 | -9 | % | 519 | 519 | 460 | 460 | 13 | 13 | % | 566 
      Other Markets | Other Markets | Other Markets | 378 | 378 | 355 | 355 | 7 | 7 | % | 418 | 418 | -10 | -10 | % | 320 | 320 | 320 | 320 | 0 | 0 | % | 390 | 390 | 
      Total Steel Products | Total Steel Products | Total Steel Products | 4137 | 4137 | 3739 | 3739 | 11 | 11 | % | 3733 | 3733 | 11 | 11 | % | 3858 | 3858 | 3709 | 
      Other Products | Other Products | Other Products | 56 | 56 | 75 | 75 | -26 | -26 | % | 79 | 79 | -30 | -30 | %
      Total Steel Segment | Total Steel Segment | Total Steel Segment | 4192 | 4192 | 3814 | 3814 | 10 | 10 | % | 3812 | 3812 | 10 | 10 | %
      
      
comunicados trimestrales en 'recent': 29; primero ('2020-04-28', 'prternium1q2020.htm'); files extra 0
_(0.5 s)_

## [Materias primas] Comex Stat Brasil (con pausa)
Brasil importa: carbón coque, coque, chatarra, DRI: HTTP 200 8764 bytes
   filas 48, desde 2025-01
   27011200 Hulha betuminosa, não aglomerada: 2026-09 169 USD/t (CIF), 1274.9 mil t
   72031000 Produtos ferrosos obtidos por redução direta dos m: 2026-07 27190 USD/t (CIF), 0.0 mil t
   72044900 Outros desperdícios e resíduos de ferro ou aço: 2026-09 254 USD/t (CIF), 0.4 mil t
Brasil exporta a la Argentina: HTTP 200 20631 bytes
   filas 64, desde 2025-01
   72071200 Outros produtos semimanufaturados de ferro ou aço : 2025-12 482 USD/t (FOB), 30.1 mil t
   72083910 Produtos laminados planos, de ferro ou aço não lig: 2025-04 1049 USD/t (FOB), 0.0 mil t
   72085200 Produtos laminados planos, de ferro ou aço não lig: 2026-09 893 USD/t (FOB), 0.3 mil t
   72091800 Produtos laminados planos, de ferro ou aço não lig: 2026-08 699 USD/t (FOB), 0.0 mil t
   72104910 Produtos laminados planos, de ferro ou aço não lig: 2026-09 1440 USD/t (FOB), 9.5 mil t
   72142000 Barras de ferro ou aço não ligado, a quente, denta: 2026-08 4046 USD/t (FOB), 0.0 mil t
Historia larga: mineral de hierro desde 1997: HTTP 200 83760 bytes
   filas 357, desde 1997-01
   26011100 Minérios de ferro e seus concentrados, exceto as p: 2026-09 56 USD/t (FOB), 31660.5 mil t
_(47.8 s)_

## [Materias primas] Eurostat Comext (formato de período)
variante {'sinceTimePeriod': '2025-01'}: HTTP 200 '{"version":"2.0","class":"dataset","label":"EU trade since 1988 by HS2-4-6 and CN8","source":"ESTAT","updated":"2026-10-16T11:00:00+0200","value":{"0":309644545'
   Chatarra UE->Turquía: 2026-08 312 EUR/t (736 mil t)
   Barra Turquía->UE: 2026-08 785 EUR/t (4 mil t)
   HRC UE desde China: 2026-08 846 EUR/t (23 mil t)
   HRC UE extra-UE: {'VALUE_IN_EUROS': {}, 'QUANTITY_IN_100KG': {}} list index out of range
_(10.6 s)_

## [Materias primas] Banco de Japón (ítems de materias primas)
ERROR
```
Traceback (most recent call last):
  File "/home/runner/work/monitor-insumos-metal-rgicos/monitor-insumos-metal-rgicos/tests/test_fuentes.py", line 50, in caso
    texto = f()
            ^^^
  File "/home/runner/work/monitor-insumos-metal-rgicos/monitor-insumos-metal-rgicos/tests/test_fuentes_2.py", line 138, in boj
    meta = json.loads((T.SAMPLES / "boj_PR01_meta.json").read_text()) if (T.SAMPLES / "boj_PR01_meta.json").exists() else None
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/json/decoder.py", line 338, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/hostedtoolcache/Python/3.12.15/x64/lib/python3.12/json/decoder.py", line 354, in raw_decode
    obj, end = self.scan_once(s, idx)
               ^^^^^^^^^^^^^^^^^^^^^^
json.decoder.JSONDecodeError: Unterminated string starting at: line 1 column 399992 (char 399991)

```
_(0.0 s)_

## [No ferrosos] Yahoo (búsqueda de futuros y chequeo)
ERROR
```
Traceback (most recent call last):
  File "/home/runner/work/monitor-insumos-metal-rgicos/monitor-insumos-metal-rgicos/tests/test_fuentes.py", line 50, in caso
    texto = f()
            ^^^
  File "/home/runner/work/monitor-insumos-metal-rgicos/monitor-insumos-metal-rgicos/tests/test_fuentes_2.py", line 174, in yahoo_busqueda
    cl = [c for c in x["indicators"]["quote"][0]["close"] if c is not None]
                     ~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
KeyError: 'close'

```
_(1.5 s)_

## [No ferrosos] Changjiang (páginas de precio)
https://copper.ccmn.cn/copperprice/cjxh/ -> HTTP 200 41408 bytes; tablas 1; muestra [['【长江铜价格】', '10月16日长江铜价格行情参考', '2026-10-16'], ['【长江铜价格】', '10月15日长江铜价格行情参考', '2026-10-15'], ['【长江铜价格】', '10月14日长江铜价格行情参考', '2026-10-14']]
https://alu.ccmn.cn/aluprice/cjxh/ -> HTTP 200 38640 bytes; tablas 1; muestra [['【长江铝锭价格】', '10月16日长江铝锭价格行情参考', '2026-10-16'], ['【长江铝锭价格】', '10月15日长江铝锭价格行情参考', '2026-10-15'], ['【长江铝锭价格】', '10月14日长江铝锭价格行情参考', '2026-10-14']]
https://zinc.ccmn.cn/zincprice/cjxh/ -> ERROR `Import beautifulsoup4` failed.  Use pip or conda to install the beautifulsoup4 package.
https://lead.ccmn.cn/leadprice/cjxh/ -> ERROR `Import beautifulsoup4` failed.  Use pip or conda to install the beautifulsoup4 package.
https://tin.ccmn.cn/tinprice/cjxh/ -> ERROR `Import beautifulsoup4` failed.  Use pip or conda to install the beautifulsoup4 package.
https://nickel.ccmn.cn/nickelprice/cjxh/ -> ERROR `Import beautifulsoup4` failed.  Use pip or conda to install the beautifulsoup4 package.
_(7.9 s)_

## [No ferrosos] FMI (estructura de la API)
https://api.imf.org/external/sdmx/3.0/structure/dataflow/IMF.RES/PCPS/+?references=datastructure
   -> HTTP 200 8725 bytes; dimensiones []; '{"data":{"dataStructures":[{"annotations":[{"id":"origin","value":"INTEGRATION"},{"id":"isFinal"},{"id":"lastUpdatedAt","value":"2025-06-16T17:59:44.614958Z"}],"id":"DSD_PCPS","name":"Primary Commodity Price System\xa0(PCPS)","names":{"en":"Primary Comm'
https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.RES/PCPS/+/*.PCOPP.*.M?c[TIME_PERIOD]=ge:2026-01
   -> HTTP 200 3807 bytes; dimensiones []; '{"meta":{},"data":{"dataSets":[{"structure":0,"action":"Replace","series":{"0:0:0:0":{"attributes":[0,null,null],"observations":{"0":["266.7806174195774",null,0],"1":["266.0562427035652",null,0],"2":["257.374148213018",null,0],"3":["264.8101755132878'
https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.RES/PCPS/+/G001.PCOPP.USD.M
   -> HTTP 200 24483 bytes; dimensiones []; '{"meta":{},"data":{"dataSets":[{"structure":0,"action":"Replace","series":{"0:0:0:0":{"attributes":[0,null,null],"observations":{"0":["2150.57962901611",null,0],"1":["2208.89225860596",null,0],"2":["2231.78550956421",null,0],"3":["2214.16681599274",n'
_(1.1 s)_

## [Acero] NBS (listado e historia)
links: 9
   2026年9月下旬流通领域重要生产资料市场价格变动情况
										 -> ./202610/t20261008_1965465.html
   2026年9月下旬流通领域重要生产资料市场价格变动情况
										 -> ./202610/t20261008_1965465.html
   2026年9月下旬流通领域重要生产资料市场...
										 -> ./202610/t20261008_1965465.html
   2026年9月中旬流通领域重要生产资料市场价格变动情况
										 -> ./202609/t20260923_1965403.html
   2026年9月中旬流通领域重要生产资料市场价格变动情况
										 -> ./202609/t20260923_1965403.html
   2026年9月中旬流通领域重要生产资料市场...
										 -> ./202609/t20260923_1965403.html
   index_1.html: HTTP 200, informes ['2026年8月下旬', '2026年8月下旬', '2026年8月下旬']
   index_10.html: HTTP 200, informes ['2025年12月中旬', '2025年12月中旬', '2025年12月中旬']
   index_30.html: HTTP 200, informes ['2024年7月上旬', '2024年7月上旬', '2024年7月上旬']
_(13.4 s)_

## [Acero] CISA (índice de precios)
HTTP 200; contexto: '                 \r\n             \r\n             \r\n                 \r\n                     \r\n                          钢材价格指数  \r\n                     \r\n                     \r\n                         综合价格指数  | \r\n                        <a class="right" href="list'
links con 价格: [('list.html?columnId=a44207e193a5caa5e64102604b6933896a0025eb85c57c583b39626f33d4dafd', '市场价格分析'), ('list.html?columnId=17b6a9a214c94ccc28e56d4d1a2dbb5acef3e73da431ddc0a849a4dcfc487d04', '钢材价格指数'), ('list.html?columnId=63913b906a7a663f7f71961952b1ddfa845714b5982655b773a62b85dd3b064e', '综合价格指数'), ('list.html?columnId=fc816c75aed82b9bc25563edc9cf0a0488a2012da38cbef5258da614d6e51ba9', '地区价格'), ('javascript: void(0);', '2019年4月12日中国铁矿石价格指数'), ('javascript: void(0);', '2019年4月11日中国铁矿石价格指数'), ('javascript: void(0);', '2019年4月10日中国铁矿石价格指数'), ('javascript: void(0);', '2019年4月9日中国铁矿石价格指数'), ('javascript: void(0);', '2019年4月8日中国铁矿石价格指数'), ('javascript: void(0);', '3月中国铁矿石价格指数（CIOPI）波动调整后期难以维...')]
_(1.4 s)_

## [Acero] Destatis (API nueva)
POST helloworld/logincheck -> HTTP 200 165 bytes application/json;charset=UTF-8
   '{"Status":"Sie wurden erfolgreich an- und abgemeldet! Bei mehr als 3 parallelen Requests wurden länger als 15 Minuten laufende Requests beendet.","Username":"GAST"}'
POST data/tablefile -> HTTP 401 209 bytes application/json
   '{"Code":15,"Content":"Sie sind nicht berechtigt diesen Service aufzurufen oder der Header Ihres Requests enthält nicht alle notwendigen Angaben, sodass Ihre Zugangsdaten nicht erkannt werden.","Type":"ERROR"}'
GET data/tablefile -> HTTP 200 2506 bytes text/html
   '<!doctype html>\n<html lang="de">\n  <head>\n    <meta charset="utf-8" />\n    <meta name="viewport" content="width=device-width, user-scalable=yes" />\n    <meta name="theme-color" content="#000000" />\n    <meta\n      http-equiv="Content-Security-Policy"\n      content="\n      default-src \'none\';\n      b'
POST catalogue/tables -> HTTP 401 209 bytes application/json
   '{"Code":15,"Content":"Sie sind nicht berechtigt diesen Service aufzurufen oder der Header Ihres Requests enthält nicht alle notwendigen Angaben, sodass Ihre Zugangsdaten nicht erkannt werden.","Type":"ERROR"}'
_(8.5 s)_

## [Acero] India WPI (ítems)
HTTP 200 331956 bytes
   hoja 'Sheet3' (1138, 46); encabezado ['Level', 'Commodity Name', 'Commodity Code', 'Commodity Weight', 'Apr-23', 'May-23'] ... ['Jul-26', 'Aug-26', 'Sep-26']
   45 filas de interés
      Item | Zinc concentrate | 1103010003
      Item | Copper concentrate | 1103010006
      Sub Group | a. Coking Coal | 1201010000
      Item | Coking Coal  | 1201010100
      Sub Group | b. Non-Coking Coal | 1201020000
      Item | a.) Non-Coking Coal G1 to G6 [GCV exceeding 5500 Kcal/kg.] | 1201020100
      Item | b.) Non-Coking Coal G7 to G14 [GCV 3100 Kcal/kg. to 5500 Kcal/kg.] | 1201020200
      Item | c.) Non-Coking Coal G15 to G17 [GCV < 3100 Kcal/kg.] | 1201020300
      Item | Petroleum Coke | 1202010010
      Item | Printed Aluminium Foil (Not Backed) | 1309010005
      Item | Recycled plastics incl. Scrap/Waste | 1312030031
      Item | Sponge Iron/Iron pellets/Hot Briquette Iron | 1314010001
      Item | Pig iron | 1314010003
      Item | Ferro-manganese/Ferrosilico manganese | 1314010004
      Item | Bars and Rods of Mild steel | 1314010014
      Item | Forged Spring Steel Bars and Rods | 1314010015
      Item | Mild Steel Bright Rectangular Bars | 1314010016
      Item | Bars (Rounds/Square/Hexagonal) | 1314010017
      Item | Bars and Rods of Alloy and stainless steel | 1314010023
      Item | Ferrochrome | 1314010025
      Item | Ferrosilicon | 1314010026
      Item | Scrap Iron/Steel | 1314010027
      Item | Other ferro alloys | 1314010033
      Sub Group | b.Manufacture of basic precious and other non-ferrous metals | 1314020000
      Item | Copper cathodes and sections of cathodes | 1314020002
_(2.9 s)_
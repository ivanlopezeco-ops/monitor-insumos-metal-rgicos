
# Resumen

| Bloque | Fuente | Estado | Detalle |
|---|---|---|---|
| No ferrosos | Westmetall (LME oficial y precios alemanes) | OK | LME_Cu_cash: HTTP 200, tablas 1, filas 209, columnas ['date', 'LME Copper Cash-Settlement', 'LME Copper 3-mont |
| No ferrosos | Yahoo Finance (futuros CME/COMEX y BDRY) | OK | HG=F: Copper Dec 26 [CMX, USD] obs 6562, desde 2000-08-30, último (datetime.date(2026, 10, 16), 6.561999797821 |
| No ferrosos | Banco Mundial Pink Sheet (mensual) | OK | Link: https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical- |
| No ferrosos | FMI PCPS (API) | OK | https://api.imf.org/external/sdmx/2.1/data/IMF.RES,PCPS/M.G001.PCOPP.USD?startPeriod=2025-01 |
| No ferrosos | FRED (respaldo) | OK | PCOPPUSDM: ERROR ReadTimeout |
| No ferrosos | SHFE futuros (Shanghái) | OK | https://www.shfe.com.cn/data/tradedata/future/dailydata/kx20261015.dat -> HTTP 200 123484 bytes application/js |
| No ferrosos | Changjiang spot (ccmn.cn) | OK | https://www.ccmn.cn/ -> HTTP 200 177960 bytes; coincidencias [('1#铜', '1000')] |
| No ferrosos | MCX India | OK | HTTP 403 398 bytes; menciona 'bhavcopy' True |
| Materias primas | DCE (mineral, carbón coque, coque) | OK | GET http://www.dce.com.cn/publicweb/quotesdata/dayQuotesCh.html -> HTTP 412 2667 bytes; 铁矿石 False;焦煤 False; te |
| Materias primas | ZCE (ferroaleaciones) | OK | http://www.czce.com.cn/cn/DFSStaticFiles/Future/2026/20261015/FutureDataDaily.txt -> HTTP 200 38378 bytes |
| Materias primas | Comex Stat Brasil (valores unitarios por NCM) | OK | export: HTTP 200 39135 bytes |
| Materias primas | Eurostat Comext (chatarra y barra Turquía, HRC UE) | OK | Chatarra 7204 UE->Turquía: HTTP 400 97 bytes '{ "error": [{"status": 400,"id": 400,"label": "Invalid value for |
| Materias primas | Banco de Japón (precios corporativos e importación) | OK | PR01 metadata -> HTTP 200 14233406 bytes |
| Acero | BLS PPI (EE.UU.) | PARCIAL | HTTP 200 status REQUEST_SUCCEEDED ['Series does not exist for Series WPU10170811'] |
| Acero | NBS China (precios cada 10 días) | OK | Página conocida -> HTTP 200 194096 bytes |
| Acero | CISA (índice de precios del acero China) | OK | https://www.chinaisa.org.cn/ -> HTTP 200 286 bytes; menciona 价格指数: False |
| Acero | Aduana China | OK | http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/302277/index.html -> HTTP 412 2126 bytes; 钢材 Fa |
| Acero | Eurostat PPI por país | OK | EU27_2020 C241: ['2026-08', '2026-09'] -> [105.1] |
| Acero | Destatis GENESIS (precios por producto Alemania) | OK | GET helloworld/logincheck -> HTTP 200 2506 bytes text/html |
| Acero | IBGE IPP Brasil | OK | https://apisidra.ibge.gov.br/values/t/6903/n1/all/v/all/p/last%202/c842/all -> HTTP 200 78355 bytes |
| Acero | India WPI por ítem | OK | HTTP 200 20270 bytes; links ['indx_download_7071/index_7071.xls', 'indx_download_6162/index_6162.xls', 'indx_d |
| Local | Ternium (SEC, precio realizado) | OK | Ternium S.A.: 561 presentaciones recientes |
| Local | INDEC SIPM (IPIM 4 dígitos) | ERROR | TypeError: sequence item 1: expected str instance, float found |
| Local | INDEC ICC (materiales) | ERROR | TypeError: sequence item 1: expected str instance, float found |
| Local | DGE Rosario (materiales) | OK | CKAN -> HTTP 404 14067 bytes |
| Local | BCRA A3500 | OK | A3500: [{"idVariable": 5, "detalle": [{"fecha": "2026-10-16", "valor": 1514.5655}, {"fecha": "2026-10-15", "va |
# Test de fuentes — 2026-10-16 22:55 UTC


## [No ferrosos] Westmetall (LME oficial y precios alemanes)
LME_Cu_cash: HTTP 200, tablas 1, filas 209, columnas ['date', 'LME Copper Cash-Settlement', 'LME Copper 3-month', 'LME Copper stock']
   primeras filas: 15. October 2026 ; 14539.00 ; 14362.00 ; 226600 || 14. October 2026 ; 14751.00 ; 14635.00 ; 228000
LME_Al_cash: HTTP 200, tablas 1, filas 209, columnas ['date', 'LME Aluminium Cash-Settlement', 'LME Aluminium 3-month', 'LME Aluminium stock']
   primeras filas: 15. October 2026 ; 2999.00 ; 2994.50 ; 238125 || 14. October 2026 ; 3010.00 ; 3013.50 ; 238375
LME_Ni_cash: HTTP 200, tablas 1, filas 209, columnas ['date', 'LME Nickel Cash-Settlement', 'LME Nickel 3-month', 'LME Nickel stock']
   primeras filas: 15. October 2026 ; 14885.00 ; 15125.00 ; 282066 || 14. October 2026 ; 15475.00 ; 15680.00 ; 282654
LME_Zn_cash: HTTP 200, tablas 1, filas 209, columnas ['date', 'LME Zinc Cash-Settlement', 'LME Zinc 3-month', 'LME Zinc stock']
   primeras filas: 15. October 2026 ; 3724.00 ; 3681.50 ; 151050 || 14. October 2026 ; 3803.00 ; 3749.00 ; 144125
LME_Sn_cash: HTTP 200, tablas 1, filas 209, columnas ['date', 'LME Tin Cash-Settlement', 'LME Tin 3-month', 'LME Tin stock']
   primeras filas: 15. October 2026 ; 50100.00 ; 50000.00 ; 4205 || 14. October 2026 ; 51100.00 ; 50950.00 ; 4215
LME_Pb_cash: HTTP 200, tablas 1, filas 209, columnas ['date', 'LME Lead Cash-Settlement', 'LME Lead 3-month', 'LME Lead stock']
   primeras filas: 15. October 2026 ; 1853.00 ; 1889.00 ; 339800 || 14. October 2026 ; 1866.00 ; 1906.00 ; 340075
WM_Cu_low: HTTP 200, tablas 1, filas 210, columnas ['date', 'WM_Cu_low']
   primeras filas: 16. October 2026 ; 1326.56 || 15. October 2026 ; 1327.29
MB_MS_58_1: HTTP 200, tablas 1, filas 204, columnas ['date', 'Brass MS 58, 1st processing level']
   primeras filas: 16. October 2026 ; 1105.00 || 15. October 2026 ; 1106.00
Historia (year=2010): 1 tablas, filas [264], muestra [['31. December 2010', '9739.50', '9665.00', '377550']]
_(9.3 s)_

## [No ferrosos] Yahoo Finance (futuros CME/COMEX y BDRY)
HG=F: Copper Dec 26 [CMX, USD] obs 6562, desde 2000-08-30, último (datetime.date(2026, 10, 16), 6.561999797821045)
ALI=F: Aluminum Futures,Jan-2027 [CMX, USD] obs 3094, desde 2014-05-06, último (datetime.date(2026, 10, 16), 3092.25)
HRC=F: U.S. Midwest Domestic Hot-Rolle [CMX, USD] obs 4487, desde 2008-10-20, último (datetime.date(2026, 10, 16), 1357.0)
TIO=F: Iron Ore 62% Fe, CFR China (TSI [CMX, USD] obs 4012, desde 2010-10-14, último (datetime.date(2026, 10, 15), 90.56999969482422)
BUS=F: U.S. Midwest Busheling Ferrous  [CMX, USD] obs 3239, desde 2012-09-10, último (datetime.date(2025, 12, 10), 421.0)
TSR=F: HTTP 404 sin resultado ({'chart': {'result': None, 'error': {'code': 'Not Found', 'description': 'No data found, symbol may be delisted'}}})
EHR=F: North European Hot-Rolled Coil  [CMX, EUR] obs 1, desde 2026-10-15, último (datetime.date(2026, 10, 15), 763.0)
NSF=F: HTTP 404 sin resultado ({'chart': {'result': None, 'error': {'code': 'Not Found', 'description': 'No data found, symbol may be delisted'}}})
HMS=F: HTTP 404 sin resultado ({'chart': {'result': None, 'error': {'code': 'Not Found', 'description': 'No data found, symbol may be delisted'}}})
AUP=F: Aluminum MW U.S. Transaction Pr [CMX, USD] obs 3468, desde 2012-12-14, último (datetime.date(2026, 10, 16), 1.0175000429153442)
EDP=F: Aluminium European Premium Duty [CMX, USD] obs 2626, desde 2016-03-14, último (datetime.date(2026, 10, 15), 561.6300048828125)
ZNC=F: Zinc Futures,Sep-2026 [CMX, USD] obs 2829, desde 2015-06-29, último (datetime.date(2026, 10, 15), 3943.5)
NICKEL=F: HTTP 404 sin resultado ({'chart': {'result': None, 'error': {'code': 'Not Found', 'description': 'No data found, symbol may be delisted'}}})
BDRY: Breakwave Dry Bulk Shipping ETF [PCX, USD] obs 2155, desde 2018-03-22, último (datetime.date(2026, 10, 16), 12.550000190734863)
_(1.4 s)_

## [No ferrosos] Banco Mundial Pink Sheet (mensual)
Link: https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx
Filas: 801, primera 1960M01, última 2026M09
  Coal, Australian [($/mt)]: últimos [131.9, 135.2, 147.1]
  Coal, South African ** [($/mt)]: últimos [96.3, 96.8, 98.2]
  Aluminum [($/mt)]: últimos [3161, 3251, 3283]
  Iron ore, cfr spot [($/dmtu)]: últimos [98.2, 96.3, 97.7]
  Copper [($/mt)]: últimos [13543, 14326, 14474]
  Lead [($/mt)]: últimos [1842, 1855, 1873]
  Tin [($/mt)]: últimos [52971, 55385, 53712]
  Nickel [($/mt)]: últimos [16651, 16751, 16324]
  Zinc [($/mt)]: últimos [3599, 3875, 4021]
  Platinum [($/troy oz)]: últimos [1622, 1780, 1784]
_(1.1 s)_

## [No ferrosos] FMI PCPS (API)
https://api.imf.org/external/sdmx/2.1/data/IMF.RES,PCPS/M.G001.PCOPP.USD?startPeriod=2025-01
   -> HTTP 400 353 bytes: '{"status":400,"code":40000,"message":"com.fasterxml.jackson.core.JsonGenerationException: Current context not Object but Array","devMessage":null,"timestamp":"2026-10-16T22:55:52.894803Z","correlation'
https://api.imf.org/external/sdmx/2.1/data/PCPS/M.W00.PCOPP.USD?startPeriod=2025-01
   -> HTTP 400 344 bytes: '{"status":400,"code":40000,"message":"com.fasterxml.jackson.core.JsonGenerationException: Current context not Object but Array","devMessage":null,"timestamp":"2026-10-16T22:55:53.930919Z","correlation'
https://api.imf.org/external/sdmx/3.0/data/dataflow/IMF.RES/PCPS/+/M.*.PCOPP.USD?c[TIME_PERIOD]=ge:2025-01
   -> HTTP 200 2051 bytes: '{"meta":{},"data":{"dataSets":[{"structure":0,"action":"Replace"}],"structures":[{"dataSets":[0],"links":[{"urn":"urn:sdmx:org.sdmx.infomodel.datastructure.Dataflow=IMF.RES:PCPS(9.0.0)","title":"Dataf'
http://dataservices.imf.org/REST/SDMX_JSON.svc/CompactData/PCPS/M.W00.PCOPP.USD?startPeriod=2025
   -> ERROR HTTPConnectionPool(host='dataservices.imf.org', port=80): Max retries exceeded with url: /REST/SDMX_JSON.svc/CompactData/PCPS/M.W00.PCOPP.USD
_(2.4 s)_

## [No ferrosos] FRED (respaldo)
PCOPPUSDM: ERROR ReadTimeout
PALUMUSDM: ERROR ReadTimeout
PIORECRUSDM: ERROR ReadTimeout
WPU101704: ERROR ReadTimeout
_(160.6 s)_

## [No ferrosos] SHFE futuros (Shanghái)
https://www.shfe.com.cn/data/tradedata/future/dailydata/kx20261015.dat -> HTTP 200 123484 bytes application/json
   productos: ['ad_f', 'ag_f', 'al_f', 'ao_f', 'au_f', 'bc_f', 'br_f', 'bu_f', 'cu_f', 'ec_f', 'fu_f', 'hc_f', 'lu_f', 'ni_f', 'nr_f', 'op_f', 'pb_f', 'rb_f', 'ru_f', 'sc_f', 'sc_tas', 'sn_f', 'sp_f', 'ss_f', 'wr_f', 'zn_f', '总计']
   cu_f 2610 cierre 109600 liq 110400
_(1.4 s)_

## [No ferrosos] Changjiang spot (ccmn.cn)
https://www.ccmn.cn/ -> HTTP 200 177960 bytes; coincidencias [('1#铜', '1000')]
https://www.ccmn.cn/historyprice/ -> HTTP 200 107173 bytes; coincidencias []
_(2.7 s)_

## [No ferrosos] MCX India
HTTP 403 398 bytes; menciona 'bhavcopy' True
_(0.2 s)_

## [Materias primas] DCE (mineral, carbón coque, coque)
GET http://www.dce.com.cn/publicweb/quotesdata/dayQuotesCh.html -> HTTP 412 2667 bytes; 铁矿石 False;焦煤 False; texto: ' document.createElement("section") $_ts=window[\'$_ts\'];if(!$_ts)$_ts={};$_ts.nsd=13342;$_ts.cd="qErSrcqlEO9miqgcHqqyqu9qicQyruGirkaGingVHqq4hfVyqk9rcGqVxr0yqkGirsaqiA3yruGvi1EgkGWZqk9qiAlgxu9DqrV9ms9k'
POST http://www.dce.com.cn/publicweb/quotesdata/dayQuotesCh.html -> HTTP 412 3176 bytes; 铁矿石 False;焦煤 False; texto: ' document.createElement("section") $_ts=window[\'$_ts\'];if(!$_ts)$_ts={};$_ts.nsd=62427;$_ts.cd="qWTSr1qlJk9qiqgmHqqyqO9kicQZqk9riA32xuaqiAAyrsGvHqqyqu9qx1QyrOAEHqqyrk9micQ9rp0Vrc7yruAEHqqyrs9cicQfqk9q'
GET http://www.dce.com.cn/dalianshangpin/xqsj/tjsj26/rtj/rxq/index.html -> HTTP 412 2745 bytes; 铁矿石 False;焦煤 False; texto: ' document.createElement("section") $_ts=window[\'$_ts\'];if(!$_ts)$_ts={};$_ts.nsd=63452;$_ts.cd="qtNSr1qlEOaqiAEyquGvHqq4hfAZqk9qiAlvxu9liqgmiAWgkGAyqAqVDnWZqk9oiAAgxuaqiAEyqnQvHqqyqs9DicQZqk9liAVvxu9c'
_(2.3 s)_

## [Materias primas] ZCE (ferroaleaciones)
http://www.czce.com.cn/cn/DFSStaticFiles/Future/2026/20261015/FutureDataDaily.txt -> HTTP 200 38378 bytes
   SF610 |5,992.00  |6,000.00  |6,000.00  |6,000.00  |6,000.00  |6,000.00  |8.00     |8.00     |500       |2,477     |0         |1,500.00    |5,988.00      
   SF611 |5,996.00  |5,950.00  |6,050.00  |5,910.00  |6,026.00  |5,992.00  |30.00    |-4.00    |198,913   |115,021   |-32,970   |595,905.53  |
   SF612 |5,944.00  |5,908.00  |6,004.00  |5,864.00  |5,986.00  |5,962.00  |42.00    |18.00    |42,069    |64,085    |1,789     |125,417.21  |
   SF701 |5,932.00  |5,894.00  |5,990.00  |5,850.00  |5,966.00  |5,936.00  |34.00    |4.00     |149,948   |185,044   |19,713    |445,020.04  |
_(2.9 s)_

## [Materias primas] Comex Stat Brasil (valores unitarios por NCM)
export: HTTP 200 39135 bytes
   26011100 Mineral de hierro no aglomerado: último 2026-09 56 USD/t (31660.5 mil t)
   72011000 Arrabio no aleado: último 2026-09 456 USD/t (339.8 mil t)
   72071200 Semis (planchones) de acero: último 2026-09 623 USD/t (409.2 mil t)
   72083990 Laminado en caliente, rollos <3mm (otros): último 2026-09 680 USD/t (0.8 mil t)
   72091800 Laminado en frío <0,5mm: último 2026-08 982 USD/t (0.0 mil t)
   72104910 Galvanizado: último 2026-09 1439 USD/t (9.5 mil t)
   72142000 Barras para hormigón: último 2026-09 630 USD/t (23.1 mil t)
import: HTTP 429 131 bytes
   {"error":{"code":429,"message":"Voc\u00ea excedeu o limite de solicita\u00e7\u00f5es. Por favor, tente novamente em 10 segundos."}}
export a Argentina: HTTP 429 131 bytes
   {"error":{"code":429,"message":"Voc\u00ea excedeu o limite de solicita\u00e7\u00f5es. Por favor, tente novamente em 10 segundos."}}
_(3.0 s)_

## [Materias primas] Eurostat Comext (chatarra y barra Turquía, HRC UE)
Chatarra 7204 UE->Turquía: HTTP 400 97 bytes '{ "error": [{"status": 400,"id": 400,"label": "Invalid value for \'sinceTimePeriod\' parameter."}]}'
Barra 7214 Turquía->UE: HTTP 400 97 bytes '{ "error": [{"status": 400,"id": 400,"label": "Invalid value for \'sinceTimePeriod\' parameter."}]}'
HRC 7208 importado UE (total extra): HTTP 400 97 bytes '{ "error": [{"status": 400,"id": 400,"label": "Invalid value for \'sinceTimePeriod\' parameter."}]}'
_(1.6 s)_

## [Materias primas] Banco de Japón (precios corporativos e importación)
PR01 metadata -> HTTP 200 14233406 bytes
   series: 32086, coincidencias 803
   PRCG20_2200930001: Subgroup/__Pig iron and crude steel
   PRCG20_2200940002: Commodity class/___Hot rolled steel
   PRCG20_2200950003: Commodity/____Light steel bars
   PRCG20_2200950006: Commodity/____Hot rolled steel strips
   PRCG20_2200950013: Commodity/____Cold rolled steel strips
   PRCG20_2200950014: Commodity/____Cold rolled electrical steel hoops
   PRCG20_2200950016: Commodity/____Cold rolled stainless steel sheets
   PRCG20_2200950019: Commodity/____Zinc-coated steel sheets
   PRCG20_2201040001: Commodity class/___Copper
   PRCG20_2201050001: Commodity/____Copper
   PRCG20_2201040002: Commodity class/___Lead and zinc
   PRCG20_2201050006: Commodity/____Copper wire rods
   PRCG20_2201050007: Commodity/____Bare copper wires
   PRCG20_2201050008: Commodity/____Plastic insulated copper wires
   PRCG20_2201050009: Commodity/____Copper coils
   PRCG20_2201040006: Commodity class/___Rolled and drawn copper and copper alloys
   PRCG20_2201050011: Commodity/____Rolled and drawn copper products
   PRCG20_2201050014: Commodity/____Copper and aluminum castings
   PRCG20_2202350003: Commodity/____Copper and aluminum scrap
   PRCG20_2400350001: Commodity/____Ferro-nickel
   PRCG20_2400340002: Commodity class/___Hot rolled steel
   PRCG20_2400350006: Commodity/____Hot rolled steel strips
   PRCG20_2400350012: Commodity/____Cold rolled electrical steel hoops and steel strips
   PRCG20_2400350013: Commodity/____Cold rolled stainless steel sheets
   PRCG20_2400350014: Commodity/____Zinc-coated steel sheets
   PRCG20_2400340006: Commodity class/___Copper
   PRCG20_2400350016: Commodity/____Copper
   PRCG20_2400340008: Commodity class/___Rolled and drawn copper and copper alloys
   PRCG20_2400350018: Commodity/____Rolled and drawn copper products
   PRCG20_2400350026: Commodity/____Copper scrap
   PRCG20_2300350001: Commodity/____Ferro-nickel
   PRCG20_2300340002: Commodity class/___Hot rolled steel
   PRCG20_2300350006: Commodity/____Hot rolled steel strips
   PRCG20_2300350012: Commodity/____Cold rolled electrical steel hoops and steel strips
   PRCG20_2300350013: Commodity/____Cold rolled stainless steel sheets
   PRCG20_2300350014: Commodity/____Zinc-coated steel sheets
   PRCG20_2300340006: Commodity class/___Copper
   PRCG20_2300350016: Commodity/____Copper
   PRCG20_2300340008: Commodity class/___Rolled and drawn copper and copper alloys
   PRCG20_2300350018: Commodity/____Rolled and drawn copper products
   datos ['PRCG20_2200930001', 'PRCG20_2200940002', 'PRCG20_2200950003']: HTTP 200 '{\n"STATUS":200,\n"MESSAGEID":"M181000I",\n"MESSAGE":"Successfully completed",\n"DATE":"2026-10-17T07:58:50.679+09:00",\n"PARAMETER":{\n"FORMAT":"JSON",\n"LANG":"EN",\n"DB":"PR01",\n"STARTDATE":"202501",\n"ENDDATE":"",\n"STARTPOSITION":""\n},\n"NEXTPOSITION":null,\n"RESULTSET":[\n{\n"SERIES_CODE":"PRCG20_2200930001",\n"NAME_OF_TIME_SERIES":"Subgroup/__Pig iron and crude steel",\n"UNIT":"CY2020 average=100",\n"FREQUE'
PR02 metadata -> HTTP 200 1332843 bytes
   series: 3160, coincidencias 0
_(1.7 s)_

## [Acero] BLS PPI (EE.UU.)
HTTP 200 status REQUEST_SUCCEEDED ['Series does not exist for Series WPU10170811']
   WPU1017 Laminados de acero: último 2026-M09 = 388.580
   WPU101704 Barras, chapa gruesa y perfiles en caliente: último 2026-M09 = 319.693
   WPU101707 Laminado en frío: último 2026-M09 = 492.454
   WPU101 Hierro y acero: último 2026-M09 = 383.330
   WPU1012 Chatarra hierro y acero: último 2026-M09 = 580.952
   WPU101211 Chatarra de acero al carbono: último 2026-M09 = 535.388
   WPU101708 Galvanizado (a confirmar): último 2026-M09 = 277.314
   WPU10170811 Galvanizado (otra variante): SIN DATOS
   WPU1011 Mineral de hierro (a confirmar): último 2026-M09 = 206.602
   WPU101702 Semis (a confirmar): último 2026-M09 = 399.420
_(0.3 s)_

## [Acero] NBS China (precios cada 10 días)
Página conocida -> HTTP 200 194096 bytes
   tablas 2; filas [60, 59]
   螺纹钢（Φ20mm，HRB400E） | 吨 | 3175.9 | 10.8 | 0.3
   热轧普通板卷（4.75—11.5mm，Q235） | 吨 | 3297.1 | -11.8 | -0.4
   电解铜（1#） | 吨 | 111742.5 | 2972.5 | 2.7
   焦煤（主焦煤） | 吨 | 2470.0 | -79.3 | -3.1
   焦炭（准一级冶金焦） | 吨 | 2096.4 | 0.0 | 0.0
Listado https://www.stats.gov.cn/sj/zxfb/ -> HTTP 200, menciones del informe: 18
Listado https://www.stats.gov.cn/xxgk/sjfb/zxfb2020/ -> HTTP 200, menciones del informe: 2
_(9.3 s)_

## [Acero] CISA (índice de precios del acero China)
https://www.chinaisa.org.cn/ -> HTTP 200 286 bytes; menciona 价格指数: False
http://www.chinaisa.org.cn/gxportal/xfgl/portal/index.html -> HTTP 200 40510 bytes; menciona 价格指数: True
_(2.5 s)_

## [Acero] Aduana China
http://www.customs.gov.cn/customs/302249/zfxxgk/2799825/302274/302277/index.html -> HTTP 412 2126 bytes; 钢材 False; steel False
http://english.customs.gov.cn/statics/report/preliminary.html -> HTTP 200 27769 bytes; 钢材 False; steel False
_(1.9 s)_

## [Acero] Eurostat PPI por país
EU27_2020 C241: ['2026-08', '2026-09'] -> [105.1]
EU27_2020 C2442: ['2026-08', '2026-09'] -> [139.8]
EU27_2020 C2444: ['2026-08', '2026-09'] -> [151.6]
DE C241: ['2026-08', '2026-09'] -> [107.2]
DE C2442: ['2026-08', '2026-09'] -> [142.1]
DE C2444: ['2026-08', '2026-09'] -> [152.2]
IT C241: ['2026-08', '2026-09'] -> [96.5]
IT C2442: ['2026-08', '2026-09'] -> [133.2]
IT C2444: ['2026-08', '2026-09'] -> [139.5]
ES C241: ['2026-08', '2026-09'] -> [110.2]
ES C2442: ['2026-08', '2026-09'] -> [145.6]
ES C2444: ['2026-08', '2026-09'] -> [151.8]
FR C241: ['2026-08', '2026-09'] -> [104.0]
FR C2442: ['2026-08', '2026-09'] -> [137.1]
FR C2444: ['2026-08', '2026-09'] -> [176.4]
_(19.7 s)_

## [Acero] Destatis GENESIS (precios por producto Alemania)
GET helloworld/logincheck -> HTTP 200 2506 bytes text/html
   '<!doctype html>\n<html lang="de">\n  <head>\n    <meta charset="utf-8" />\n    <meta name="viewport" content="width=device-width, user-scalable=yes" />\n    <meta name="theme-color" content="#000000" />\n    <meta\n      http-equiv="Content-Security-Policy"\n      content="\n      default-src \'none\';\n      base-uri \'none\';\n      object-src \'none\';\n      font-src \'self\';\n      script-src \'self\' https://code'
   'Betonstahl': 0 filas; ej: -
   'Warmbreitband': 0 filas; ej: -
   'verzinkt': 0 filas; ej: -
   'Kaltgewalzt': 0 filas; ej: -
   'Walzdraht': 0 filas; ej: -
   'Stahlschrott': 0 filas; ej: -
_(2.3 s)_

## [Acero] IBGE IPP Brasil
https://apisidra.ibge.gov.br/values/t/6903/n1/all/v/all/p/last%202/c842/all -> HTTP 200 78355 bytes
   filas 209, con 'metal' 16: [{"NC": "1", "NN": "Brasil", "MC": "2", "MN": "%", "V": "-0.83", "D1C": "1", "D1N": "Brasil", "D2C": "1396", "D2N": "IPP - Variação mês/mês imediatamente anterior (M/M-1)", "D3C": "202607", "D3N": "julho 2026", "D4C": "46641", "D4N": "24 METALURGIA"}, {"NC": "1", "NN": "Brasil", "MC": "2", "MN": "%", "V": "1.16", "D1C": "1", "D1N": "Brasil", "D2C": "1396", "D2N": "IPP - Variação mês/mês imediatamente anterior (M/M-1)", "D3C": "202607", "D3N": "julho 2026", "D4C": "46643", "D4N": "25 FABRICAÇÃO D
https://servicodados.ibge.gov.br/api/v3/agregados/6903/metadados -> HTTP 200 3731 bytes
   nombre: Índice de Preços ao Produtor, por tipo de índice, indústria geral, indústrias extrativas e indústrias de transformação e atividades (dezembro de 2018 = 100); periodicidad {'frequencia': 'mensal', 'inicio': 200912, 'fim': 202608}; clasificaciones ['Indústria geral, indústrias extrativas e indústrias de transformação e atividades (CNAE 2.0)']
_(1.3 s)_

## [Acero] India WPI por ítem
HTTP 200 20270 bytes; links ['indx_download_7071/index_7071.xls', 'indx_download_6162/index_6162.xls', 'indx_download_5253/index_5253.xls', 'eight_core_infra/Core Industries 2004-05.xlsx', 'indx_download_2223/wpi_monthly_index_202610.xlsx', 'indx_download_2223/oppi_monthly_index_202610.xlsx', 'indx_download_2223/trial_ippi_monthly_index_202610.xlsx', 'indx_download_2223/SPPIs_quarterly_index_202608.xlsx', 'indx_download_2223/wpi_yearly_index_202606.xlsx', 'indx_download_2223/oppi_yearly_index_202606.xlsx', 'indx_download_2223/SPPIs_yearly_index_202608.xlsx']
_(1.4 s)_

## [Local] Ternium (SEC, precio realizado)
Ternium S.A.: 561 presentaciones recientes
   2026-10-08 6-K analystdaypresentation8oct.htm
   2026-08-05 6-K a2026junternium6-k.htm
   2026-08-04 6-K prternium2q2026.htm
   2026-07-08 6-K MainDocument.htm
   2026-07-08 6-K MainDocument.htm
   2026-05-12 6-K a2026-05x12pragsmresolutio.htm
   2026-05-12 6-K a2026may12agsmresolutions.htm
   2026-05-06 6-K a2026marternium6-k.htm
   2026-05-05 6-K prternium1q2026.htm
   2026-04-16 6-K supplementtothebrochureand.htm
   2026-04-15 6-K prnewdividendproposal.htm
   2026-03-31 6-K pr20-f2026x03x31.htm
   comunicados: ['2026-08-04 6-K prternium2q2026.htm', '2026-05-05 6-K prternium1q2026.htm', '2026-04-15 6-K prnewdividendproposal.htm', '2026-03-31 6-K pr20-f2026x03x31.htm']
_(0.3 s)_

## [Local] INDEC SIPM (IPIM 4 dígitos)
ERROR
```
Traceback (most recent call last):
  File "/home/runner/work/monitor-insumos-metal-rgicos/monitor-insumos-metal-rgicos/tests/test_fuentes.py", line 50, in caso
    texto = f()
            ^^^
  File "/home/runner/work/monitor-insumos-metal-rgicos/monitor-insumos-metal-rgicos/tests/test_fuentes.py", line 492, in indec_sipm
    res.append("      " + " | ".join(x for x in f.tolist()[:4] if x != "nan")[:140])
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: sequence item 1: expected str instance, float found

```
_(6.3 s)_

## [Local] INDEC ICC (materiales)
ERROR
```
Traceback (most recent call last):
  File "/home/runner/work/monitor-insumos-metal-rgicos/monitor-insumos-metal-rgicos/tests/test_fuentes.py", line 50, in caso
    texto = f()
            ^^^
  File "/home/runner/work/monitor-insumos-metal-rgicos/monitor-insumos-metal-rgicos/tests/test_fuentes.py", line 509, in indec_icc
    res.append("      " + " | ".join(x for x in f.tolist()[:3] if x != "nan")[:140])
                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: sequence item 1: expected str instance, float found

```
_(5.2 s)_

## [Local] DGE Rosario (materiales)
CKAN -> HTTP 404 14067 bytes
PDF jul-26 -> HTTP 200 722174 bytes
_(7.6 s)_

## [Local] BCRA A3500
A3500: [{"idVariable": 5, "detalle": [{"fecha": "2026-10-16", "valor": 1514.5655}, {"fecha": "2026-10-15", "valor": 1513.9308}, {"fecha": "2026-10-14", "valor": 1514.5655}]}]
_(1.0 s)_
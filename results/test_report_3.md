
# Resumen

| Bloque | Fuente | Estado | Detalle |
|---|---|---|---|
| Local | INDEC IPIM por código (2710, 2720, 28...) | OK | fila de fechas: 4; últimas fechas ['Jul', 'Ago', 'Sep*'] |
| Materias primas | Banco de Japón (ítems) | OK | series 32086; ítems de interés 2681 |
| No ferrosos | Yahoo (búsqueda) | OK | 'scrap': ['FSF=F (HMS 80/20 Ferrous Scrap, CFR Tu)', 'FSFF27.CMX (HMS 80/20 Ferrous Scrap, CFR Tu)', 'FSFX26.C |
| No ferrosos | Changjiang (valores del día) | OK | cobre: https://copper.ccmn.cn/copperprice/2026-10-16/b60827bea0074fbf9e950d47aa8cfa32.html -> HTTP 200; tablas |
| Acero | CISA (lista del índice) | OK | lista -> HTTP 200 26263 bytes; links ['content.html']; texto ' 中国钢铁工业协会 localStorage.User = psUtil.checkLogin( |
| General | Profundidad histórica SHFE / ZCE / NBS | OK | SHFE 2010-01-04: HTTP 200 35629 bytes |
# Test 3 — 2026-10-16 23:05 UTC


## [Local] INDEC IPIM por código (2710, 2720, 28...)
fila de fechas: 4; últimas fechas ['Jul', 'Ago', 'Sep*']
   27 Productos metálicos básicos: últimos [13644.2, 13879.9, 13960.3]
   271 Productos de minerales ferrosos en formas básicas: últimos [14608.9, 14903.9, 15094.0]
   2710: no está
   272 Productos de minerales no ferrosos en formas básicas: últimos [16458.7, 16685.7, 16823.9]
   2720: no está
   273 Productos de fundición: últimos [11832.6, 11983.3, 11895.5]
   28 Productos metálicos excepto máquinas y equipos: últimos [13945.8, 14080.2, 14387.3]
   281 Productos metálicos estructurales, recipientes y generadores de vapor: últimos [14595.6, 14703.5, 15114.7]
   289 Otros productos metálicos excepto máquinas, equipos y muebles: últimos [13649.8, 13796.4, 14056.1]
   29 Máquinas y equipos: últimos [14706.1, 14885.9, 15125.4]
   2899 Otros productos metálicos n.c.e.p.: últimos [13946.9, 14105.2, 14367.3]
   2811 Productos metálicos para uso estructural: últimos [14578.8, 14682.8, 15101.1]
_(2.1 s)_

## [Materias primas] Banco de Japón (ítems)
series 32086; ítems de interés 2681
Encabezados de bloque (para saber cuál es doméstico, export, import):
   : Corporate Goods Price Index (2020 base)
   PRCG20_220: [Producer Price Index] All commodities
   PRCG20_22G: (Reference) All commodities (excluding extra charges for summer electricity)
   PRCG20_240: [Export Price Index / yen basis] All commodities
   PRCG20_230: [Export Price Index / contract currency basis] All commodities
   PRCG20_260: [Import Price Index / yen basis] All commodities
   PRCG20_250: [Import Price Index / contract currency basis] All commodities
   PRCG20_120: [Producer Price Index excluding Consumption Tax] All commodities
   PRCG20_12G: (Reference) [Producer Price Index excluding Consumption Tax] All commodities (excluding extra charges for summer electricity)
   PRCG20_24G: Passenger cars (for North America)
   PRCG20_23G: Passenger cars (for North America)
   PRCG20_18K: Investment Goods Index
   PRCG15_220: [Producer Price Index] All commodities
   PRCG15_22G: (Reference) All commodities (excluding extra charges for summer electricity)
   PRCG15_240: [Export Price Index / yen basis] All commodities
   PRCG15_230: [Export Price Index / contract currency basis] All commodities
   PRCG15_260: [Import Price Index / yen basis] All commodities
   PRCG15_250: [Import Price Index / contract currency basis] All commodities
   PRCG15_18K: Domestic demand products
   PRCG15_18L: Domestic demand products
   PRCG15_18M: Exports
   PRCG15_120: [Producer Price Index excluding Consumption Tax] All commodities
   PRCG15_12G: (Reference) [Producer Price Index excluding Consumption Tax] All commodities (excluding extra charges for summer electricity)
   PRCG15_24G: Passenger cars (for North America)
   PRCG15_23G: Passenger cars (for North America)
   PRCG10_220: [Producer Price Index] All commodities
   PRCG10_22G: (Reference) [Producer Price Index] All commodities (excluding extra charges for summer electricity)
   PRCG10_240: [Export Price Index / yen basis] All commodities
   PRCG10_230: [Export Price Index / contract currency basis] All commodities
   PRCG10_260: [Import Price Index / yen basis] All commodities
   PRCG20_2200450002: Commodity/____Non-painted printing paper [CY2020 average=100] 202001-202609
   PRCG20_2200450003: Commodity/____Coated printing paper [CY2020 average=100] 202001-202609
   PRCG20_2200450006: Commodity/____Converting paper [CY2020 average=100] 198501-202609
   PRCG20_2200540012: Commodity class/___Thermo-setting resins [CY2020 average=100] 202001-202609
   PRCG20_2200550021: Commodity/____Thermo-setting resins [CY2020 average=100] 202001-202609
   PRCG20_2200550041: Commodity/____Electrical insulating paints [CY2020 average=100] 199501-202609
   PRCG20_2200540021: Commodity class/___Printing ink [CY2020 average=100] 202001-202609
   PRCG20_2200550044: Commodity/____Printing ink [CY2020 average=100] 198001-202609
   PRCG20_2200540023: Commodity class/___Gelatin and adhesives [CY2020 average=100] 202001-202609
   PRCG20_2200650008: Commodity/____Lubricating oil [CY2020 average=100] 200001-202609
   PRCG20_2200640002: Commodity class/___Coal products [CY2020 average=100] 202001-202609
   PRCG20_2200650011: Commodity/____Coal coke [CY2020 average=100] 198001-202609
   PRCG20_2200750003: Commodity/____Plastic pipe and tube fittings [CY2020 average=100] 198001-202609
   PRCG20_2200940001: Commodity class/___Ferro-alloys [CY2020 average=100] 202001-202609
   PRCG20_2200950001: Commodity/____Ferro-manganese [CY2020 average=100] 200501-202609
   PRCG20_2200940002: Commodity class/___Hot rolled steel [CY2020 average=100] 202001-202609
   PRCG20_2200950003: Commodity/____Light steel bars [CY2020 average=100] 198001-202609
   PRCG20_2200950004: Commodity/____Wire rods [CY2020 average=100] 200501-202609
   PRCG20_2200950005: Commodity/____Heavy and medium steel plates [CY2020 average=100] 200001-202609
   PRCG20_2200950006: Commodity/____Hot rolled steel strips [CY2020 average=100] 198001-202609
   PRCG20_2200940003: Commodity class/___Steel pipes and tubes [CY2020 average=100] 202001-202609
   PRCG20_2200950011: Commodity/____Ordinary steel pipes and tubes [CY2020 average=100] 200501-202609
   PRCG20_2200950012: Commodity/____Stainless steel pipes and tubes [CY2020 average=100] 198001-202609
   PRCG20_2200950013: Commodity/____Cold rolled steel strips [CY2020 average=100] 198001-202609
   PRCG20_2200950014: Commodity/____Cold rolled electrical steel hoops [CY2020 average=100] 198001-202609
   PRCG20_2200950016: Commodity/____Cold rolled stainless steel sheets [CY2020 average=100] 201001-202609
   PRCG20_2200950017: Commodity/____Cold finished bars [CY2020 average=100] 198001-202609
   PRCG20_2200950019: Commodity/____Zinc-coated steel sheets [CY2020 average=100] 202001-202609
   PRCG20_2200950020: Commodity/____Tin plates and chromium-coated steel sheets [CY2020 average=100] 201001-202609
   PRCG20_2200950022: Commodity/____Iron castings for machinery [CY2020 average=100]
_(0.6 s)_

## [No ferrosos] Yahoo (búsqueda)
'scrap': ['FSF=F (HMS 80/20 Ferrous Scrap, CFR Tu)', 'FSFF27.CMX (HMS 80/20 Ferrous Scrap, CFR Tu)', 'FSFX26.CMX (HMS 80/20 Ferrous Scrap, CFR Tu)', 'FSFV26.CMX (HMS 80/20 Ferrous Scrap, CFR Tu)', 'FSFZ26.CMX (HMS 80/20 Ferrous Scrap, CFR Tu)']
'steel': ['HDG=F (U.S. Midwest Domestic Steel Pre)']
'rebar': []
'coking coal': []
'iron ore': []
'cobalt': []
'lithium': ['LTH=F (Lithium Hydroxide CIF CJK (Fast)']
'hot-rolled': ['EHR=F (North European Hot-Rolled Coil )', 'EHRZ26.CMX (North European Hot-Rolled Coil )', 'EHRV26.CMX (North European Hot-Rolled Coil )', 'EHRF27.CMX (North European Hot-Rolled Coil )', 'EHRH27.CMX (North European Hot-Rolled Coil )', 'EHRX26.CMX (North European Hot-Rolled Coil )', 'EHRG27.CMX (North European Hot-Rolled Coil )']
'turkish': []
'aluminium': []
BUS=F: 0 obs en 3 meses; últimos []; meta 445.0
EHR=F: 1 obs en 3 meses; últimos [763.0]; meta 763.0
TIO=F: 65 obs en 3 meses; últimos [90.83000183105469, 90.72000122070312, 90.73999786376953, 90.56999969482422]; meta 161.91
HRC=F: 66 obs en 3 meses; últimos [1276.0, 1285.0, 1285.0, 1357.0]; meta 1357.0
ZNC=F: 65 obs en 3 meses; últimos [3943.5, 3943.5, 3943.5, 3943.5]; meta 4050.0
_(4.1 s)_

## [No ferrosos] Changjiang (valores del día)
cobre: https://copper.ccmn.cn/copperprice/2026-10-16/b60827bea0074fbf9e950d47aa8cfa32.html -> HTTP 200; tablas 2 [[['1#铜', '1#', '未登录', '元/吨', -100, '国产', '2026-10-16', '含税']], [['QAL9-4铝青铜 C18150铬锆铜棒铜管铜板', '17370171211', '江西鹰潭市贵溪市铜产业循环经济基地', '1千克  起', '103  元/千克', '我要购买'], ['出售1#电解铜，好铜，平水铜', '1020*1020*2500', '上海，常州', '1吨  起', '110,000  元/吨', '我要购买'], ['磷铜板 锡青铜板 铝青铜板', '1.0-70*430*1500', '上海 广东 江西', '500千克  起; rangos []
   página 2 del listado: HTTP 200
aluminio: https://alu.ccmn.cn/aluprice/2026-10-16/aced11dd867c48b2ae5fabe34794f956.html -> HTTP 200; tablas 2 [[['A00铝', 'A00', '未登录', '元/吨', 190, '国产', '2026-10-16', '含税']], [['现货出售A00标铝含量99.7%', '10*30*1000', '无锡，上海，常州', '5吨  起', '23,500  元/吨', '我要购买'], ['供应纯铝板}合金铝板', '0.7*1500*2500', '山东省济南市平阴县', '12吨  起', '16,500  元/吨', '我要购买'], ['铝镍中间合金厂家 AlNi10 AlNi20', '1.5mm*1000mm*200', '浙江省宁波市江北区慈城镇三板桥8号', '1千克  起; rangos []
   página 2 del listado: HTTP 200
zinc: HTTP 200, sin links
níquel: HTTP 200, sin links
_(15.0 s)_

## [Acero] CISA (lista del índice)
lista -> HTTP 200 26263 bytes; links ['content.html']; texto ' 中国钢铁工业协会 localStorage.User = psUtil.checkLogin(); // 导入公共模板 if(localStorage.User==null || localStorage.User==undefined || localStorage.User==""){ $(".top").load("common/top.html"); } else{ $(".top").load("common/top_vip.html"); } 首页 &nbsp;&gt;&nbsp;钢协动态 --> 钢协动态 钢协要闻 会议报道 领导讲话 领导讲话2 --> 钢协要闻 习近平同智利'
POST http://www.chinaisa.org.cn/gxportal/xfgl/portal/getColumnList -> HTTP 200 'ï»¿ï»¿<html>\r\n<head>\r\n    <meta charset="UTF-8">\r\n    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">\r\n    <meta name="renderer" content="webkit">\r\n    <title>ä¸\xadå\x9b½é\x92¢é\x93\x81å·¥ä¸\x9aå\x8d\x8fä¼\x9a</title>\r\n    <meta name="keywords" content="ä¸\xadå\x9b½é\x92¢é\x93\x81å·¥ä¸\x9aå\x8d\x8fä¼\x9aï¼\x8cä¸\xadå\x9b½é\x92¢é\x93\x81å·¥ä¸\x9aå\x8d\x8fä¼\x9aç½\x91ç«\x99'
POST http://www.chinaisa.org.cn/gxportal/xfpt/portal/getColumnList -> HTTP 200 '{"articleListHtml":"<div class=\'tab-con active\'><div class=\'head-tit\'><span class=\'point\'></span><span>钢材价格指数</span></div><div class=\'con-list\'><ul class=\'list\'><li><a href=\'content.html?articleId=c78222867bfaea05041e13f21526ac909c129c1c9c29959072d6b6d194c1cb38&columnId=17b6a9a214c94ccc28e56d4d1a2db'
_(4.8 s)_

## [General] Profundidad histórica SHFE / ZCE / NBS
SHFE 2010-01-04: HTTP 200 35629 bytes
SHFE 2018-01-02: HTTP 200 60579 bytes
ZCE 2018-01-02: HTTP 200 24738 bytes
NBS listado pág. 60: informes ['2022年4月上旬', '2022年4月上旬']
_(16.0 s)_
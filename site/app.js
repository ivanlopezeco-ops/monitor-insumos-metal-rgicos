/* Monitor de insumos metalúrgicos. Lee data.json (generado por el pipeline) y arma una sección por grupo de insumos. */
"use strict";

let D = null;
const R = { dias: 1095 };          // período general; cada tarjeta arranca con una copia
let TAB = "Acero";
const charts = [];

const MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];
const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const COLS = ["azul", "naranja", "verde", "violeta", "ocre", "turquesa", "rojo", "celeste", "marron", "gris"];
const COL = () => Object.fromEntries([...COLS, "tinta", "texto2", "nota", "grilla", "eje", "card", "borde"].map((k) => [k, css("--" + k)]));
const TIPOS = { precio_real: "Precio real", futuro: "Futuro", precio_comercio_exterior: "Comercio exterior", indice: "Índice", estimacion: "Estimación" };
const GRUPOS = ["Acero", "Materias primas siderúrgicas", "Metales no ferrosos", "Precios locales"];

// ------------------------------------------------------------------ formato y fechas
const nf = (dec) => new Intl.NumberFormat("es-AR", { minimumFractionDigits: dec, maximumFractionDigits: dec });
const fmt = (v, dec = 0) => (v == null || isNaN(v) ? "s/d" : nf(dec).format(v));
const decPara = (v) => (Math.abs(v) >= 1000 ? 0 : Math.abs(v) >= 10 ? 1 : 2);
const iso = (t) => new Date(t).toISOString().slice(0, 10);
const hoy = () => iso(Date.now());
const fechaCorta = (s) => { const [y, m, d] = s.split("-"); return `${+d}-${MESES[+m - 1]}-${y.slice(2)}`; };
const mesCorto = (s) => { const [y, m] = s.split("-"); return `${MESES[+m - 1]}-${y.slice(2)}`; };
const trimestre = (s) => { const [y, m] = s.split("-"); return `${Math.ceil(+m / 3)}T${y.slice(2)}`; };
const fechaSerie = (s, f) => (s.frecuencia === "trimestral" ? trimestre(f) : s.frecuencia === "mensual" ? mesCorto(f) : fechaCorta(f));
const rango = (r) => [r.dias ? iso(Date.now() - r.dias * 864e5) : "1900-01-01", hoy()];
const esc = (t) => String(t ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

// ------------------------------------------------------------------ datos
const M = (id) => D.series[id];
const valEn = (d, f) => { let lo = 0, hi = d.length - 1, r = null; while (lo <= hi) { const m = (lo + hi) >> 1; if (d[m][0] <= f) { r = d[m][1]; lo = m + 1; } else hi = m - 1; } return r; };
let A3M = null;  // A3500 promedio mensual
function enPesos(id, d) {
  const s = M(id); const mensual = ["mensual", "trimestral"].includes(s.frecuencia);
  if (!A3M) { A3M = new Map(); const acc = new Map(); D.a3500.forEach(([f, x]) => { const k = f.slice(0, 7); const o = acc.get(k) || [0, 0]; o[0] += x; o[1]++; acc.set(k, o); }); acc.forEach(([t, n], k) => A3M.set(k, t / n)); }
  return d.map(([f, x]) => { const tc = mensual ? A3M.get(f.slice(0, 7)) : valEn(D.a3500, f); return [f, tc ? x * tc : null]; }).filter((p) => p[1] != null);
}
function datos(id, moneda) {
  const s = M(id);
  if (moneda === "original" && s.o) return s.o;
  if (moneda === "pesos" && s.unidad_tablero === "USD/t") return enPesos(id, s.d);
  return s.d;
}
function unidad(id, moneda) {
  const s = M(id);
  if (moneda === "original") return s.unidad_original || s.unidad_tablero;
  if (moneda === "pesos" && s.unidad_tablero === "USD/t") return "$/t";
  return s.unidad_tablero;
}
const variacion = (d, dias) => { if (!d.length) return null; const [f, x] = d.at(-1); const y = valEn(d, iso(Date.parse(f) - dias * 864e5)); return y ? (x / y - 1) * 100 : null; };
const enAnio = (d) => { if (!d.length) return null; const [f, x] = d.at(-1); const y = valEn(d, `${+f.slice(0, 4) - 1}-12-31`); return y ? (x / y - 1) * 100 : null; };

// ------------------------------------------------------------------ gráfico
function grafico(el, cfg) {
  const c = COL(); const ch = echarts.init(el, null, { renderer: "canvas" }); charts.push(ch);
  const [ra, rb] = rango(cfg.r);
  const ancho = el.clientWidth || 600;
  const leyenda = !cfg.conChips && cfg.series.length > 3;
  const etiquetas = !leyenda && cfg.series.length <= 6;
  const margen = !etiquetas ? 16 : Math.round(Math.min(170, Math.max(90, ancho * 0.24)));
  let fMin = null;
  const series = cfg.series.map((s, i) => {
    let d = s.d;
    if (cfg.base100) {
      const p0 = d.find((p) => p[0] >= ra && p[1] != null);
      d = p0 ? d.map(([f, x]) => [f, (x / p0[1]) * 100]) : [];
    }
    if (d.length && (!fMin || d[0][0] < fMin)) fMin = d[0][0];
    const vis = d.filter((p) => p[0] >= ra && p[0] <= rb);
    const color = c[s.color];
    const dec = cfg.base100 ? 1 : decPara(vis.at(-1)?.[1] ?? d.at(-1)?.[1] ?? 0);
    return {
      name: s.nombre, type: "line", data: d, showSymbol: s.mensual && vis.length < 60, symbol: "circle", symbolSize: 4,
      lineStyle: { width: i === 0 ? 2.2 : 1.6, color, type: s.punteado ? [5, 4] : "solid" }, itemStyle: { color },
      emphasis: { disabled: true }, connectNulls: true, sampling: d.length > 1500 ? "lttb" : undefined, z: 10 - i,
      endLabel: { show: etiquetas, formatter: (p) => `${s.corto || s.nombre} ${fmt(p.value[1], dec)}`, color, fontSize: 11, fontWeight: 600, fontFamily: "Poppins", distance: 6 },
      labelLayout: { moveOverlap: "shiftY" }, _u: s.unidad, _dec: dec,
    };
  });
  const t0 = Math.max(Date.parse(ra), fMin ? Date.parse(fMin) : 0);
  ch.setOption({
    animation: false, textStyle: { fontFamily: "Poppins" },
    legend: leyenda ? { top: 0, left: 0, itemWidth: 14, itemHeight: 8, textStyle: { color: c.texto2, fontSize: 11 } } : undefined,
    grid: { left: 8, right: margen, top: leyenda ? 16 + 18 * Math.ceil(cfg.series.length / Math.max(2, Math.floor(ancho / 210))) : 14, bottom: 46, containLabel: true },
    tooltip: {
      trigger: "axis", backgroundColor: c.card, borderColor: c.eje, textStyle: { color: c.tinta, fontSize: 12 }, confine: true,
      formatter: (ps) => {
        const f = iso(ps[0].axisValue);
        return `<div style="font-size:11px;color:${c.texto2}">${fechaCorta(f)}</div>` + ps.filter((p) => p.value && p.value[1] != null).map((p) => {
          const s = series[p.seriesIndex];
          return `<span style="color:${p.color}">●</span> ${p.seriesName}: <b>${fmt(p.value[1], s._dec)}</b> <span style="color:${c.nota}">${cfg.base100 ? "" : esc(s._u)} · ${fechaCorta(p.value[0])}</span>`;
        }).join("<br>");
      },
    },
    xAxis: { type: "time", axisLine: { lineStyle: { color: c.eje } }, axisTick: { show: false }, splitLine: { show: false },
      axisLabel: { color: c.texto2, fontSize: 11, hideOverlap: true, formatter: (v) => { const d = new Date(v); const anios = (Date.parse(rb) - t0) / 864e5 / 365;
        return anios > 4 ? String(d.getFullYear()) : `${MESES[d.getMonth()]}-${String(d.getFullYear()).slice(2)}`; } } },
    yAxis: { type: cfg.log ? "log" : "value", scale: true, axisTick: { show: false }, splitLine: { lineStyle: { color: c.grilla } },
      axisLabel: { color: c.texto2, fontSize: 11, formatter: (v) => fmt(v, Math.abs(v) < 10 && !cfg.base100 ? 1 : 0) } },
    dataZoom: [{ type: "slider", xAxisIndex: 0, filterMode: "weakFilter", realtime: false, height: 16, bottom: 4, left: 46, right: Math.max(46, margen - 10),
      startValue: t0, endValue: Date.parse(rb) + 864e5, brushSelect: false, borderColor: c.borde, backgroundColor: "transparent", fillerColor: c.azul + "1f",
      dataBackground: { lineStyle: { color: c.gris, width: 1 }, areaStyle: { color: c.gris, opacity: 0.1 } },
      selectedDataBackground: { lineStyle: { color: c.azul, width: 1 }, areaStyle: { color: c.azul, opacity: 0.12 } },
      handleSize: "120%", handleStyle: { color: c.card, borderColor: c.azul }, moveHandleSize: 0, showDetail: true,
      textStyle: { color: c.texto2, fontSize: 10, fontFamily: "Poppins" }, labelFormatter: (v) => (v ? fechaCorta(iso(v)) : "") }],
    series,
  });
  ch.on("datazoom", () => {
    const z = ch.getOption().dataZoom[0]; if (z.startValue == null || !cfg.alZoom) return;
    cfg.alZoom(iso(z.startValue));
  });
}

// ------------------------------------------------------------------ tarjeta
const RANGOS = [["1A", 365], ["3A", 1095], ["5A", 1826], ["10A", 3652], ["Todo", 0]];

function segmento(cont, opciones, actual, alElegir) {
  const s = document.createElement("div"); s.className = "segmento";
  opciones.forEach(([t, v]) => { const b = document.createElement("button"); b.textContent = t; if (v === actual) b.className = "on"; b.onclick = () => alElegir(v); s.appendChild(b); });
  cont.appendChild(s);
}

function chipTipo(t) { return `<span class="tipo ${t}">${TIPOS[t] || t}</span>`; }

function ficha(id) {
  const s = M(id); const f = s.fuente || {}; const v = s.validacion || {};
  const ultimo = s.d.length ? s.d.at(-1) : null;
  const orig = s.o && s.o.length ? s.o.at(-1) : null;
  const avisos = (v.notas || []).map((n) => `<span class="aviso">${esc(n)}</span>`).join(" · ");
  return `<div class="ficha"><h4>${esc(s.nombre)} ${chipTipo(s.tipo)} ${s.licencia === "uso_interno" ? '<span class="interno">uso interno</span>' : ""}</h4>
    <p><b>Qué mide.</b> ${esc(s.que_mide)}</p>
    ${s.limitaciones ? `<p><b>A tener en cuenta.</b> ${esc(s.limitaciones)}</p>` : ""}
    <p class="meta">Fuente: ${f.url ? `<a href="${esc(f.url)}" target="_blank" rel="noopener">${esc(f.nombre)}</a>` : esc(f.nombre)} · ${esc(s.frecuencia)}${s.rezago ? ", se publica con " + esc(s.rezago) + " de demora" : ""}
    · unidad original: ${esc(s.unidad_original || s.unidad_tablero)}${s.conversion ? " (" + esc(s.conversion) + ")" : ""}
    ${ultimo ? ` · último dato: ${fechaSerie(s, ultimo[0])}, ${fmt(ultimo[1], decPara(ultimo[1]))} ${esc(s.unidad_tablero)}${orig ? ` (${fmt(orig[1], decPara(orig[1]))} ${esc(s.unidad_original)})` : ""}` : " · <span class='aviso'>todavía sin datos</span>"}
    ${s.p ? ` · <span class="prov">el último dato es del día y puede cambiar</span>` : ""}</p>
    ${avisos ? `<p class="meta">${avisos}</p>` : ""}</div>`;
}

function tablaVariaciones(ids, moneda) {
  const filas = ids.map((id) => {
    const s = M(id); const d = datos(id, moneda); if (!d.length) return `<tr><td>${esc(s.nombre)}</td><td colspan="6">sin datos todavía</td></tr>`;
    const [f, x] = d.at(-1);
    const celda = (v) => `<td class="${v == null ? "" : v >= 0 ? "pos" : "neg2"}">${v == null ? "s/d" : (v > 0 ? "+" : "") + fmt(v, 1) + "%"}</td>`;
    const corto = ["diaria", "decadal", "semanal"].includes(s.frecuencia);
    return `<tr><td>${esc(s.nombre)}<span class="tsub">${TIPOS[s.tipo]} · ${esc(unidad(id, moneda))}</span></td><td>${fmt(x, decPara(x))}<span class="tsub">${fechaSerie(s, f)}</span></td>
      ${celda(corto ? variacion(d, 30) : null)}${celda(variacion(d, s.frecuencia === "trimestral" ? 91 : 90))}${celda(variacion(d, 365))}${celda(enAnio(d))}</tr>`;
  });
  return `<div class="tw"><table class="tabla"><tr><th>Serie</th><th>Último</th><th>1 mes</th><th>3 meses</th><th>12 meses</th><th>En el año</th></tr>${filas.join("")}</table></div>`;
}

// cfg: {titulo, bajada, ids, indice (siempre base 100), monedas (permitir USD/$/original)}
function tarjeta(cont, cfg) {
  const card = document.createElement("section"); card.className = "card ancha";
  const conDatos = cfg.ids.filter((id) => M(id).d.length);
  const sinRuido = conDatos.filter((id) => M(id).tipo !== "precio_comercio_exterior");
  const st = { r: { ...R }, moneda: "usd", base100: !!cfg.indice, on: new Set((sinRuido.length >= 2 ? sinRuido : conDatos).slice(0, 6)) };
  if (!st.on.size) cfg.ids.forEach((id) => st.on.add(id));
  card.innerHTML = `<div class="card-top"><h3></h3><div class="mini-rangos" role="group" aria-label="Período de este gráfico"></div></div>
    <p class="bajada"></p><div class="controles"></div><div class="chips"></div><div class="chart"></div><div class="vars"></div>
    <details class="midiendo"><summary>Qué estamos midiendo</summary><div class="fichas"></div></details><p class="fuente"></p>`;
  cont.appendChild(card);
  const el = card.querySelector(".chart");
  card._dibujar = () => {
    const i = echarts.getInstanceByDom(el); if (i) { charts.splice(charts.indexOf(i), 1); i.dispose(); }
    const c = COL();
    const ids = cfg.ids.filter((id) => st.on.has(id));
    const colorDe = (id) => COLS[cfg.ids.indexOf(id) % COLS.length];
    card.querySelector("h3").textContent = cfg.titulo;
    const u = ids.length ? unidad(ids[0], st.moneda) : "";
    let baj = cfg.bajada || "";
    if (st.base100) baj += (baj ? " " : "") + "Base 100 al inicio del período visible: muestra cuánto subió o bajó cada serie desde ese momento.";
    else if (st.moneda === "original") baj += (baj ? " " : "") + "Cada serie en su moneda y unidad original (ver tabla). Para comparar entre mercados conviene usar base 100.";
    else if (u) baj += (baj ? " " : "") + `En ${u === "$/t" ? "pesos por tonelada, al dólar mayorista A3500 de cada fecha" : u === "USD/t" ? "dólares por tonelada" : u}.`;
    card.querySelector(".bajada").textContent = baj;
    // controles
    const ctr = card.querySelector(".controles"); ctr.innerHTML = "";
    if (!cfg.indice && cfg.monedas) segmento(ctr, [["USD/t", "usd"], ["$/t", "pesos"], ["Moneda original", "original"]], st.moneda, (v) => { st.moneda = v; card._dibujar(); });
    if (!cfg.indice) segmento(ctr, [["Valores", false], ["Base 100", true]], st.base100, (v) => { st.base100 = v; card._dibujar(); });
    const chips = card.querySelector(".chips"); chips.innerHTML = "";
    if (cfg.ids.length > 1) cfg.ids.forEach((id) => {
      const b = document.createElement("button"); b.className = st.on.has(id) ? "on" : "";
      b.innerHTML = `<span class="punto" style="background:${c[colorDe(id)]}"></span>${esc(M(id).nombre)}`;
      b.title = TIPOS[M(id).tipo]; b.onclick = () => { if (st.on.has(id)) { if (st.on.size > 1) st.on.delete(id); } else st.on.add(id); card._dibujar(); };
      chips.appendChild(b);
    });
    const mr = card.querySelector(".mini-rangos"); mr.innerHTML = "";
    RANGOS.forEach(([t, d]) => { const b = document.createElement("button"); b.textContent = t; if (st.r.dias === d && !st.r.desde) b.className = "on";
      b.onclick = () => { st.r = { dias: d }; card._dibujar(); }; mr.appendChild(b); });
    const corto = (id) => { const s = M(id); return s.mercado + (s.tipo === "futuro" ? " (fut.)" : s.tipo === "precio_comercio_exterior" ? " (com. ext.)" : s.tipo === "estimacion" ? " (est.)" : ""); };
    const series = ids.map((id) => ({ d: datos(id, st.moneda), nombre: M(id).nombre, corto: corto(id), color: colorDe(id),
      mensual: !["diaria"].includes(M(id).frecuencia), punteado: ["estimacion"].includes(M(id).tipo), unidad: unidad(id, st.moneda) })).filter((s) => s.d.length);
    if (series.length) grafico(el, { series, r: st.r, conChips: cfg.ids.length > 1, base100: st.base100, alZoom: (a) => { st.r = { dias: Math.round((Date.now() - Date.parse(a)) / 864e5) }; card._dibujarTabla(); } });
    else el.innerHTML = `<p class="bajada" style="padding:40px 0;text-align:center">Todavía no hay datos para estas series. Se completan a medida que corre la actualización.</p>`;
    card._dibujarTabla();
    card.querySelector(".fichas").innerHTML = ids.map(ficha).join("");
    const fuentes = [...new Set(ids.map((id) => (M(id).fuente || {}).nombre).filter(Boolean))];
    card.querySelector(".fuente").textContent = "Fuente: " + fuentes.join("; ") + ".";
  };
  card._dibujarTabla = () => { card.querySelector(".vars").innerHTML = tablaVariaciones(cfg.ids.filter((id) => st.on.has(id)), st.moneda); };
  card._dibujar();
}

// ------------------------------------------------------------------ secciones
function seccion(main, grupo) {
  D.insumos.filter((i) => i.grupo === grupo).forEach((ins) => {
    const ids = ins.series.filter((id) => M(id));
    if (!ids.length) return;
    const h = document.createElement("div"); h.className = "insumo";
    h.innerHTML = `<h2>${esc(ins.nombre)}</h2><p>${esc(ins.que_es)}${ins.por_que_importa ? ` <b>Por qué importa:</b> ${esc(ins.por_que_importa)}` : ""}</p>`;
    main.appendChild(h);
    const g = document.createElement("div"); g.className = "grilla"; main.appendChild(g);
    const precios = ids.filter((id) => M(id).unidad_tablero === "USD/t" && !/prima/.test(id));
    const indices = ids.filter((id) => M(id).tipo === "indice");
    const otros = ids.filter((id) => !precios.includes(id) && !indices.includes(id));
    if (precios.length) tarjeta(g, { titulo: `${ins.nombre}: precios por mercado`, ids: precios, monedas: true,
      bajada: precios.length > 1 ? "Tocá los nombres para sumar o sacar mercados." : "" });
    if (indices.length) tarjeta(g, { titulo: `${ins.nombre}: índices oficiales de precios`, ids: indices, indice: true,
      bajada: "Los índices no dan el precio en dinero; muestran cómo se movió." });
    otros.forEach((id) => tarjeta(g, { titulo: M(id).nombre, ids: [id], monedas: M(id).unidad_tablero === "USD/t" }));
  });
}

function fuentesYGlosario(main) {
  const t = D.tipos;
  const glos = [
    ["Precio real (spot o de contado)", "Lo que se paga hoy por el producto para entrega inmediata."],
    ["Futuro", t.futuro + " En el tablero se toma el contrato más cercano o el más negociado."],
    ["Precio de comercio exterior", t.precio_comercio_exterior],
    ["Índice", t.indice + " Para comparar índices de distinta base se usan en base 100."],
    ["Estimación", t.estimacion],
    ["FOB y CIF", "FOB: precio puesto en el puerto de salida, sin flete. CIF: con flete y seguro hasta el puerto de llegada."],
    ["CFR China", "Precio con flete pagado hasta un puerto chino. Es la referencia del mineral de hierro."],
    ["Base 100", "Cada serie se divide por su valor al inicio del período y se multiplica por 100. Así se ve cuánto subió o bajó cada una, sin importar su moneda."],
    ["Precio oficial LME (contado)", "Precio de referencia que fija cada día la Bolsa de Metales de Londres para entrega inmediata."],
    ["IVA en los precios chinos", "Los precios chinos incluyen 13% de IVA. En dólares se muestran sin IVA para poder compararlos con el resto."],
    ["Tonelada corta y libra", "En EE.UU. el acero cotiza por tonelada corta (907 kg) y el cobre por libra (0,454 kg). Todo se pasa a tonelada métrica."],
    ["Pase a pesos", "Dólares por el tipo de cambio mayorista A3500 del BCRA de cada fecha (promedio del mes en las series mensuales)."],
    ["Uso interno", "La fuente no permite redistribuir el dato. Sirve para el tablero interno y no para una versión pública."],
  ];
  main.innerHTML = `<section class="card glosario"><h3>Cómo leer el tablero</h3><dl>${glos.map(([a, b]) => `<dt>${esc(a)}</dt><dd>${esc(b)}</dd>`).join("")}</dl></section>`;
  const filas = Object.entries(D.fuentes).map(([k, v]) => `<tr><td>${esc(k)}</td><td>${esc(v.estado)}</td><td>${v.ultimo_ok ? fechaCorta(v.ultimo_ok.slice(0, 10)) : ""}</td><td style="text-align:left">${esc((v.error || v.detalle || "").slice(0, 160))}</td></tr>`);
  const avisos = Object.entries(D.series).filter(([, s]) => (s.validacion?.notas || []).length || !s.d.length)
    .map(([, s]) => `<tr><td>${esc(s.nombre)}</td><td style="text-align:left">${s.d.length ? esc(s.validacion.notas.join("; ")) : "todavía sin datos"}</td></tr>`);
  main.insertAdjacentHTML("beforeend", `<section class="card" style="margin-top:14px"><h3>Estado de las fuentes en la última actualización</h3>
    <div class="tw"><table class="tabla"><tr><th>Fuente</th><th>Estado</th><th>Último OK</th><th style="text-align:left">Detalle</th></tr>${filas.join("")}</table></div></section>
    <section class="card" style="margin-top:14px"><h3>Series con avisos</h3><p class="bajada">Datos viejos, saltos grandes para revisar o series que todavía no tienen datos.</p>
    <div class="tw"><table class="tabla"><tr><th>Serie</th><th style="text-align:left">Aviso</th></tr>${avisos.join("") || "<tr><td colspan=2>Sin avisos</td></tr>"}</table></div></section>`);
}

function render() {
  charts.splice(0).forEach((c) => c.dispose());
  const main = document.getElementById("main"); main.innerHTML = "";
  if (TAB === "Fuentes") fuentesYGlosario(main); else seccion(main, TAB);
}

function iniciar() {
  const gen = new Date(D.generado);
  document.getElementById("actualizado").textContent = `Datos al ${gen.toLocaleDateString("es-AR", { day: "numeric", month: "long", year: "numeric" })}, ${gen.toLocaleTimeString("es-AR", { hour: "2-digit", minute: "2-digit", hour12: false })} h`;
  const tabs = document.getElementById("tabs");
  [...GRUPOS, "Fuentes"].forEach((g) => { const b = document.createElement("button"); b.textContent = g === "Fuentes" ? "Fuentes y glosario" : g;
    if (g === TAB) b.className = "on";
    b.onclick = () => { TAB = g; tabs.querySelectorAll("button").forEach((x) => x.classList.toggle("on", x === b)); try { history.replaceState(null, "", "#" + encodeURIComponent(g)); } catch (e) {} render(); window.scrollTo(0, 0); };
    tabs.appendChild(b); });
  document.querySelectorAll("#rangos button").forEach((b) => b.onclick = () => {
    R.dias = +b.dataset.r; document.querySelectorAll("#rangos button").forEach((x) => x.classList.toggle("on", x === b)); render(); });
  document.getElementById("tema").onclick = () => {
    const oscuro = document.documentElement.dataset.theme ? document.documentElement.dataset.theme === "dark" : matchMedia("(prefers-color-scheme: dark)").matches;
    document.documentElement.dataset.theme = oscuro ? "light" : "dark";
    try { localStorage.setItem("tema", document.documentElement.dataset.theme); } catch (e) {}
    render();
  };
  let ancho = window.innerWidth, tr = null;
  window.addEventListener("resize", () => { if (window.innerWidth === ancho) return; ancho = window.innerWidth; clearTimeout(tr); tr = setTimeout(render, 250); });
}

const h = decodeURIComponent(location.hash.slice(1)); if ([...GRUPOS, "Fuentes"].includes(h)) TAB = h;
fetch("data.json", { cache: "no-cache" }).then((r) => r.json()).then((j) => { D = j; iniciar(); render(); })
  .catch((e) => { document.getElementById("main").textContent = "No se pudieron cargar los datos: " + e; });

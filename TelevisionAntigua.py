import base64
import json

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Televisor", page_icon="📺", layout="wide",
                   initial_sidebar_state="collapsed")

st.markdown("""
<style>
#MainMenu, footer {visibility: hidden;}
header {background: transparent !important;}
.block-container {padding: 0 !important; max-width: 100% !important;}
.stApp {background: #14110e;}
iframe {display: block;}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("Configurar el susto")
    img_files = st.file_uploader("Tus propias imágenes (opcional, varias)",
                                 type=["png", "jpg", "jpeg", "gif", "webp"],
                                 accept_multiple_files=True)
    snd_file = st.file_uploader("Sonido propio (opcional)", type=["mp3", "wav", "ogg"])
    static_ms = st.slider("Estática antes del susto (ms)", 0, 1000, 16, 1,
                          help="16 ms es un solo cuadro de pantalla: lo mínimo visible.")
    frame_ms = st.slider("Duración de cada aparición (ms)", 150, 1500, 420, 10)
    boost = st.slider("Amplificación digital del sonido", 1.0, 6.0, 4.0, 0.5)


def to_data_uri(f):
    return f"data:{f.type};base64,{base64.b64encode(f.getvalue()).decode()}"


custom_imgs = [to_data_uri(f) for f in (img_files or [])]
custom_snd = to_data_uri(snd_file) if snd_file else ""

HTML = r"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<style>
  html, body { margin: 0; height: 100%; background: #14110e; overflow: hidden; }
  body { display: flex; align-items: center; justify-content: center;
         font-family: "Georgia", "Times New Roman", serif; }

  /* ---------- Televisor ---------- */
  .stage { position: relative; display: flex; flex-direction: column; align-items: center; }
  .antenna { position: absolute; top: -120px; left: 50%; width: 0; height: 0; }
  .antenna::before, .antenna::after {
    content: ""; position: absolute; bottom: 0; width: 4px; height: 150px;
    background: linear-gradient(#cfcfcf, #6d6d6d); border-radius: 3px; transform-origin: bottom center; }
  .antenna::before { transform: rotate(-32deg); }
  .antenna::after  { transform: rotate(28deg); }
  .antenna-base { position: absolute; top: -26px; left: 50%; transform: translateX(-50%);
    width: 90px; height: 30px; border-radius: 45px 45px 6px 6px;
    background: radial-gradient(circle at 40% 30%, #4a4440, #1d1a18); }
  .tv { position: relative; display: flex; gap: 26px; width: min(780px, 92vw); padding: 30px;
    background: repeating-linear-gradient(92deg, rgba(0,0,0,.10) 0 3px, transparent 3px 11px),
                linear-gradient(180deg, #7a4a26, #5a3216 60%, #3f220e);
    border-radius: 26px;
    box-shadow: inset 0 2px 0 rgba(255,220,180,.25), inset 0 -6px 14px rgba(0,0,0,.5), 0 30px 60px rgba(0,0,0,.7); }
  .bezel { flex: 1; padding: 18px; border-radius: 22px; background: linear-gradient(145deg, #2b2724, #0f0d0c);
    box-shadow: inset 0 0 0 3px #1a1715, inset 0 4px 10px rgba(0,0,0,.8); }
  .screen { position: relative; aspect-ratio: 4 / 3; border-radius: 38px / 30px; overflow: hidden;
    background: radial-gradient(ellipse at 50% 45%, #2a302c 0%, #141816 60%, #070808 100%);
    box-shadow: inset 0 0 40px rgba(0,0,0,.95), inset 0 0 6px #000; }
  .screen::after { content: ""; position: absolute; inset: 0; pointer-events: none;
    background: linear-gradient(130deg, rgba(255,255,255,.10) 0%, rgba(255,255,255,0) 35%),
                radial-gradient(ellipse at 30% 20%, rgba(255,255,255,.07), transparent 50%); }
  .panel { width: 130px; display: flex; flex-direction: column; align-items: center; gap: 22px;
    padding: 18px 0; border-radius: 14px; background: linear-gradient(180deg, #c9b48a, #9c8660);
    box-shadow: inset 0 2px 0 rgba(255,255,255,.35), inset 0 -3px 8px rgba(0,0,0,.35); }
  .brand { font-style: italic; font-size: 17px; color: #3a2a14; }
  .knob { width: 64px; height: 64px; border-radius: 50%; position: relative;
    background: radial-gradient(circle at 35% 30%, #5a524b, #1c1917 70%);
    box-shadow: 0 4px 8px rgba(0,0,0,.5), inset 0 0 0 4px #2a2522; }
  .knob::after { content: ""; position: absolute; top: 6px; left: 50%; width: 4px; height: 18px;
    margin-left: -2px; background: #d8cbb0; border-radius: 2px; }
  .knob.b { transform: rotate(130deg); width: 52px; height: 52px; }
  .grill { width: 90px; height: 60px; border-radius: 6px;
    background: repeating-linear-gradient(0deg, #3a2d1c 0 3px, #9c8660 3px 7px); opacity: .8; }
  .power-wrap { display: flex; flex-direction: column; align-items: center; gap: 8px; }
  .led { width: 9px; height: 9px; border-radius: 50%; background: #3b1010; box-shadow: inset 0 0 2px #000; }
  .led.on { background: #ff3b2f; box-shadow: 0 0 10px #ff3b2f; }
  .power { width: 54px; height: 54px; border-radius: 50%; border: none; cursor: pointer;
    background: radial-gradient(circle at 40% 35%, #e9e2d4, #9b9282);
    box-shadow: 0 5px 0 #5c564c, 0 8px 14px rgba(0,0,0,.5); font-size: 22px; color: #3a3530;
    transition: transform .08s, box-shadow .08s; }
  .power:active { transform: translateY(4px); box-shadow: 0 1px 0 #5c564c, 0 3px 6px rgba(0,0,0,.5); }
  .power:focus-visible { outline: 3px solid #ffd27a; outline-offset: 4px; }
  .hint { font-size: 12px; color: #3a2a14; }
  .legs { display: flex; justify-content: space-between; width: min(640px, 76vw); }
  .legs span { width: 14px; height: 46px; background: linear-gradient(#4a2a12, #2a170a); border-radius: 0 0 6px 6px; }
  .legs span:first-child { transform: skewX(12deg); }
  .legs span:last-child  { transform: skewX(-12deg); }

  /* ---------- Transmisión intervenida ---------- */
  #overlay { position: fixed; inset: 0; z-index: 9999; background: #000; display: none; overflow: hidden; }
  #overlay.show { display: block; }
  #scare { position: absolute; inset: 0; display: none; background: #000; overflow: hidden; }
  #scare.show { display: block; animation: flash .09s steps(2) infinite; }
  #face { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;
    animation: lunge .16s ease-out forwards, shake .06s linear .16s infinite; }
  .slice { position: absolute; inset: 0; background-size: cover; background-position: center;
    mix-blend-mode: screen; pointer-events: none; }
  .slice.r { filter: sepia(1) saturate(8) hue-rotate(-50deg); }
  .slice.c { filter: sepia(1) saturate(6) hue-rotate(140deg); }
  #scare::after { content: ""; position: absolute; inset: 0; pointer-events: none;
    background: radial-gradient(ellipse at center, transparent 35%, rgba(120,0,0,.8) 100%); }
  @keyframes lunge { from { transform: scale(.4); } to { transform: scale(1.12); } }
  @keyframes shake {
    0% { transform: scale(1.12) translate(0,0); }   25% { transform: scale(1.14) translate(-14px,9px); }
    50% { transform: scale(1.12) translate(12px,-11px); } 75% { transform: scale(1.15) translate(-9px,-7px); }
    100% { transform: scale(1.12) translate(10px,12px); } }
  @keyframes flash { 0% { filter: contrast(1.5) brightness(1.05); }
    100% { filter: contrast(2.1) brightness(.75) invert(.1) hue-rotate(-15deg); } }

  #noise { position: absolute; inset: 0; width: 100%; height: 100%; image-rendering: pixelated;
    pointer-events: none; opacity: 1; }
  #noise.grain { opacity: .17; mix-blend-mode: screen; }
  .scanlines { position: absolute; inset: 0; pointer-events: none;
    background: repeating-linear-gradient(0deg, rgba(0,0,0,.4) 0 2px, transparent 2px 4px); }

  #hud { position: absolute; inset: 0; pointer-events: none; display: none;
    font-family: "Courier New", Courier, monospace; color: #e8e8e8; text-shadow: 0 0 4px #000, 2px 0 #f00, -2px 0 #0ff; }
  #hud.show { display: block; }
  .tl { position: absolute; top: max(18px, env(safe-area-inset-top)); left: 22px; font-size: clamp(14px, 2.2vw, 26px); }
  .tr { position: absolute; top: max(18px, env(safe-area-inset-top)); right: 22px; font-size: clamp(14px, 2.2vw, 26px); }
  .bl { position: absolute; bottom: 20px; left: 22px; font-size: clamp(11px, 1.4vw, 16px); opacity: .75; }
  .rec { color: #ff2a2a; animation: blink 1s steps(2) infinite; }
  @keyframes blink { 50% { opacity: 0; } }
  #msg { position: absolute; left: 0; right: 0; bottom: 14%; text-align: center;
    font-size: clamp(26px, 6vw, 80px); font-weight: bold; color: #fff; letter-spacing: 2px;
    animation: jitter .08s steps(2) infinite; }
  @keyframes jitter { 0% { transform: translate(-3px, 1px); } 100% { transform: translate(3px, -2px); } }
  #exitHint { position: absolute; bottom: 14px; right: 22px; color: rgba(255,255,255,.35);
    font: 13px sans-serif; display: none; }

  @media (max-width: 600px) {
    .tv { flex-direction: column; padding: 18px; }
    .panel { width: 100%; flex-direction: row; justify-content: space-around; padding: 12px; }
    .grill { display: none; }
  }
  @media (prefers-reduced-motion: reduce) { #scare.show { animation-duration: .4s; } }
</style>
</head>
<body>

<div class="stage">
  <div class="antenna"></div><div class="antenna-base"></div>
  <div class="tv">
    <div class="bezel"><div class="screen"></div></div>
    <div class="panel">
      <div class="brand">Radiola</div>
      <div class="knob"></div><div class="knob b"></div>
      <div class="grill"></div>
      <div class="power-wrap">
        <div class="led" id="led"></div>
        <button class="power" id="power" aria-label="Encender televisor">⏻</button>
        <div class="hint">Encender</div>
      </div>
    </div>
  </div>
  <div class="legs"><span></span><span></span></div>
</div>

<div id="overlay">
  <div id="scare">
    <img id="face" alt="">
    <div class="slice r"></div><div class="slice c"></div><div class="slice"></div>
  </div>
  <canvas id="noise" width="200" height="150"></canvas>
  <div class="scanlines"></div>
  <div id="hud">
    <div class="tl"><span class="rec">●</span> REC&nbsp;&nbsp;<span id="cam">CAM_01</span></div>
    <div class="tr" id="clock">03:33:00</div>
    <div class="bl" id="addr"></div>
    <div id="msg"></div>
  </div>
  <div id="exitHint">Esc para apagar</div>
</div>

<script>
const CUSTOM_IMGS = __IMGS__;
const CUSTOM_SND  = __SND__;
const STATIC_MS   = __STATIC_MS__;
const FRAME_MS    = __FRAME_MS__;
const BOOST       = __BOOST__;

const svg = s => "data:image/svg+xml;utf8," + encodeURIComponent(
  `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice">${s}</svg>`);

/* ---------- Criaturas originales ---------- */

// 1. Lo que gatea por el pasillo
const HALL = svg(`
<defs><radialGradient id="l" cx="50%" cy="45%" r="60%"><stop offset="0" stop-color="#2b2a22"/><stop offset="1" stop-color="#000"/></radialGradient>
<filter id="b"><feGaussianBlur stdDeviation="3"/></filter></defs>
<rect width="400" height="300" fill="url(#l)"/>
<polygon points="0,0 160,100 160,210 0,300" fill="#14130f"/>
<polygon points="400,0 240,100 240,210 400,300" fill="#100f0c"/>
<polygon points="160,210 240,210 400,300 0,300" fill="#1c1a14"/>
<rect x="160" y="100" width="80" height="110" fill="#050505"/>
<g stroke="#bdb8a8" stroke-width="7" fill="none" stroke-linecap="round">
<path d="M200 170 Q150 140 70 55"/><path d="M200 170 Q260 135 340 45"/>
<path d="M195 200 Q140 240 55 292"/><path d="M205 200 Q270 235 350 294"/></g>
<g stroke="#bdb8a8" stroke-width="3" stroke-linecap="round">
<path d="M70 55 L52 38 M70 55 L60 30 M70 55 L76 28"/><path d="M340 45 L358 30 M340 45 L350 22 M340 45 L332 20"/></g>
<ellipse cx="200" cy="188" rx="17" ry="32" fill="#a9a493"/>
<ellipse cx="200" cy="150" rx="23" ry="27" fill="#cfc9b8"/>
<circle cx="191" cy="147" r="7" fill="#fff" filter="url(#b)"/><circle cx="209" cy="147" r="7" fill="#fff" filter="url(#b)"/>
<circle cx="191" cy="147" r="3" fill="#fff"/><circle cx="209" cy="147" r="3" fill="#fff"/>
<path d="M187 163 Q200 175 213 163" stroke="#000" stroke-width="3" fill="none"/>`);

// 2. La máscara cosida
const MASK = svg(`
<defs><radialGradient id="m" cx="45%" cy="35%" r="70%"><stop offset="0" stop-color="#f2eee4"/><stop offset=".75" stop-color="#9e998c"/><stop offset="1" stop-color="#2a2824"/></radialGradient></defs>
<rect width="400" height="300" fill="#020202"/>
<ellipse cx="200" cy="150" rx="108" ry="142" fill="url(#m)"/>
<path d="M136 120 Q160 92 184 122 Q160 142 136 120Z" fill="#000"/>
<path d="M216 122 Q240 92 264 120 Q240 142 216 122Z" fill="#000"/>
<circle cx="160" cy="121" r="3.5" fill="#ff1a1a"/><circle cx="240" cy="121" r="3.5" fill="#ff1a1a"/>
<path d="M156 136 Q153 190 158 250 Q163 256 166 248 Q164 190 166 136Z" fill="#120000"/>
<line x1="160" y1="226" x2="240" y2="226" stroke="#111" stroke-width="4"/>
<g stroke="#111" stroke-width="3">${[168,180,192,204,216,228].map(x=>`<line x1="${x}" y1="216" x2="${x+4}" y2="236"/>`).join("")}</g>
<path d="M232 14 L216 68 L238 94 L206 142 L214 170" stroke="#3b3a35" stroke-width="2.5" fill="none"/>
<path d="M120 200 L146 214 L138 244" stroke="#3b3a35" stroke-width="2" fill="none"/>`);

// 3. La cara al revés
const INV = svg(`
<defs><radialGradient id="i" cx="50%" cy="60%" r="65%"><stop offset="0" stop-color="#c9c4b6"/><stop offset=".8" stop-color="#6e6a60"/><stop offset="1" stop-color="#151412"/></radialGradient></defs>
<rect width="400" height="300" fill="#000"/>
<ellipse cx="200" cy="150" rx="112" ry="155" fill="url(#i)"/>
<ellipse cx="200" cy="105" rx="32" ry="82" fill="#000"/>
<path d="M172 40 L185 52 L171 64 L185 76 L170 88 L185 100 L170 112 L185 124 L171 136 L185 148 L173 162" stroke="#e9e3c7" stroke-width="6" fill="none" stroke-linejoin="bevel"/>
<path d="M228 40 L215 52 L229 64 L215 76 L230 88 L215 100 L230 112 L215 124 L229 136 L215 148 L227 162" stroke="#e9e3c7" stroke-width="6" fill="none" stroke-linejoin="bevel"/>
<path d="M200 190 L190 208 L210 208Z" fill="#3e3b35"/>
<ellipse cx="158" cy="232" rx="28" ry="20" fill="#000"/><ellipse cx="242" cy="232" rx="28" ry="20" fill="#000"/>
<circle cx="158" cy="234" r="3" fill="#fff"/><circle cx="242" cy="234" r="3" fill="#fff"/>
<path d="M130 262 Q158 278 186 262 M214 262 Q242 278 270 262" stroke="#1d1b18" stroke-width="5" fill="none"/>`);

// 4. Los que miran
const EYES = svg(`
<defs><radialGradient id="e" cx="50%" cy="50%" r="70%"><stop offset="0" stop-color="#1a0303"/><stop offset="1" stop-color="#000"/></radialGradient>
<g id="eye"><path d="M-30 0 Q0 -19 30 0 Q0 19 -30 0Z" fill="#d8d3c4"/><circle r="9" fill="#8a0000"/><circle r="4" fill="#000"/><circle cx="-3" cy="-3" r="1.5" fill="#fff"/></g></defs>
<rect width="400" height="300" fill="url(#e)"/>
${[[60,50,.8],[150,35,.6],[250,60,1],[340,40,.7],[30,140,.9],[120,120,1.3],[205,150,2],[300,130,1.1],[375,170,.6],
   [70,235,1],[160,260,.7],[250,240,.9],[340,255,1.2],[110,195,.5],[290,200,.55]]
  .map(([x,y,s])=>`<use href="#eye" transform="translate(${x},${y}) scale(${s})"/>`).join("")}`);

// 5. Cámara de seguridad
const CAM = svg(`
<defs><radialGradient id="v" cx="50%" cy="45%" r="70%"><stop offset="0" stop-color="#2c332c"/><stop offset="1" stop-color="#050605"/></radialGradient>
<filter id="s"><feGaussianBlur stdDeviation="9 1"/></filter></defs>
<rect width="400" height="300" fill="url(#v)"/>
<path d="M30 300 Q55 215 200 205 Q345 215 370 300Z" fill="#070807"/>
<g filter="url(#s)">
<ellipse cx="200" cy="125" rx="82" ry="102" fill="#9aa39a"/>
<ellipse cx="168" cy="112" rx="18" ry="24" fill="#000"/><ellipse cx="232" cy="112" rx="18" ry="24" fill="#000"/>
<ellipse cx="200" cy="182" rx="22" ry="30" fill="#000"/></g>
<ellipse cx="168" cy="112" rx="12" ry="16" fill="#000"/><ellipse cx="232" cy="112" rx="12" ry="16" fill="#000"/>
<ellipse cx="200" cy="184" rx="15" ry="24" fill="#000"/>`);

// 6. El final
const FINAL = svg(`
<defs><radialGradient id="k" cx="50%" cy="40%" r="60%"><stop offset="0" stop-color="#d9d6cc"/><stop offset=".7" stop-color="#8d887c"/><stop offset="1" stop-color="#2a2824"/></radialGradient></defs>
<rect width="400" height="300" fill="#050505"/>
<ellipse cx="200" cy="160" rx="120" ry="160" fill="url(#k)"/>
<ellipse cx="150" cy="120" rx="34" ry="44" fill="#000"/><ellipse cx="250" cy="120" rx="34" ry="44" fill="#000"/>
<circle cx="155" cy="125" r="4" fill="#fff"/><circle cx="245" cy="125" r="4" fill="#fff"/>
<path d="M195 150 L188 185 L205 185 Z" fill="#4a463f"/>
<ellipse cx="200" cy="245" rx="70" ry="80" fill="#000"/>
<path d="M132 210 L145 232 L157 208 L170 232 L183 206 L196 232 L209 206 L222 232 L235 208 L248 232 L262 210 Z" fill="#e8e2c8"/>
<path d="M140 300 L152 278 L165 300 L178 276 L191 300 L204 276 L217 300 L230 278 L243 300 L256 280 L262 300 Z" fill="#e8e2c8"/>`);

const FRAMES = CUSTOM_IMGS.length ? CUSTOM_IMGS : [HALL, MASK, INV, EYES, CAM, FINAL];
const MSGS = ["¿POR QUÉ LA ENCENDISTE?", "NO MIRES ATRÁS", "YA ESTÁ DENTRO", "TE ESTAMOS VIENDO",
              "SIGUES AHÍ", "NO APAGUES LA TELE"];

/* ---------- Elementos ---------- */
const $ = id => document.getElementById(id);
const power = $("power"), led = $("led"), overlay = $("overlay"), canvas = $("noise"),
      scare = $("scare"), face = $("face"), hud = $("hud"), exitHint = $("exitHint");
const slices = [...document.querySelectorAll(".slice")];
const cctx = canvas.getContext("2d");

let ac = null, bus = null, staticSrc = null, customAudio = null, rafId = null;
let timers = [], intervals = [], active = false, savedFrameStyle = null;

/* ---------- Pantalla completa ---------- */
function goFullscreen() {
  const el = document.documentElement;
  const req = el.requestFullscreen || el.webkitRequestFullscreen;
  let p = null;
  try { if (req) p = req.call(el); } catch (e) {}
  try {
    const fe = window.frameElement;
    if (fe) {
      savedFrameStyle = fe.getAttribute("style") || "";
      fe.style.cssText = "position:fixed;inset:0;width:100vw;height:100vh;z-index:2147483647;border:0;";
      if (p && p.catch) p.catch(() => { try { fe.requestFullscreen(); } catch (e) {} });
    }
  } catch (e) {}
}
function exitFullscreen() {
  try { if (document.fullscreenElement) document.exitFullscreen(); } catch (e) {}
  try { if (window.frameElement && savedFrameStyle !== null) window.frameElement.setAttribute("style", savedFrameStyle); } catch (e) {}
  savedFrameStyle = null;
}

/* ---------- Audio ---------- */
function setupAudio() {
  ac = new (window.AudioContext || window.webkitAudioContext)();
  ac.resume();
  const comp = ac.createDynamicsCompressor();
  comp.threshold.value = -24; comp.knee.value = 0; comp.ratio.value = 20;
  comp.attack.value = 0.001; comp.release.value = 0.1;
  const master = ac.createGain(); master.gain.value = 1.0;
  comp.connect(master); master.connect(ac.destination);
  bus = comp;
}
function noiseBuffer(sec) {
  const b = ac.createBuffer(1, Math.max(1, ac.sampleRate * sec), ac.sampleRate);
  const d = b.getChannelData(0);
  for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  return b;
}
function distortionCurve(k) {
  const n = 2048, c = new Float32Array(n);
  for (let i = 0; i < n; i++) { const x = i * 2 / n - 1;
    c[i] = (3 + k) * x * 20 * Math.PI / 180 / (Math.PI + k * Math.abs(x)); }
  return c;
}
function playStatic() {
  staticSrc = ac.createBufferSource(); staticSrc.buffer = noiseBuffer(1); staticSrc.loop = true;
  const g = ac.createGain(); g.gain.value = 0.4;
  staticSrc.connect(g); g.connect(bus); staticSrc.start();
}
function stopStatic() { try { staticSrc && staticSrc.stop(); } catch (e) {} staticSrc = null; }

function playScream(dur) {
  const now = ac.currentTime;
  const pre = ac.createGain(); pre.gain.value = BOOST;
  const shaper = ac.createWaveShaper(); shaper.curve = distortionCurve(300);
  const env = ac.createGain();
  env.gain.setValueAtTime(0, now); env.gain.linearRampToValueAtTime(1, now + 0.012);
  env.gain.setValueAtTime(1, now + dur - 0.4); env.gain.linearRampToValueAtTime(0, now + dur);
  pre.connect(shaper); shaper.connect(env); env.connect(bus);
  [1, 1.48, 2.03, 0.51, 2.97].forEach((m, i) => {
    const o = ac.createOscillator(); o.type = "sawtooth";
    o.frequency.setValueAtTime(320 * m, now);
    o.frequency.exponentialRampToValueAtTime(1150 * m, now + 0.2);
    o.frequency.exponentialRampToValueAtTime(700 * m, now + dur);
    const lfo = ac.createOscillator(); lfo.frequency.value = 6 + i * 2.7;
    const lg = ac.createGain(); lg.gain.value = 70 * m;
    lfo.connect(lg); lg.connect(o.frequency);
    const g = ac.createGain(); g.gain.value = 0.28;
    o.connect(g); g.connect(pre);
    o.start(now); lfo.start(now); o.stop(now + dur); lfo.stop(now + dur);
  });
  const n = ac.createBufferSource(); n.buffer = noiseBuffer(dur);
  const bp = ac.createBiquadFilter(); bp.type = "bandpass"; bp.frequency.value = 2600; bp.Q.value = 0.8;
  const ng = ac.createGain(); ng.gain.value = 0.6;
  n.connect(bp); bp.connect(ng); ng.connect(pre); n.start(now);
}
function playGlitchBurst() {   // golpe de interferencia en cada corte
  const now = ac.currentTime;
  const n = ac.createBufferSource(); n.buffer = noiseBuffer(0.14);
  const hp = ac.createBiquadFilter(); hp.type = "highpass"; hp.frequency.value = 1800;
  const o = ac.createOscillator(); o.type = "square"; o.frequency.value = 55 + Math.random() * 40;
  const g = ac.createGain(); g.gain.setValueAtTime(BOOST * 0.6, now); g.gain.exponentialRampToValueAtTime(0.001, now + 0.14);
  n.connect(hp); hp.connect(g); o.connect(g); g.connect(bus);
  n.start(now); o.start(now); o.stop(now + 0.14);
}
function prepareCustomAudio() {
  if (!CUSTOM_SND) return;
  customAudio = new Audio(CUSTOM_SND); customAudio.volume = 1.0;
  const src = ac.createMediaElementSource(customAudio);
  const g = ac.createGain(); g.gain.value = BOOST;
  src.connect(g); g.connect(bus);
  customAudio.muted = true;
  customAudio.play().then(() => { customAudio.pause(); customAudio.currentTime = 0; customAudio.muted = false; }).catch(() => {});
}

/* ---------- Efectos visuales ---------- */
function drawNoise() {
  const img = cctx.createImageData(canvas.width, canvas.height), d = img.data;
  for (let i = 0; i < d.length; i += 4) { const v = Math.random() * 255 | 0; d[i] = d[i+1] = d[i+2] = v; d[i+3] = 255; }
  cctx.putImageData(img, 0, 0);
  rafId = requestAnimationFrame(drawNoise);
}
function glitch() {
  const src = face.src;
  slices.forEach(s => {
    if (Math.random() < 0.45) { s.style.display = "none"; return; }
    const t = Math.random() * 90, h = 2 + Math.random() * 14;
    s.style.display = "block";
    s.style.backgroundImage = `url("${src}")`;
    s.style.clipPath = `inset(${t}% 0 ${Math.max(0, 100 - t - h)}% 0)`;
    s.style.transform = `translateX(${(Math.random() - 0.5) * 90}px) scale(1.12)`;
  });
}
function fakeAddress() {
  const a = "abcdefghijklmnopqrstuvwxyz234567"; let s = "";
  for (let i = 0; i < 16; i++) s += a[Math.random() * a.length | 0];
  return `hxxp://${s}.onion/feed/live?id=${(Math.random() * 9999 | 0).toString().padStart(4, "0")}`;
}
function tickClock() {
  const d = new Date(), p = n => String(n).padStart(2, "0");
  $("clock").textContent = `${p(d.getDate())}/${p(d.getMonth()+1)}/${d.getFullYear()}  03:33:${p(d.getSeconds())}`;
}

/* ---------- Secuencia ---------- */
function showFrame(i) {
  face.src = FRAMES[i];
  face.style.animation = "none"; void face.offsetWidth; face.style.animation = "";
  $("cam").textContent = "CAM_" + String(i + 1).padStart(2, "0");
  $("msg").textContent = MSGS[i % MSGS.length];
  $("addr").textContent = fakeAddress();
  playGlitchBurst();
  if (i < FRAMES.length - 1) timers.push(setTimeout(() => showFrame(i + 1), FRAME_MS));
  else timers.push(setTimeout(() => { exitHint.style.display = "block"; }, 2500));
}

function startScare() {
  stopStatic();
  canvas.classList.add("grain");
  scare.classList.add("show");
  hud.classList.add("show");
  tickClock(); intervals.push(setInterval(tickClock, 1000));
  intervals.push(setInterval(glitch, 60));
  if (customAudio) { customAudio.currentTime = 0; customAudio.play().catch(() => playScream(3.5)); }
  else playScream(FRAME_MS * (FRAMES.length - 1) / 1000 + 2.2);
  showFrame(0);
}

function turnOn() {
  if (active) return;
  active = true;
  led.classList.add("on");
  goFullscreen();
  setupAudio();
  prepareCustomAudio();
  overlay.classList.add("show");
  canvas.classList.remove("grain");
  drawNoise();
  if (STATIC_MS > 0) { playStatic(); timers.push(setTimeout(startScare, STATIC_MS)); }
  else startScare();
}

function reset() {
  if (!active) return;
  active = false;
  timers.forEach(clearTimeout); intervals.forEach(clearInterval); timers = []; intervals = [];
  cancelAnimationFrame(rafId); stopStatic();
  if (customAudio) { try { customAudio.pause(); } catch (e) {} customAudio = null; }
  if (ac) { try { ac.close(); } catch (e) {} ac = null; }
  scare.classList.remove("show"); hud.classList.remove("show"); overlay.classList.remove("show");
  slices.forEach(s => s.style.display = "none");
  exitHint.style.display = "none"; led.classList.remove("on");
  exitFullscreen();
}

power.addEventListener("click", turnOn);
document.addEventListener("fullscreenchange", () => { if (!document.fullscreenElement) reset(); });
document.addEventListener("keydown", e => { if (e.key === "Escape") reset(); });
</script>
</body>
</html>
"""

html = (HTML
        .replace("__IMGS__", json.dumps(custom_imgs))
        .replace("__SND__", json.dumps(custom_snd))
        .replace("__STATIC_MS__", str(static_ms))
        .replace("__FRAME_MS__", str(frame_ms))
        .replace("__BOOST__", str(boost)))

components.html(html, height=760, scrolling=False)

import base64

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Televisor", page_icon="📺", layout="wide",
                   initial_sidebar_state="collapsed")

# Ocultar el "chrome" de Streamlit para que solo se vea el televisor
st.markdown("""
<style>
#MainMenu, footer {visibility: hidden;}
header {background: transparent !important;}
.block-container {padding: 0 !important; max-width: 100% !important;}
.stApp {background: #14110e;}
iframe {display: block;}
</style>
""", unsafe_allow_html=True)

# Configuración opcional (barra lateral, oculta por defecto)
with st.sidebar:
    st.header("Configurar el susto")
    img_file = st.file_uploader("Imagen del screamer (opcional)",
                                type=["png", "jpg", "jpeg", "gif", "webp"])
    snd_file = st.file_uploader("Sonido del screamer (opcional)",
                                type=["mp3", "wav", "ogg"])
    static_ms = st.slider("Duración de la estática antes del susto (ms)",
                          300, 5000, 1600, 100)
    boost = st.slider("Amplificación digital del sonido", 1.0, 6.0, 4.0, 0.5)


def to_data_uri(f):
    if f is None:
        return ""
    return f"data:{f.type};base64,{base64.b64encode(f.getvalue()).decode()}"


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
    background: linear-gradient(#cfcfcf, #6d6d6d); border-radius: 3px; transform-origin: bottom center;
  }
  .antenna::before { transform: rotate(-32deg); }
  .antenna::after  { transform: rotate(28deg); }
  .antenna-base { position: absolute; top: -26px; left: 50%; transform: translateX(-50%);
    width: 90px; height: 30px; border-radius: 45px 45px 6px 6px;
    background: radial-gradient(circle at 40% 30%, #4a4440, #1d1a18); }

  .tv {
    position: relative; display: flex; gap: 26px;
    width: min(780px, 92vw); padding: 30px;
    background:
      repeating-linear-gradient(92deg, rgba(0,0,0,.10) 0 3px, transparent 3px 11px),
      linear-gradient(180deg, #7a4a26, #5a3216 60%, #3f220e);
    border-radius: 26px;
    box-shadow: inset 0 2px 0 rgba(255,220,180,.25), inset 0 -6px 14px rgba(0,0,0,.5),
                0 30px 60px rgba(0,0,0,.7);
  }
  .bezel {
    flex: 1; padding: 18px; border-radius: 22px;
    background: linear-gradient(145deg, #2b2724, #0f0d0c);
    box-shadow: inset 0 0 0 3px #1a1715, inset 0 4px 10px rgba(0,0,0,.8);
  }
  .screen {
    position: relative; aspect-ratio: 4 / 3; border-radius: 38px / 30px; overflow: hidden;
    background: radial-gradient(ellipse at 50% 45%, #2a302c 0%, #141816 60%, #070808 100%);
    box-shadow: inset 0 0 40px rgba(0,0,0,.95), inset 0 0 6px rgba(0,0,0,1);
  }
  .screen::after { /* reflejo del vidrio */
    content: ""; position: absolute; inset: 0; pointer-events: none;
    background: linear-gradient(130deg, rgba(255,255,255,.10) 0%, rgba(255,255,255,0) 35%),
                radial-gradient(ellipse at 30% 20%, rgba(255,255,255,.07), transparent 50%);
  }

  .panel {
    width: 130px; display: flex; flex-direction: column; align-items: center; gap: 22px;
    padding: 18px 0; border-radius: 14px;
    background: linear-gradient(180deg, #c9b48a, #9c8660);
    box-shadow: inset 0 2px 0 rgba(255,255,255,.35), inset 0 -3px 8px rgba(0,0,0,.35);
  }
  .brand { font-style: italic; font-size: 17px; color: #3a2a14; letter-spacing: .5px; }
  .knob {
    width: 64px; height: 64px; border-radius: 50%; position: relative;
    background: radial-gradient(circle at 35% 30%, #5a524b, #1c1917 70%);
    box-shadow: 0 4px 8px rgba(0,0,0,.5), inset 0 0 0 4px #2a2522;
  }
  .knob::after { content: ""; position: absolute; top: 6px; left: 50%; width: 4px; height: 18px;
    margin-left: -2px; background: #d8cbb0; border-radius: 2px; }
  .knob.b { transform: rotate(130deg); width: 52px; height: 52px; }
  .grill { width: 90px; height: 60px; border-radius: 6px;
    background: repeating-linear-gradient(0deg, #3a2d1c 0 3px, #9c8660 3px 7px); opacity: .8; }

  .power-wrap { display: flex; flex-direction: column; align-items: center; gap: 8px; }
  .led { width: 9px; height: 9px; border-radius: 50%; background: #3b1010; box-shadow: inset 0 0 2px #000; }
  .led.on { background: #ff3b2f; box-shadow: 0 0 10px #ff3b2f; }
  .power {
    width: 54px; height: 54px; border-radius: 50%; border: none; cursor: pointer;
    background: radial-gradient(circle at 40% 35%, #e9e2d4, #9b9282);
    box-shadow: 0 5px 0 #5c564c, 0 8px 14px rgba(0,0,0,.5);
    font-size: 22px; color: #3a3530; transition: transform .08s, box-shadow .08s;
  }
  .power:active { transform: translateY(4px); box-shadow: 0 1px 0 #5c564c, 0 3px 6px rgba(0,0,0,.5); }
  .power:focus-visible { outline: 3px solid #ffd27a; outline-offset: 4px; }
  .hint { font-size: 12px; color: #3a2a14; }

  .legs { display: flex; justify-content: space-between; width: min(640px, 76vw); }
  .legs span { width: 14px; height: 46px; background: linear-gradient(#4a2a12, #2a170a);
    border-radius: 0 0 6px 6px; }
  .legs span:first-child { transform: skewX(12deg); }
  .legs span:last-child  { transform: skewX(-12deg); }

  /* ---------- Capa del susto (pantalla completa) ---------- */
  #overlay { position: fixed; inset: 0; z-index: 9999; background: #000; display: none; }
  #overlay.show { display: block; }
  #noise { width: 100%; height: 100%; image-rendering: pixelated; display: block; }
  #turnon { position: absolute; left: 0; right: 0; top: 50%; height: 2px; background: #fff;
    box-shadow: 0 0 30px #fff; transform: scaleX(0); }
  #turnon.go { animation: crt .45s ease-out forwards; }
  @keyframes crt {
    0% { transform: scaleX(0); height: 2px; }
    50% { transform: scaleX(1); height: 2px; }
    100% { transform: scaleX(1); height: 100vh; top: 0; opacity: 0; }
  }
  .scanlines { position: absolute; inset: 0; pointer-events: none;
    background: repeating-linear-gradient(0deg, rgba(0,0,0,.35) 0 2px, transparent 2px 4px); }

  #scare { position: absolute; inset: 0; display: none; align-items: center; justify-content: center;
    background: #000; overflow: hidden; }
  #scare.show { display: flex; animation: flash .09s steps(2) infinite; }
  #scare .face { width: 100vw; height: 100vh; object-fit: cover;
    animation: lunge .18s ease-out forwards, shake .06s linear .18s infinite; }
  #scare::after { content: ""; position: absolute; inset: 0; pointer-events: none;
    background: radial-gradient(ellipse at center, transparent 40%, rgba(160,0,0,.75) 100%); }
  @keyframes lunge { from { transform: scale(.35); } to { transform: scale(1.12); } }
  @keyframes shake {
    0% { transform: scale(1.12) translate(0,0); }
    25% { transform: scale(1.14) translate(-14px, 9px); }
    50% { transform: scale(1.12) translate(12px,-11px); }
    75% { transform: scale(1.15) translate(-9px,-7px); }
    100% { transform: scale(1.12) translate(10px, 12px); }
  }
  @keyframes flash {
    0% { filter: contrast(1.6) brightness(1.1); }
    100% { filter: contrast(2.2) brightness(.8) invert(.12) hue-rotate(-15deg); }
  }
  #exitHint { position: absolute; bottom: 14px; width: 100%; text-align: center;
    color: rgba(255,255,255,.35); font: 13px sans-serif; display: none; }

  @media (max-width: 600px) {
    .tv { flex-direction: column; padding: 18px; }
    .panel { width: 100%; flex-direction: row; justify-content: space-around; padding: 12px; }
    .grill { display: none; }
  }
</style>
</head>
<body>

<div class="stage">
  <div class="antenna"></div>
  <div class="antenna-base"></div>
  <div class="tv">
    <div class="bezel"><div class="screen"></div></div>
    <div class="panel">
      <div class="brand">Radiola</div>
      <div class="knob"></div>
      <div class="knob b"></div>
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
  <canvas id="noise" width="200" height="150"></canvas>
  <div id="turnon"></div>
  <div id="scare"></div>
  <div class="scanlines"></div>
  <div id="exitHint">Presiona Esc para apagar</div>
</div>

<script>
const CUSTOM_IMG = "__IMG__";
const CUSTOM_SND = "__SND__";
const STATIC_MS  = __STATIC_MS__;
const BOOST      = __BOOST__;

// Cara original por defecto (SVG)
const FACE_SVG = `data:image/svg+xml;utf8,` + encodeURIComponent(`
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" preserveAspectRatio="xMidYMid slice">
  <rect width="400" height="300" fill="#050505"/>
  <defs>
    <radialGradient id="skin" cx="50%" cy="40%" r="60%">
      <stop offset="0" stop-color="#d9d6cc"/><stop offset=".7" stop-color="#8d887c"/>
      <stop offset="1" stop-color="#2a2824"/>
    </radialGradient>
  </defs>
  <ellipse cx="200" cy="160" rx="120" ry="160" fill="url(#skin)"/>
  <ellipse cx="150" cy="120" rx="34" ry="44" fill="#000"/>
  <ellipse cx="250" cy="120" rx="34" ry="44" fill="#000"/>
  <circle cx="155" cy="125" r="4" fill="#fff"/>
  <circle cx="245" cy="125" r="4" fill="#fff"/>
  <path d="M150 85 Q120 60 100 80" stroke="#1b1916" stroke-width="5" fill="none"/>
  <path d="M250 85 Q280 60 300 80" stroke="#1b1916" stroke-width="5" fill="none"/>
  <path d="M195 150 L188 185 L205 185 Z" fill="#4a463f"/>
  <ellipse cx="200" cy="245" rx="70" ry="80" fill="#000"/>
  <path d="M132 210 L145 232 L157 208 L170 232 L183 206 L196 232 L209 206 L222 232 L235 208 L248 232 L262 210 Z" fill="#e8e2c8"/>
  <path d="M140 300 L152 278 L165 300 L178 276 L191 300 L204 276 L217 300 L230 278 L243 300 L256 280 L262 300 Z" fill="#e8e2c8"/>
  <path d="M110 60 L130 140 M300 70 L270 150 M200 20 L195 70" stroke="#3a0000" stroke-width="2" opacity=".6"/>
</svg>`);

const power   = document.getElementById("power");
const led     = document.getElementById("led");
const overlay = document.getElementById("overlay");
const canvas  = document.getElementById("noise");
const turnon  = document.getElementById("turnon");
const scare   = document.getElementById("scare");
const exitHint= document.getElementById("exitHint");
const cctx    = canvas.getContext("2d");

let ac = null, master = null, staticSrc = null, customAudio = null, rafId = null;
let timers = [], active = false, savedFrameStyle = null;

// ---------- Pantalla completa ----------
function goFullscreen() {
  const el = document.documentElement;
  const req = el.requestFullscreen || el.webkitRequestFullscreen || el.msRequestFullscreen;
  let p = null;
  try { if (req) p = req.call(el); } catch (e) {}
  // Respaldo: estirar el iframe de Streamlit sobre toda la ventana
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
  try { if (window.frameElement && savedFrameStyle !== null)
          window.frameElement.setAttribute("style", savedFrameStyle); } catch (e) {}
  savedFrameStyle = null;
}

// ---------- Audio ----------
function setupAudio() {
  ac = new (window.AudioContext || window.webkitAudioContext)();
  ac.resume();
  const comp = ac.createDynamicsCompressor();      // limita para que suene fuerte sin romperse
  comp.threshold.value = -24; comp.knee.value = 0; comp.ratio.value = 20;
  comp.attack.value = 0.001; comp.release.value = 0.1;
  master = ac.createGain(); master.gain.value = 1.0; // volumen máximo de la página
  comp.connect(master); master.connect(ac.destination);
  return comp;
}
let bus = null;

function noiseBuffer(sec) {
  const b = ac.createBuffer(1, ac.sampleRate * sec, ac.sampleRate);
  const d = b.getChannelData(0);
  for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  return b;
}

function playStatic() {
  staticSrc = ac.createBufferSource();
  staticSrc.buffer = noiseBuffer(2); staticSrc.loop = true;
  const g = ac.createGain(); g.gain.value = 0.35;
  staticSrc.connect(g); g.connect(bus); staticSrc.start();
}
function stopStatic() { try { staticSrc && staticSrc.stop(); } catch (e) {} staticSrc = null; }

function distortionCurve(k) {
  const n = 2048, c = new Float32Array(n);
  for (let i = 0; i < n; i++) { const x = i * 2 / n - 1;
    c[i] = (3 + k) * x * 20 * Math.PI / 180 / (Math.PI + k * Math.abs(x)); }
  return c;
}

function playSynthScream() {
  const now = ac.currentTime, dur = 3.4;
  const pre = ac.createGain(); pre.gain.value = BOOST;
  const shaper = ac.createWaveShaper(); shaper.curve = distortionCurve(300);
  const env = ac.createGain();
  env.gain.setValueAtTime(0, now);
  env.gain.linearRampToValueAtTime(1, now + 0.015);
  env.gain.setValueAtTime(1, now + dur - 0.4);
  env.gain.linearRampToValueAtTime(0, now + dur);
  pre.connect(shaper); shaper.connect(env); env.connect(bus);

  [1, 1.48, 2.03, 0.51, 2.97].forEach((m, i) => {
    const o = ac.createOscillator(); o.type = "sawtooth";
    o.frequency.setValueAtTime(320 * m, now);
    o.frequency.exponentialRampToValueAtTime(1150 * m, now + 0.22);
    o.frequency.exponentialRampToValueAtTime(760 * m, now + dur);
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

function prepareCustomAudio() {
  if (!CUSTOM_SND) return;
  customAudio = new Audio(CUSTOM_SND);
  customAudio.volume = 1.0;
  const src = ac.createMediaElementSource(customAudio);
  const g = ac.createGain(); g.gain.value = BOOST;
  src.connect(g); g.connect(bus);
  // "desbloquear" la reproducción dentro del clic del usuario
  customAudio.muted = true;
  customAudio.play().then(() => { customAudio.pause(); customAudio.currentTime = 0;
                                   customAudio.muted = false; }).catch(() => {});
}

// ---------- Estática visual ----------
function drawNoise() {
  const img = cctx.createImageData(canvas.width, canvas.height);
  const d = img.data;
  for (let i = 0; i < d.length; i += 4) {
    const v = Math.random() * 255 | 0;
    d[i] = d[i + 1] = d[i + 2] = v; d[i + 3] = 255;
  }
  cctx.putImageData(img, 0, 0);
  rafId = requestAnimationFrame(drawNoise);
}

// ---------- Secuencia ----------
function turnOn() {
  if (active) return;
  active = true;
  led.classList.add("on");

  // Todo lo que requiere gesto del usuario va aquí, sincrónicamente
  goFullscreen();
  bus = setupAudio();
  prepareCustomAudio();

  overlay.classList.add("show");
  turnon.classList.remove("go"); void turnon.offsetWidth; turnon.classList.add("go");
  drawNoise();
  playStatic();

  timers.push(setTimeout(showScare, STATIC_MS));
}

function showScare() {
  cancelAnimationFrame(rafId);
  stopStatic();
  master.gain.value = 1.0;
  scare.innerHTML = "";
  const img = document.createElement("img");
  img.className = "face";
  img.src = CUSTOM_IMG || FACE_SVG;
  img.alt = "";
  scare.appendChild(img);
  scare.classList.add("show");

  if (customAudio) {
    customAudio.currentTime = 0; customAudio.volume = 1.0; customAudio.muted = false;
    customAudio.play().catch(playSynthScream);
  } else {
    playSynthScream();
  }
  timers.push(setTimeout(() => { exitHint.style.display = "block"; }, 3500));
}

function reset() {
  if (!active) return;
  active = false;
  timers.forEach(clearTimeout); timers = [];
  cancelAnimationFrame(rafId);
  stopStatic();
  if (customAudio) { try { customAudio.pause(); } catch (e) {} customAudio = null; }
  if (ac) { try { ac.close(); } catch (e) {} ac = null; }
  scare.classList.remove("show"); scare.innerHTML = "";
  overlay.classList.remove("show");
  exitHint.style.display = "none";
  led.classList.remove("on");
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
        .replace("__IMG__", to_data_uri(img_file))
        .replace("__SND__", to_data_uri(snd_file))
        .replace("__STATIC_MS__", str(static_ms))
        .replace("__BOOST__", str(boost)))

components.html(html, height=760, scrolling=False)

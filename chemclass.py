# =====================================================================
# 📚 DASHBOARD BELAJAR - KIMIA ASAM BASA
# Versi: 2.0 (Fixed + Enhanced)
# =====================================================================

import streamlit as st
import time
import math
import pandas as pd
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────
# KONFIGURASI HALAMAN  ← hanya boleh dipanggil SEKALI di paling atas
# ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Belajar Kimia",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────
# SESSION STATE  ← inisialisasi sekali
# ─────────────────────────────────────────────────────────────────────
for key, default in {
    "theme": "Dark",
    "tasks": [],
    "timer_running": False,
    "time_left": 25 * 60,
    "selected_menu": "🏠 Dashboard",
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ─────────────────────────────────────────────────────────────────────
# DATA: INDIKATOR
# ─────────────────────────────────────────────────────────────────────
INDICATORS = {
    "lakmus":    {"name": "Kertas Lakmus",         "range": (4.5, 8.3),  "low": "#ef4444", "low_lbl": "MERAH – Asam",        "high": "#3b82f6", "high_lbl": "BIRU – Basa",         "mid": "#a855f7", "mid_lbl": "UNGU – Transisi"},
    "pp":        {"name": "Fenolftalein (PP)",      "range": (8.2, 10.0), "low": "#f1f5f9", "low_lbl": "TAK BERWARNA – Asam", "high": "#ec4899", "high_lbl": "MERAH MUDA – Basa",   "mid": "#fbcfe8", "mid_lbl": "MERAH MUDA PUCAT"},
    "btb":       {"name": "Bromothymol Blue (BTB)", "range": (6.0, 7.6),  "low": "#eab308", "low_lbl": "KUNING – Asam",       "high": "#1d4ed8", "high_lbl": "BIRU – Basa",         "mid": "#22c55e", "mid_lbl": "HIJAU – Netral"},
    "mr":        {"name": "Metil Merah",            "range": (4.4, 6.2),  "low": "#dc2626", "low_lbl": "MERAH – Asam",        "high": "#ca8a04", "high_lbl": "KUNING – Basa",       "mid": "#f97316", "mid_lbl": "JINGGA – Transisi"},
    "mo":        {"name": "Metil Oranye",           "range": (3.1, 4.4),  "low": "#f97316", "low_lbl": "MERAH-ORANYE – Asam", "high": "#facc15", "high_lbl": "KUNING – Basa",       "mid": "#fb923c", "mid_lbl": "ORANYE – Transisi"},
    "universal": {"name": "Indikator Universal",    "range": (0.0, 14.0), "low": "#dc2626", "low_lbl": "MERAH – Sangat Asam", "high": "#581c87", "high_lbl": "UNGU – Sangat Basa",  "mid": "#16a34a", "mid_lbl": "HIJAU – Netral"},
}

# ─────────────────────────────────────────────────────────────────────
# DATA: ZAT KIMIA
# ─────────────────────────────────────────────────────────────────────
CHEMICALS = [
    {"name":"HCl (Asam Klorida)",       "formula":"HCl",        "pH":1.0,  "type":"asam",   "cat":"Laboratorium",  "desc":"Asam kuat pembersih porselen",          "dis":"HCl → H⁺ + Cl⁻"},
    {"name":"H₂SO₄ (Asam Sulfat)",      "formula":"H₂SO₄",      "pH":1.5,  "type":"asam",   "cat":"Laboratorium",  "desc":"Air aki kendaraan",                     "dis":"H₂SO₄ → 2H⁺ + SO₄²⁻"},
    {"name":"HNO₃ (Asam Nitrat)",       "formula":"HNO₃",       "pH":1.0,  "type":"asam",   "cat":"Laboratorium",  "desc":"Oksidator kuat, pelarut logam",         "dis":"HNO₃ → H⁺ + NO₃⁻"},
    {"name":"CH₃COOH (Cuka)",           "formula":"CH₃COOH",    "pH":3.0,  "type":"asam",   "cat":"Sehari-hari",   "desc":"Cuka dapur 5%",                         "dis":"CH₃COOH ⇌ H⁺ + CH₃COO⁻"},
    {"name":"C₆H₈O₇ (Asam Sitrat)",    "formula":"C₆H₈O₇",     "pH":2.2,  "type":"asam",   "cat":"Sehari-hari",   "desc":"Sari jeruk lemon",                      "dis":"C₆H₈O₇ ⇌ 3H⁺ + C₆H₅O₇³⁻"},
    {"name":"HF (Asam Fluorida)",       "formula":"HF",         "pH":3.2,  "type":"asam",   "cat":"Laboratorium",  "desc":"Pelarut silika dan kaca",               "dis":"HF ⇌ H⁺ + F⁻"},
    {"name":"H₂CO₃ (Asam Karbonat)",   "formula":"H₂CO₃",      "pH":4.6,  "type":"asam",   "cat":"Sehari-hari",   "desc":"Soda berkarbonasi",                     "dis":"H₂CO₃ ⇌ 2H⁺ + CO₃²⁻"},
    {"name":"H₂O (Air Murni)",          "formula":"H₂O",        "pH":7.0,  "type":"netral", "cat":"Sehari-hari",   "desc":"Air suling / Aquades",                  "dis":"H₂O ⇌ H⁺ + OH⁻"},
    {"name":"NaCl (Garam Dapur)",       "formula":"NaCl",       "pH":7.0,  "type":"netral", "cat":"Sehari-hari",   "desc":"Garam dapur biasa",                     "dis":"NaCl → Na⁺ + Cl⁻"},
    {"name":"NaHCO₃ (Soda Kue)",       "formula":"NaHCO₃",     "pH":8.3,  "type":"basa",   "cat":"Sehari-hari",   "desc":"Pengembang roti",                       "dis":"NaHCO₃ → Na⁺ + HCO₃⁻"},
    {"name":"Na₂CO₃ (Soda Abu)",       "formula":"Na₂CO₃",     "pH":11.6, "type":"basa",   "cat":"Standar Primer","desc":"Standarisasi larutan asam",             "dis":"Na₂CO₃ → 2Na⁺ + CO₃²⁻"},
    {"name":"NH₃ (Amonia)",             "formula":"NH₃",        "pH":11.1, "type":"basa",   "cat":"Laboratorium",  "desc":"Basa lemah berbau tajam",               "dis":"NH₃ + H₂O ⇌ NH₄⁺ + OH⁻"},
    {"name":"Ca(OH)₂ (Air Kapur)",     "formula":"Ca(OH)₂",    "pH":11.5, "type":"basa",   "cat":"Laboratorium",  "desc":"Air kapur sirih",                       "dis":"Ca(OH)₂ → Ca²⁺ + 2OH⁻"},
    {"name":"NaOH (Soda Api)",         "formula":"NaOH",       "pH":13.0, "type":"basa",   "cat":"Laboratorium",  "desc":"Basa kuat",                             "dis":"NaOH → Na⁺ + OH⁻"},
    {"name":"KOH (Kalium Hidroksida)", "formula":"KOH",        "pH":13.0, "type":"basa",   "cat":"Laboratorium",  "desc":"Basa kuat reaksi penyabunan",           "dis":"KOH → K⁺ + OH⁻"},
    {"name":"Mg(OH)₂ (Susu Magnesia)","formula":"Mg(OH)₂",    "pH":10.5, "type":"basa",   "cat":"Farmasi",       "desc":"Antasida obat maag",                    "dis":"Mg(OH)₂ ⇌ Mg²⁺ + 2OH⁻"},
    {"name":"KMnO₄ (Kalium Perm.)",   "formula":"KMnO₄",      "pH":7.5,  "type":"netral", "cat":"Permanganometri","desc":"Oksidator kuat autoindikator",          "dis":"KMnO₄ → K⁺ + MnO₄⁻"},
    {"name":"CuSO₄ (Tembaga Sulfat)", "formula":"CuSO₄",      "pH":4.0,  "type":"asam",   "cat":"Analisis",      "desc":"Reagen biuret untuk protein",           "dis":"CuSO₄ → Cu²⁺ + SO₄²⁻"},
    {"name":"AgNO₃ (Perak Nitrat)",   "formula":"AgNO₃",      "pH":5.5,  "type":"asam",   "cat":"Argentometri",  "desc":"Titran penentuan klorida",              "dis":"AgNO₃ → Ag⁺ + NO₃⁻"},
    {"name":"KHP (Standar Primer)",   "formula":"KHC₈H₄O₄",   "pH":4.0,  "type":"asam",   "cat":"Standar Primer","desc":"Standarisasi larutan NaOH",             "dis":"KHC₈H₄O₄ → K⁺ + HC₈H₄O₄⁻"},
]

MUSIK = {
    "🎵 Lo-Fi Chill": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    "🌊 Ambient Nature": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
    "🌙 Piano Relaksasi": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
    "⚡ Deep Focus": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
    "☕ Coffee Shop": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3",
}

# ─────────────────────────────────────────────────────────────────────
# FUNGSI UTILITAS
# ─────────────────────────────────────────────────────────────────────
def warna_indikator(ph: float, ind: dict) -> str:
    lo, hi = ind["range"]
    if ind["name"] == "Indikator Universal":
        if ph < 3:   return "#dc2626"
        elif ph < 5: return "#f97316"
        elif ph < 6.5: return "#eab308"
        elif ph < 7.5: return "#16a34a"
        elif ph < 9:   return "#0284c7"
        elif ph < 11:  return "#1d4ed8"
        else:          return "#581c87"
    if ph < lo:  return ind["low"]
    if ph > hi:  return ind["high"]
    return ind["mid"]

def label_indikator(ph: float, ind: dict) -> str:
    lo, hi = ind["range"]
    if ph < lo:  return ind["low_lbl"]
    if ph > hi:  return ind["high_lbl"]
    return ind["mid_lbl"]

def klasifikasi(ph: float):
    if ph < 7: return "ASAM", "#ef4444"
    if ph > 7: return "BASA", "#3b82f6"
    return "NETRAL", "#22c55e"

def hitung_ph(jenis: str, konsentrasi: float) -> tuple[float, str]:
    c = max(konsentrasi, 1e-15)
    if jenis == "Asam Kuat (HCl, H₂SO₄, HNO₃)":
        ph = -math.log10(c)
        rumus = f"pH = −log[H⁺] = −log({c:.4f}) = **{ph:.2f}**"
    elif jenis == "Basa Kuat (NaOH, KOH)":
        poh = -math.log10(c)
        ph = 14 - poh
        rumus = f"pOH = −log[OH⁻] = −log({c:.4f}) = {poh:.2f} → pH = 14 − {poh:.2f} = **{ph:.2f}**"
    elif jenis == "Asam Lemah (CH₃COOH) Ka=1.8×10⁻⁵":
        Ka = 1.8e-5
        H = math.sqrt(Ka * c)
        ph = -math.log10(H)
        rumus = f"[H⁺] = √(Ka×C) = √(1.8×10⁻⁵ × {c:.4f}) = {H:.2e} → pH = **{ph:.2f}**"
    elif jenis == "Basa Lemah (NH₃) Kb=1.8×10⁻⁵":
        Kb = 1.8e-5
        OH = math.sqrt(Kb * c)
        poh = -math.log10(OH)
        ph = 14 - poh
        rumus = f"[OH⁻] = √(Kb×C) = {OH:.2e} → pOH = {poh:.2f} → pH = **{ph:.2f}**"
    else:
        ph = 7.0
        rumus = "pH = 7.00 (larutan netral)"
    return round(max(0.0, min(14.0, ph)), 2), rumus

def add_task(name):
    if name.strip():
        st.session_state.tasks.append({"name": name.strip(), "done": False, "ts": datetime.now().strftime("%H:%M")})

def toggle_task(i):
    st.session_state.tasks[i]["done"] = not st.session_state.tasks[i]["done"]

def del_task(i):
    st.session_state.tasks.pop(i)


# ─────────────────────────────────────────────────────────────────────
# CSS TEMA
# ─────────────────────────────────────────────────────────────────────
def apply_theme():
    is_dark = st.session_state.theme == "Dark"
    bg     = "#0f0f1a" if is_dark else "#f0f4f8"
    sbg    = "#1a1a2e" if is_dark else "#e2e8f0"
    txt    = "#e2e8f0" if is_dark else "#1e293b"
    card   = "rgba(255,255,255,0.05)" if is_dark else "rgba(0,0,0,0.04)"
    border = "rgba(255,255,255,0.1)"  if is_dark else "rgba(0,0,0,0.1)"
    inp    = "#16213e" if is_dark else "#ffffff"
    btn    = "#7c3aed" if is_dark else "#3b82f6"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Outfit:wght@300;400;600;800&display=swap');

    html, body, [class*="css"] {{ font-family: 'Outfit', sans-serif; }}
    .stApp {{ background-color: {bg}; }}
    h1,h2,h3,h4,h5,h6,p,label,span,div {{ color: {txt} !important; }}
    section[data-testid="stSidebar"] {{ background-color: {sbg}; }}
    .stTextInput>div>div>input, .stNumberInput>div>div>input {{
        background-color: {inp} !important; color: {txt} !important;
        border: 1px solid {border} !important; border-radius: 8px !important;
    }}
    .stSelectbox>div>div>div {{ background-color: {inp} !important; color: {txt} !important; }}
    .stButton>button {{
        background: linear-gradient(135deg, {btn}, #06b6d4) !important;
        color: white !important; border: none !important; border-radius: 10px !important;
        font-family: 'Outfit', sans-serif !important; font-weight: 600 !important;
        transition: transform 0.2s, box-shadow 0.2s !important;
    }}
    .stButton>button:hover {{ transform: translateY(-2px) !important; box-shadow: 0 6px 20px rgba(124,58,237,0.4) !important; }}
    .stProgress>div>div>div {{ background: linear-gradient(90deg,{btn},#06b6d4) !important; }}
    .stAlert {{ background-color: {card} !important; color: {txt} !important; border-radius: 10px !important; }}
    .streamlit-expanderHeader {{ background-color: {card} !important; border-radius: 10px !important; }}
    hr {{ border-color: {border} !important; }}

    /* Custom card class */
    .ccard {{
        background: {card}; border: 1px solid {border};
        border-radius: 16px; padding: 1.2rem 1.5rem; margin-bottom: 0.8rem;
    }}
    .mono {{ font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; }}
    .badge {{
        display: inline-block; padding: 3px 12px; border-radius: 999px;
        font-size: 0.75rem; font-weight: 700; font-family: 'JetBrains Mono', monospace;
    }}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Pengaturan")
    tema = st.radio("🎨 Tema:", ["Dark", "Light"],
                    index=0 if st.session_state.theme == "Dark" else 1,
                    horizontal=True)
    st.session_state.theme = tema
    apply_theme()   # terapkan tema SETELAH diset

    st.markdown("---")
    st.markdown("## 📚 Menu")
    MENUS = ["🏠 Dashboard", "✅ To-Do List", "⏱️ Timer Belajar",
             "🎵 Musik Fokus", "🧪 Simulasi Indikator", "🧮 Kalkulator pH"]
    selected_menu = st.radio("", MENUS, label_visibility="collapsed")


# ─────────────────────────────────────────────────────────────────────
# ███  1. DASHBOARD
# ─────────────────────────────────────────────────────────────────────
if selected_menu == "🏠 Dashboard":
    st.markdown("# 📚 Dashboard Belajar Kimia")
    st.markdown("Selamat datang! Pilih menu di sidebar untuk memulai sesi belajar.")

    c1, c2, c3, c4 = st.columns(4)
    total   = len(st.session_state.tasks)
    selesai = sum(1 for t in st.session_state.tasks if t["done"])
    pending = total - selesai
    persen  = int(selesai / total * 100) if total else 0

    c1.metric("📝 Total Tugas",   total)
    c2.metric("⏳ Tertunda",       pending)
    c3.metric("✅ Selesai",        selesai)
    c4.metric("📊 Progress",       f"{persen}%")

    if total:
        st.progress(persen / 100)

    st.markdown("---")
    st.info("💡 **Tip Pomodoro:** 25 menit belajar fokus → 5 menit istirahat. Ulangi 4 kali, lalu istirahat 15 menit.")

    st.markdown("### 🗺️ Menu yang Tersedia")
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("""
        <div class="ccard">
          <b>✅ To-Do List</b><br><span class="mono">Catat & kelola tugas harian mu</span>
        </div>
        <div class="ccard">
          <b>⏱️ Timer Belajar</b><br><span class="mono">Pomodoro timer interaktif</span>
        </div>
        <div class="ccard">
          <b>🎵 Musik Fokus</b><br><span class="mono">Putar musik belajar lo-fi</span>
        </div>
        """, unsafe_allow_html=True)
    with col_b:
        st.markdown("""
        <div class="ccard">
          <b>🧪 Simulasi Indikator</b><br><span class="mono">Lihat perubahan warna larutan</span>
        </div>
        <div class="ccard">
          <b>🧮 Kalkulator pH</b><br><span class="mono">Hitung pH dari konsentrasi</span>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# ███  2. TO-DO LIST
# ─────────────────────────────────────────────────────────────────────
elif selected_menu == "✅ To-Do List":
    st.markdown("# ✅ To-Do List Harian")

    ci1, ci2 = st.columns([5, 1])
    with ci1:
        new_task = st.text_input("Tambah tugas:", placeholder="Contoh: Baca bab 3 Kimia Kelas XI")
    with ci2:
        st.write("")
        if st.button("➕ Tambah", type="primary"):
            add_task(new_task)
            st.rerun()

    st.markdown("---")
    if not st.session_state.tasks:
        st.warning("📭 Belum ada tugas. Tambahkan di atas!")
    else:
        total_t = len(st.session_state.tasks)
        done_t  = sum(1 for t in st.session_state.tasks if t["done"])
        st.progress(done_t / total_t, text=f"Progress: {done_t}/{total_t} selesai")
        st.markdown("")

        for i, task in enumerate(st.session_state.tasks):
            cc1, cc2, cc3 = st.columns([0.5, 7, 1])
            with cc1:
                st.checkbox("", value=task["done"], key=f"chk_{i}", on_change=toggle_task, args=(i,))
            with cc2:
                style = "~~" if task["done"] else "**"
                end   = "~~ ✅" if task["done"] else "**"
                st.markdown(f"{style}{task['name']}{end}")
                st.caption(f"Ditambahkan pukul {task['ts']}")
            with cc3:
                if st.button("🗑️", key=f"del_{i}"):
                    del_task(i)
                    st.rerun()
            st.markdown("---")


# ─────────────────────────────────────────────────────────────────────
# ███  3. TIMER BELAJAR
# ─────────────────────────────────────────────────────────────────────
elif selected_menu == "⏱️ Timer Belajar":
    st.markdown("# ⏱️ Timer Belajar — Teknik Pomodoro")

    ct1, ct2 = st.columns(2)
    with ct1:
        st.markdown("### ⚙️ Pengaturan")
        mode = st.selectbox("Mode:", ["🍅 25 menit – Belajar", "☕ 5 menit – Istirahat", "🛌 15 menit – Istirahat Panjang"])
        default_map = {"🍅 25 menit – Belajar": 25*60, "☕ 5 menit – Istirahat": 5*60, "🛌 15 menit – Istirahat Panjang": 15*60}
        default_time = default_map[mode]

        if st.button("🔄 Reset Timer"):
            st.session_state.time_left = default_time
            st.session_state.timer_running = False
            st.rerun()

        st.markdown("---")
        ck1, ck2 = st.columns(2)
        with ck1:
            if st.button("▶️ Mulai", type="primary"):
                st.session_state.time_left = st.session_state.time_left or default_time
                st.session_state.timer_running = True
                st.rerun()
        with ck2:
            if st.button("⏹️ Stop"):
                st.session_state.timer_running = False
                st.rerun()

    with ct2:
        menit = st.session_state.time_left // 60
        detik = st.session_state.time_left % 60
        wkt = f"{menit:02d}:{detik:02d}"

        if menit <= 5:   clr, sts = "#ef4444", "🔴 Hampir Selesai!"
        elif menit <= 10: clr, sts = "#f59e0b", "🟡 Tetap Fokus"
        else:             clr, sts = "#22c55e", "🟢 Fokus Penuh"

        st.markdown(f"""
        <div style="text-align:center; padding:40px 20px; background:rgba(0,0,0,0.2);
             border-radius:24px; border:2px solid {clr}33;">
          <div style="font-family:'JetBrains Mono',monospace; font-size:5rem;
               font-weight:700; color:{clr}; line-height:1; text-shadow:0 0 30px {clr}88;">{wkt}</div>
          <div style="font-size:1.1rem; margin-top:1rem; font-weight:600;">{sts}</div>
        </div>
        """, unsafe_allow_html=True)

        pct = st.session_state.time_left / default_time
        st.progress(max(0.0, min(1.0, pct)))

    if st.session_state.timer_running:
        if st.session_state.time_left > 0:
            time.sleep(1)
            st.session_state.time_left -= 1
            st.rerun()
        else:
            st.session_state.timer_running = False
            st.balloons()
            st.success("⏰ Waktu selesai! Saatnya istirahat 🎉")


# ─────────────────────────────────────────────────────────────────────
# ███  4. MUSIK FOKUS
# ─────────────────────────────────────────────────────────────────────
elif selected_menu == "🎵 Musik Fokus":
    st.markdown("# 🎵 Musik Fokus")
    st.markdown("Pilih musik latar untuk menemani sesi belajarmu.")

    pilihan = st.selectbox("🎧 Pilih Trek:", list(MUSIK.keys()))
    st.audio(MUSIK[pilihan], format="audio/mp3")

    st.markdown("---")
    st.markdown("""
    <div class="ccard">
      <b>💡 Tips Musik Belajar</b><br>
      <span class="mono">
      • Lo-Fi → cocok untuk membaca & menulis<br>
      • Ambient Nature → cocok untuk konsentrasi dalam<br>
      • Piano → cocok untuk menghafal<br>
      • Deep Focus → cocok untuk mengerjakan soal<br>
      • Coffee Shop → cocok untuk brainstorming
      </span>
    </div>
    """, unsafe_allow_html=True)
    st.info("⚠️ Jika audio tidak muncul, coba pilih trek lain atau periksa koneksi internet.")


# ─────────────────────────────────────────────────────────────────────
# ███  5. SIMULASI INDIKATOR
# ─────────────────────────────────────────────────────────────────────
elif selected_menu == "🧪 Simulasi Indikator":
    st.markdown("# 🧪 Simulasi Indikator Asam-Basa")
    st.markdown("Pilih zat kimia dan indikator, lalu amati perubahan warna larutan.")

    col_left, col_right = st.columns([5, 7])

    with col_left:
        st.markdown("### 🔬 Parameter Simulasi")

        preset_names = [c["name"] for c in CHEMICALS]
        pilihan_zat  = st.selectbox("Pilih Zat Kimia:", preset_names, index=0)
        zat_data     = next(c for c in CHEMICALS if c["name"] == pilihan_zat)

        pilihan_ind  = st.selectbox("Pilih Indikator:",
                                    list(INDICATORS.keys()),
                                    format_func=lambda k: INDICATORS[k]["name"])
        ind_data     = INDICATORS[pilihan_ind]

        st.markdown("---")
        ph_sim = st.slider("🎚️ Atur pH Manual:", 0.0, 14.0,
                           value=float(zat_data["pH"]), step=0.1,
                           help="Geser untuk mengubah pH secara manual")

        # Info ionisasi
        kls, kls_clr = klasifikasi(ph_sim)
        st.markdown(f"""
        <div class="ccard" style="margin-top:1rem;">
          <div class="mono">
            <b>Rumus:</b> {zat_data['formula']}<br>
            <b>Kelas:</b> <span style="color:{kls_clr};font-weight:700;">{kls}</span><br>
            <b>Ionisasi:</b> {zat_data['dis']}<br>
            <b>Kategori:</b> {zat_data['cat']}<br>
            <b>Keterangan:</b> {zat_data['desc']}
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown("### 🔮 Beaker Reaktif")

        liq_color  = warna_indikator(ph_sim, ind_data)
        liq_label  = label_indikator(ph_sim, ind_data)
        H_conc     = 10 ** (-ph_sim)
        OH_conc    = 10 ** (-(14 - ph_sim))
        level_px   = int(ph_sim * 7) + 50    # ketinggian cairan 50–148 px

        st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; gap:16px;">

          <!-- Beaker -->
          <div style="position:relative; width:160px; height:200px;">

            <!-- Tabung beaker -->
            <div style="
              position:absolute; bottom:0; left:50%; transform:translateX(-50%);
              width:140px; height:180px;
              border: 3px solid rgba(200,200,255,0.35);
              border-top: none;
              border-radius: 0 0 22px 22px;
              overflow: hidden;
              background: rgba(255,255,255,0.03);
              box-shadow: inset 0 0 20px rgba(0,0,0,0.3), 0 0 20px {liq_color}44;
            ">
              <!-- Cairan -->
              <div style="
                position:absolute; bottom:0; left:0; right:0;
                height:{level_px}px;
                background: {liq_color};
                opacity: 0.85;
                border-radius: 0 0 18px 18px;
                transition: height 0.5s ease, background 0.5s ease;
                box-shadow: inset 0 6px 12px rgba(255,255,255,0.2);
              ">
                <!-- Gelembung animasi -->
                <div style="position:absolute;bottom:10px;left:25%;width:6px;height:6px;
                  background:rgba(255,255,255,0.5);border-radius:50%;
                  animation:bubble 2s infinite;"></div>
                <div style="position:absolute;bottom:20px;left:60%;width:4px;height:4px;
                  background:rgba(255,255,255,0.4);border-radius:50%;
                  animation:bubble 2.5s infinite 0.5s;"></div>
              </div>
              <!-- Skala ukur -->
              <div style="position:absolute;right:8px;top:15px;height:140px;
                display:flex;flex-direction:column;justify-content:space-between;
                font-family:'JetBrains Mono',monospace;font-size:8px;color:rgba(200,220,255,0.6);">
                <span>150ml</span><span>100ml</span><span>50ml</span>
              </div>
            </div>

            <!-- Mulut beaker -->
            <div style="
              position:absolute; top:0; left:50%; transform:translateX(-50%);
              width:152px; height:12px;
              border: 3px solid rgba(200,200,255,0.35);
              border-radius: 4px;
            "></div>
          </div>

          <!-- Nilai pH besar -->
          <div style="text-align:center;">
            <div style="font-family:'JetBrains Mono',monospace; font-size:3.2rem;
              font-weight:700; color:{liq_color}; text-shadow:0 0 20px {liq_color}99;
              line-height:1;">pH {ph_sim:.1f}</div>
            <div style="font-size:0.9rem; font-weight:600; margin-top:4px;
              color:{liq_color}; opacity:0.85;">{liq_label}</div>
          </div>
        </div>

        <style>
        @keyframes bubble {{
          0%   {{ transform:translateY(0);   opacity:0.6; }}
          100% {{ transform:translateY(-40px); opacity:0; }}
        }}
        </style>
        """, unsafe_allow_html=True)

        st.markdown("")

        # Metrik bawah beaker
        m1, m2, m3 = st.columns(3)
        m1.metric("Klasifikasi", kls)
        m2.metric("[H⁺] mol/L",  f"{H_conc:.2e}")
        m3.metric("[OH⁻] mol/L", f"{OH_conc:.2e}")

    # Tabel semua indikator
    with st.expander("📋 Status Semua Indikator pada pH ini"):
        rows = []
        for k, v in INDICATORS.items():
            lo, hi = v["range"]
            rows.append({
                "Indikator": v["name"],
                "Rentang pH": f"{lo} – {hi}",
                "Status": "Asam" if ph_sim < lo else ("Basa" if ph_sim > hi else "Transisi"),
                "Warna": warna_indikator(ph_sim, v),
                "Keterangan": label_indikator(ph_sim, v),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────
# ███  6. KALKULATOR pH
# ─────────────────────────────────────────────────────────────────────
elif selected_menu == "🧮 Kalkulator pH":
    st.markdown("# 🧮 Kalkulator pH Lengkap")
    st.markdown("Hitung nilai pH dari berbagai jenis larutan berdasarkan konsentrasi.")

    tab1, tab2, tab3 = st.tabs(["⚗️ Hitung dari Konsentrasi", "📊 Buffer Henderson-Hasselbalch", "🧫 Titrasi Asam-Basa"])

    # ── Tab 1: Dari Konsentrasi ──────────────────────────────────────
    with tab1:
        k1, k2 = st.columns(2)
        with k1:
            jenis_lar = st.selectbox("Jenis Larutan:", [
                "Asam Kuat (HCl, H₂SO₄, HNO₃)",
                "Basa Kuat (NaOH, KOH)",
                "Asam Lemah (CH₃COOH) Ka=1.8×10⁻⁵",
                "Basa Lemah (NH₃) Kb=1.8×10⁻⁵",
            ])
            konsentrasi = st.number_input("Konsentrasi (mol/L):", min_value=0.0001,
                                          max_value=10.0, value=0.1, step=0.01, format="%.4f")

        ph_hasil, rumus_str = hitung_ph(jenis_lar, konsentrasi)
        kls2, kls2_clr = klasifikasi(ph_hasil)
        H2  = 10 ** (-ph_hasil)
        OH2 = 10 ** (-(14 - ph_hasil))

        with k2:
            st.markdown(f"""
            <div style="background:rgba(0,0,0,0.2); border-radius:20px; padding:2rem;
              text-align:center; border:2px solid {kls2_clr}44; margin-top:0.5rem;">
              <div style="font-family:'JetBrains Mono',monospace; font-size:4rem;
                font-weight:700; color:{kls2_clr}; line-height:1;
                text-shadow:0 0 20px {kls2_clr}88;">pH {ph_hasil:.2f}</div>
              <div style="font-size:1.1rem; font-weight:700; color:{kls2_clr};
                margin-top:8px;">{kls2}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="ccard" style="margin-top:1rem;">
          <b>📐 Langkah Perhitungan:</b><br>
          <span class="mono">{rumus_str.replace('**','')}</span>
        </div>
        """, unsafe_allow_html=True)

        r1, r2 = st.columns(2)
        r1.metric("[H⁺]",  f"{H2:.3e} mol/L")
        r2.metric("[OH⁻]", f"{OH2:.3e} mol/L")

        # Visualisasi mini semua indikator
        st.markdown("---")
        st.markdown("**🎨 Tampilan Semua Indikator:**")
        ind_cols = st.columns(len(INDICATORS))
        for i, (k, v) in enumerate(INDICATORS.items()):
            warna = warna_indikator(ph_hasil, v)
            with ind_cols[i]:
                st.markdown(f"""
                <div style="text-align:center; padding:0.8rem;">
                  <div style="width:50px;height:50px;border-radius:50%;
                    background:{warna};margin:0 auto 8px;
                    box-shadow:0 0 15px {warna}88;
                    border:2px solid rgba(255,255,255,0.2);"></div>
                  <div style="font-size:0.65rem; font-family:'JetBrains Mono',monospace;
                    color:{warna};">{v['name'].split('(')[0].strip()}</div>
                </div>
                """, unsafe_allow_html=True)

    # ── Tab 2: Buffer ────────────────────────────────────────────────
    with tab2:
        st.markdown("""
        <div class="ccard">
          <b>Persamaan Henderson-Hasselbalch:</b><br>
          <span class="mono" style="font-size:1.1rem;">pH = pKa + log ( [A⁻] / [HA] )</span><br><br>
          Gunakan untuk menghitung pH larutan <b>penyangga (buffer)</b>,
          yaitu campuran asam lemah dengan basa konjugasinya.
        </div>
        """, unsafe_allow_html=True)

        b1, b2, b3 = st.columns(3)
        with b1:
            pKa = st.number_input("pKa Asam Lemah:", value=4.74, step=0.01, format="%.2f",
                                  help="CH₃COOH=4.74 | H₂CO₃=6.35 | NH₄⁺=9.25 | H₂PO₄⁻=7.20")
        with b2:
            c_asam = st.number_input("[HA] (mol/L):", value=0.10, step=0.01,
                                     min_value=0.001, format="%.3f")
        with b3:
            c_garam = st.number_input("[A⁻] (mol/L):", value=0.10, step=0.01,
                                      min_value=0.001, format="%.3f")

        rasio = c_garam / c_asam
        ph_buf = round(max(0, min(14, pKa + math.log10(rasio))), 2)
        kls3, kls3_clr = klasifikasi(ph_buf)

        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.2); border-radius:16px; padding:1.5rem;
          text-align:center; border:2px solid {kls3_clr}44; margin-top:1rem;">
          <div class="mono" style="color:#94a3b8; margin-bottom:8px;">
            log([A⁻]/[HA]) = log({rasio:.4f}) = {math.log10(rasio):.4f}
          </div>
          <div style="font-family:'JetBrains Mono',monospace; font-size:3rem; font-weight:700;
            color:{kls3_clr}; text-shadow:0 0 15px {kls3_clr}88;">pH = {ph_buf:.2f}</div>
          <div style="color:{kls3_clr}; font-weight:700; margin-top:4px;">{kls3}</div>
        </div>
        """, unsafe_allow_html=True)

        # Tabel sensitivitas buffer
        st.markdown("---")
        st.markdown("**📈 Sensitivitas pH terhadap rasio [A⁻]/[HA]:**")
        ratios    = [0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 100.0]
        ph_vals   = [round(pKa + math.log10(r), 2) for r in ratios]
        tabel_buf = pd.DataFrame({"[A⁻]/[HA]": ratios, "pH": ph_vals})
        st.dataframe(tabel_buf, use_container_width=True, hide_index=True)

    # ── Tab 3: Titrasi ───────────────────────────────────────────────
    with tab3:
        st.markdown("""
        <div class="ccard">
          <b>Prinsip Titrasi (Titik Ekuivalen):</b><br>
          <span class="mono">M₁ × V₁ = M₂ × V₂</span><br><br>
          Titik ekuivalen tercapai saat mol asam = mol basa.
        </div>
        """, unsafe_allow_html=True)

        t1, t2 = st.columns(2)
        with t1:
            st.markdown("**Analit (larutan yang dititrasi)**")
            M1 = st.number_input("Molaritas Analit (M):", value=0.1, step=0.01,
                                  min_value=0.001, key="M1", format="%.3f")
            V1 = st.number_input("Volume Analit (mL):", value=25.0, step=1.0,
                                  min_value=0.1, key="V1", format="%.1f")
        with t2:
            st.markdown("**Titran (larutan yang diteteskan)**")
            M2 = st.number_input("Molaritas Titran (M):", value=0.1, step=0.01,
                                  min_value=0.001, key="M2", format="%.3f")

        V2_eq = (M1 * V1) / M2
        mol_eq = M1 * (V1 / 1000)

        st.markdown(f"""
        <div style="background:rgba(0,0,0,0.2); border-radius:16px; padding:1.5rem;
          text-align:center; margin-top:1rem; border:2px solid rgba(124,58,237,0.4);">
          <div class="mono" style="color:#94a3b8; margin-bottom:8px;">
            V₂ = (M₁ × V₁) / M₂ = ({M1} × {V1}) / {M2}
          </div>
          <div style="font-family:'JetBrains Mono',monospace; font-size:3rem; font-weight:700;
            color:#a78bfa; text-shadow:0 0 15px rgba(167,139,250,0.5);">{V2_eq:.2f} mL</div>
          <div style="color:#a78bfa; font-weight:600; margin-top:4px;">
            Volume titran untuk mencapai titik ekuivalen
          </div>
        </div>
        """, unsafe_allow_html=True)

        r3, r4 = st.columns(2)
        r3.metric("Mol Ekuivalen",    f"{mol_eq:.4f} mol")
        r4.metric("Volume Titran",    f"{V2_eq:.2f} mL")

        # Tabel titrasi bertahap
        st.markdown("---")
        st.markdown("**📊 Tabel Volume vs Persen Titrasi:**")
        vols    = [v for v in [5, 10, 15, 20, 25, V2_eq * 0.9, V2_eq, V2_eq * 1.1, 30, 40, 50] if 0 < v <= 100]
        vols    = sorted(set(round(v, 2) for v in vols))
        records = []
        for v in vols:
            persen = round(v / V2_eq * 100, 1) if V2_eq > 0 else 0
            records.append({"V Titran (mL)": v, "% Titrasi": persen,
                             "Status": "Sebelum Eq." if persen < 100 else ("Titik Eq. ✅" if persen == 100 else "Setelah Eq.")})
        st.dataframe(pd.DataFrame(records), use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; font-family:'JetBrains Mono',monospace;
  font-size:0.7rem; color:#475569; padding:0.5rem 0;">
  🧪 Dashboard Belajar Kimia — Simulasi Interaktif Indikator Asam-Basa
</div>
""", unsafe_allow_html=True)

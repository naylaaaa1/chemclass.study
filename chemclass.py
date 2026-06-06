# =====================================================================
# 📚 DASHBOARD BELAJAR - KIMIA ASAM BASA
# Versi: 3.1 (Bug Fixes, Cache Migration & Poliprotik)
# =====================================================================

import streamlit as st
import time
import math
import uuid
import pandas as pd
from datetime import datetime

# ─────────────────────────────────────────────────────────────────────
# FUNGSI RERUN AMAN
# ─────────────────────────────────────────────────────────────────────
def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.experimental_rerun()

# ─────────────────────────────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Dashboard Belajar Kimia",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────
# SESSION STATE MIGRATION & INIT (Perbaikan Error Cache)
# ─────────────────────────────────────────────────────────────────────
if "tasks" not in st.session_state:
    st.session_state.tasks = []
else:
    # Memperbaiki data To-Do list lama agar tidak error KeyError: 'id'
    for t in st.session_state.tasks:
        if "id" not in t:
            t["id"] = str(uuid.uuid4())

for key, default in {
    "theme": "Dark",
    "timer_running": False,
    "time_left": 25 * 60,
    "selected_menu": "🏠 Dashboard",
    "new_task_input": "",
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
# DATA: ZAT KIMIA (Untuk Simulasi Indikator Visual)
# ─────────────────────────────────────────────────────────────────────
CHEMICALS = [
    {"name":"HCl (Asam Klorida)",       "formula":"HCl",        "pH":1.0,  "type":"asam",   "cat":"Laboratorium",  "desc":"Asam kuat pembersih porselen",     "dis":"HCl → H⁺ + Cl⁻"},
    {"name":"H₂SO₄ (Asam Sulfat)",      "formula":"H₂SO₄",      "pH":1.5,  "type":"asam",   "cat":"Laboratorium",  "desc":"Air aki kendaraan",                "dis":"H₂SO₄ → 2H⁺ + SO₄²⁻"},
    {"name":"HNO₃ (Asam Nitrat)",       "formula":"HNO₃",       "pH":1.0,  "type":"asam",   "cat":"Laboratorium",  "desc":"Oksidator kuat, pelarut logam",    "dis":"HNO₃ → H⁺ + NO₃⁻"},
    {"name":"CH₃COOH (Cuka)",           "formula":"CH₃COOH",    "pH":3.0,  "type":"asam",   "cat":"Sehari-hari",   "desc":"Cuka dapur 5%",                    "dis":"CH₃COOH ⇌ H⁺ + CH₃COO⁻"},
    {"name":"C₆H₈O₇ (Asam Sitrat)",     "formula":"C₆H₈O₇",     "pH":2.2,  "type":"asam",   "cat":"Sehari-hari",   "desc":"Sari jeruk lemon",                 "dis":"C₆H₈O₇ ⇌ 3H⁺ + C₆H₅O₇³⁻"},
    {"name":"H₂O (Air Murni)",          "formula":"H₂O",        "pH":7.0,  "type":"netral", "cat":"Sehari-hari",   "desc":"Air suling / Aquades",             "dis":"H₂O ⇌ H⁺ + OH⁻"},
    {"name":"NaOH (Soda Api)",          "formula":"NaOH",       "pH":13.0, "type":"basa",   "cat":"Laboratorium",  "desc":"Basa kuat",                        "dis":"NaOH → Na⁺ + OH⁻"},
    {"name":"NH₃ (Amonia)",             "formula":"NH₃",        "pH":11.1, "type":"basa",   "cat":"Laboratorium",  "desc":"Basa lemah berbau tajam",          "dis":"NH₃ + H₂O ⇌ NH₄⁺ + OH⁻"},
]

# ─────────────────────────────────────────────────────────────────────
# DATA: DATABASE LARUTAN KALKULATOR pH & TITRASI
# Ditambahkan parameter 'valensi' untuk perhitungan poliprotik
# ─────────────────────────────────────────────────────────────────────
DATABASE_LARUTAN = {
    # --- ASAM KUAT ---
    "Asam Klorida (HCl)": {"jenis": "asam_kuat", "valensi": 1},
    "Asam Sulfat (H₂SO₄)": {"jenis": "asam_kuat", "valensi": 2},
    "Asam Nitrat (HNO₃)": {"jenis": "asam_kuat", "valensi": 1},
    "Asam Bromida (HBr)": {"jenis": "asam_kuat", "valensi": 1},
    "Asam Iodida (HI)": {"jenis": "asam_kuat", "valensi": 1},
    "Asam Perklorat (HClO₄)": {"jenis": "asam_kuat", "valensi": 1},
    
    # --- BASA KUAT ---
    "Natrium Hidroksida (NaOH)": {"jenis": "basa_kuat", "valensi": 1},
    "Kalium Hidroksida (KOH)": {"jenis": "basa_kuat", "valensi": 1},
    "Litium Hidroksida (LiOH)": {"jenis": "basa_kuat", "valensi": 1},
    "Barium Hidroksida (Ba(OH)₂)": {"jenis": "basa_kuat", "valensi": 2},
    "Kalsium Hidroksida (Ca(OH)₂)": {"jenis": "basa_kuat", "valensi": 2},
    "Stronsium Hidroksida (Sr(OH)₂)": {"jenis": "basa_kuat", "valensi": 2},

    # --- ASAM LEMAH ---
    "Asam Asetat (CH₃COOH)": {"jenis": "asam_lemah", "K": 1.8e-5, "valensi": 1},
    "Asam Format (HCOOH)": {"jenis": "asam_lemah", "K": 1.8e-4, "valensi": 1},
    "Asam Sianida (HCN)": {"jenis": "asam_lemah", "K": 4.9e-10, "valensi": 1},
    "Asam Fluorida (HF)": {"jenis": "asam_lemah", "K": 6.8e-4, "valensi": 1},
    "Asam Nitrit (HNO₂)": {"jenis": "asam_lemah", "K": 4.5e-4, "valensi": 1},
    "Asam Karbonat (H₂CO₃)": {"jenis": "asam_lemah", "K": 4.3e-7, "valensi": 2},
    "Asam Sulfit (H₂SO₃)": {"jenis": "asam_lemah", "K": 1.5e-2, "valensi": 2},
    "Asam Sulfida (H₂S)": {"jenis": "asam_lemah", "K": 8.9e-8, "valensi": 2},
    "Asam Fosfat (H₃PO₄)": {"jenis": "asam_lemah", "K": 7.5e-3, "valensi": 3},
    "Asam Benzoat (C₆H₅COOH)": {"jenis": "asam_lemah", "K": 6.5e-5, "valensi": 1},
    "Asam Laktat (C₃H₆O₃)": {"jenis": "asam_lemah", "K": 1.4e-4, "valensi": 1},
    "Asam Oksalat (H₂C₂O₄)": {"jenis": "asam_lemah", "K": 5.9e-2, "valensi": 2},
    "Asam Sitrat (C₆H₈O₇)": {"jenis": "asam_lemah", "K": 7.4e-4, "valensi": 3},
    "Asam Tartarat (C₄H₆O₆)": {"jenis": "asam_lemah", "K": 1.0e-3, "valensi": 2},
    "Asam Askorbat (Vit C)": {"jenis": "asam_lemah", "K": 8.0e-5, "valensi": 1},
    "Asam Borat (H₃BO₃)": {"jenis": "asam_lemah", "K": 5.8e-10, "valensi": 1},

    # --- BASA LEMAH ---
    "Amonia (NH₃)": {"jenis": "basa_lemah", "K": 1.8e-5, "valensi": 1},
    "Metilamin (CH₃NH₂)": {"jenis": "basa_lemah", "K": 4.4e-4, "valensi": 1},
    "Etilamin (C₂H₅NH₂)": {"jenis": "basa_lemah", "K": 5.6e-4, "valensi": 1},
    "Dimetilamin ((CH₃)₂NH)": {"jenis": "basa_lemah", "K": 5.4e-4, "valensi": 1},
    "Anilin (C₆H₅NH₂)": {"jenis": "basa_lemah", "K": 3.8e-10, "valensi": 1},
    "Piridin (C₅H₅N)": {"jenis": "basa_lemah", "K": 1.7e-9, "valensi": 1},
    "Hidrazin (N₂H₄)": {"jenis": "basa_lemah", "K": 1.3e-6, "valensi": 2},
    "Etilendiamin (C₂H₈N₂)": {"jenis": "basa_lemah", "K": 8.5e-5, "valensi": 2},
}

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

def hitung_ph_konsentrasi(data_larutan: dict, konsentrasi: float) -> tuple[float, str]:
    c = max(konsentrasi, 1e-15)
    jenis = data_larutan["jenis"]
    valensi = data_larutan.get("valensi", 1)

    if jenis == "asam_kuat":
        H = valensi * c
        ph = -math.log10(H)
        rumus = f"[H⁺] = Valensi × C <br> [H⁺] = {valensi} × {c:.4f} = {H:.4e} <br> pH = −log[H⁺] = **{ph:.2f}**"
        
    elif jenis == "basa_kuat":
        OH = valensi * c
        poh = -math.log10(OH)
        ph = 14 - poh
        rumus = f"[OH⁻] = Valensi × C = {OH:.4e} <br> pOH = −log[OH⁻] = {poh:.2f} <br> pH = 14 − {poh:.2f} = **{ph:.2f}**"
        
    elif jenis == "asam_lemah":
        Ka = data_larutan["K"]
        H = math.sqrt(Ka * c)
        ph = -math.log10(H)
        rumus = f"[H⁺] = √(Ka × C) <br> [H⁺] = √({Ka:.1e} × {c:.4f}) = {H:.2e} <br> pH = −log[H⁺] = **{ph:.2f}**"
        
    elif jenis == "basa_lemah":
        Kb = data_larutan["K"]
        OH = math.sqrt(Kb * c)
        poh = -math.log10(OH)
        ph = 14 - poh
        rumus = f"[OH⁻] = √(Kb × C) <br> [OH⁻] = √({Kb:.1e} × {c:.4f}) = {OH:.2e} <br> pOH = {poh:.2f} <br> pH = 14 − {poh:.2f} = **{ph:.2f}**"
        
    else:
        ph = 7.0
        rumus = "pH = 7.00 (larutan netral)"
        
    return round(max(0.0, min(14.0, ph)), 2), rumus

def add_task(name):
    if name.strip():
        st.session_state.tasks.append({
            "id": str(uuid.uuid4()), 
            "name": name.strip(), 
            "done": False, 
            "ts": datetime.now().strftime("%H:%M")
        })

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

    .ccard {{
        background: {card}; border: 1px solid {border};
        border-radius: 16px; padding: 1.2rem 1.5rem; margin-bottom: 0.8rem;
    }}
    .mono {{ font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; }}
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Pengaturan")
    tema = st.radio("🎨 Tema:", ["Dark", "Light"], index=0 if st.session_state.theme == "Dark" else 1, horizontal=True)
    st.session_state.theme = tema
    apply_theme()

    st.markdown("---")
    st.markdown("## 📚 Menu")
    MENUS = ["🏠 Dashboard", "✅ To-Do List", "⏱️ Timer Belajar", "🎵 Musik Fokus", "🧪 Simulasi Indikator", "🧮 Kalkulator pH"]
    selected_menu = st.radio("", MENUS, label_visibility="collapsed")


# ─────────────────────────────────────────────────────────────────────
# ███  1. DASHBOARD
# ─────────────────────────────────────────────────────────────────────
if selected_menu == "🏠 Dashboard":
    st.markdown("# 📚 Dashboard Belajar Kimia")
    st.markdown("Selamat datang! Pilih menu di sidebar untuk memulai sesi belajar.")

    c1, c2, c3, c4 = st.columns(4)
    total   = len(st.session_state.tasks)
    selesai = sum(1 for t in st.session_state.tasks if t.get("done", False))
    pending = total - selesai
    persen  = int(selesai / total * 100) if total else 0

    c1.metric("📝 Total Tugas",   total)
    c2.metric("⏳ Tertunda",       pending)
    c3.metric("✅ Selesai",        selesai)
    c4.metric("📊 Progress",       f"{persen}%")

    if total:
        st.progress(persen / 100)

    st.markdown("---")
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
          <b>🧮 Kalkulator pH</b><br><span class="mono">Titrasi Asidimetri & Alkalimetri</span>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# ███  2. TO-DO LIST
# ─────────────────────────────────────────────────────────────────────
elif selected_menu == "✅ To-Do List":
    st.markdown("# ✅ To-Do List Harian")

    ci1, ci2 = st.columns([5, 1])
    with ci1:
        new_task = st.text_input("Tambah tugas:", key="new_task_input", placeholder="Contoh: Buat Laporan Titrasi Kompleksometri")
    with ci2:
        st.write("")
        if st.button("➕ Tambah", type="primary"):
            add_task(new_task)
            st.session_state["new_task_input"] = ""
            safe_rerun()

    st.markdown("---")
    if not st.session_state.tasks:
        st.warning("📭 Belum ada tugas. Tambahkan di atas!")
    else:
        for task in st.session_state.tasks:
            cc1, cc2, cc3 = st.columns([0.5, 7, 1])
            with cc1:
                # Menggunakan task.get() sebagai pengaman ekstra
                is_checked = st.checkbox("", value=task.get("done", False), key=f"chk_{task['id']}")
                if is_checked != task.get("done", False):
                    task["done"] = is_checked
                    safe_rerun()
            with cc2:
                style = "~~" if task.get("done", False) else "**"
                end   = "~~ ✅" if task.get("done", False) else "**"
                st.markdown(f"{style}{task['name']}{end}")
            with cc3:
                if st.button("🗑️", key=f"del_{task['id']}"):
                    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task["id"]]
                    safe_rerun()
            st.markdown("---")


# ─────────────────────────────────────────────────────────────────────
# ███  3. TIMER BELAJAR
# ─────────────────────────────────────────────────────────────────────
elif selected_menu == "⏱️ Timer Belajar":
    st.markdown("# ⏱️ Timer Belajar — Teknik Pomodoro")

    ct1, ct2 = st.columns(2)
    with ct1:
        st.markdown("### ⚙️ Pengaturan")
        mode = st.selectbox("Mode:", ["🍅 25 menit – Belajar", "☕ 5 menit – Istirahat"])
        default_time = 25*60 if "25" in mode else 5*60

        if st.button("🔄 Reset Timer"):
            st.session_state.time_left = default_time
            st.session_state.timer_running = False
            safe_rerun()

        ck1, ck2 = st.columns(2)
        with ck1:
            if st.button("▶️ Mulai", type="primary"):
                st.session_state.timer_running = True
                safe_rerun()
        with ck2:
            if st.button("⏹️ Stop"):
                st.session_state.timer_running = False
                safe_rerun()

    with ct2:
        menit = max(0, st.session_state.time_left) // 60
        detik = max(0, st.session_state.time_left) % 60
        wkt = f"{menit:02d}:{detik:02d}"

        clr = "#ef4444" if menit <= 5 else ("#f59e0b" if menit <= 10 else "#22c55e")
        st.markdown(f"""
        <div style="text-align:center; padding:40px; background:rgba(0,0,0,0.2); border-radius:24px; border:2px solid {clr}33;">
          <div style="font-family:'JetBrains Mono',monospace; font-size:5rem; font-weight:700; color:{clr};">{wkt}</div>
        </div>
        """, unsafe_allow_html=True)
        st.progress(max(0.0, min(1.0, st.session_state.time_left / default_time)))

    if st.session_state.timer_running and st.session_state.time_left > 0:
        time.sleep(1)
        st.session_state.time_left -= 1
        safe_rerun()


# ─────────────────────────────────────────────────────────────────────
# ███  4. MUSIK FOKUS
# ─────────────────────────────────────────────────────────────────────
elif selected_menu == "🎵 Musik Fokus":
    st.markdown("# 🎵 Musik Fokus")
    pilihan = st.selectbox("🎧 Pilih Trek:", list(MUSIK.keys()))
    st.audio(MUSIK[pilihan], format="audio/mp3")


# ─────────────────────────────────────────────────────────────────────
# ███  5. SIMULASI INDIKATOR
# ─────────────────────────────────────────────────────────────────────
elif selected_menu == "🧪 Simulasi Indikator":
    st.markdown("# 🧪 Simulasi Indikator Asam-Basa")

    col_left, col_right = st.columns([5, 7])
    with col_left:
        preset_names = [c["name"] for c in CHEMICALS]
        pilihan_zat  = st.selectbox("Pilih Zat Kimia (Sampel Visual):", preset_names, index=0)
        zat_data     = next(c for c in CHEMICALS if c["name"] == pilihan_zat)
        pilihan_ind  = st.selectbox("Pilih Indikator:", list(INDICATORS.keys()), format_func=lambda k: INDICATORS[k]["name"])
        ind_data     = INDICATORS[pilihan_ind]

        ph_sim = st.slider("🎚️ Atur pH Manual:", 0.0, 14.0, value=float(zat_data["pH"]), step=0.1)
        kls, kls_clr = klasifikasi(ph_sim)

    with col_right:
        liq_color  = warna_indikator(ph_sim, ind_data)
        liq_label  = label_indikator(ph_sim, ind_data)
        level_px   = int(ph_sim * 7) + 50

        beaker_html = f"""
        <div style='display:flex;flex-direction:column;align-items:center;gap:16px;'>
            <div style='position:relative;width:180px;height:220px;'>
                <div style='position:absolute;bottom:0;left:50%;transform:translateX(-50%);width:150px;height:200px;border:3px solid rgba(200,200,255,0.35);border-top:none;border-radius:0 0 22px 22px;background:rgba(255,255,255,0.03);'>
                    <div style='position:absolute;bottom:0;left:0;right:0;height:{level_px}px;background:{liq_color};border-radius:0 0 18px 18px;'></div>
                </div>
            </div>
            <div style='text-align:center;'>
                <div style='font-family:monospace;font-size:3rem;font-weight:700;color:{liq_color};'>pH {ph_sim:.1f}</div>
                <div style='font-weight:600;color:{liq_color};'>{liq_label}</div>
            </div>
        </div>
        """
        st.markdown(beaker_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# ███  6. KALKULATOR pH
# ─────────────────────────────────────────────────────────────────────
elif selected_menu == "🧮 Kalkulator pH":
    st.markdown("# 🧮 Kalkulator pH & Titrasi")

    tab1, tab2, tab3 = st.tabs(["⚗️ Hitung pH Larutan Tunggal", "📊 Kalkulator Buffer", "🧫 Simulasi Titrasi Asam-Basa"])

    # ── Tab 1: Larutan Tunggal ──────────────────────────────────────
    with tab1:
        k1, k2 = st.columns(2)
        with k1:
            nama_larutan = st.selectbox("Pilih Larutan:", list(DATABASE_LARUTAN.keys()), key="tab1_larutan")
            konsentrasi = st.number_input("Konsentrasi (M):", min_value=0.0001, max_value=10.0, value=0.1, step=0.01, format="%.4f", key="tab1_konsentrasi")

        data_terpilih = DATABASE_LARUTAN[nama_larutan]
        ph_hasil, rumus_str = hitung_ph_konsentrasi(data_terpilih, konsentrasi)
        kls2, kls2_clr = klasifikasi(ph_hasil)

        with k2:
            st.markdown(f"""
            <div style="background:rgba(0,0,0,0.2); border-radius:20px; padding:2rem; text-align:center; border:2px solid {kls2_clr}44;">
              <div style="font-family:'JetBrains Mono',monospace; font-size:4rem; font-weight:700; color:{kls2_clr};">pH {ph_hasil:.2f}</div>
              <div style="font-size:1.1rem; font-weight:700; color:{kls2_clr};">{kls2}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 2: Buffer ────────────────────────────────────────────────
    with tab2:
        st.markdown("""
        <div class="ccard">
          <b>Persamaan Henderson-Hasselbalch:</b><br>
          <span class="mono">pH = pKa + log ( [A⁻] / [HA] )</span>
        </div>
        """, unsafe_allow_html=True)
        b1, b2, b3 = st.columns(3)
        with b1: pKa = st.number_input("pKa Asam Lemah:", value=4.74, step=0.01)
        # Menambahkan min_value agar mencegah ZeroDivisionError
        with b2: c_asam = st.number_input("[Asam] (M):", min_value=0.001, value=0.10, step=0.01)
        with b3: c_garam = st.number_input("[Garam] (M):", min_value=0.001, value=0.10, step=0.01)

        ph_buf = round(pKa + math.log10(c_garam / c_asam), 2)
        st.success(f"**pH Larutan Penyangga (Buffer) = {ph_buf:.2f}**")

    # ── Tab 3: TITRASI POLIPROTIK & HIDROLISIS ───────────────────────
    with tab3:
        st.markdown("""
        <div class="ccard">
          <b>Prinsip Titik Ekuivalen Asidimetri / Alkalimetri:</b><br>
          <span class="mono">n₁ × M₁ × V₁ = n₂ × M₂ × V₂</span><br><br>
          <i>Dimana <b>n</b> adalah valensi (jumlah ion H⁺ atau OH⁻ yang dilepaskan). pH pada titik ekuivalen dihitung secara otomatis menggunakan prinsip hidrolisis garam.</i>
        </div>
        """, unsafe_allow_html=True)

        t1, t2 = st.columns(2)
        with t1:
            st.markdown("**Analit (Larutan di Erlenmeyer)**")
            analit_name = st.selectbox("Jenis Analit:", list(DATABASE_LARUTAN.keys()), key="analit_sel")
            M1 = st.number_input("Molaritas Analit (M₁):", value=0.100, step=0.01, min_value=0.001, format="%.3f")
            V1 = st.number_input("Volume Analit (V₁ mL):", value=25.0, step=1.0, min_value=0.1, format="%.1f")
        with t2:
            st.markdown("**Titran (Larutan di Buret)**")
            titran_name = st.selectbox("Jenis Titran:", list(DATABASE_LARUTAN.keys()), key="titran_sel")
            M2 = st.number_input("Molaritas Titran (M₂):", value=0.100, step=0.01, min_value=0.001, format="%.3f")

        data_analit = DATABASE_LARUTAN[analit_name]
        data_titran = DATABASE_LARUTAN[titran_name]
        
        n1 = data_analit.get("valensi", 1)
        n2 = data_titran.get("valensi", 1)
        
        is_analit_asam = "asam" in data_analit["jenis"]
        is_titran_asam = "asam" in data_titran["jenis"]
        
        # Cegah perhitungan Asam dengan Asam / Basa dengan Basa
        if is_analit_asam == is_titran_asam:
            st.error("⚠️ **Titrasi Tidak Valid!** Analit dan Titran harus kombinasi Asam dan Basa (tidak boleh sejenis).")
        else:
            # 1. Menghitung Volume Titran (V2)
            V2_eq = (n1 * M1 * V1) / (n2 * M2)
            mol_eq = n1 * M1 * (V1 / 1000)
            
            # 2. Menghitung pH pada Titik Ekuivalen (Hidrolisis Garam)
            V_total = V1 + V2_eq
            Cs = (M1 * V1) / V_total 
            Kw = 1e-14
            
            if "kuat" in data_analit["jenis"] and "kuat" in data_titran["jenis"]:
                pH_eq = 7.00
                rumus_ph = "pH = 7.00 (Tidak terjadi hidrolisis, garam bersifat netral)"
                
            elif "lemah" in data_analit["jenis"] and "kuat" in data_titran["jenis"]:
                if is_analit_asam: # Asam Lemah + Basa Kuat
                    Ka = data_analit["K"]
                    OH = math.sqrt((Kw / Ka) * Cs)
                    pH_eq = 14 - (-math.log10(OH))
                    rumus_ph = f"Hidrolisis Basa: [OH⁻] = √((Kw / Ka) × M_garam) = {OH:.2e} M"
                else: # Basa Lemah + Asam Kuat
                    Kb = data_analit["K"]
                    H = math.sqrt((Kw / Kb) * Cs)
                    pH_eq = -math.log10(H)
                    rumus_ph = f"Hidrolisis Asam: [H⁺] = √((Kw / Kb) × M_garam) = {H:.2e} M"
                    
            elif "kuat" in data_analit["jenis"] and "lemah" in data_titran["jenis"]:
                if is_titran_asam: # Basa Kuat + Asam Lemah
                    Ka = data_titran["K"]
                    OH = math.sqrt((Kw / Ka) * Cs)
                    pH_eq = 14 - (-math.log10(OH))
                    rumus_ph = f"Hidrolisis Basa: [OH⁻] = √((Kw / Ka) × M_garam) = {OH:.2e} M"
                else: # Asam Kuat + Basa Lemah
                    Kb = data_titran["K"]
                    H = math.sqrt((Kw / Kb) * Cs)
                    pH_eq = -math.log10(H)
                    rumus_ph = f"Hidrolisis Asam: [H⁺] = √((Kw / Kb) × M_garam) = {H:.2e} M"
                    
            else:
                # Lemah + Lemah (Logika disederhanakan agar tidak error)
                if is_analit_asam:
                    Ka = data_analit["K"]
                    Kb = data_titran["K"]
                else:
                    Ka = data_titran["K"]
                    Kb = data_analit["K"]
                    
                pH_eq = 7 + 0.5 * (-math.log10(Ka)) - 0.5 * (-math.log10(Kb))
                rumus_ph = "Hidrolisis Total: pH = 7 + ½(pKa - pKb)"
            
            # Tampilan Hasil UI
            st.markdown(f"""
            <div style="background:rgba(0,0,0,0.2); border-radius:16px; padding:1.5rem; text-align:center; margin-top:1rem; border:2px solid rgba(124,58,237,0.4);">
              <div class="mono" style="color:#94a3b8; margin-bottom:8px;">
                V₂ = (n₁ × M₁ × V₁) / (n₂ × M₂) = ({n1} × {M1} × {V1}) / ({n2} × {M2})
              </div>
              <div style="font-family:'JetBrains Mono',monospace; font-size:3rem; font-weight:700; color:#a78bfa;">{V2_eq:.2f} mL</div>
              <div style="color:#a78bfa; font-weight:600; margin-top:4px;">
                Volume Titran yang Dibutuhkan (V₂)
              </div>
              <hr style="border-color:rgba(124,58,237,0.2); margin: 15px 0;">
              <div style="font-family:'JetBrains Mono',monospace; font-size:2rem; font-weight:700; color:{klasifikasi(pH_eq)[1]};">
                pH Titik Ekuivalen ≈ {pH_eq:.2f}
              </div>
              <div class="mono" style="font-size:0.8rem; color:#94a3b8; margin-top:5px;">
                {rumus_ph}
              </div>
            </div>
            """, unsafe_allow_html=True)

            r3, r4, r5 = st.columns(3)
            r3.metric("Mol Ekuivalen Bereaksi", f"{mol_eq:.4f} mol")
            r4.metric("Valensi Analit (n₁)", f"{n1} eq/mol")
            r5.metric("Valensi Titran (n₂)", f"{n2} eq/mol")


# ─────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:#475569; padding:0.5rem 0;">
  🧪 Dashboard Belajar Kimia — Alat Analisis Kuantitatif Titrimetri
</div>
""", unsafe_allow_html=True)

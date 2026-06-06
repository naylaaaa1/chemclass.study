# =====================================================================
# 📚 DASHBOARD BELAJAR - KIMIA ASAM BASA
# Versi: 3.0 (Titrasi Poliprotik & Hidrolisis pH Ekuivalen)
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
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────
for key, default in {
    "theme": "Dark",
    "tasks": [],
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
# Ditambahkan parameter 'valensi' untuk semua zat agar support poliprotik
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
        st.session_state.tasks.append({"id": str(uuid.uuid4()), "name": name.strip(), "done": False, "ts": datetime.now().strftime("%H:%M")})

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
    tema = st.radio("🎨 Tema:", ["Dark", "Light"],
                    index=0 if st.session_state.theme == "Dark" else 1,
                    horizontal=True)
    st.session_state.theme = tema
    apply_theme()

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
          <b>🧮 Kalkulator pH</b><br><span class="mono">Titrasi Asidimetri & Alkalimetri (Baru!)</span>
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
                is_checked = st.checkbox("", value=task["done"], key=f"chk_{task['id']}")
                if is_checked != task["done"]:
                    task["done"] = is_checked
                    safe_rerun()
            with cc2:
                style = "~~" if task["done"] else "**"
                end   = "~~ ✅" if task["done"] else "**"
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
        with b2: c_asam = st.number_input("[Asam] (M):", value=0.10, step=0.01)
        with b3: c_garam = st.number_input("[Garam] (M):", value=0.10, step=0.01)

        ph_buf = round(pKa + math.log10(c_garam / c_asam), 2)
        st.success(f"**pH Larutan Penyangga (Buffer) = {ph_buf:.2f}**")

    # ── Tab 3: TITRASI POLIPROTIK & HIDROLISIS ───────────────────────
    with tab3:
        st.markdown("""
        <div class="ccard">
          <b>Prinsip Titik Ekuivalen Asidimetri / Alkalimetri:</b><br>
          <span class="mono">$n_1 \cdot M_1 \cdot V_1 = n_2 \cdot M_2 \cdot V_2$</span><br><br>
          <i>Dimana <b>n</b> adalah valensi (jumlah ion H⁺ atau OH⁻ yang dilepaskan). pH pada titik ekuivalen dihitung secara otomatis menggunakan prinsip hidrolisis garam.</i>
        </div>
        """, unsafe_allow_html=True)

        t1, t2 = st.columns(2)
        with t1:
            st.markdown("**Analit (Larutan di Erlenmeyer)**")
            analit_name = st.selectbox("Jenis Analit:", list(DATABASE_LARUTAN.keys()), key="analit_sel")
            M1 = st.number_input("Molaritas Analit ($M_1$):", value=0.100, step=0.01, min_value=0.001, format="%.3f")
            V1 = st.number_input("Volume Analit ($V_1$ mL):", value=25.0, step=1.0, min_value=0.1, format="%.1f")
        with t2:
            st.markdown("**Titran (Larutan di Buret)**")
            titran_name = st.selectbox("Jenis Titran:", list(DATABASE_LARUTAN.keys()), key="titran_sel")
            M2 = st.number_input("Molaritas Titran ($M_2$):", value=0.100, step=0.01, min_value=0.001, format="%.3f")

        data_analit = DATABASE_LARUTAN[analit_name]
        data_titran = DATABASE_LARUTAN[titran_name]
        
        # Ekstraksi valensi dari database (Mendukung asam/basa poliprotik)
        n1 = data_analit.get("valensi", 1)
        n2 = data_titran.get("valensi", 1)
        
        # Validasi: Mencegah simulasi Asam vs Asam atau Basa vs Basa
        is_analit_asam = "asam" in data_analit["jenis"]
        is_titran_asam = "asam" in data_titran["jenis"]
        
        if is_analit_asam == is_titran_asam:
            st.error("⚠️ **Titrasi Tidak Valid!** Analit dan Titran harus merupakan kombinasi Asam dan Basa (tidak boleh sejenis).")
        else:
            # 1. Menghitung Volume Titran (V2)
            V2_eq = (n1 * M1 * V1) / (n2 * M2)
            mol_eq = n1 * M1 * (V1 / 1000)
            
            # 2. Menghitung pH pada Titik Ekuivalen (Berdasarkan Hidrolisis Garam)
            V_total = V1 + V2_eq
            # Konsentrasi ekuivalen garam yang terbentuk
            Cs = (M1 * V1) / V_total 
            Kw = 1e-14
            
            if "kuat" in data_analit["jenis"] and "kuat" in data_titran["jenis"]:
                # Kuat + Kuat -> Netral
                pH_eq = 7.00
                rumus_ph = "pH = 7.00 (Tidak terjadi hidrolisis, garam bersifat netral)"
                
            elif "lemah" in data_analit["jenis"] and "kuat" in data_titran["jenis"]:
                if is_analit_asam: # Asam Lemah + Basa Kuat -> pH Basa
                    Ka = data_analit["K"]
                    OH = math.sqrt((Kw / Ka) * Cs)
                    pH_eq = 14 - (-math.log10(OH))
                    rumus_ph = f"Hidrolisis Anion (Basa): [OH⁻] = √((Kw / Ka) × M_garam) <br> [OH⁻] = {OH:.2e} M"
                else: # Basa Lemah + Asam Kuat -> pH Asam
                    Kb = data_analit["K"]
                    H = math.sqrt((Kw / Kb) * Cs)
                    pH_eq = -math.log10(H)
                    rumus_ph = f"Hidrolisis Kation (Asam): [H⁺] = √((Kw / Kb) × M_garam) <br> [H⁺] = {H:.2e} M"
                    
            elif "kuat" in data_analit["jenis"] and "lemah" in data_titran["jenis"]:
                if is_titran_asam: # Basa Kuat + Asam Lemah -> pH Basa
                    Ka = data_titran["K"]
                    OH = math.sqrt((Kw / Ka) * Cs)
                    pH_eq = 14 - (-math.log10(OH))
                    rumus_ph = f"Hidrolisis Anion (Basa): [OH⁻] = √((Kw / Ka) × M_garam) <br> [OH⁻] = {OH:.2e} M"
                else: # Asam Kuat + Basa Lemah -> pH Asam
                    Kb = data_titran["K"]
                    H = math.sqrt((Kw / Kb) * Cs)
                    pH_eq = -math.log10(H)
                    rumus_ph = f"Hidrolisis Kation (Asam): [H⁺] = √((Kw / Kb) × M_garam) <br> [H⁺] = {H:.2e} M"
                    
            else:
                # Lemah + Lemah -> pH tergantung pKa dan pKb
                Ka = data_analit["K"] if is_analit_asam else data_titran["K"]
                Kb = data_titran["K"] if is_titran_asam else data_analit["K"]
                pH_eq = 7 + 0.5 * (-math.log10(Ka)) - 0.5 * (-math.log10(Kb))
                rumus_ph = "Hidrolisis Total: pH = 7 + ½(pKa - pKb)"
            
            # Tampilan Hasil UI
            st.markdown(f"""
            <div style="background:rgba(0,0,0,0.2); border-radius:16px; padding:1.5rem; text-align:center; margin-top:1rem; border:2px solid rgba(124,58,237,0.4);">
              <div class="mono" style="color:#94a3b8; margin-bottom:8px;">
                $V_2 = \\frac{{n_1 \\cdot M_1 \\cdot V_1}}{{n_2 \\cdot M_2}} = \\frac{{{n1} \\cdot {M1} \\cdot {V1}}}{{{n2} \\cdot {M2}}}$
              </div>
              <div style="font-family:'JetBrains Mono',monospace; font-size:3rem; font-weight:700; color:#a78bfa;">{V2_eq:.2f} mL</div>
              <div style="color:#a78bfa; font-weight:600; margin-top:4px;">
                Volume Titran yang Dibutuhkan ($V_2$)
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
            r4.metric("Valensi Analit ($n_1$)", f"{n1} eq/mol")
            r5.metric("Valensi Titran ($n_2$)", f"{n2} eq/mol")


# ─────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:#475569; padding:0.5rem 0;">
  🧪 Dashboard Belajar Kimia — Alat Analisis Kuantitatif Titrimetri
</div>
""", unsafe_allow_html=True)# =====================================================================
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
    {"name":"HCl (Asam Klorida)",       "formula":"HCl",        "pH":1.0,  "type":"asam",   "cat":"Laboratorium",  "desc":"Asam kuat pembersih porselen",     "dis":"HCl → H⁺ + Cl⁻"},
    {"name":"H₂SO₄ (Asam Sulfat)",      "formula":"H₂SO₄",      "pH":1.5,  "type":"asam",   "cat":"Laboratorium",  "desc":"Air aki kendaraan",                "dis":"H₂SO₄ → 2H⁺ + SO₄²⁻"},
    {"name":"HNO₃ (Asam Nitrat)",       "formula":"HNO₃",       "pH":1.0,  "type":"asam",   "cat":"Laboratorium",  "desc":"Oksidator kuat, pelarut logam",    "dis":"HNO₃ → H⁺ + NO₃⁻"},
    {"name":"CH₃COOH (Cuka)",           "formula":"CH₃COOH",    "pH":3.0,  "type":"asam",   "cat":"Sehari-hari",   "desc":"Cuka dapur 5%",                    "dis":"CH₃COOH ⇌ H⁺ + CH₃COO⁻"},
    {"name":"C₆H₈O₇ (Asam Sitrat)",     "formula":"C₆H₈O₇",     "pH":2.2,  "type":"asam",   "cat":"Sehari-hari",   "desc":"Sari jeruk lemon",                 "dis":"C₆H₈O₇ ⇌ 3H⁺ + C₆H₅O₇³⁻"},
    {"name":"HF (Asam Fluorida)",       "formula":"HF",         "pH":3.2,  "type":"asam",   "cat":"Laboratorium",  "desc":"Pelarut silika dan kaca",          "dis":"HF ⇌ H⁺ + F⁻"},
    {"name":"H₂CO₃ (Asam Karbonat)",    "formula":"H₂CO₃",      "pH":4.6,  "type":"asam",   "cat":"Sehari-hari",   "desc":"Soda berkarbonasi",                "dis":"H₂CO₃ ⇌ 2H⁺ + CO₃²⁻"},
    {"name":"H₂O (Air Murni)",          "formula":"H₂O",        "pH":7.0,  "type":"netral", "cat":"Sehari-hari",   "desc":"Air suling / Aquades",             "dis":"H₂O ⇌ H⁺ + OH⁻"},
    {"name":"NaCl (Garam Dapur)",       "formula":"NaCl",       "pH":7.0,  "type":"netral", "cat":"Sehari-hari",   "desc":"Garam dapur biasa",                "dis":"NaCl → Na⁺ + Cl⁻"},
    {"name":"NaHCO₃ (Soda Kue)",        "formula":"NaHCO₃",     "pH":8.3,  "type":"basa",   "cat":"Sehari-hari",   "desc":"Pengembang roti",                  "dis":"NaHCO₃ → Na⁺ + HCO₃⁻"},
    {"name":"Na₂CO₃ (Soda Abu)",        "formula":"Na₂CO₃",     "pH":11.6, "type":"basa",   "cat":"Standar Primer","desc":"Standarisasi larutan asam",        "dis":"Na₂CO₃ → 2Na⁺ + CO₃²⁻"},
    {"name":"NH₃ (Amonia)",             "formula":"NH₃",        "pH":11.1, "type":"basa",   "cat":"Laboratorium",  "desc":"Basa lemah berbau tajam",          "dis":"NH₃ + H₂O ⇌ NH₄⁺ + OH⁻"},
    {"name":"Ca(OH)₂ (Air Kapur)",      "formula":"Ca(OH)₂",    "pH":11.5, "type":"basa",   "cat":"Laboratorium",  "desc":"Air kapur sirih",                  "dis":"Ca(OH)₂ → Ca²⁺ + 2OH⁻"},
    {"name":"NaOH (Soda Api)",          "formula":"NaOH",       "pH":13.0, "type":"basa",   "cat":"Laboratorium",  "desc":"Basa kuat",                        "dis":"NaOH → Na⁺ + OH⁻"},
    {"name":"KOH (Kalium Hidroksida)",  "formula":"KOH",        "pH":13.0, "type":"basa",   "cat":"Laboratorium",  "desc":"Basa kuat reaksi penyabunan",      "dis":"KOH → K⁺ + OH⁻"},
    {"name":"Mg(OH)₂ (Susu Magnesia)",  "formula":"Mg(OH)₂",    "pH":10.5, "type":"basa",   "cat":"Farmasi",       "desc":"Antasida obat maag",               "dis":"Mg(OH)₂ ⇌ Mg²⁺ + 2OH⁻"},
    {"name":"KMnO₄ (Kalium Perm.)",     "formula":"KMnO₄",      "pH":7.5,  "type":"netral", "cat":"Permanganometri","desc":"Oksidator kuat autoindikator",    "dis":"KMnO₄ → K⁺ + MnO₄⁻"},
    {"name":"CuSO₄ (Tembaga Sulfat)",   "formula":"CuSO₄",      "pH":4.0,  "type":"asam",   "cat":"Analisis",      "desc":"Reagen biuret untuk protein",      "dis":"CuSO₄ → Cu²⁺ + SO₄²⁻"},
    {"name":"AgNO₃ (Perak Nitrat)",     "formula":"AgNO₃",      "pH":5.5,  "type":"asam",   "cat":"Argentometri",  "desc":"Titran penentuan klorida",         "dis":"AgNO₃ → Ag⁺ + NO₃⁻"},
    {"name":"KHP (Standar Primer)",     "formula":"KHC₈H₄O₄",   "pH":4.0,  "type":"asam",   "cat":"Standar Primer","desc":"Standarisasi larutan NaOH",        "dis":"KHC₈H₄O₄ → K⁺ + HC₈H₄O₄⁻"},
    
    # --- 80 SENYAWA TAMBAHAN ---
    {"name":"HBr (Asam Bromida)",       "formula":"HBr",        "pH":1.0,  "type":"asam",   "cat":"Laboratorium",  "desc":"Asam kuat",                        "dis":"HBr → H⁺ + Br⁻"},
    {"name":"HI (Asam Iodida)",         "formula":"HI",         "pH":1.0,  "type":"asam",   "cat":"Laboratorium",  "desc":"Asam kuat",                        "dis":"HI → H⁺ + I⁻"},
    {"name":"HClO₄ (Asam Perklorat)",   "formula":"HClO₄",      "pH":1.0,  "type":"asam",   "cat":"Laboratorium",  "desc":"Asam kuat oksidator",              "dis":"HClO₄ → H⁺ + ClO₄⁻"},
    {"name":"H₃PO₄ (Asam Fosfat)",      "formula":"H₃PO₄",      "pH":1.5,  "type":"asam",   "cat":"Industri",      "desc":"Bahan pupuk dan minuman",          "dis":"H₃PO₄ ⇌ H⁺ + H₂PO₄⁻"},
    {"name":"HCOOH (Asam Format)",      "formula":"HCOOH",      "pH":2.3,  "type":"asam",   "cat":"Industri",      "desc":"Penggumpal lateks",                "dis":"HCOOH ⇌ H⁺ + HCOO⁻"},
    {"name":"H₂SO₃ (Asam Sulfit)",      "formula":"H₂SO₃",      "pH":1.5,  "type":"asam",   "cat":"Laboratorium",  "desc":"Zat pereduksi",                    "dis":"H₂SO₃ ⇌ 2H⁺ + SO₃²⁻"},
    {"name":"HNO₂ (Asam Nitrit)",       "formula":"HNO₂",       "pH":2.0,  "type":"asam",   "cat":"Laboratorium",  "desc":"Reagen sintesis organik",          "dis":"HNO₂ ⇌ H⁺ + NO₂⁻"},
    {"name":"H₂S (Asam Sulfida)",       "formula":"H₂S",        "pH":4.0,  "type":"asam",   "cat":"Laboratorium",  "desc":"Gas berbau busuk khas",            "dis":"H₂S ⇌ 2H⁺ + S²⁻"},
    {"name":"HCN (Asam Sianida)",       "formula":"HCN",        "pH":5.0,  "type":"asam",   "cat":"Laboratorium",  "desc":"Zat sangat beracun",               "dis":"HCN ⇌ H⁺ + CN⁻"},
    {"name":"H₂C₂O₄ (Asam Oksalat)",    "formula":"H₂C₂O₄",     "pH":1.3,  "type":"asam",   "cat":"Laboratorium",  "desc":"Penghilang karat",                 "dis":"H₂C₂O₄ ⇌ 2H⁺ + C₂O₄²⁻"},
    {"name":"C₃H₆O₃ (Asam Laktat)",     "formula":"C₃H₆O₃",     "pH":2.4,  "type":"asam",   "cat":"Sehari-hari",   "desc":"Asam dalam susu asam",             "dis":"C₃H₆O₃ ⇌ H⁺ + C₃H₅O₃⁻"},
    {"name":"C₆H₅COOH (Asam Benzoat)",  "formula":"C₆H₅COOH",   "pH":2.8,  "type":"asam",   "cat":"Sehari-hari",   "desc":"Pengawet makanan",                 "dis":"C₆H₅COOH ⇌ H⁺ + C₆H₅COO⁻"},
    {"name":"C₄H₆O₆ (Asam Tartarat)",   "formula":"C₄H₆O₆",     "pH":2.9,  "type":"asam",   "cat":"Sehari-hari",   "desc":"Asam pada buah anggur",            "dis":"C₄H₆O₆ ⇌ 2H⁺ + C₄H₄O₆²⁻"},
    {"name":"C₄H₄O₄ (Asam Maleat)",     "formula":"C₄H₄O₄",     "pH":1.9,  "type":"asam",   "cat":"Industri",      "desc":"Bahan baku polimer",               "dis":"C₄H₄O₄ ⇌ 2H⁺ + C₄H₂O₄²⁻"},
    {"name":"C₄H₆O₄ (Asam Suksinat)",   "formula":"C₄H₆O₄",     "pH":2.7,  "type":"asam",   "cat":"Industri",      "desc":"Zat aditif makanan",               "dis":"C₄H₆O₄ ⇌ 2H⁺ + C₄H₄O₄²⁻"},
    {"name":"C₆H₈O₆ (Asam Askorbat)",   "formula":"C₆H₈O₆",     "pH":3.0,  "type":"asam",   "cat":"Farmasi",       "desc":"Vitamin C",                        "dis":"C₆H₈O₆ ⇌ H⁺ + C₆H₇O₆⁻"},
    {"name":"HClO₃ (Asam Klorat)",      "formula":"HClO₃",      "pH":1.0,  "type":"asam",   "cat":"Laboratorium",  "desc":"Oksidator kuat",                   "dis":"HClO₃ → H⁺ + ClO₃⁻"},
    {"name":"HClO (Asam Hipoklorit)",   "formula":"HClO",       "pH":4.0,  "type":"asam",   "cat":"Sehari-hari",   "desc":"Bahan pemutih",                    "dis":"HClO ⇌ H⁺ + ClO⁻"},
    {"name":"H₃BO₃ (Asam Borat)",       "formula":"H₃BO₃",      "pH":5.1,  "type":"asam",   "cat":"Farmasi",       "desc":"Antiseptik ringan pencuci mata",   "dis":"H₃BO₃ + H₂O ⇌ H⁺ + B(OH)₄⁻"},
    {"name":"C₂H₅COOH (Asam Propanoat)","formula":"C₂H₅COOH",   "pH":2.9,  "type":"asam",   "cat":"Industri",      "desc":"Pengawet roti",                    "dis":"C₂H₅COOH ⇌ H⁺ + C₂H₅COO⁻"},
    {"name":"LiOH (Litium Hidroksida)", "formula":"LiOH",       "pH":13.0, "type":"basa",   "cat":"Industri",      "desc":"Penyerap CO₂",                     "dis":"LiOH → Li⁺ + OH⁻"},
    {"name":"Ba(OH)₂ (Barium Hidroks.)","formula":"Ba(OH)₂",    "pH":13.0, "type":"basa",   "cat":"Laboratorium",  "desc":"Basa kuat analitik",               "dis":"Ba(OH)₂ → Ba²⁺ + 2OH⁻"},
    {"name":"Sr(OH)₂ (Stronsium Hidr.)","formula":"Sr(OH)₂",    "pH":13.0, "type":"basa",   "cat":"Industri",      "desc":"Pemurnian gula",                   "dis":"Sr(OH)₂ → Sr²⁺ + 2OH⁻"},
    {"name":"Al(OH)₃ (Aluminium Hidr.)","formula":"Al(OH)₃",    "pH":9.0,  "type":"basa",   "cat":"Farmasi",       "desc":"Komponen antasida",                "dis":"Al(OH)₃ ⇌ Al³⁺ + 3OH⁻"},
    {"name":"Fe(OH)₃ (Besi(III) Hidr.)","formula":"Fe(OH)₃",    "pH":8.0,  "type":"basa",   "cat":"Laboratorium",  "desc":"Endapan cokelat kemerahan",        "dis":"Fe(OH)₃ ⇌ Fe³⁺ + 3OH⁻"},
    {"name":"Fe(OH)₂ (Besi(II) Hidr.)", "formula":"Fe(OH)₂",    "pH":8.5,  "type":"basa",   "cat":"Laboratorium",  "desc":"Endapan hijau",                    "dis":"Fe(OH)₂ ⇌ Fe²⁺ + 2OH⁻"},
    {"name":"Zn(OH)₂ (Seng Hidroksida)","formula":"Zn(OH)₂",    "pH":8.0,  "type":"basa",   "cat":"Laboratorium",  "desc":"Basa amfoter",                     "dis":"Zn(OH)₂ ⇌ Zn²⁺ + 2OH⁻"},
    {"name":"Cu(OH)₂ (Tembaga(II) Hid)","formula":"Cu(OH)₂",    "pH":8.0,  "type":"basa",   "cat":"Laboratorium",  "desc":"Endapan biru muda",                "dis":"Cu(OH)₂ ⇌ Cu²⁺ + 2OH⁻"},
    {"name":"NH₂OH (Hidroksilamin)",    "formula":"NH₂OH",      "pH":9.0,  "type":"basa",   "cat":"Laboratorium",  "desc":"Zat pereduksi",                    "dis":"NH₂OH + H₂O ⇌ NH₃OH⁺ + OH⁻"},
    {"name":"CH₃NH₂ (Metilamin)",       "formula":"CH₃NH₂",     "pH":11.8, "type":"basa",   "cat":"Industri",      "desc":"Bahan sintesis kimia organik",     "dis":"CH₃NH₂ + H₂O ⇌ CH₃NH₃⁺ + OH⁻"},
    {"name":"C₆H₅NH₂ (Anilin)",         "formula":"C₆H₅NH₂",    "pH":8.8,  "type":"basa",   "cat":"Industri",      "desc":"Bahan baku pewarna sintesis",      "dis":"C₆H₅NH₂ + H₂O ⇌ C₆H₅NH₃⁺ + OH⁻"},
    {"name":"C₅H₅N (Piridin)",          "formula":"C₅H₅N",      "pH":8.8,  "type":"basa",   "cat":"Laboratorium",  "desc":"Pelarut basa organik",             "dis":"C₅H₅N + H₂O ⇌ C₅H₅NH⁺ + OH⁻"},
    {"name":"RbOH (Rubidium Hidrok.)",  "formula":"RbOH",       "pH":13.0, "type":"basa",   "cat":"Laboratorium",  "desc":"Basa alkali sangat kuat",          "dis":"RbOH → Rb⁺ + OH⁻"},
    {"name":"CsOH (Sesium Hidroksida)", "formula":"CsOH",       "pH":13.0, "type":"basa",   "cat":"Laboratorium",  "desc":"Basa alkali sangat kuat",          "dis":"CsOH → Cs⁺ + OH⁻"},
    {"name":"AgOH (Perak Hidroksida)",  "formula":"AgOH",       "pH":9.0,  "type":"basa",   "cat":"Laboratorium",  "desc":"Tidak stabil (menjadi Ag₂O)",      "dis":"AgOH ⇌ Ag⁺ + OH⁻"},
    {"name":"N₂H₄ (Hidrazin)",          "formula":"N₂H₄",       "pH":10.5, "type":"basa",   "cat":"Industri",      "desc":"Bahan bakar roket antariksa",      "dis":"N₂H₄ + H₂O ⇌ N₂H₅⁺ + OH⁻"},
    {"name":"(CH₃)₂NH (Dimetilamin)",   "formula":"(CH₃)₂NH",   "pH":10.7, "type":"basa",   "cat":"Industri",      "desc":"Bahan akselerator karet",          "dis":"(CH₃)₂NH + H₂O ⇌ (CH₃)₂NH₂⁺ + OH⁻"},
    {"name":"(CH₃)₃N (Trimetilamin)",   "formula":"(CH₃)₃N",    "pH":9.8,  "type":"basa",   "cat":"Laboratorium",  "desc":"Gas khas berbau ikan",             "dis":"(CH₃)₃N + H₂O ⇌ (CH₃)₃NH⁺ + OH⁻"},
    {"name":"C₂H₅NH₂ (Etilamin)",       "formula":"C₂H₅NH₂",    "pH":11.0, "type":"basa",   "cat":"Industri",      "desc":"Bahan intermediet kimia",          "dis":"C₂H₅NH₂ + H₂O ⇌ C₂H₅NH₃⁺ + OH⁻"},
    {"name":"Ni(OH)₂ (Nikel Hidroks.)", "formula":"Ni(OH)₂",    "pH":8.5,  "type":"basa",   "cat":"Industri",      "desc":"Bahan katoda baterai",             "dis":"Ni(OH)₂ ⇌ Ni²⁺ + 2OH⁻"},
    {"name":"KCl (Kalium Klorida)",     "formula":"KCl",        "pH":7.0,  "type":"netral", "cat":"Sehari-hari",   "desc":"Bahan pupuk kalium",               "dis":"KCl → K⁺ + Cl⁻"},
    {"name":"KBr (Kalium Bromida)",     "formula":"KBr",        "pH":7.0,  "type":"netral", "cat":"Farmasi",       "desc":"Obat penenang (historis)",         "dis":"KBr → K⁺ + Br⁻"},
    {"name":"KI (Kalium Iodida)",       "formula":"KI",         "pH":7.0,  "type":"netral", "cat":"Farmasi",       "desc":"Suplemen anti-radiasi yodium",     "dis":"KI → K⁺ + I⁻"},
    {"name":"NaBr (Natrium Bromida)",   "formula":"NaBr",       "pH":7.0,  "type":"netral", "cat":"Industri",      "desc":"Bahan campuran fotografi",         "dis":"NaBr → Na⁺ + Br⁻"},
    {"name":"NaNO₃ (Natrium Nitrat)",   "formula":"NaNO₃",      "pH":7.0,  "type":"netral", "cat":"Industri",      "desc":"Pupuk penyubur (Sendawa Chili)",   "dis":"NaNO₃ → Na⁺ + NO₃⁻"},
    {"name":"KNO₃ (Kalium Nitrat)",     "formula":"KNO₃",       "pH":7.0,  "type":"netral", "cat":"Industri",      "desc":"Bahan pembuat mesiu",              "dis":"KNO₃ → K⁺ + NO₃⁻"},
    {"name":"Na₂SO₄ (Natrium Sulfat)",  "formula":"Na₂SO₄",     "pH":7.0,  "type":"netral", "cat":"Industri",      "desc":"Bahan pengisi deterjen",           "dis":"Na₂SO₄ → 2Na⁺ + SO₄²⁻"},
    {"name":"K₂SO₄ (Kalium Sulfat)",    "formula":"K₂SO₄",      "pH":7.0,  "type":"netral", "cat":"Industri",      "desc":"Pupuk K (Kalium bebas klor)",      "dis":"K₂SO₄ → 2K⁺ + SO₄²⁻"},
    {"name":"CaCl₂ (Kalsium Klorida)",  "formula":"CaCl₂",      "pH":7.0,  "type":"netral", "cat":"Industri",      "desc":"Zat pengering jalan bersalju",     "dis":"CaCl₂ → Ca²⁺ + 2Cl⁻"},
    {"name":"BaCl₂ (Barium Klorida)",   "formula":"BaCl₂",      "pH":7.0,  "type":"netral", "cat":"Laboratorium",  "desc":"Reagen uji ion sulfat",            "dis":"BaCl₂ → Ba²⁺ + 2Cl⁻"},
    {"name":"NH₄Cl (Amonium Klorida)",  "formula":"NH₄Cl",      "pH":5.0,  "type":"asam",   "cat":"Sehari-hari",   "desc":"Pengisi baterai kering (Salmiak)", "dis":"NH₄Cl → NH₄⁺ + Cl⁻"},
    {"name":"NH₄NO₃ (Amonium Nitrat)",  "formula":"NH₄NO₃",     "pH":5.5,  "type":"asam",   "cat":"Industri",      "desc":"Bahan peledak dan pupuk",          "dis":"NH₄NO₃ → NH₄⁺ + NO₃⁻"},
    {"name":"(NH₄)₂SO₄ (Amonium Sulf.)","formula":"(NH₄)₂SO₄",  "pH":5.5,  "type":"asam",   "cat":"Industri",      "desc":"Pupuk nitrogen ZA",                "dis":"(NH₄)₂SO₄ → 2NH₄⁺ + SO₄²⁻"},
    {"name":"AlCl₃ (Aluminium Klorida)","formula":"AlCl₃",      "pH":3.0,  "type":"asam",   "cat":"Industri",      "desc":"Katalis reaksi Friedel-Crafts",    "dis":"AlCl₃ → Al³⁺ + 3Cl⁻"},
    {"name":"FeCl₃ (Besi(III) Klorida)","formula":"FeCl₃",      "pH":2.0,  "type":"asam",   "cat":"Laboratorium",  "desc":"Koagulan penjernih limbah air",    "dis":"FeCl₃ → Fe³⁺ + 3Cl⁻"},
    {"name":"ZnCl₂ (Seng Klorida)",     "formula":"ZnCl₂",      "pH":4.0,  "type":"asam",   "cat":"Industri",      "desc":"Bahan pengawet kayu",              "dis":"ZnCl₂ → Zn²⁺ + 2Cl⁻"},
    {"name":"CuCl₂ (Tembaga Klorida)",  "formula":"CuCl₂",      "pH":4.0,  "type":"asam",   "cat":"Industri",      "desc":"Pewarna kembang api piroteknik",   "dis":"CuCl₂ → Cu²⁺ + 2Cl⁻"},
    {"name":"MgSO₄ (Magnesium Sulfat)", "formula":"MgSO₄",      "pH":6.0,  "type":"asam",   "cat":"Farmasi",       "desc":"Garam pereda nyeri (Garam Epsom)", "dis":"MgSO₄ → Mg²⁺ + SO₄²⁻"},
    {"name":"NaHSO₄ (Natrium Bisulfat)","formula":"NaHSO₄",     "pH":1.5,  "type":"asam",   "cat":"Laboratorium",  "desc":"Garam bersifat asam kuat",         "dis":"NaHSO₄ → Na⁺ + H⁺ + SO₄²⁻"},
    {"name":"NaH₂PO₄ (Natrium Dihid. F)","formula":"NaH₂PO₄",   "pH":4.5,  "type":"asam",   "cat":"Analisis",      "desc":"Komponen larutan buffer asam",     "dis":"NaH₂PO₄ → Na⁺ + H₂PO₄⁻"},
    {"name":"K₂CO₃ (Kalium Karbonat)",  "formula":"K₂CO₃",      "pH":11.0, "type":"basa",   "cat":"Industri",      "desc":"Bahan baku pembuatan kaca",        "dis":"K₂CO₃ → 2K⁺ + CO₃²⁻"},
    {"name":"CH₃COONa (Natrium Asetat)","formula":"CH₃COONa",   "pH":9.0,  "type":"basa",   "cat":"Analisis",      "desc":"Komponen buffer penghangat",       "dis":"CH₃COONa → Na⁺ + CH₃COO⁻"},
    {"name":"CH₃COOK (Kalium Asetat)",  "formula":"CH₃COOK",    "pH":9.0,  "type":"basa",   "cat":"Industri",      "desc":"Bahan aktif pemadam api kelas K",  "dis":"CH₃COOK → K⁺ + CH₃COO⁻"},
    {"name":"NaCN (Natrium Sianida)",   "formula":"NaCN",       "pH":11.0, "type":"basa",   "cat":"Industri",      "desc":"Pelarut ekstraksi tambang emas",   "dis":"NaCN → Na⁺ + CN⁻"},
    {"name":"KCN (Kalium Sianida)",     "formula":"KCN",        "pH":11.0, "type":"basa",   "cat":"Laboratorium",  "desc":"Reagen kimia toksik",              "dis":"KCN → K⁺ + CN⁻"},
    {"name":"NaF (Natrium Fluorida)",   "formula":"NaF",        "pH":8.0,  "type":"basa",   "cat":"Sehari-hari",   "desc":"Penguat email di pasta gigi",      "dis":"NaF → Na⁺ + F⁻"},
    {"name":"KF (Kalium Fluorida)",     "formula":"KF",         "pH":8.0,  "type":"basa",   "cat":"Industri",      "desc":"Fluks dalam peleburan metalurgi",  "dis":"KF → K⁺ + F⁻"},
    {"name":"Na₃PO₄ (Trinatrium Fosf.)","formula":"Na₃PO₄",     "pH":12.0, "type":"basa",   "cat":"Industri",      "desc":"Bahan aktif agen pembersih",       "dis":"Na₃PO₄ → 3Na⁺ + PO₄³⁻"},
    {"name":"K₃PO₄ (Trikalium Fosfat)", "formula":"K₃PO₄",      "pH":12.0, "type":"basa",   "cat":"Industri",      "desc":"Zat aditif makanan dan emulsifier","dis":"K₃PO₄ → 3K⁺ + PO₄³⁻"},
    {"name":"Na₂HPO₄ (Dinatrium Hid. F)","formula":"Na₂HPO₄",   "pH":9.0,  "type":"basa",   "cat":"Analisis",      "desc":"Komponen pembuat buffer",          "dis":"Na₂HPO₄ → 2Na⁺ + HPO₄²⁻"},
    {"name":"Na₂SO₃ (Natrium Sulfit)",  "formula":"Na₂SO₃",     "pH":9.0,  "type":"basa",   "cat":"Industri",      "desc":"Pengawet pewarna makanan",         "dis":"Na₂SO₃ → 2Na⁺ + SO₃²⁻"},
    {"name":"NaNO₂ (Natrium Nitrit)",   "formula":"NaNO₂",      "pH":9.0,  "type":"basa",   "cat":"Industri",      "desc":"Pengawet olahan daging",           "dis":"NaNO₂ → Na⁺ + NO₂⁻"},
    {"name":"Na₂S (Natrium Sulfida)",   "formula":"Na₂S",       "pH":12.0, "type":"basa",   "cat":"Industri",      "desc":"Bahan penyamakan kulit hewan",     "dis":"Na₂S → 2Na⁺ + S²⁻"},
    {"name":"K₂S (Kalium Sulfida)",     "formula":"K₂S",        "pH":12.0, "type":"basa",   "cat":"Laboratorium",  "desc":"Reagen penguji kation logam",      "dis":"K₂S → 2K⁺ + S²⁻"},
    {"name":"NaClO (Nat. Hipoklorit)",  "formula":"NaClO",      "pH":11.0, "type":"basa",   "cat":"Sehari-hari",   "desc":"Pemutih pakaian (Bayclin)",        "dis":"NaClO → Na⁺ + ClO⁻"},
    {"name":"K₂Cr₂O₇ (Kalium Dikromat)","formula":"K₂Cr₂O₇",    "pH":4.0,  "type":"asam",   "cat":"Analisis",      "desc":"Oksidator titrasi dikromatometri", "dis":"K₂Cr₂O₇ → 2K⁺ + Cr₂O₇²⁻"},
    {"name":"Na₂CrO₄ (Natrium Kromat)", "formula":"Na₂CrO₄",    "pH":9.0,  "type":"basa",   "cat":"Laboratorium",  "desc":"Indikator titrasi Mohr",           "dis":"Na₂CrO₄ → 2Na⁺ + CrO₄²⁻"},
    {"name":"KSCN (Kalium Tiosianat)",  "formula":"KSCN",       "pH":7.0,  "type":"netral", "cat":"Analisis",      "desc":"Titrasi presipitasi Volhard",      "dis":"KSCN → K⁺ + SCN⁻"},
    {"name":"K₃[Fe(CN)₆] (Kal. Ferisi.)","formula":"K₃[Fe(CN)₆]","pH":7.0, "type":"netral", "cat":"Laboratorium",  "desc":"Reagen biru Prusia analitik",      "dis":"K₃[Fe(CN)₆] → 3K⁺ + [Fe(CN)₆]³⁻"},
    {"name":"Na₂S₂O₃ (Nat. Tiosulfat)", "formula":"Na₂S₂O₃",    "pH":7.0,  "type":"netral", "cat":"Iodometri",     "desc":"Titran iodometri (Hiposulfit)",    "dis":"Na₂S₂O₃ → 2Na⁺ + S₂O₃²⁻"},
]

# ─────────────────────────────────────────────────────────────────────
# DATA: DATABASE LARUTAN KALKULATOR pH (60 Jenis Larutan)
# ─────────────────────────────────────────────────────────────────────
DATABASE_LARUTAN = {
    # --- ASAM KUAT ---
    "Asam Klorida (HCl) - Asam Kuat (Valensi 1)": {"jenis": "asam_kuat", "valensi": 1},
    "Asam Sulfat (H₂SO₄) - Asam Kuat (Valensi 2)": {"jenis": "asam_kuat", "valensi": 2},
    "Asam Nitrat (HNO₃) - Asam Kuat (Valensi 1)": {"jenis": "asam_kuat", "valensi": 1},
    "Asam Bromida (HBr) - Asam Kuat (Valensi 1)": {"jenis": "asam_kuat", "valensi": 1},
    "Asam Iodida (HI) - Asam Kuat (Valensi 1)": {"jenis": "asam_kuat", "valensi": 1},
    "Asam Perklorat (HClO₄) - Asam Kuat (Valensi 1)": {"jenis": "asam_kuat", "valensi": 1},
    "Asam Klorat (HClO₃) - Asam Kuat (Valensi 1)": {"jenis": "asam_kuat", "valensi": 1},

    # --- BASA KUAT ---
    "Natrium Hidroksida (NaOH) - Basa Kuat (Valensi 1)": {"jenis": "basa_kuat", "valensi": 1},
    "Kalium Hidroksida (KOH) - Basa Kuat (Valensi 1)": {"jenis": "basa_kuat", "valensi": 1},
    "Litium Hidroksida (LiOH) - Basa Kuat (Valensi 1)": {"jenis": "basa_kuat", "valensi": 1},
    "Rubidium Hidroksida (RbOH) - Basa Kuat (Valensi 1)": {"jenis": "basa_kuat", "valensi": 1},
    "Sesium Hidroksida (CsOH) - Basa Kuat (Valensi 1)": {"jenis": "basa_kuat", "valensi": 1},
    "Barium Hidroksida (Ba(OH)₂) - Basa Kuat (Valensi 2)": {"jenis": "basa_kuat", "valensi": 2},
    "Kalsium Hidroksida (Ca(OH)₂) - Basa Kuat (Valensi 2)": {"jenis": "basa_kuat", "valensi": 2},
    "Stronsium Hidroksida (Sr(OH)₂) - Basa Kuat (Valensi 2)": {"jenis": "basa_kuat", "valensi": 2},

    # --- ASAM LEMAH ---
    "Asam Asetat (CH₃COOH) Ka=1.8×10⁻⁵": {"jenis": "asam_lemah", "K": 1.8e-5},
    "Asam Format (HCOOH) Ka=1.8×10⁻⁴": {"jenis": "asam_lemah", "K": 1.8e-4},
    "Asam Sianida (HCN) Ka=4.9×10⁻¹⁰": {"jenis": "asam_lemah", "K": 4.9e-10},
    "Asam Fluorida (HF) Ka=6.8×10⁻⁴": {"jenis": "asam_lemah", "K": 6.8e-4},
    "Asam Nitrit (HNO₂) Ka=4.5×10⁻⁴": {"jenis": "asam_lemah", "K": 4.5e-4},
    "Asam Hipoklorit (HClO) Ka=2.9×10⁻⁸": {"jenis": "asam_lemah", "K": 2.9e-8},
    "Asam Klorit (HClO₂) Ka=1.1×10⁻²": {"jenis": "asam_lemah", "K": 1.1e-2},
    "Asam Karbonat (H₂CO₃) Ka=4.3×10⁻⁷": {"jenis": "asam_lemah", "K": 4.3e-7},
    "Asam Sulfit (H₂SO₃) Ka=1.5×10⁻²": {"jenis": "asam_lemah", "K": 1.5e-2},
    "Asam Sulfida (H₂S) Ka=8.9×10⁻⁸": {"jenis": "asam_lemah", "K": 8.9e-8},
    "Asam Fosfat (H₃PO₄) Ka=7.5×10⁻³": {"jenis": "asam_lemah", "K": 7.5e-3},
    "Asam Benzoat (C₆H₅COOH) Ka=6.5×10⁻⁵": {"jenis": "asam_lemah", "K": 6.5e-5},
    "Fenol (C₆H₅OH) Ka=1.0×10⁻¹⁰": {"jenis": "asam_lemah", "K": 1.0e-10},
    "Asam Propanoat (C₂H₅COOH) Ka=1.3×10⁻⁵": {"jenis": "asam_lemah", "K": 1.3e-5},
    "Asam Butanoat (C₃H₇COOH) Ka=1.5×10⁻⁵": {"jenis": "asam_lemah", "K": 1.5e-5},
    "Asam Laktat (C₃H₆O₃) Ka=1.4×10⁻⁴": {"jenis": "asam_lemah", "K": 1.4e-4},
    "Asam Askorbat / Vit C (C₆H₈O₆) Ka=8.0×10⁻⁵": {"jenis": "asam_lemah", "K": 8.0e-5},
    "Asam Tartarat (C₄H₆O₆) Ka=1.0×10⁻³": {"jenis": "asam_lemah", "K": 1.0e-3},
    "Asam Sitrat (C₆H₈O₇) Ka=7.4×10⁻⁴": {"jenis": "asam_lemah", "K": 7.4e-4},
    "Asam Oksalat (H₂C₂O₄) Ka=5.9×10⁻²": {"jenis": "asam_lemah", "K": 5.9e-2},
    "Asam Ftalat (C₈H₆O₄) Ka=1.1×10⁻³": {"jenis": "asam_lemah", "K": 1.1e-3},
    "Asam Salisilat (C₇H₆O₃) Ka=1.0×10⁻³": {"jenis": "asam_lemah", "K": 1.0e-3},
    "Asam Borat (H₃BO₃) Ka=5.8×10⁻¹⁰": {"jenis": "asam_lemah", "K": 5.8e-10},
    "Asam Kloroasetat (CH₂ClCOOH) Ka=1.4×10⁻³": {"jenis": "asam_lemah", "K": 1.4e-3},
    "Asam Dikloroasetat (CHCl₂COOH) Ka=5.0×10⁻²": {"jenis": "asam_lemah", "K": 5.0e-2},
    "Asam Bromoasetat (CH₂BrCOOH) Ka=1.3×10⁻³": {"jenis": "asam_lemah", "K": 1.3e-3},
    "Asam Arsenat (H₃AsO₄) Ka=5.5×10⁻³": {"jenis": "asam_lemah", "K": 5.5e-3},
    "Asam Arsenit (H₃AsO₃) Ka=5.1×10⁻¹⁰": {"jenis": "asam_lemah", "K": 5.1e-10},
    "Asam Sianat (HOCN) Ka=3.5×10⁻⁴": {"jenis": "asam_lemah", "K": 3.5e-4},
    "Asam Urat (C₅H₄N₄O₃) Ka=4.0×10⁻⁶": {"jenis": "asam_lemah", "K": 4.0e-6},

    # --- BASA LEMAH ---
    "Amonia (NH₃) Kb=1.8×10⁻⁵": {"jenis": "basa_lemah", "K": 1.8e-5},
    "Metilamin (CH₃NH₂) Kb=4.4×10⁻⁴": {"jenis": "basa_lemah", "K": 4.4e-4},
    "Etilamin (C₂H₅NH₂) Kb=5.6×10⁻⁴": {"jenis": "basa_lemah", "K": 5.6e-4},
    "Propilamin (C₃H₇NH₂) Kb=3.5×10⁻⁴": {"jenis": "basa_lemah", "K": 3.5e-4},
    "Butilamin (C₄H₉NH₂) Kb=4.0×10⁻⁴": {"jenis": "basa_lemah", "K": 4.0e-4},
    "Dimetilamin ((CH₃)₂NH) Kb=5.4×10⁻⁴": {"jenis": "basa_lemah", "K": 5.4e-4},
    "Dietilamin ((C₂H₅)₂NH) Kb=8.6×10⁻⁴": {"jenis": "basa_lemah", "K": 8.6e-4},
    "Trimetilamin ((CH₃)₃N) Kb=6.3×10⁻⁵": {"jenis": "basa_lemah", "K": 6.3e-5},
    "Trietilamin ((C₂H₅)₃N) Kb=5.2×10⁻⁴": {"jenis": "basa_lemah", "K": 5.2e-4},
    "Anilin (C₆H₅NH₂) Kb=3.8×10⁻¹⁰": {"jenis": "basa_lemah", "K": 3.8e-10},
    "Piridin (C₅H₅N) Kb=1.7×10⁻⁹": {"jenis": "basa_lemah", "K": 1.7e-9},
    "Hidrazin (N₂H₄) Kb=1.3×10⁻⁶": {"jenis": "basa_lemah", "K": 1.3e-6},
    "Hidroksilamin (NH₂OH) Kb=1.1×10⁻⁸": {"jenis": "basa_lemah", "K": 1.1e-8},
    "Benzilamin (C₆H₅CH₂NH₂) Kb=2.1×10⁻⁵": {"jenis": "basa_lemah", "K": 2.1e-5},
    "Etilendiamin (C₂H₈N₂) Kb=8.5×10⁻⁵": {"jenis": "basa_lemah", "K": 8.5e-5},
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

def hitung_ph(data_larutan: dict, konsentrasi: float) -> tuple[float, str]:
    c = max(konsentrasi, 1e-15)
    jenis = data_larutan["jenis"]

    if jenis == "asam_kuat":
        valensi = data_larutan["valensi"]
        H = valensi * c
        ph = -math.log10(H)
        rumus = f"[H⁺] = Valensi × C <br> [H⁺] = {valensi} × {c:.4f} = {H:.4e} <br> pH = −log[H⁺] = **{ph:.2f}**"
        
    elif jenis == "basa_kuat":
        valensi = data_larutan["valensi"]
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
        level_px   = int(ph_sim * 7) + 50  # ketinggian cairan 50-148 px

        # Inject animasi bubble via CSS terpisah
        st.markdown("""
        <style>
        @keyframes bubble {
          0%   { transform: translateY(0);    opacity: 0.6; }
          100% { transform: translateY(-40px); opacity: 0;   }
        }
        </style>
        """, unsafe_allow_html=True)

        # Bangun HTML beaker tanpa komentar HTML agar tidak mengacaukan render
        shadow_box  = f"inset 0 0 20px rgba(0,0,0,0.3), 0 0 20px {liq_color}44"
        text_shadow = f"0 0 20px {liq_color}99"

        beaker_html = (
            "<div style='display:flex;flex-direction:column;align-items:center;gap:16px;'>"

            # -- wrapper beaker
            "<div style='position:relative;width:180px;height:220px;'>"

            # -- bibir atas beaker
            "<div style='position:absolute;top:0;left:50%;transform:translateX(-50%);"
            "width:164px;height:12px;"
            "border:3px solid rgba(200,200,255,0.35);border-radius:4px;'></div>"

            # -- tabung beaker
            f"<div style='position:absolute;bottom:0;left:50%;transform:translateX(-50%);"
            f"width:150px;height:200px;"
            f"border:3px solid rgba(200,200,255,0.35);border-top:none;"
            f"border-radius:0 0 22px 22px;overflow:hidden;"
            f"background:rgba(255,255,255,0.03);"
            f"box-shadow:{shadow_box};'>"

            # -- cairan
            f"<div style='position:absolute;bottom:0;left:0;right:0;"
            f"height:{level_px}px;"
            f"background:{liq_color};opacity:0.85;"
            f"border-radius:0 0 18px 18px;"
            f"box-shadow:inset 0 6px 12px rgba(255,255,255,0.2);'>"

            # -- gelembung 1
            "<div style='position:absolute;bottom:10px;left:25%;width:6px;height:6px;"
            "background:rgba(255,255,255,0.5);border-radius:50%;"
            "animation:bubble 2s infinite;'></div>"

            # -- gelembung 2
            "<div style='position:absolute;bottom:20px;left:60%;width:4px;height:4px;"
            "background:rgba(255,255,255,0.4);border-radius:50%;"
            "animation:bubble 2.5s infinite 0.5s;'></div>"

            "</div>"  # tutup cairan

            # -- skala ukur
            "<div style='position:absolute;right:8px;top:15px;height:155px;"
            "display:flex;flex-direction:column;justify-content:space-between;"
            "font-family:monospace;font-size:8px;color:rgba(200,220,255,0.6);'>"
            "<span>150ml</span><span>100ml</span><span>50ml</span>"
            "</div>"

            "</div>"  # tutup tabung beaker
            "</div>"  # tutup wrapper beaker

            # -- label pH besar
            "<div style='text-align:center;'>"
            f"<div style='font-family:monospace;font-size:3.2rem;font-weight:700;"
            f"color:{liq_color};text-shadow:{text_shadow};line-height:1;'>"
            f"pH {ph_sim:.1f}</div>"
            f"<div style='font-size:0.9rem;font-weight:600;margin-top:4px;"
            f"color:{liq_color};opacity:0.85;'>{liq_label}</div>"
            "</div>"

            "</div>"  # tutup flex container
        )

        st.markdown(beaker_html, unsafe_allow_html=True)

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
            # Dropdown kini mengambil list dari DATABASE_LARUTAN
            nama_larutan = st.selectbox("Jenis Larutan:", list(DATABASE_LARUTAN.keys()))
            konsentrasi = st.number_input("Konsentrasi (mol/L):", min_value=0.0001,
                                          max_value=10.0, value=0.1, step=0.01, format="%.4f")

        # Mengambil dictionary data yang spesifik berdasarkan nama yang dipilih
        data_terpilih = DATABASE_LARUTAN[nama_larutan]
        
        # Eksekusi fungsi pH dinamis
        ph_hasil, rumus_str = hitung_ph(data_terpilih, konsentrasi)
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

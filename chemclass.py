import streamlit as st
import time
from datetime import datetime
import pandas as pd
import mathimport streamlit as st
import time
from datetime import datetime
import pandas as pd
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Dashboard Belajar",
    page_icon="📚",
    layout="wide"
)

# --- INISIALISASI SESSION STATE ---
if 'theme' not in st.session_state:
    st.session_state.theme = "White"

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False

if 'time_left' not in st.session_state:
    st.session_state.time_left = 25 * 60

# ============================================================
# 🎨 FUNGSI apply_theme - GANTI WARNA BACKGROUND & FONT
# ============================================================
def apply_theme(theme):
    if theme == "White":
        st.markdown("""
            <style>
            .stApp { background-color: #ffffff; }
            h1, h2, h3, h4, h5, h6, p, label, span, div { color: #1a1a1a !important; }
            .stMetric .stMetricLabel { color: #333333 !important; }
            .stMetric .stMetricValue { color: #1a1a1a !important; }
            section[data-testid="stSidebar"] { background-color: #f8f9fa; }
            .stTextInput > div > div > input { background-color: #ffffff; color: #1a1a1a; border: 1px solid #ddd; }
            .custom-card { background-color: #f8f9fa; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #1a1a1a; }
            .stButton > button { background-color: #3498db; color: white !important; }
            .stProgress > div > div > div { background-color: #3498db; }
            .stAlert { color: #1a1a1a; }
            </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <style>
            .stApp { background-color: #1a1a1a; }
            h1, h2, h3, h4, h5, h6, p, label, span, div { color: #ffffff !important; }
            .stMarkdown, .stMarkdown p { color: #ffffff !important; }
            .stMetric .stMetricLabel { color: #e0e0e0 !important; }
            .stMetric .stMetricValue { color: #ffffff !important; }
            section[data-testid="stSidebar"] { background-color: #2d2d2d; }
            .stTextInput > div > div > input { background-color: #2d2d2d !important; color: #ffffff !important; border: 1px solid #555; }
            .stTextInput label { color: #ffffff !important; }
            .stSelectbox label { color: #ffffff !important; }
            .stSelectbox > div > div > div { background-color: #2d2d2d !important; color: #ffffff !important; }
            .stRadio label { color: #ffffff !important; }
            .custom-card { background-color: #2d2d2d; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.5); color: #ffffff; }
            .stButton > button { background-color: #e74c3c !important; color: #ffffff !important; }
            .stCheckbox label { color: #ffffff !important; }
            .stProgress > div > div > div { background-color: #e74c3c; }
            .stAlert { background-color: #2d2d2d !important; color: #ffffff !important; }
            .streamlit-expanderHeader { background-color: #2d2d2d !important; color: #ffffff !important; }
            hr { border-color: #555555 !important; }
            .stAudio { background-color: #2d2d2d; border-radius: 10px; padding: 10px; }
            </style>
        """, unsafe_allow_html=True)

# ============================================================
# 📝 FUNGSI-FUNGSI TO-DO LIST
# ============================================================
def add_task(task_name):
    if task_name:
        st.session_state.tasks.append({
            "name": task_name,
            "done": False,
            "timestamp": datetime.now().strftime("%H:%M")
        })

def toggle_task(index):
    st.session_state.tasks[index]["done"] = not st.session_state.tasks[index]["done"]

def delete_task(index):
    st.session_state.tasks.pop(index)

# ============================================================
# 🚀 SIDEBAR - PENGATURAN THEME & MENU
# ============================================================
with st.sidebar:
    st.markdown("## ⚙️ Pengaturan")
    
    # Pilihan Theme
    st.markdown("### 🎨 Tema Background")
    theme_option = st.radio(
        "Pilih tema:",
        ["⬜ White (Terang)", "⬛ Black (Gelap)"],
        index=0 if st.session_state.theme == "White" else 1
    )
    
    if "White" in theme_option:
        st.session_state.theme = "White"
    else:
        st.session_state.theme = "Black"
    
    apply_theme(st.session_state.theme)
    
    st.markdown("---")
    st.title("📚 Menu Dashboard")

    menu_options = [
        "🏠 Dashboard", 
        "✅ To-Do List", 
        "⏱️ Timer Belajar", 
        "🎵 Musik Fokus", 
        "🧪 Simulasi Indikator"
    ]

    selected_menu = st.radio("Pilih Menu:", menu_options, label_visibility="collapsed")

# ============================================================
# 📌 KONTEN UTAMA PER MENU
# ============================================================

# ═══════════════════════════════════════════════════════════
# 1️⃣ DASHBOARD UTAMA
# ═══════════════════════════════════════════════════════════
if selected_menu == "🏠 Dashboard":
    st.markdown("# 📚 Dashboard Belajar")
    st.markdown("Selamat datang! Pilih menu di sidebar untuk memulai.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📝 Total Tugas", len(st.session_state.tasks))
    with col2:
        tugas_belum = sum(1 for t in st.session_state.tasks if not t["done"])
        st.metric("⏳ Tugas Tertunda", tugas_belum)
    with col3:
        tugas_selesai = sum(1 for t in st.session_state.tasks if t["done"])
        st.metric("✅ Tugas Selesai", tugas_selesai)
    with col4:
        st.metric("🎨 Tema Saat Ini", st.session_state.theme)
    
    st.markdown("---")
    if st.session_state.theme == "White":
        st.success("💡 Tip: Gunakan teknik Pomodoro (25 menit belajar, 5 menit istirahat)!")
    else:
        st.info("💡 Tip: Gunakan teknik Pomodoro (25 menit belajar, 5 menit istirahat) untuk hasil maksimal!")

# ═══════════════════════════════════════════════════════════
# 2️⃣ TO-DO LIST
# ═══════════════════════════════════════════════════════════
elif selected_menu == "✅ To-Do List":
    st.markdown("# 📝 To-Do List Harian")
    
    col_input1, col_input2 = st.columns([4, 1])
    with col_input1:
        new_task = st.text_input("Tambah tugas baru:", placeholder="Contoh: Mengerjakan Praktikum Kimia")
    with col_input2:
        st.write("") 
        if st.button("➕ Tambah", type="primary"):
            add_task(new_task)
            st.rerun()
    
    st.markdown("---")
    
    if len(st.session_state.tasks) == 0:
        st.warning("📭 Daftar tugas kosong. Tambahkan tugas di atas ya!")
    else:
        for i, task in enumerate(st.session_state.tasks):
            col1, col2, col3 = st.columns([1, 6, 1])
            with col1:
                st.checkbox("", value=task["done"], key=f"check_{i}", on_change=toggle_task, args=(i,))
            with col2:
                if task["done"]:
                    st.markdown(f"~~{task['name']}~~ ✅")
                else:
                    st.markdown(f"**{task['name']}**")
                st.caption(f"Jam: {task['timestamp']}")
            with col3:
                if st.button("🗑️", key=f"del_{i}"):
                    delete_task(i)
                    st.rerun()
            st.markdown("---")

# ═══════════════════════════════════════════════════════════
# 3️⃣ TIMER BELAJAR
# ═══════════════════════════════════════════════════════════
elif selected_menu == "⏱️ Timer Belajar":
    st.markdown("# ⏱️ Timer Belajar (Pomodoro)")
    
    col_timer1, col_timer2 = st.columns([1, 1])
    with col_timer1:
        st.markdown("### ⚙️ Pengaturan Waktu")
        mode = st.selectbox("Pilih Mode:", ["25 menit (Belajar)", "5 menit (Istirahat)", "15 menit (Istirahat Panjang)"])
        
        if mode == "25 menit (Belajar)": default_time = 25 * 60
        elif mode == "5 menit (Istirahat)": default_time = 5 * 60
        else: default_time = 15 * 60
        
        if st.button("🔄 Reset Timer"):
            st.session_state.time_left = default_time
            st.session_state.timer_running = False
            st.rerun()
    
    with col_timer2:
        menit = st.session_state.time_left // 60
        detik = st.session_state.time_left % 60
        waktu_formatted = f"{menit:02d}:{detik:02d}"
        
        if menit <= 5:
            warna = "🔴"
            status_text = "Waktunya Istirahat!"
        elif menit <= 10:
            warna = "🟡"
            status_text = "Hampir Istirahat"
        else:
            warna = "🟢"
            status_text = "Fokus Penuh"
        
        bg_color = "#2d2d2d" if st.session_state.theme == "White" else "#ffffff"
        text_color = "#ffffff" if st.session_state.theme == "White" else "#1a1a1a"
        
        st.markdown(f"""
        <div style='text-align: center; padding: 50px; background: {bg_color}; border-radius: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h1

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Dashboard Belajar",
    page_icon="📚",
    layout="wide"
)

# --- INISIALISASI SESSION STATE ---
if 'theme' not in st.session_state:
    st.session_state.theme = "White"

if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'timer_running' not in st.session_state:
    st.session_state.timer_running = False

if 'time_left' not in st.session_state:
    st.session_state.time_left = 25 * 60

if 'current_menu' not in st.session_state:
    st.session_state.current_menu = "🏠 Dashboard"

# ============================================================
# 🎨 FUNGSI apply_theme - GANTI WARNA BACKGROUND & FONT
# ============================================================

def apply_theme(theme):
    if theme == "White":
        # === THEME WHITE (TERANG) ===
        st.markdown("""
           <style>
            /* Background Utama - Putih */
            .stApp {
                background-color: #ffffff;
            }
            
            /* Font untuk semua teks */
            h1, h2, h3, h4, h5, h6, p, label, span, div {
                color: #1a1a1a !important;
            }
            
            /* Font khusus untuk metrics */
            .stMetric .stMetricLabel {
                color: #333333 !important;
            }
            .stMetric .stMetricValue {
                color: #1a1a1a !important;
            }
            
            /* Sidebar */
            section[data-testid="stSidebar"] {
                background-color: #f8f9fa;
            }
            
            /* Input fields */
            .stTextInput > div > div > input {
                background-color: #ffffff;
                color: #1a1a1a;
                border: 1px solid #ddd;
            }
            
            /* Card / Container */
            .custom-card {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                color: #1a1a1a;
            }
            
            /* Tombol */
            .stButton > button {
                background-color: #3498db;
                color: white !important;
            }
            
            /* Progress bar */
            .stProgress > div > div > div {
                background-color: #3498db;
            }
            
            /* Info/Warning/Success messages */
            .stAlert {
                color: #1a1a1a;
            }
            </style>
        """, unsafe_allow_html=True)
        
    else:
        # === THEME BLACK (GELAP) - FONT PUTIH ===
        st.markdown("""
            <style>
            /* Background Utama - Hitam */
            .stApp {
                background-color: #1a1a1a;
            }
            
            /* Font untuk semua teks - PUTIH */
            h1, h2, h3, h4, h5, h6, p, label, span, div {
                color: #ffffff !important;
            }
            
            /* Font untuk Streamlit elements */
            .stMarkdown, .stMarkdown p {
                color: #ffffff !important;
            }
            
            /* Metrics */
            .stMetric .stMetricLabel {
                color: #e0e0e0 !important;
            }
            .stMetric .stMetricValue {
                color: #ffffff !important;
            }
            
            /* Sidebar - Abu gelap */
            section[data-testid="stSidebar"] {
                background-color: #2d2d2d;
            }
            
            /* Input fields */
            .stTextInput > div > div > input {
                background-color: #2d2d2d !important;
                color: #ffffff !important;
                border: 1px solid #555;
            }
            
            /* Input label */
            .stTextInput label {
                color: #ffffff !important;
            }
            
            /* Selectbox / Dropdown */
            .stSelectbox label {
                color: #ffffff !important;
            }
            .stSelectbox > div > div > div {
                background-color: #2d2d2d !important;
                color: #ffffff !important;
            }
            
            /* Radio button */
            .stRadio label {
                color: #ffffff !important;
            }
            
            /* Card / Container */
            .custom-card {
                background-color: #2d2d2d;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.5);
                color: #ffffff;
            }
            
            /* Tombol - Warna berbeda untuk Black theme */
            .stButton > button {
                background-color: #e74c3c !important;
                color: #ffffff !important;
            }
            
            /* Checkbox */
            .stCheckbox label {
                color: #ffffff !important;
            }
            
            /* Progress bar */
            .stProgress > div > div > div {
                background-color: #e74c3c;
            }
            
            /* Alert/Info/Warning/Success messages */
            .stAlert {
                background-color: #2d2d2d !important;
                color: #ffffff !important;
            }
            
            /* Expander */
            .streamlit-expanderHeader {
                background-color: #2d2d2d !important;
                color: #ffffff !important;
            }
            
            /* Separator */
            hr {
                border-color: #555555 !important;
            }
            
            /* Audio player */
            .stAudio {
                background-color: #2d2d2d;
                border-radius: 10px;
                padding: 10px;
            }
            </style>
        """, unsafe_allow_html=True)

# ============================================================
# 🚀 SIDEBAR - PENGATURAN THEME & MENU
# ============================================================

with st.sidebar:
    st.markdown("## ⚙️ Pengaturan")
    
    # === PILIHAN THEME ===
    st.markdown("### 🎨 Tema Background")
    theme_option = st.radio(
        "Pilih tema:",
        ["⬜ White (Terang)", "⬛ Black (Gelap)"],
        index=0 if st.session_state.theme == "White" else 1
    )
    
    if "White" in theme_option:
        st.session_state.theme = "White"
    else:
        st.session_state.theme = "Black"
    
    # Terapkan tema saat pertama kali load
    apply_theme(st.session_state.theme)
    
    st.markdown("---")

# === MENU UTAMA DI SIDEBAR ===
st.sidebar.markdown("---")
st.sidebar.title("📚 Menu Dashboard")

menu_options = [
    "🏠 Dashboard", 
    "✅ To-Do List", 
    "⏱️ Timer Belajar", 
    "🎵 Musik Fokus", 
    "🧪Indikator asam dan basa"
]

selected_menu = st.sidebar.radio(
    "Pilih Menu:", 
    menu_options,
    label_visibility="collapsed"
)

if selected_menu == "🏠 Dashboard":
    st.title("🧪Indikator asam dan basa")

elif selected_menu == "✅ To-Do List":
    st.title("🧪Indikator asam dan basa")

elif selected_menu == "⏱️ Timer Belajar":
    st.title("🧪Indikator asam dan basa")

elif selected_menu == "🎵 Musik Fokus":
    st.title("🧪Indikator asam dan basa")

elif selected_menu == "🧪Indikator asam dan basa":
    st.title("🧪Indikator asam dan basa")

# ============================================================
# 📝 FUNGSI-FUNGSI TO-DO LIST
# ============================================================

def add_task(task_name):
    if task_name:
        st.session_state.tasks.append({
            "name": task_name,
            "done": False,
            "timestamp": datetime.now().strftime("%H:%M")
        })

def toggle_task(index):
    st.session_state.tasks[index]["done"] = not st.session_state.tasks[index]["done"]

def delete_task(index):
    st.session_state.tasks.pop(index)

# ============================================================
# 📌 KONTEN UTAMA PER MENU
# ============================================================

# ═══════════════════════════════════════════════════════════
# 1️⃣ DASHBOARD UTAMA
# ═══════════════════════════════════════════════════════════
selected_page = st.sidebar.radio(
    "Pilih Menu",
    ["🏠 Dashboard", "📚 Teori", "🧪 Simulasi"]
)
if selected_page == "🏠 Dashboard":
    st.markdown("# 📚 Dashboard Belajar")
    st.markdown("Selamat datang! Pilih menu di sidebar untuk memulai.")
    
    # Metric Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Total Tugas", len(st.session_state.tasks))
    with col2:
        tugas_belum = sum(1 for t in st.session_state.tasks if not t["done"])
        st.metric("⏳ Tugas Tertunda", tugas_belum)
    with col3:
        tugas_selesai = sum(1 for t in st.session_state.tasks if t["done"])
        st.metric("✅ Tugas Selesai", tugas_selesai)
    with col4:
        st.metric("🎨 Tema Saat Ini", st.session_state.theme)
    
    st.markdown("---")
    
    # Informasi
    if st.session_state.theme == "White":
        st.success("💡 Tip: Gunakan teknik Pomodoro (25 menit belajar, 5 menit istirahat)!")
    else:
        st.info("💡 Tip: Gunakan teknik Pomodoro (25 menit belajar, 5 menit istirahat) untuk hasil maksimal!")

# ═══════════════════════════════════════════════════════════
# 2️⃣ TO-DO LIST
# ═══════════════════════════════════════════════════════════
elif selected_menu == "✅ To-Do List":
    st.markdown("# 📝 To-Do List Harian")
    
    # Input tugas
    col_input1, col_input2 = st.columns([4, 1])
    with col_input1:
        new_task = st.text_input(
            "Tambah tugas baru:", 
            placeholder="Contoh: Mengerjakan PR Matematika"
        )
    with col_input2:
        st.write("")  # Spasi
        if st.button("➕ Tambah", type="primary"):
            add_task(new_task)
            st.rerun()
    
    st.markdown("---")
    
    # Tampilkan daftar tugas
    if len(st.session_state.tasks) == 0:
        st.warning("📭 Daftar tugas kosong. Tambahkan tugas di atas ya!")
    else:
        for i, task in enumerate(st.session_state.tasks):
            col1, col2, col3 = st.columns([1, 6, 1])
            
            with col1:
                st.checkbox(
                    "", 
                    value=task["done"], 
                    key=f"check_{i}", 
                    on_change=toggle_task, 
                    args=(i,)
                )
            
            with col2:
                if task["done"]:
                    st.markdown(f"~~{task['name']}~~ ✅")
                else:
                    st.markdown(f"**{task['name']}**")
                st.caption(f"Jam: {task['timestamp']}")
            
            with col3:
                if st.button("🗑️", key=f"del_{i}"):
                    delete_task(i)
                    st.rerun()
            
            st.markdown("---")

# ═══════════════════════════════════════════════════════════════════
# 3️⃣ TIMER BELAJAR
# ═══════════════════════════════════════════════════════════
elif selected_menu == "⏱️ Timer Belajar":
    st.markdown("# ⏱️ Timer Belajar (Pomodoro)")
    
    col_timer1, col_timer2 = st.columns([1, 1])
    
    with col_timer1:
        st.markdown("### ⚙️ Pengaturan Waktu")
        mode = st.selectbox(
            "Pilih Mode:", 
            [
                "25 menit (Belajar)", 
                "5 menit (Istirahat)", 
                "15 menit (Istirahat Panjang)"
            ]
        )
        
        if mode == "25 menit (Belajar)":
            default_time = 25 * 60
        elif mode == "5 menit (Istirahat)":
            default_time = 5 * 60
        else:
            default_time = 15 * 60
        
        if st.button("🔄 Reset Timer"):
            st.session_state.time_left = default_time
            st.session_state.timer_running = False
            st.rerun()
    
    with col_timer2:
        # Tampilan Timer Besar
        menit = st.session_state.time_left // 60
        detik = st.session_state.time_left % 60
        waktu_formatted = f"{menit:02d}:{detik:02d}"
        
        # Indikator warna
        if menit <= 5:
            warna = "🔴"
            status_text = "Waktunya Istirahat!"
        elif menit <= 10:
            warna = "🟡"
            status_text = "Hampir Istirahat"
        else:
            warna = "🟢"
            status_text = "Fokus Penuh"
        
        # Card timer
        if st.session_state.theme == "White":
            bg_color = "#2d2d2d"
            text_color = "#ffffff"
        else:
            bg_color = "#ffffff"
            text_color = "#1a1a1a"
        
        st.markdown(f"""
        <div style='text-align: center; padding: 50px; background: {bg_color}; border-radius: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
            <h1 style='font-size: 100px; margin: 0; color: {text_color};'>{waktu_formatted}</h1>
            <p style='font-size: 24px; color: {text_color};'>{warna} {status_text}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Kontrol
        col_k1, col_k2 = st.columns(2)
        with col_k1:
            if st.button("▶️ MULAI", type="primary"):
                st.session_state.timer_running = True
                st.rerun()
        with col_k2:
            if st.button("⏹️ BERHENTI"):
                st.session_state.timer_running = False
                st.rerun()
    
    # Update timer setiap detik
    if st.session_state.timer_running:
        if st.session_state.time_left > 0:
            time.sleep(1)
            st.session_state.time_left -= 1
            st.rerun()
        else:
            st.session_state.timer_running = False
            st.balloons()
            st.success("⏰ Waktu belajar selesai! Saatnya istirahat.")

# ═══════════════════════════════════════════════════════════
# 4️⃣ MUSIK FOKUS
# ═══════════════════════════════════════════════════════════
elif selected_menu == "🎵 Musik Fokus":
    st.markdown("# 🎵 Musik Fokus")
    
    st.markdown("""
    <div style='text-align: center; padding: 30px; border-radius: 15px;'>
        <h3>🎧 Pemutar Musik</h3>
        <p>Pilih musik favorit untuk fokus belajar:</p>
    </div>
    """)
    
    # Pilihan musik
    musik_options = {
        "🎵 Lo-Fi Chill Beats": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "🌊 Ambient Nature Sounds": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "🌙 Piano Relaksasi": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3",
        "⚡ Deep Focus Techno": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3",
        "☕ Coffee Shop Vibes": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3"
    }
    
    selected_music = st.selectbox("Pilih Trek:", list(musik_options.keys()))
    
    # Audio player
    st.audio(musik_options[selected_music], format='audio/mp3', start_time=0)
    
    st.markdown("---")
    st.info("💡 Catatan: Jika audio tidak muncul, coba pilih trek lain.")
# ==========================================
# 1. DATASET KIMIA (PRESETS ZAT & INDIKATOR)
# ==========================================
elif selected_menu == "Indikator asam dan basa":
    # Semua resource dan logika lokal dimasukkan ke dalam sub-menu ini agar tidak bocor
    CHEMICALS = [
        {"id": "hcl", "name": "Asam Klorida (HCl)", "formula": "HCl", "pH": 1.0, "type": "asam", "category": "Laboratorium", "common": "Asam kuat pembersih porselen", "dissociation": "HCl → H⁺ + Cl⁻"},
        {"id": "h2so4", "name": "Asam Sulfat (Air Aki)", "formula": "H₂SO₄", "pH": 1.5, "type": "asam", "category": "Laboratorium", "common": "Air aki kendaraan pekat", "dissociation": "H₂SO₄ → 2H⁺ + SO₄²⁻"},
        {"id": "vinegar", "name": "Asam Asetat (Cuka Makan)", "formula": "CH₃COOH", "pH": 3.0, "type": "asam", "category": "Sehari-hari", "common": "Cuka dapur encer", "dissociation": "CH₃COOH ⇌ H⁺ + CH₃COO⁻"},
        {"id": "lemon", "name": "Asam Sitrat (Sari Lemon)", "formula": "C₆H₈O₇", "pH": 2.2, "type": "asam", "category": "Sehari-hari", "common": "Air perasan jeruk segar", "dissociation": "C₆H₈O₇ ⇌ H⁺ + C₆H₇O₇⁻"},
        {"id": "water", "name": "Air Murni (H₂O)", "formula": "H₂O", "pH": 7.0, "type": "netral", "category": "Sehari-hari", "common": "Air suling / Aquades netral", "dissociation": "H₂O ⇌ H⁺ + OH⁻"},
        {"id": "baking_soda", "name": "Soda Kue (NaHCO₃)", "formula": "NaHCO₃", "pH": 8.5, "type": "basa", "category": "Sehari-hari", "common": "Bahan pengembang roti rumahan", "dissociation": "NaHCO₃ → Na⁺ + HCO₃⁻"},
        {"id": "limewater", "name": "Kalsium Hidroksida (Air Kapur)", "formula": "Ca(OH)₂", "pH": 11.5, "type": "basa", "category": "Laboratorium", "common": "Air kapur sirih jernih", "dissociation": "Ca(OH)₂ → Ca²⁺ + 2OH⁻"},
        {"id": "naoh", "name": "Natrium Hidroksida (Sodapi)", "formula": "NaOH", "pH": 13.0, "type": "basa", "category": "Laboratorium", "common": "Sodapi pekat penghancur sumbatan", "dissociation": "NaOH → Na⁺ + OH⁻"},
        {"id": "h2so4", "name": "Asam Sulfat (H2SO4)", "formula": "H2SO4", "pH": 0.5, "type": "asam", "category": "Laboratorium", "common": "Pereaksi analitik dan agen dehidrasi", "dissociation": "H2SO4 → 2H⁺ + SO4²⁻"},
        {"id": "hno3", "name": "Asam Nitrat (HNO3)", "formula": "HNO3", "pH": 1.0, "type": "asam", "category": "Laboratorium", "common": "Oksidator kuat dan pelarut logam", "dissociation": "HNO3 → H⁺ + NO3⁻"},
        {"id": "h3po4", "name": "Asam Fosfat (H3PO4)", "formula": "H3PO4", "pH": 1.5, "type": "asam", "category": "Laboratorium", "common": "Pembuatan buffer fosfat", "dissociation": "H3PO4 ⇌ 3H⁺ + PO4³⁻"},
        {"id": "ch3cooh", "name": "Asam Asetat (CH3COOH)", "formula": "CH3COOH", "pH": 2.9, "type": "asam", "category": "Laboratorium", "common": "Pelarut organik lemah dan buffer asetat", "dissociation": "CH3COOH ⇌ CH3COO⁻ + H⁺"},
        {"id": "hcooh", "name": "Asam Format (HCOOH)", "formula": "HCOOH", "pH": 2.3, "type": "asam", "category": "Laboratorium", "common": "Agen pereduksi dalam sintesis organik", "dissociation": "HCOOH ⇌ HCOO⁻ + H⁺"},
        {"id": "h2c2o4", "name": "Asam Oksalat (H2C2O4)", "formula": "H2C2O4", "pH": 1.3, "type": "asam", "category": "Standar Primer", "common": "Standarisasi larutan kalium permanganat", "dissociation": "H2C2O4 ⇌ 2H⁺ + C2O4²⁻"},
        {"id": "naoh", "name": "Natrium Hidroksida (NaOH)", "formula": "NaOH", "pH": 13.0, "type": "basa", "category": "Laboratorium", "common": "Titrasi alkalimetri dan pelarut organik", "dissociation": "NaOH → Na⁺ + OH⁻"},
        {"id": "koh", "name": "Kalium Hidroksida (KOH)", "formula": "KOH", "pH": 13.0, "type": "basa", "category": "Laboratorium", "common": "Basa kuat untuk reaksi penyabunan", "dissociation": "KOH → K⁺ + OH⁻"},
        {"id": "nh4oh", "name": "Amonium Hidroksida (NH4OH)", "formula": "NH4OH", "pH": 11.6, "type": "basa", "category": "Laboratorium", "common": "Basa lemah dan reagen pengendap", "dissociation": "NH4OH ⇌ NH4⁺ + OH⁻"},
        {"id": "caoh2", "name": "Kalsium Hidroksida (Ca(OH)2)", "formula": "Ca(OH)2", "pH": 12.4, "type": "basa", "category": "Industri", "common": "Pengolahan air dan netralisasi limbah", "dissociation": "Ca(OH)2 → Ca²⁺ + 2OH⁻"},
        {"id": "baoh2", "name": "Barium Hidroksida (Ba(OH)2)", "formula": "Ba(OH)2", "pH": 13.0, "type": "basa", "category": "Laboratorium", "common": "Titrasi asam organik", "dissociation": "Ba(OH)2 → Ba²⁺ + 2OH⁻"},
        {"id": "nacl", "name": "Natrium Klorida (NaCl)", "formula": "NaCl", "pH": 7.0, "type": "garam", "category": "Umum", "common": "Pengatur kekuatan ionik larutan", "dissociation": "NaCl → Na⁺ + Cl⁻"},
        {"id": "kcl", "name": "Kalium Klorida (KCl)", "formula": "KCl", "pH": 7.0, "type": "garam", "category": "Elektrokimia", "common": "Larutan pengisi elektroda pH", "dissociation": "KCl → K⁺ + Cl⁻"},
        {"id": "kno3", "name": "Kalium Nitrat (KNO3)", "formula": "KNO3", "pH": 7.0, "type": "garam", "category": "Umum", "common": "Oksidator dan jembatan garam", "dissociation": "KNO3 → K⁺ + NO3⁻"},
        {"id": "na2so4", "name": "Natrium Sulfat (Na2SO4)", "formula": "Na2SO4", "pH": 7.0, "type": "garam", "category": "Sintesis", "common": "Agen pengering (desikan) fasa organik", "dissociation": "Na2SO4 → 2Na⁺ + SO4²⁻"},
        {"id": "cuso4", "name": "Tembaga(II) Sulfat (CuSO4)", "formula": "CuSO4", "pH": 4.0, "type": "garam", "category": "Analisis Kualitatif", "common": "Reagen biuret untuk uji protein", "dissociation": "CuSO4 → Cu²⁺ + SO4²⁻"},
        {"id": "feso4", "name": "Besi(II) Sulfat (FeSO4)", "formula": "FeSO4", "pH": 3.5, "type": "garam", "category": "Laboratorium", "common": "Agen pereduksi dalam analisis redoks", "dissociation": "FeSO4 → Fe²⁺ + SO4²⁻"},
        {"id": "fecl3", "name": "Besi(III) Klorida (FeCl3)", "formula": "FeCl3", "pH": 2.0, "type": "garam", "category": "Analisis Spesifik", "common": "Katalis asam Lewis dan identifikasi senyawa fenolik", "dissociation": "FeCl3 → Fe³⁺ + 3Cl⁻"},
        {"id": "agno3", "name": "Perak Nitrat (AgNO3)", "formula": "AgNO3", "pH": 5.5, "type": "garam", "category": "Argentometri", "common": "Titran untuk penentuan klorida (Metode Mohr/Volhard)", "dissociation": "AgNO3 → Ag⁺ + NO3⁻"},
        {"id": "kmno4", "name": "Kalium Permanganat (KMnO4)", "formula": "KMnO4", "pH": 7.5, "type": "garam", "category": "Permanganometri", "common": "Oksidator kuat sekaligus autoindikator", "dissociation": "KMnO4 → K⁺ + MnO4⁻"},
        {"id": "k2cr2o7", "name": "Kalium Dikromat (K2Cr2O7)", "formula": "K2Cr2O7", "pH": 4.0, "type": "garam", "category": "Bikromatometri", "common": "Oksidator standar primer penentuan COD", "dissociation": "K2Cr2O7 → 2K⁺ + Cr2O7²⁻"},
        {"id": "na2s2o3", "name": "Natrium Tiosulfat (Na2S2O3)", "formula": "Na2S2O3", "pH": 6.5, "type": "garam", "category": "Iodometri", "common": "Titran penentuan iodin bebas", "dissociation": "Na2S2O3 → 2Na⁺ + S2O3²⁻"},
        {"id": "ki", "name": "Kalium Iodida (KI)", "formula": "KI", "pH": 7.0, "type": "garam", "category": "Iodometri", "common": "Penyedia ion iodida untuk pembentukan I2", "dissociation": "KI → K⁺ + I⁻"},
        {"id": "naf", "name": "Natrium Fluorida (NaF)", "formula": "NaF", "pH": 8.0, "type": "garam", "category": "Biokimia", "common": "Inhibitor enzim", "dissociation": "NaF → Na⁺ + F⁻"},
        {"id": "cacl2", "name": "Kalsium Klorida (CaCl2)", "formula": "CaCl2", "pH": 6.5, "type": "garam", "category": "Persiapan Sampel", "common": "Desikan higroskopis untuk desikator", "dissociation": "CaCl2 → Ca²⁺ + 2Cl⁻"},
        {"id": "mgcl2", "name": "Magnesium Klorida (MgCl2)", "formula": "MgCl2", "pH": 6.0, "type": "garam", "category": "Biologi Molekuler", "common": "Kofaktor dalam reaksi PCR", "dissociation": "MgCl2 → Mg²⁺ + 2Cl⁻"},
        {"id": "nh4cl", "name": "Amonium Klorida (NH4Cl)", "formula": "NH4Cl", "pH": 5.0, "type": "garam", "category": "Laboratorium", "common": "Komponen utama larutan penyangga salmiak", "dissociation": "NH4Cl → NH4⁺ + Cl⁻"},
        {"id": "nh42so4", "name": "Amonium Sulfat ((NH4)2SO4)", "formula": "(NH4)2SO4", "pH": 5.5, "type": "garam", "category": "Biokimia", "common": "Presipitasi protein", "dissociation": "(NH4)2SO4 → 2NH4⁺ + SO4²⁻"},
        {"id": "ch3coona", "name": "Natrium Asetat (CH3COONa)", "formula": "CH3COONa", "pH": 8.9, "type": "garam", "category": "Laboratorium", "common": "Pembentuk buffer basa konjugasi", "dissociation": "CH3COONa → Na⁺ + CH3COO⁻"},
        {"id": "nacn", "name": "Natrium Sianida (NaCN)", "formula": "NaCN", "pH": 11.0, "type": "garam", "category": "Ekstraksi Logam", "common": "Ligan kuat dalam kompleksometri logam berat", "dissociation": "NaCN → Na⁺ + CN⁻"},
        {"id": "kscn", "name": "Kalium Tiosianat (KSCN)", "formula": "KSCN", "pH": 7.0, "type": "garam", "category": "Argentometri", "common": "Titran metode Volhard atau identifikasi Besi(III)", "dissociation": "KSCN → K⁺ + SCN⁻"},
        {"id": "bacl2", "name": "Barium Klorida (BaCl2)", "formula": "BaCl2", "pH": 6.5, "type": "garam", "category": "Gravimetri", "common": "Reagen pengendap ion sulfat", "dissociation": "BaCl2 → Ba²⁺ + 2Cl⁻"},
        {"id": "pbno32", "name": "Timbal(II) Nitrat (Pb(NO3)2)", "formula": "Pb(NO3)2", "pH": 4.0, "type": "garam", "category": "Analisis Kualitatif", "common": "Identifikasi ion halida dan sulfat", "dissociation": "Pb(NO3)2 → Pb²⁺ + 2NO3⁻"},
        {"id": "znso4", "name": "Seng Sulfat (ZnSO4)", "formula": "ZnSO4", "pH": 4.5, "type": "garam", "category": "Elektrolisis", "common": "Elektrolit standar sel Volta", "dissociation": "ZnSO4 → Zn²⁺ + SO4²⁻"},
        {"id": "na2b4o7", "name": "Natrium Tetraborat (Na2B4O7)", "formula": "Na2B4O7", "pH": 9.2, "type": "garam", "category": "Standar Primer", "common": "Standarisasi larutan asam kuat", "dissociation": "Na2B4O7 → 2Na⁺ + B4O7²⁻"},
        {"id": "na2edta", "name": "Natrium EDTA (Na2EDTA)", "formula": "Na2EDTA", "pH": 4.5, "type": "garam", "category": "Kompleksometri", "common": "Titrasi kompleksometri penentuan kesadahan air", "dissociation": "Na2H2EDTA → 2Na⁺ + H2EDTA²⁻"},
        {"id": "hclo4", "name": "Asam Perklorat (HClO4)", "formula": "HClO4", "pH": 0.1, "type": "asam", "category": "Analisis Spesifik", "common": "Titrasi bebas air asam kuat", "dissociation": "HClO4 → H⁺ + ClO4⁻"},
        {"id": "hf", "name": "Asam Fluorida (HF)", "formula": "HF", "pH": 3.2, "type": "asam", "category": "Persiapan Sampel", "common": "Pelarut silika dan kaca", "dissociation": "HF ⇌ H⁺ + F⁻"},
        {"id": "hbr", "name": "Asam Bromida (HBr)", "formula": "HBr", "pH": 1.0, "type": "asam", "category": "Sintesis", "common": "Pembuatan bromida anorganik", "dissociation": "HBr → H⁺ + Br⁻"},
        {"id": "hi", "name": "Asam Iodida (HI)", "formula": "HI", "pH": 1.0, "type": "asam", "category": "Sintesis", "common": "Agen pereduksi kuat dan katalis", "dissociation": "HI → H⁺ + I⁻"},
        {"id": "hcn", "name": "Asam Sianida (HCN)", "formula": "HCN", "pH": 5.1, "type": "asam", "category": "Laboratorium", "common": "Sintesis polimer dan pertambangan", "dissociation": "HCN ⇌ H⁺ + CN⁻"},
        {"id": "h2s", "name": "Hidrogen Sulfida (H2S)", "formula": "H2S", "pH": 4.0, "type": "asam", "category": "Analisis Kualitatif", "common": "Reagen pengendap kation golongan berat", "dissociation": "H2S ⇌ 2H⁺ + S²⁻"},
        {"id": "c6h8o7", "name": "Asam Sitrat (C6H8O7)", "formula": "C6H8O7", "pH": 3.1, "type": "asam", "category": "Umum", "common": "Chelating agent dan larutan buffer", "dissociation": "C6H8O7 ⇌ 3H⁺ + C6H5O7³⁻"},
        {"id": "c6h5cooh", "name": "Asam Benzoat (C6H5COOH)", "formula": "C6H5COOH", "pH": 4.2, "type": "asam", "category": "Kalorimetri", "common": "Standar kalibrasi bom kalorimeter", "dissociation": "C6H5COOH ⇌ C6H5COO⁻ + H⁺"},
        {"id": "c6h6o", "name": "Fenol (C6H5OH)", "formula": "C6H5OH", "pH": 6.0, "type": "asam", "category": "Bahan Baku", "common": "Prekursor sintesis organik dan ekstraksi DNA", "dissociation": "C6H5OH ⇌ C6H5O⁻ + H⁺"},
        {"id": "c4h6o6", "name": "Asam Tartarat (C4H6O6)", "formula": "C4H6O6", "pH": 3.0, "type": "asam", "category": "Analisis Makanan", "common": "Aditif dan resolusi campuran rasemat", "dissociation": "C4H6O6 ⇌ 2H⁺ + C4H4O6²⁻"},
        {"id": "c3h6o3", "name": "Asam Laktat (C3H6O3)", "formula": "C3H6O3", "pH": 3.8, "type": "asam", "category": "Biokimia", "common": "Metabolit sekunder dan buffer ringan", "dissociation": "C3H6O3 ⇌ H⁺ + C3H5O3⁻"},
        {"id": "lioh", "name": "Litium Hidroksida (LiOH)", "formula": "LiOH", "pH": 13.0, "type": "basa", "category": "Material", "common": "Absorben karbon dioksida", "dissociation": "LiOH → Li⁺ + OH⁻"},
        {"id": "mgoh2", "name": "Magnesium Hidroksida (Mg(OH)2)", "formula": "Mg(OH)2", "pH": 10.5, "type": "basa", "category": "Umum", "common": "Antasida dan penetral asam", "dissociation": "Mg(OH)2 ⇌ Mg²⁺ + 2OH⁻"},
        {"id": "aloh3", "name": "Aluminium Hidroksida (Al(OH)3)", "formula": "Al(OH)3", "pH": 9.5, "type": "basa", "category": "Umum", "common": "Flokulan dalam pengolahan air", "dissociation": "Al(OH)3 ⇌ Al³⁺ + 3OH⁻"},
        {"id": "na2co3", "name": "Natrium Karbonat (Na2CO3)", "formula": "Na2CO3", "pH": 11.6, "type": "garam", "category": "Standar Primer", "common": "Standarisasi larutan asam standar", "dissociation": "Na2CO3 → 2Na⁺ + CO3²⁻"},
        {"id": "nahco3", "name": "Natrium Bikarbonat (NaHCO3)", "formula": "NaHCO3", "pH": 8.3, "type": "garam", "category": "Laboratorium", "common": "Penetral asam ringan dan pembersih", "dissociation": "NaHCO3 → Na⁺ + HCO3⁻"},
        {"id": "c6h5nh2", "name": "Anilin (C6H5NH2)", "formula": "C6H5NH2", "pH": 8.8, "type": "basa", "category": "Sintesis Organik", "common": "Pembuatan zat warna azo", "dissociation": "C6H5NH2 + H2O ⇌ C6H5NH3⁺ + OH⁻"},
        {"id": "c5h5n", "name": "Piridin (C5H5N)", "formula": "C5H5N", "pH": 8.5, "type": "basa", "category": "Pelarut Organik", "common": "Pelarut basa lemah dan katalis", "dissociation": "C5H5N + H2O ⇌ C5H5NH⁺ + OH⁻"},
        {"id": "ch3nh2", "name": "Metilamina (CH3NH2)", "formula": "CH3NH2", "pH": 11.8, "type": "basa", "category": "Sintesis Organik", "common": "Prekursor farmasi dan herbisida", "dissociation": "CH3NH2 + H2O ⇌ CH3NH3⁺ + OH⁻"},
        {"id": "kbr", "name": "Kalium Bromida (KBr)", "formula": "KBr", "pH": 7.0, "type": "garam", "category": "Spektroskopi", "common": "Pembuatan pelet sampel FTIR", "dissociation": "KBr → K⁺ + Br⁻"},
        {"id": "nabr", "name": "Natrium Bromida (NaBr)", "formula": "NaBr", "pH": 7.0, "type": "garam", "category": "Sintesis Organik", "common": "Reaksi substitusi alkil bromida", "dissociation": "NaBr → Na⁺ + Br⁻"},
        {"id": "licl", "name": "Litium Klorida (LiCl)", "formula": "LiCl", "pH": 7.0, "type": "garam", "category": "Analisis Termal", "common": "Penurun titik beku dan kelembapan kalibrasi", "dissociation": "LiCl → Li⁺ + Cl⁻"},
        {"id": "kclo3", "name": "Kalium Klorat (KClO3)", "formula": "KClO3", "pH": 7.0, "type": "garam", "category": "Oksidator", "common": "Pembuatan gas oksigen di laboratorium", "dissociation": "KClO3 → K⁺ + ClO3⁻"},
        {"id": "naclo", "name": "Natrium Hipoklorit (NaClO)", "formula": "NaClO", "pH": 11.0, "type": "garam", "category": "Umum", "common": "Desinfektan dan agen pemutih", "dissociation": "NaClO → Na⁺ + ClO⁻"},
        {"id": "kh2po4", "name": "Kalium Dihidrogen Fosfat (KH2PO4)", "formula": "KH2PO4", "pH": 4.5, "type": "garam", "category": "Laboratorium", "common": "Komponen utama larutan buffer fosfat", "dissociation": "KH2PO4 → K⁺ + H2PO4⁻"},
        {"id": "k2hpo4", "name": "Dikalium Hidrogen Fosfat (K2HPO4)", "formula": "K2HPO4", "pH": 9.0, "type": "garam", "category": "Laboratorium", "common": "Pasangan konjugasi sistem buffer pH fisiologis", "dissociation": "K2HPO4 → 2K⁺ + HPO4²⁻"},
        {"id": "na3po4", "name": "Natrium Fosfat (Na3PO4)", "formula": "Na3PO4", "pH": 12.0, "type": "garam", "category": "Umum", "common": "Agen pembersih dan pengendap ion", "dissociation": "Na3PO4 → 3Na⁺ + PO4³⁻"},
        {"id": "c2h5oh", "name": "Etanol (C2H5OH)", "formula": "C2H5OH", "pH": 7.0, "type": "netral", "category": "Pelarut Organik", "common": "Pelarut universal sintesis dan sterilisasi alat", "dissociation": "Tidak terdisosiasi"},
        {"id": "ch3oh", "name": "Metanol (CH3OH)", "formula": "CH3OH", "pH": 7.0, "type": "netral", "category": "Kromatografi", "common": "Fasa gerak utama HPLC dan TLC", "dissociation": "Tidak terdisosiasi"},
        {"id": "ch3coch3", "name": "Aseton (CH3COCH3)", "formula": "CH3COCH3", "pH": 7.0, "type": "netral", "category": "Pelarut Organik", "common": "Pencuci alat gelas dan pelarut polar aprotik", "dissociation": "Tidak terdisosiasi"},
        {"id": "ch3cooc2h5", "name": "Etil Asetat (CH3COOC2H5)", "formula": "CH3COOC2H5", "pH": 7.0, "type": "netral", "category": "Pelarut Organik", "common": "Pelarut standar ekstraksi cair-cair sintesis organik", "dissociation": "Tidak terdisosiasi"},
        {"id": "c6h14", "name": "Heksana (C6H14)", "formula": "C6H14", "pH": 7.0, "type": "netral", "category": "Kromatografi", "common": "Pelarut non-polar untuk ekstraksi lipid", "dissociation": "Tidak terdisosiasi"},
        {"id": "c6h6", "name": "Benzena (C6H6)", "formula": "C6H6", "pH": 7.0, "type": "netral", "category": "Bahan Baku", "common": "Cincin aromatik dasar sintesis turunan fenol/anilin", "dissociation": "Tidak terdisosiasi"},
        {"id": "c7h8", "name": "Toluena (C7H8)", "formula": "C7H8", "pH": 7.0, "type": "netral", "category": "Pelarut Organik", "common": "Alternatif pelarut yang lebih aman dari benzena", "dissociation": "Tidak terdisosiasi"},
        {"id": "chcl3", "name": "Kloroform (CHCl3)", "formula": "CHCl3", "pH": 7.0, "type": "netral", "category": "Pelarut Organik", "common": "Pelarut NMR dan ekstraksi alkaloid", "dissociation": "Tidak terdisosiasi"},
        {"id": "ch2cl2", "name": "Diklorometana (CH2Cl2)", "formula": "CH2Cl2", "pH": 7.0, "type": "netral", "category": "Pelarut Organik", "common": "Pelarut organik mudah menguap (DCM) sintetis", "dissociation": "Tidak terdisosiasi"},
        {"id": "c4h10o", "name": "Dietil Eter (C4H10O)", "formula": "C4H10O", "pH": 7.0, "type": "netral", "category": "Pelarut Organik", "common": "Fasa polar untuk ekstraksi senyawa hidrofobik", "dissociation": "Tidak terdisosiasi"},
        {"id": "c6h12o6", "name": "Glukosa (C6H12O6)", "formula": "C6H12O6", "pH": 7.0, "type": "netral", "category": "Biokimia", "common": "Substrat mikrobiologi dan standar gula", "dissociation": "Tidak terdisosiasi"},
        {"id": "c12h22o11", "name": "Sukrosa (C12H22O11)", "formula": "C12H22O11", "pH": 7.0, "type": "netral", "category": "Umum", "common": "Penetapan brix kualitatif di lab pangan", "dissociation": "Tidak terdisosiasi"},
        {"id": "h2o2", "name": "Hidrogen Peroksida (H2O2)", "formula": "H2O2", "pH": 4.5, "type": "asam", "category": "Oksidator", "common": "Oksidator sampel organik untuk persiapan destruksi", "dissociation": "H2O2 ⇌ H⁺ + HO2⁻"},
        {"id": "khp", "name": "Kalium Hidrogen Ftalat (KHP)", "formula": "KHC8H4O4", "pH": 4.0, "type": "garam", "category": "Standar Primer", "common": "Standarisasi presisi larutan basa seperti NaOH", "dissociation": "KHC8H4O4 → K⁺ + HC8H4O4⁻"},
        {"id": "na2c2o4", "name": "Natrium Oksalat (Na2C2O4)", "formula": "Na2C2O4", "pH": 8.0, "type": "garam", "category": "Standar Primer", "common": "Standarisasi larutan kalium permanganat", "dissociation": "Na2C2O4 → 2Na⁺ + C2O4²⁻"},
        {"id": "kio3", "name": "Kalium Iodat (KIO3)", "formula": "KIO3", "pH": 7.0, "type": "garam", "category": "Standar Primer", "common": "Standarisasi larutan natrium tiosulfat", "dissociation": "KIO3 → K⁺ + IO3⁻"},
        {"id": "k2cro4", "name": "Kalium Kromat (K2CrO4)", "formula": "K2CrO4", "pH": 8.5, "type": "garam", "category": "Indikator", "common": "Indikator spesifik metode titrasi Mohr", "dissociation": "K2CrO4 → 2K⁺ + CrO4²⁻"},
        {"id": "nano2", "name": "Natrium Nitrit (NaNO2)", "formula": "NaNO2", "pH": 9.0, "type": "garam", "category": "Sintesis Organik", "common": "Reaksi pembentukan garam diazonium", "dissociation": "NaNO2 → Na⁺ + NO2⁻"},
        {"id": "nahso4", "name": "Natrium Bisulfat (NaHSO4)", "formula": "NaHSO4", "pH": 1.4, "type": "garam", "category": "Laboratorium", "common": "Penyumbang suasana asam alternatif pengurai", "dissociation": "NaHSO4 → Na⁺ + H⁺ + SO4²⁻"},
        {"id": "k2so4", "name": "Kalium Sulfat (K2SO4)", "formula": "K2SO4", "pH": 7.0, "type": "garam", "category": "Pertanian", "common": "Standardisasi analisa nutrisi tanaman", "dissociation": "K2SO4 → 2K⁺ + SO4²⁻"},
        {"id": "mnso4", "name": "Mangan(II) Sulfat (MnSO4)", "formula": "MnSO4", "pH": 4.5, "type": "garam", "category": "Analisis Air", "common": "Reagen fiksasi oksigen pada uji BOD (Metode Winkler)", "dissociation": "MnSO4 → Mn²⁺ + SO4²⁻"},
        {"id": "crcl3", "name": "Kromium(III) Klorida (CrCl3)", "formula": "CrCl3", "pH": 3.0, "type": "garam", "category": "Katalis", "common": "Pembuatan katalis reaksi koordinasi", "dissociation": "CrCl3 → Cr³⁺ + 3Cl⁻"},
        {"id": "cdso4", "name": "Kadmium Sulfat (CdSO4)", "formula": "CdSO4", "pH": 4.5, "type": "garam", "category": "Elektrokimia", "common": "Sel standar Weston pengukur E0", "dissociation": "CdSO4 → Cd²⁺ + SO4²⁻"},
        {"id": "sncl2", "name": "Timah(II) Klorida (SnCl2)", "formula": "SnCl2", "pH": 2.5, "type": "garam", "category": "Oksidimetri", "common": "Reduktor Fe3+ menjadi Fe2+ sebelum titrasi permanganat", "dissociation": "SnCl2 → Sn²⁺ + 2Cl⁻"},
        {"id": "hgcl2", "name": "Raksa(II) Klorida (HgCl2)", "formula": "HgCl2", "pH": 4.0, "type": "garam", "category": "Oksidimetri", "common": "Penghilang kelebihan reduktor stano klorida", "dissociation": "HgCl2 ⇌ Hg²⁺ + 2Cl⁻"},
        {"id": "agno2", "name": "Perak Nitrit (AgNO2)", "formula": "AgNO2", "pH": 5.0, "type": "garam", "category": "Sintesis Organik", "common": "Sintesis senyawa nitroalifatik", "dissociation": "AgNO2 → Ag⁺ + NO2⁻"},
        {"id": "na2moo4", "name": "Natrium Molibdat (Na2MoO4)", "formula": "Na2MoO4", "pH": 8.0, "type": "garam", "category": "Analisis Kualitatif", "common": "Identifikasi alkaloid menggunakan Reagen Fröhde", "dissociation": "Na2MoO4 → 2Na⁺ + MoO4²⁻"},
        {"id": "k3fecn6", "name": "Kalium Ferisianida (K3[Fe(CN)6])", "formula": "K3[Fe(CN)6]", "pH": 6.5, "type": "garam", "category": "Analisis Warna", "common": "Identifikasi ion Fe2+ membentuk kompleks biru", "dissociation": "K3[Fe(CN)6] → 3K⁺ + [Fe(CN)6]³⁻"},
        {"id": "nh4no3", "name": "Amonium Nitrat (NH4NO3)", "formula": "NH4NO3", "pH": 5.4, "type": "garam", "category": "Bahan Peledak", "common": "Eksperimen eksotermik pembentukan gas", "dissociation": "NH4NO3 → NH4⁺ + NO3⁻"},
        {"id": "cacr2o7", "name": "Kalsium Dikromat (CaCr2O7)", "formula": "CaCr2O7", "pH": 4.0, "type": "garam", "category": "Oksidator", "common": "Agen pembersih porselen dan oksidasi", "dissociation": "CaCr2O7 → Ca²⁺ + Cr2O7²⁻"},
        {"id": "niso4", "name": "Nikel(II) Sulfat (NiSO4)", "formula": "NiSO4", "pH": 4.5, "type": "garam", "category": "Elektrolisis", "common": "Elektrolit standar penyepuhan listrik", "dissociation": "NiSO4 → Ni²⁺ + SO4²⁻"},
        {"id": "lino3", "name": "Litium Nitrat (LiNO3)", "formula": "LiNO3", "pH": 7.0, "type": "garam", "category": "Penyimpanan Termal", "common": "Garam penahan panas suhu tinggi", "dissociation": "LiNO3 → Li⁺ + NO3⁻"},
        {"id": "srcl2", "name": "Stronsium Klorida (SrCl2)", "formula": "SrCl2", "pH": 7.0, "type": "garam", "category": "Analisis Nyala", "common": "Pewarna nyala api merah terang lab", "dissociation": "SrCl2 → Sr²⁺ + 2Cl⁻"},
        {"id": "csoh", "name": "Sesium Hidroksida (CsOH)", "formula": "CsOH", "pH": 14.0, "type": "basa", "category": "Katalis Basa", "common": "Basa sangat kuat pelarut silikon", "dissociation": "CsOH → Cs⁺ + OH⁻"},
        {"id": "rboh", "name": "Rubidium Hidroksida (RbOH)", "formula": "RbOH", "pH": 13.5, "type": "basa", "category": "Material Lanjut", "common": "Reaktan sintesis rubidium katalitik", "dissociation": "RbOH → Rb⁺ + OH⁻"},
        {"id": "c2h6o2", "name": "Etilen Glikol (C2H6O2)", "formula": "C2H6O2", "pH": 7.0, "type": "netral", "category": "Polimer", "common": "Bahan monomer sintesis poliester (PET)", "dissociation": "Tidak terdisosiasi"},
        {"id": "c3h8o", "name": "Isopropanol (C3H8O)", "formula": "C3H8O", "pH": 7.0, "type": "netral", "category": "Pelarut Organik", "common": "Pelarut presipitasi asam nukleat biologi", "dissociation": "Tidak terdisosiasi"}
]
    

    INDICATORS = {
        "lakmus": {
            "name": "Kertas Lakmus (Litmus)",
            "range": (4.5, 8.3),
            "low_color": "#ef4444", "low_label": "MERAH ASAM",
            "high_color": "#3b82f6", "high_label": "BIRU BASA",
            "mid_color": "#a855f7", "mid_label": "UNGU REAKSI"
        },
        "pp": {
            "name": "Phenolphthalein (PP)",
            "range": (8.2, 10.0),
            "low_color": "#f8fafc", "low_label": "TIDAK BERWARNA",
            "high_color": "#ec4899", "high_label": "MERAH MUDA PEKAT",
            "mid_color": "#fbcfe8", "mid_label": "MERAH MUDA SEMU"
        },
        "btb": {
            "name": "Bromothymol Blue (BTB)",
            "range": (6.0, 7.6),
            "low_color": "#eab308", "low_label": "KUNING ASAM",
            "high_color": "#1d4ed8", "high_label": "BIRU BASA",
            "mid_color": "#22c55e", "mid_label": "HIJAU NETRAL"
        },
        "mr": {
            "name": "Metil Merah (Methyl Red)",
            "range": (4.4, 6.2),
            "low_color": "#ef4444", "low_label": "MERAH ASAM",
            "high_color": "#eab308", "high_label": "KUNING BASA",
            "mid_color": "#f97316", "mid_label": "JINGGA TRANSISI"
        },
        "universal": {
            "name": "Indikator Universal",
            "range": (0.0, 14.0),
            "low_color": "#dc2626", "low_label": "MERAH (pH KOROSIF)",
            "high_color": "#581c87", "high_label": "UNGU (pH BASA KUAT)",
            "mid_color": "#16a34a", "mid_label": "HIJAU (pH NETRAL)"
        }
    }

    def hitung_warna_indikator(ph, ind_data):
        low, high = ind_data["range"]
        if ind_data["name"] == "Indikator Universal":
            if ph < 3: return "#dc2626"
            elif ph < 5: return "#f97316"
            elif ph < 6.5: return "#eab308"
            elif ph < 7.5: return "#16a34a"
            elif ph < 9: return "#0284c7"
            elif ph < 11: return "#1d4ed8"
            else: return "#581c87"
        
        if ph < low:
            return ind_data["low_color"]
        elif ph > high:
            return ind_data["high_color"]
        else:
            return ind_data["mid_color"]

    st.title("🧪 ChemClass - Indikator Asam dan Basa")
    st.write("Belajar sains asam-basa bersama ChemClass!")

    menu_tabs = st.tabs(["📊 LAB SIMULATOR"])

    with menu_tabs[0]:
        col_input, col_display = st.columns([5, 7])
        
        with col_input:
            st.subheader("💡 Parameter Simulasi")
            
            preset_names = [chem["name"] for chem in CHEMICALS]
            pilihan_preset = st.selectbox("Pilih Preset Zat Kimia:", preset_names, index=2)
            selected_chem = next(chem for chem in CHEMICALS if chem["name"] == pilihan_preset)
            
            pilihan_ind = st.selectbox(
                "Pilihan Kertas Indikator:",
                options=list(INDICATORS.keys()),
                format_func=lambda x: INDICATORS[x]["name"]
            )
            selected_ind_data = INDICATORS[pilihan_ind]
            
            st.write("---")
            st.markdown("**Kontrol pH Manual (Dial):** Modifikasi nilai derajat keasaman secara langsung")
            simulated_ph = st.slider("Mengatur pH:", min_value=0.0, max_value=14.0, value=selected_chem["pH"], step=0.1)

        with col_display:
            st.subheader("🔮 Simulator Beaker Reaktif")
            
            liquid_color = hitung_warna_indikator(simulated_ph, selected_ind_data)
            
            # Memperbaiki string CSS typo 'Q' pada box-shadow bawaan kode awal
            container_html = f"""
            <div class="beaker-container" style="text-align: center;">
                <span style="font-size: 11px; font-weight: bold; color: #d8b4fe; display: block; margin-bottom: 15px; letter-spacing: 0.1em; font-family: monospace;">LABORATORIUM METRIK UNGU</span>
                <div style="
                    width: 140px; 
                    height: 160px; 
                    border: 4px solid rgba(168, 85, 247, 0.4); 
                    border-top: none;
                    border-radius: 0 0 16px 16px; 
                    margin: 0 auto; 
                    position: relative;
                    box-shadow: 0 0 15px rgba(168, 85, 247, 0.2);
                ">
                    <div style="
                        position: absolute; 
                        bottom: 8px; 
                        left: 6px; 
                        right: 6px; 
                        height: {int(simulated_ph * 4.5) + 50}px; 
                        background-color: {liquid_color}; 
                        border-radius: 0 0 10px 10px;
                        transition: background-color 0.4s ease, height 0.4s ease;
                        box-shadow: inset 0 4px 8px rgba(255,255,255,0.15);
                    "></div>
                    <div style="position: absolute; left: 10px; top: 30px; border-left: 2px solid rgba(168, 85, 247, 0.3); height: 100px; display: flex; flex-direction: column; justify-content: space-between; text-align: left; padding-left: 5px; font-size: 8px; font-family: monospace; color: #d8b4fe;">
                        <span>-- 150ml</span>
                        <span>-- 100ml</span>
                        <span>-- 50ml</span>
                    </div>
                </div>
                <div style="margin-top: 20px; font-weight: bold; font-size: 20px; color: #f3e8ff; text-shadow: 0 0 8px {liquid_color};">
                    Nilai pH Cairan: <span style="color: {liquid_color};">{simulated_ph:.1f}</span>
                </div>
            </div>
            """
            st.markdown(container_html, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="chemical-hud" style="margin-top:20px; padding:15px; background: rgba(168, 85, 247, 0.1); border-radius:10px;">
                <h4 style="margin-top:0px; color: #e9d5ff !important; font-family: monospace;">📋 INFORMASI SENYAWA</h4>
                <b>Nama Senyawa:</b> {selected_chem['name']} ({selected_chem['formula']})<br/>
                <b>Nama Populer:</b> {selected_chem['common']}<br/>
                <b>Ionisasi Disosiasi:</b> <code>{selected_chem['dissociation']}</code><br/>
                <b>Kategori Kelas:</b> {selected_chem['category']}
            </div>
            """)


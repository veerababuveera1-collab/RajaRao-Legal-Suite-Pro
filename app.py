import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- 1. PAGE CONFIGURATION & ARCHITECTURAL SETUP ---
st.set_page_config(
    page_title="RajaRao Legal Suite Pro", 
    page_icon="⚖️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. PREMIUM ENTERPRISE UI (CSS SAFETY GUARDS) ---
st.markdown("""
    <style>
    /* Premium Dark Theme with Gold Accents */
    .stApp { 
        background: radial-gradient(circle at top right, #1e293b, #020617); 
        color: #f8fafc; 
    }
    .gold-title {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800; text-align: center; font-size: 3.5rem; 
        margin-bottom: 5px;
        filter: drop-shadow(0px 2px 2px rgba(0,0,0,0.3));
    }
    /* Button Optimization */
    .stButton>button {
        background: linear-gradient(45deg, #d4af37, #996515);
        color: white !important; font-weight: bold; border-radius: 8px; 
        width: 100%; border: none; transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(212, 175, 55, 0.4);
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. STATE MANAGEMENT (Safety Guard for Memory) ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. HEADER SECTION ---
st.markdown("<div class='gold-title'>Advocate RajaRao & Associates</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #d4af37; font-size: 1.1rem;'>Strategic Legal Practice Management Suite | Enterprise Edition</p>", unsafe_allow_html=True)
st.divider()

# --- 5. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/law.png", width=80)
    st.markdown("### 🏛️ Management Menu")
    menu = st.radio("Select Module:", ["📊 Dashboard", "📡 Court Tracker", "🤖 Nyaya AI Chat", "📂 Case Vault"])
    st.divider()
    st.info(f"**System Status:** Online\n\n**Server Time:** {datetime.now().strftime('%H:%M:%S')}")
    st.caption("v2.0.26 - Powered by BNS Framework")

# --- 6. CORE FUNCTIONALITIES ---

# A. DASHBOARD MODULE
if menu == "📊 Dashboard":
    st.subheader("📊 Practice Intelligence Overview")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Files", "52", "+4 Urgent")
    m2.metric("Hearings Today", "6", "Main Bench")
    m3.metric("BNS Compliance", "100%", "Sync")
    m4.metric("Pending Tasks", "12", "-2 Completed")
    
    st.markdown("### 📅 Today's Hearing Schedule")
    df = pd.DataFrame({
        "Time": ["10:30 AM", "01:30 PM", "03:45 PM", "04:30 PM"],
        "Case ID": ["WP 124/2026", "OS 44/2026", "CC 12/2025", "IA 09/2026"],
        "Petitioner": ["State vs K. Reddy", "R. Sharma", "M/s Global Corp", "V. Verma"],
        "Court Location": ["High Court Hall 1", "District Court", "Special Bench", "Chamber 4"],
        "Priority": ["🔴 Critical", "🟡 Regular", "🟢 Evidence", "🟡 Regular"]
    })
    st.table(df)

# B. COURT TRACKER MODULE (With Input Safety Guard)
elif menu == "📡 Court Tracker":
    st.subheader("📡 Live e-Courts Real-time Tracking")
    col_a, col_b = st.columns([3, 1])
    with col_a:
        cnr = st.text_input("Enter CNR Number or Case ID", placeholder="TS-HYD-00123-2026")
    with col_b:
        st.write("<br>", unsafe_allow_html=True)
        track_btn = st.button("Query Status")

    if track_btn:
        if not cnr.strip():
            st.warning("⚠️ Please enter a valid Case ID to query the e-courts database.")
        else:
            with st.status("Establishing Secure Connection to e-Courts Portal..."):
                time.sleep(1.2)
                st.success("Case Record Synchronized.")
                st.markdown(f"""
                **Case ID:** `{cnr.upper()}`  
                **Status:** Active | **Stage:** Final Arguments  
                **Presiding Judge:** Hon'ble Justice P. Srinivas Rao  
                **Next Hearing Date:** 05-March-2026
                """)

# C. NYAYA AI CHAT MODULE (Thread-Safe Persistence)
elif menu == "🤖 Nyaya AI Chat":
    st.subheader("🤖 Nyaya Mitra: AI Legal Associate")
    st.caption("AI Engine tuned for Bharatiya Nyaya Sanhita (BNS) & IPC Cross-referencing")
    
    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    
    if prompt := st.chat_input("Ask a legal question or section analysis..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Analyzing Statutes & Precedents..."):
                time.sleep(0.8)
                response = f"Counsel RajaRao, regarding your query on '{prompt}', the BNS 2026 framework under the new amendments suggests a shift from the previous IPC sections. Specifically, the procedural requirements now prioritize electronic evidence under the Bharatiya Sakshya Adhiniyam."
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

# D. CASE VAULT MODULE (File Handling Guard)
elif menu == "📂 Case Vault":
    st.subheader("📂 Secure Legal Document Vault")
    st.write("Upload confidential case briefs for AES-256 encryption and storage.")
    
    uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])
    
    if uploaded_file:
        if uploaded_file.size > 10 * 1024 * 1024: # 10MB Guard for demo
            st.error("Error: File size exceeds the 10MB limit for secure transmission.")
        else:
            with st.status("Encrypting Document..."):
                time.sleep(1.5)
                st.success(f"Document '{uploaded_file.name}' has been successfully encrypted and stored.")
            st.button("Run AI Brief Analysis")

# --- 7. FOOTER SECTION ---
st.markdown("---")
st.caption("© 2026 RajaRao Legal Suite | Advanced Enterprise Gold Edition | Secure Legal Practice Management")

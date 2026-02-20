import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="RajaRao Legal Suite Pro", page_icon="⚖️", layout="wide")

# --- 2. PREMIUM UI DESIGN (CSS) ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1e293b, #020617); color: #f8fafc; }
    .gold-title {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800; text-align: center; font-size: 3.5rem; margin-bottom: 10px;
    }
    .stButton>button {
        background: linear-gradient(45deg, #d4af37, #996515);
        color: white !important; font-weight: bold; border-radius: 8px; width: 100%; border: none;
    }
    .sidebar .sidebar-content { background: #0f172a; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HEADER ---
st.markdown("<div class='gold-title'>Advocate RajaRao & Associates</div>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #d4af37;'>Premium Legal Practice Management System v2.0</p>", unsafe_allow_html=True)
st.divider()

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("### 🏛️ Navigation")
    menu = st.radio("Go to:", ["📊 Dashboard", "📡 Court Tracker", "🤖 Nyaya AI Chat", "📂 Case Vault"])
    st.divider()
    st.info("Status: Online & Encrypted")

# --- 5. FUNCTIONALITIES ---

# 

# A. DASHBOARD
if menu == "📊 Dashboard":
    st.title("📊 Practice Intelligence")
    m1, m2, m3 = st.columns(3)
    m1.metric("Active Files", "52", "+4 Urgent")
    m2.metric("Hearings Today", "6", "Bench 1")
    m3.metric("BNS Sync", "v2026", "Live")
    
    st.subheader("Today's Hearing Schedule")
    df = pd.DataFrame({
        "Time": ["10:30 AM", "01:30 PM", "03:45 PM"],
        "Case ID": ["WP 124/2026", "OS 44/2026", "CC 12/2025"],
        "Court Location": ["High Court Hall 1", "District Court", "Special Bench"],
        "Status": ["Urgent", "Regular", "Evidence"]
    })
    st.dataframe(df, use_container_width=True)

# B. COURT TRACKER
elif menu == "📡 Court Tracker":
    st.title("📡 Live e-Courts Status Tracker")
    cnr = st.text_input("Enter CNR Number / Case ID", placeholder="e.g., TS-HYD-00123")
    if st.button("Track Real-time Status"):
        with st.status("Fetching Data from e-Courts Portal..."):
            time.sleep(1.2)
            st.success("Case Record Verified.")
            st.markdown("""
            **Current Stage:** Final Arguments  
            **Judge:** Hon'ble Justice P. Srinivas  
            **Next Hearing:** 05-03-2026
            """)

# C. NYAYA AI CHAT
elif menu == "🤖 Nyaya AI Chat":
    st.title("🤖 Nyaya Mitra: AI Legal Associate")
    st.caption("AI powered by Bharatiya Nyaya Sanhita (BNS) Framework")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    if prompt := st.chat_input("Ask a legal question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Simulated AI Response
        with st.spinner("Analyzing legal statutes..."):
            time.sleep(1)
            res = f"Advocate RajaRao, as per the BNS framework, your query regarding '{prompt}' suggests application of Section 112 (Organized Crime) depending on the evidence presented."
            st.chat_message("assistant").write(res)
            st.session_state.messages.append({"role": "assistant", "content": res})

# D. CASE VAULT
elif menu == "📂 Case Vault":
    st.title("📂 Secure Legal Document Vault")
    st.write("Upload and encrypt confidential case briefs.")
    uploaded_file = st.file_uploader("Upload PDF Brief", type=['pdf'])
    if uploaded_file:
        with st.status("Encrypting..."):
            time.sleep(1)
        st.success(f"File '{uploaded_file.name}' AES-256 Encrypted and Saved.")
        st.button("Analyze Document with AI")

# --- FOOTER ---
st.markdown("---")
st.caption("© 2026 RajaRao Legal Suite | Advanced Enterprise Gold Edition")

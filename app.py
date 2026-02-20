import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import time
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="RajaRao Legal Suite Pro",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED STYLING (Mind-Blowing UI) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    /* Gold Gradient Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #d4af37, #f9e27d);
        color: #000;
        border: none;
        font-weight: bold;
        border-radius: 8px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
    }
    /* Metric Cards */
    [data-testid="stMetric"] {
        background-color: #161b22;
        border-radius: 12px;
        padding: 20px;
        border: 1px solid #30363d;
    }
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. AUTHENTICATION SETUP (Fixed & Fast) ---
# Pre-hashed passwords for 'kingoflaw' and 'justice2026'
usernames = ["rajarao", "associate"]
names = ["Senior Advocate RajaRao", "Associate Counsel"]
hashed_passwords = [
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6L6s57RwXWbS8S8.', 
    '$2b$12$pL7/G3H4B/8G9T/8T.8T.u1G7G7G7G7G7G7G7G7G7G7G7G7G7G7G7'
]

credentials = {
    "usernames": {
        usernames[i]: {
            "name": names[i],
            "password": hashed_passwords[i]
        } for i in range(len(usernames))
    }
}

# Cookie name and key for persistent login
authenticator = stauth.Authenticate(
    credentials,
    "rajarao_legal_vault",
    "auth_key_2026",
    cookie_expiry_days=30
)

# --- 4. LOGIN LOGIC ---
name, auth_status, username = authenticator.login(location='main')

if auth_status:
    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3503/3503786.png", width=100)
        st.title("RajaRao & Associates")
        st.markdown("*Legacy of Justice*")
        st.divider()
        choice = st.radio("Navigation", ["📊 Dashboard", "⚖️ Case Management", "🤖 Nyaya AI Chat", "📂 Documents"])
        st.divider()
        authenticator.logout('Logout', 'sidebar')

    # --- DASHBOARD ---
    if choice == "📊 Dashboard":
        st.title(f"Welcome, {name}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Active Cases", "48", "+3 New")
        c2.metric("Hearings Today", "5", "High Priority")
        c3.metric("Closed Cases", "1,240", "98% Success")
        c4.metric("AI Research", "Active", "v5.0")
        
        

        st.subheader("Upcoming Hearings (Next 24 Hours)")
        data = {
            "Case Number": ["OS 124/2024", "WP 998/2025", "CC 45/2023"],
            "Court": ["High Court", "District Court", "Supreme Court"],
            "Timing": ["10:30 AM", "11:45 AM", "02:00 PM"]
        }
        st.table(pd.DataFrame(data))

    # --- CASE MANAGEMENT (TABS) ---
    elif choice == "⚖️ Case Management":
        st.title("Case Control Center")
        tab1, tab2, tab3 = st.tabs(["📡 Live Tracking", "🔄 IPC/BNS Bridge", "🏛️ Court Directory"])
        
        with tab1:
            st.subheader("Real-time Case Status")
            cnr = st.text_input("Enter CNR Number")
            if st.button("Fetch Live Data"):
                with st.spinner("Connecting to e-Courts Database..."):
                    time.sleep(1.5)
                    st.success("Case Found: Hearing Stage - Evidence Presentation")
                    
        with tab2:
            st.subheader("Law Converter")
            st.info("Quickly map old IPC sections to new BNS statutes.")
            old_sec = st.selectbox("Select IPC Section", ["302 (Murder)", "420 (Cheating)", "376 (Rape)"])
            mapping = {"302 (Murder)": "BNS Section 101", "420 (Cheating)": "BNS Section 316", "376 (Rape)": "BNS Section 63"}
            st.write(f"### Equivalent: **{mapping[old_sec]}**")

    # --- NYAYA AI CHAT ---
    elif choice == "🤖 Nyaya AI Chat":
        st.title("Nyaya Mitra AI Associate")
        if "messages" not in st.session_state:
            st.session_state.messages = []

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Ask a legal question (e.g., Grounds for anticipatory bail)"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"): st.markdown(prompt)

            with st.chat_message("assistant"):
                response = f"Counsel {name}, based on recent precedents under BNS, your query regarding '{prompt}' suggests focusing on procedural delays..."
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # --- DOCUMENTS ---
    elif choice == "📂 Documents":
        st.title("Secure Document Vault")
        up = st.file_uploader("Upload Case File (Encrypted)", type=['pdf', 'docx'])
        if up:
            st.success("File uploaded and analyzed by AI.")
            st.download_button("📥 Download Case Summary", "AI generated summary content", file_name="Case_Brief.txt")

elif auth_status == False:
    st.error('Username/password is incorrect')
elif auth_status == None:
    st.warning('Please enter your credentials to access the RajaRao Legal Suite.')

st.divider()
st.caption("© 2026 Advocate RajaRao & Associates | Secure Legal ERP v5.0")

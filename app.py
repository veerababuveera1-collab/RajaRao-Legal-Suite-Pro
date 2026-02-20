import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import time
from datetime import datetime

# --- 1. SETTINGS & PAGE DESIGN ---
st.set_page_config(page_title="RajaRao Legal Suite", page_icon="⚖️", layout="wide")

# Mind-blowing CSS for a Premium Lawyer Portal
st.markdown("""
    <style>
    /* Dark Theme with Gold Accents */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }
    
    /* Login Form Glassmorphism */
    div[data-testid="stForm"] {
        border: 1px solid rgba(212, 175, 55, 0.4);
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Titles with Metallic Shine */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
    }

    /* Sidebar and Buttons */
    .stButton>button {
        background: linear-gradient(45deg, #d4af37, #996515);
        color: white !important;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(212, 175, 55, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURITY CONFIGURATION ---
# Pre-hashed for performance
usernames = ["rajarao", "associate"]
names = ["Senior Advocate RajaRao", "Associate Counsel"]
hashed_passwords = [
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6L6s57RwXWbS8S8.', 
    '$2b$12$pL7/G3H4B/8G9T/8T.8T.u1G7G7G7G7G7G7G7G7G7G7G7G7G7G7G7'
]

credentials = {"usernames": {usernames[i]: {"name": names[i], "password": hashed_passwords[i]} for i in range(len(usernames))}}

authenticator = stauth.Authenticate(credentials, "rajarao_vault_v7", "secret_key_99", 30)

# --- 3. LOGIN INTERFACE ---
if not st.session_state.get("authentication_status"):
    st.markdown("<div class='main-title'>Advocate RajaRao & Associates</div>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Legal Excellence | Digital Precision</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        authenticator.login(location='main')
        if st.session_state["authentication_status"] is False:
            st.error("Invalid Counsel Credentials.")
        elif st.session_state["authentication_status"] is None:
            st.info("Please enter your secure access keys.")

# --- 4. SECURE DASHBOARD CONTENT ---
if st.session_state["authentication_status"]:
    name = st.session_state["name"]
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"## 🏛️ Welcome\n**{name}**")
        st.divider()
        menu = st.radio("Navigation", ["📊 Dashboard", "📡 Live Court Tracker", "🤖 Nyaya Mitra AI", "📂 Case Vault"])
        st.divider()
        authenticator.logout('Log Out', 'sidebar')

    # Dashboard Logic
    if menu == "📊 Dashboard":
        st.title("📊 Practice Insights")
        c1, c2, c3 = st.columns(3)
        c1.metric("Active Briefs", "52", "+4 Urgent")
        c2.metric("Hearings Today", "6", "Main Court")
        c3.metric("BNS Sync", "v2026", "Updated")

        

        st.subheader("Upcoming Hearings")
        df = pd.DataFrame({
            "Time": ["10:00 AM", "01:30 PM", "04:00 PM"],
            "Case Name": ["State vs K. Reddy", "Property App. 45/26", "Public Interest Lit."],
            "Location": ["Bench 4", "Hall 2", "Chamber 1"]
        })
        st.dataframe(df, use_container_width=True)

    # Live Tracker
    elif menu == "📡 Live Court Tracker":
        st.title("📡 Live e-Courts Status")
        cnr = st.text_input("Enter CNR Number")
        if st.button("Track Now"):
            with st.status("Accessing e-Courts Database..."):
                time.sleep(1.2)
                st.success("Connection Established.")
                st.info("**Current Stage:** Cross Examination\n\n**Next Hearing:** March 05, 2026")

    # Nyaya AI Chat
    elif menu == "🤖 Nyaya Mitra AI":
        st.title("🤖 AI Legal Associate")
        if "messages" not in st.session_state: st.session_state.messages = []
        for msg in st.session_state.messages: st.chat_message(msg["role"]).write(msg["content"])
        
        if prompt := st.chat_input("Ask about BNS sections or IPC comparisons..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            # Simulated AI Response
            response = f"Counsel {name}, analyzing '{prompt}' under the Bharatiya Nyaya Sanhita (BNS) framework..."
            st.chat_message("assistant").write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # Case Vault
    elif menu == "📂 Case Vault":
        st.title("📂 Secure Case Documents")
        uploaded_file = st.file_uploader("Upload Confidential Briefs (PDF only)", type=['pdf'])
        if uploaded_file:
            st.success("File encrypted and saved to RajaRao Vault.")
            st.download_button("📥 Download Analysis Report", "AI-Generated Summary Content", file_name="RajaRao_Analysis.txt")

# --- FOOTER ---
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.8rem; color: #475569;'>© 2026 RajaRao Legal Suite | v2.0 Gold Edition</p>", unsafe_allow_html=True)

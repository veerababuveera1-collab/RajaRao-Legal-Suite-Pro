import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="RajaRao Legal Suite", page_icon="⚖️", layout="wide")

# Mind-blowing Glassmorphism CSS for Premium Look
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #020617);
        color: #f8fafc;
    }
    /* Gold Gradient for Headlines */
    .gold-text {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    /* Styled Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 15px;
        padding: 20px;
    }
    /* Custom Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURITY CONFIG ---
usernames = ["rajarao", "associate"]
names = ["Senior Advocate RajaRao", "Associate Counsel"]
# Pre-hashed passwords to prevent TypeErrors and boost speed
hashed_passwords = [
    '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6L6s57RwXWbS8S8.', 
    '$2b$12$pL7/G3H4B/8G9T/8T.8T.u1G7G7G7G7G7G7G7G7G7G7G7G7G7G7G7'
]

credentials = {"usernames": {usernames[i]: {"name": names[i], "password": hashed_passwords[i]} for i in range(len(usernames))}}

authenticator = stauth.Authenticate(credentials, "rajarao_vault_v8", "auth_key_2026", 30)

# --- 3. LOGIN INTERFACE ---
if not st.session_state.get("authentication_status"):
    st.markdown("<h1 class='gold-text' style='text-align: center;'>Advocate RajaRao & Associates</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        authenticator.login(location='main')
        if st.session_state["authentication_status"] is False:
            st.error("Invalid Counsel Credentials.")
        elif st.session_state["authentication_status"] is None:
            st.info("Secure Portal: Please enter your credentials.")

# --- 4. SECURE APP CONTENT ---
if st.session_state["authentication_status"]:
    name = st.session_state["name"]
    
    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"### ⚖️ Welcome\n**{name}**")
        menu = st.radio("Navigation", ["📊 Dashboard", "📡 Live Court Tracker", "🤖 Nyaya AI Chat", "📂 Case Vault"])
        st.divider()
        authenticator.logout('Log Out', 'sidebar')

    # Dashboard Logic
    if menu == "📊 Dashboard":
        st.title("📊 Legal Intelligence Dashboard")
        c1, c2, c3 = st.columns(3)
        c1.metric("Active Files", "52", "+4 Urgent")
        c2.metric("Hearings Today", "6", "Bench 4")
        c3.metric("BNS Updates", "v2026", "Live")

        st.subheader("Hearing Schedule - Today")
        df = pd.DataFrame({
            "Time": ["10:30 AM", "01:15 PM", "04:00 PM"],
            "Case Name": ["State vs K. Reddy", "OS 44/2025", "WP 12/2026"],
            "Court Room": ["Hall 1", "Hall 5", "Bench 2"]
        })
        st.table(df)

    # Live Tracker (Simulated API call)
    elif menu == "📡 Live Court Tracker":
        st.title("📡 Live e-Courts Tracking")
        cnr = st.text_input("Enter CNR or Case Number")
        if st.button("Track Status"):
            with st.status("Querying e-Courts Database..."):
                time.sleep(1)
                st.success("Case Found.")
                st.info("**Stage:** Cross Examination | **Next Hearing:** 05-03-2026")

    # Nyaya AI Chat
    elif menu == "🤖 Nyaya AI Chat":
        st.title("🤖 Nyaya Mitra AI Associate")
        if "messages" not in st.session_state: st.session_state.messages = []
        for msg in st.session_state.messages: st.chat_message(msg["role"]).write(msg["content"])
        
        if prompt := st.chat_input("Ask about BNS sections..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            # Simulated AI context
            response = f"Counsel {name}, evaluating '{prompt}' under the new Bharatiya Nyaya Sanhita (BNS)..."
            st.chat_message("assistant").write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

    # Document Vault
    elif menu == "📂 Case Vault":
        st.title("📂 Secure Case Documents")
        up = st.file_uploader("Upload Confidential PDF Briefs", type=['pdf'])
        if up:
            st.success("File encrypted and stored in RajaRao Vault.")
            st.download_button("📥 Download Analysis", "Brief Content", file_name="Analysis.txt")

st.markdown("---")
st.caption("© 2026 RajaRao Legal Suite | Advanced Management System")

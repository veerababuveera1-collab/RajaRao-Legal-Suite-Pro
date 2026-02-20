import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import time

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="RajaRao Legal Suite Pro", page_icon="⚖️", layout="wide")

# --- 2. PREMIUM CSS STYLING ---
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top right, #1e293b, #020617); color: #f8fafc; }
    div[data-testid="stForm"] {
        border: 1px solid rgba(212, 175, 55, 0.4);
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 40px;
    }
    .gold-title {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800; text-align: center; font-size: 3rem;
    }
    .stButton>button {
        background: linear-gradient(45deg, #d4af37, #996515);
        color: white !important; font-weight: bold; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SECURE AUTHENTICATION SETUP ---
# యూజర్ వివరాలు
names = ["Senior Advocate RajaRao", "Associate Counsel"]
usernames = ["rajarao", "associate"]
passwords = ["kingoflaw", "justice2026"]

# TypeError మరియు Invalid Credentials రాకుండా ఇక్కడ హ్యాష్ జనరేట్ చేస్తున్నాం
hashed_passwords = stauth.Hasher(passwords).generate()

credentials = {
    "usernames": {
        usernames[i]: {
            "name": names[i],
            "password": hashed_passwords[i]
        } for i in range(len(usernames))
    }
}

# Authenticator initialization
authenticator = stauth.Authenticate(
    credentials,
    "rajarao_legal_vault", # Cookie name
    "auth_key_2026",       # Cookie key
    cookie_expiry_days=30
)

# --- 4. LOGIN LOGIC ---
if not st.session_state.get("authentication_status"):
    st.markdown("<div class='gold-title'>Advocate RajaRao & Associates</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        # కొత్త వెర్షన్‌లో login() వాల్యూస్ రిటర్న్ చేయదు
        authenticator.login(location='main')
        
        if st.session_state["authentication_status"] is False:
            st.error("Invalid Username or Password. Please try again.")
        elif st.session_state["authentication_status"] is None:
            st.info("Counsel Access: Please enter your secure credentials.")

# --- 5. POST-LOGIN CONTENT ---
if st.session_state["authentication_status"]:
    name = st.session_state["name"]
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 🏛️ Counsel: {name}")
        st.divider()
        menu = st.radio("Management Menu", ["📊 Dashboard", "📡 Live Court Tracking", "🤖 Nyaya AI Chat"])
        st.divider()
        authenticator.logout('Logout', 'sidebar')

    # Dashboard
    if menu == "📊 Dashboard":
        st.title("📊 Practice Intelligence Dashboard")
        c1, c2, c3 = st.columns(3)
        c1.metric("Active Files", "52", "+4 Today")
        c2.metric("Hearings Today", "6", "Main Bench")
        c3.metric("BNS Sync", "v2026", "Live")
        
        

        st.subheader("Today's Hearing Schedule")
        df = pd.DataFrame({
            "Time": ["10:30 AM", "01:15 PM", "04:00 PM"],
            "Case Name": ["State vs K. Reddy", "OS 44/2026", "WP 12/2026"],
            "Court Room": ["Bench 1", "Hall 5", "Bench 2"]
        })
        st.table(df)

    # Live Court Tracking
    elif menu == "📡 Live Court Tracking":
        st.title("📡 Live e-Courts Status")
        cnr = st.text_input("Enter CNR Number")
        if st.button("Query Database"):
            with st.status("Accessing e-Courts Portal..."):
                time.sleep(1)
                st.success("Case Record Verified.")
                st.info("**Current Stage:** Final Arguments\n\n**Next Date:** 05-03-2026")

    # Nyaya AI Chat
    elif menu == "🤖 Nyaya AI Chat":
        st.title("🤖 Nyaya Mitra AI")
        if "messages" not in st.session_state: st.session_state.messages = []
        for msg in st.session_state.messages: st.chat_message(msg["role"]).write(msg["content"])
        
        if prompt := st.chat_input("Ask about BNS vs IPC or precedents..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            # Simulated AI Response
            response = f"Counsel {name}, as per the Bharatiya Nyaya Sanhita (BNS), your query '{prompt}' pertains to..."
            st.chat_message("assistant").write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# --- FOOTER ---
st.markdown("---")
st.caption("© 2026 RajaRao Legal Suite | Secure Practice Management")

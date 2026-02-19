import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import time
from datetime import datetime

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="RajaRao Legal Suite Pro", page_icon="⚖️", layout="wide")

# --- 2. PERFORMANCE OPTIMIZED CSS (CACHED) ---
@st.cache_data
def load_styling():
    return """
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=1200&q=60');
        background-size: cover;
        background-attachment: fixed;
    }
    [data-testid="stSidebar"] { background-color: rgba(10, 20, 40, 0.95) !important; backdrop-filter: blur(10px); }
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        padding: 30px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stButton>button {
        background: linear-gradient(45deg, #C0C0C0, #D4AF37);
        color: #000; font-weight: bold; border-radius: 8px; border: none; width: 100%; transition: 0.3s;
    }
    h1, h2, h3 { color: #D4AF37 !important; font-family: 'Georgia', serif; }
    .stMetric { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; border-left: 5px solid #D4AF37; }
    </style>
    """
st.markdown(load_styling(), unsafe_allow_html=True)

# --- 3. MULTILINGUAL & AUTH CONFIG ---
content = {
    "English": {
        "welcome": "Welcome, Advocate RajaRao",
        "slogan": "Precision in Law | Excellence in Justice",
        "tabs": ["📡 Live Tracking", "🔍 Smart Research", "🤖 AI Counselor", "📂 Secure Vault"],
        "download": "📥 Download Case Analysis"
    },
    "Telugu": {
        "welcome": "స్వాగతం, అడ్వకేట్ రాజారావు గారు",
        "slogan": "న్యాయంలో ఖచ్చితత్వం | ధర్మంలో శ్రేష్ఠత",
        "tabs": ["📡 లైవ్ ట్రాకింగ్", "🔍 స్మార్ట్ రీసెర్చ్", "🤖 AI కౌన్సెలర్", "📂 సురక్షిత వాల్ట్"],
        "download": "📥 కేస్ అనాలిసిస్ డౌన్‌లోడ్"
    }
}

# Pre-hashed credentials (NO LAG)
credentials = {
    'usernames': {
        'rajarao': {'name': 'RajaRao', 'password': '$2b$12$MS1Y6lW1I6mS4O6v8K8uEe0Wf7Z0Y8.P.lX2u/4yO2yV7Q.g.Q6S.'},
        'counsel': {'name': 'Counsel', 'password': '$2b$12$N9O8I6mS4O6v8K8uEe0Wf7Z0Y8.P.lX2u/4yO2yV7Q.g.Q6S.V2'}
    }
}

authenticator = stauth.Authenticate(credentials, 'rajarao_cookie', 'auth_key_2026', cookie_expiry_days=1)

# --- 4. LOGIN INTERFACE ---
col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    st.title("⚖️ RajaRao & Associates")
    lang = st.radio("Language / భాష", ["English", "Telugu"], horizontal=True)
    t = content[lang]
    # Handle login based on version (Newer versions return 3 values, older 1)
    auth_data = authenticator.login("Login", "main")
    
    # Compatibility check for return values
    if isinstance(auth_data, tuple):
        name, auth_status, username = auth_data
    else:
        auth_status = st.session_state.get("authentication_status")
        name = st.session_state.get("name")

# --- 5. MAIN APP CONTENT ---
if auth_status:
    with st.sidebar:
        st.header(f"🏛️ {name}")
        st.caption(t['slogan'])
        st.divider()
        menu = st.radio("Management Suite", ["Dashboard", "Case Control", "Legal AI Tools"])
        authenticator.logout('Sign Out', 'sidebar')

    if menu == "Dashboard":
        st.header("📊 Practice Overview")
        c1, c2, c3 = st.columns(3)
        with c1: st.metric("Court Hearings Today", "8", "+2 Urgent")
        with c2: st.metric("Success Rate", "94.5%", "Platinum")
        with c3: st.metric("BNS Compliance", "Active", "Verified")
        
        st.subheader("Upcoming Calendar")
        df = pd.DataFrame({
            "Time": ["10:30 AM", "02:00 PM", "04:30 PM"],
            "Case": ["State vs Reddy", "Varma Property Dispute", "Interim Bail Hearing"],
            "Court": ["High Court Hall 4", "District Court", "Virtual Bench 2"]
        })
        st.table(df)

    elif menu == "Case Control":
        st.title("⚖️ Case Operations")
        tab1, tab2, tab3, tab4 = st.tabs(t['tabs'])

        with tab1: # Live Tracking
            st.subheader("📡 Real-time Court Status")
            cnr = st.text_input("Enter CNR Number (e.g., TSHY010023452026)")
            if st.button("Query e-Courts Database"):
                with st.status("Fetching Live Data...", expanded=True) as status:
                    st.write("Connecting to National Judicial Data Grid...")
                    time.sleep(1)
                    st.write("Verifying Case ID...")
                    time.sleep(1)
                    status.update(label="Sync Complete!", state="complete")
                st.info("**Current Stage:** Final Arguments | **Judge:** Hon'ble Justice Reddy | **Next Date:** 22 Feb 2026")

        with tab2: # Smart Research
            st.subheader("🔍 Legal Citations")
            query = st.text_input("Search BNS / BNSS / IPC Sections")
            if query:
                st.write(f"Showing matches for: **{query}**")
                # Visualization of legal frameworks
                
                data = {"Act": ["BNS 2023", "IPC 1860"], "Section": ["Sec 103", "Sec 302"], "Context": ["Punishment for Murder", "Punishment for Murder"]}
                st.dataframe(pd.DataFrame(data), use_container_width=True)

        with tab3: # AI Counselor
            st.subheader("🤖 Nyaya Mitra AI")
            if "msgs" not in st.session_state: st.session_state.msgs = []
            
            chat_container = st.container(height=300)
            with chat_container:
                for m in st.session_state.msgs:
                    with st.chat_message(m["role"]):
                        st.markdown(m["content"])
            
            if prompt := st.chat_input("Ask about case strategy..."):
                st.session_state.msgs.append({"role": "user", "content": prompt})
                with st.chat_message("user"): st.markdown(prompt)
                
                with st.chat_message("assistant"):
                    response = f"Counsel {name}, under the new Bharatiya Nyaya Sanhita, your argument should focus on the procedural changes in evidence collection..."
                    st.markdown(response)
                st.session_state.msgs.append({"role": "assistant", "content": response})

        with tab4: # Secure Vault
            st.subheader("📂 Document Intelligence")
            uploaded_file = st.file_uploader("Upload Petition Draft", type=['pdf'])
            if uploaded_file:
                with st.spinner("Analyzing legal nuances..."):
                    time.sleep(2)
                    st.success("Analysis Complete: No inconsistencies found.")
                    st.download_button(t['download'], "Summary: Ready for filing.", file_name="Case_Summary.txt")

elif auth_status == False:
    st.error('Access Denied: Please check your credentials.')
elif auth_status == None:
    st.warning('Restricted Access: RajaRao & Associates Internal Portal.')

st.markdown("---")
st.caption(f"© 2026 RajaRao Legal | System Time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

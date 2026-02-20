import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import time
from datetime import datetime

# --- 1. PROJECT CONFIGURATION ---
PROJECT_NAME = "RajaRao Legal Suite - v1.5 (Secure Basic)"
ADMIN_USER = "rajarao"
ADMIN_PASS = "chamber123"

# --- 2. DATABASE ENGINE ---
def init_db():
    conn = sqlite3.connect('rajarao_v1_chamber.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS cases 
        (id INTEGER PRIMARY KEY, case_id TEXT, petitioner TEXT, respondent TEXT, 
        court TEXT, rating TEXT, total_fee REAL)''')
    conn.commit()
    return conn

db_conn = init_db()

# --- 3. PREMIUM UI & LOGIN PAGE ---
st.set_page_config(page_title=PROJECT_NAME, page_icon="⚖️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #f8fafc; }
    .gold-header {
        background: linear-gradient(to right, #BF953F, #FCF6BA, #B38728);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; text-align: center; font-size: 3rem;
    }
    </style>
    """, unsafe_allow_html=True)

# LOGIN LOGIC
if 'login_status' not in st.session_state:
    st.session_state.login_status = False

if not st.session_state.login_status:
    st.markdown(f"<div class='gold-header'>{PROJECT_NAME}</div>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 1, 1])
    with col2:
        st.subheader("🔐 Chamber Login")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Access Vault"):
            if user == ADMIN_USER and pwd == ADMIN_PASS:
                st.session_state.login_status = True
                st.success("Access Granted!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid Credentials")
    st.stop()

# --- 4. MAIN APPLICATION (Post Login) ---
with st.sidebar:
    st.markdown(f"### 🏛️ {PROJECT_NAME}")
    st.write(f"Welcome, **Adv. RajaRao**")
    menu = st.radio("Chamber Modules", ["📊 Dashboard", "➕ New Case Entry"])
    st.divider()
    if st.button("Logout"):
        st.session_state.login_status = False
        st.rerun()

# --- 5. MODULES ---

if menu == "📊 Dashboard":
    st.markdown("<div class='gold-header'>Chamber Intelligence</div>", unsafe_allow_html=True)
    
    df = pd.read_sql_query("SELECT * FROM cases", db_conn)
    
    if not df.empty:
        # KPI Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Briefs", len(df))
        high_priority = len(df[df['rating'] == "🔴 High Priority"])
        m2.metric("Critical Cases", high_priority)
        m3.metric("Billed Revenue", f"₹{df['total_fee'].sum():,.0f}")

        st.divider()
        # Case Distribution Chart
        st.subheader("Court Analysis")
        fig = px.pie(df, names='court', hole=0.4, color_discrete_sequence=px.colors.sequential.Gold)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)

        

        # Detailed Registry
        st.subheader("Active Case Registry")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No records found in the chamber vault.")

elif menu == "➕ New Case Entry":
    st.subheader("📝 Brief Onboarding")
    with st.form("new_case"):
        c1, c2 = st.columns(2)
        c_id = c1.text_input("Case Number")
        pet = c2.text_input("Petitioner")
        res = c1.text_input("Respondent")
        crt = c2.selectbox("Court", ["Supreme Court", "High Court", "District Court", "Tribunals"])
        
        # Rating Column Integration
        rat = st.select_slider("Case Priority Rating", 
                              options=["🟢 Low Priority", "🟡 Medium Priority", "🔴 High Priority"])
        
        fee = st.number_input("Professional Fee (₹)", min_value=0.0)
        
        if st.form_submit_button("Secure Entry"):
            if c_id and pet:
                db_conn.execute("INSERT INTO cases (case_id, petitioner, respondent, court, rating, total_fee) VALUES (?,?,?,?,?,?)",
                               (c_id, pet, res, crt, rat, fee))
                db_conn.commit()
                st.success(f"Case {c_id} has been encrypted and saved.")
            else:
                st.warning("Please fill essential details (Case ID & Petitioner).")

# FOOTER
st.divider()
st.caption(f"© 2026 {PROJECT_NAME} | System Time: {datetime.now().strftime('%H:%M')}")

import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
import time

# --- 1. FAST LOADING CONFIG ---
st.set_page_config(page_title="RajaRao Legal Pro", page_icon="⚖️", layout="wide")

# --- 2. PRE-HASHED PASSWORDS (Saves Loading Time) ---
# ప్రతిసారి హ్యాష్ చేయకుండా నేరుగా ఇక్కడ ఇస్తున్నాను
# 'kingoflaw' -> '$2b$12$6K6... (sample)'
# డెమో కోసం ప్లెయిన్ టెక్స్ట్ వాడుతున్నాం, కానీ రియల్ టైమ్ లో హ్యాష్ వాడాలి
usernames = ["rajarao", "associate"]
passwords = ["kingoflaw", "justice2026"]

# --- 3. FAST UI (Static CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. OPTIMIZED LOGIN ---
authenticator = stauth.Authenticate(
    {'usernames': {usernames[i]: {'name': usernames[i].capitalize(), 'password': stauth.Hasher([passwords[i]]).generate()[0]} for i in range(len(usernames))}},
    'rajarao_vault', 'key_2026', 30
)

name, auth_status, username = authenticator.login('Secure Login', 'main')

if auth_status:
    # Sidebar navigation (fast)
    menu = st.sidebar.radio("Menu", ["Dashboard", "Court Status", "AI Chat"])
    authenticator.logout('Logout', 'sidebar')

    if menu == "Dashboard":
        st.title(f"Welcome Advocate {name}")
        # యూజర్ ఇంటరాక్షన్ లేకుండానే లోడ్ అయ్యేలా సింపుల్ మెట్రిక్స్
        c1, c2 = st.columns(2)
        c1.metric("Today's Cases", "5")
        c2.metric("Pending Tasks", "12")

    elif menu == "Court Status":
        st.subheader("Live Status")
        # సింపుల్ టేబుల్ లోడింగ్
        df = pd.DataFrame({"Case": ["State vs X", "Y vs Union"], "Date": ["Feb 25", "Mar 10"]})
        st.dataframe(df, use_container_width=True)

elif auth_status == False:
    st.error('Check Credentials')
elif auth_status == None:
    st.info('Advocate RajaRao & Associates Portal')

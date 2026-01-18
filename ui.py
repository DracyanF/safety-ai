import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Public Safety Intelligence", layout="wide")

st.title("🚔 Public Safety Intelligence Dashboard")

# Sidebar navigation
section = st.sidebar.selectbox(
    "Select View",
    [
        "Search Incidents",
        "Crime Hotspots",
        "Crime Trends",
        "Risk Scores",
        "Patrol Recommendations"
    ]
)

# 🔍 SEARCH
if section == "Search Incidents":
    st.header("🔍 Search Crime Incidents")

    query = st.text_input("Search Query")
    days = st.number_input("Days (optional)", min_value=1, value=30)

    if st.button("Search"):
        params = {"query": query, "days": days}
        resp = requests.get(f"{API_URL}/search", params=params)
        st.json(resp.json())

# 🔥 HOTSPOTS
elif section == "Crime Hotspots":
    st.header("🔥 Crime Hotspots")

    days = st.slider("Days", 7, 365, 30)
    threshold = st.slider("Incident Threshold", 1, 10, 3)

    resp = requests.get(f"{API_URL}/hotspots", params={
        "days": days,
        "threshold": threshold
    })

    st.json(resp.json())

# 📈 TRENDS
elif section == "Crime Trends":
    st.header("📈 Crime Trends")

    window_days = st.slider("Window Size (days)", 7, 180, 15)

    resp = requests.get(f"{API_URL}/trends", params={
        "window_days": window_days
    })

    st.json(resp.json())

# 🚦 RISK
elif section == "Risk Scores":
    st.header("🚦 Area Risk Scores")

    days = st.slider("Days", 7, 365, 30)
    resp = requests.get(f"{API_URL}/risk", params={"days": days})

    st.json(resp.json())

# 🚓 PATROLS
elif section == "Patrol Recommendations":
    st.header("🚓 Patrol Recommendations")

    days = st.slider("Days", 7, 365, 30)
    resp = requests.get(f"{API_URL}/patrols", params={"days": days})

    data = resp.json()
    for rec in data:
        st.subheader(f"📍 {rec['area']}")
        st.write(f"Risk Score: {rec['risk_score']}")
        st.write(f"Priority: {rec['priority']}")
        st.write(f"Patrol Units: {rec['patrol_units']}")
        st.write(f"Recommended Time: {rec['recommended_time']}")
        st.info(rec["explanation"])

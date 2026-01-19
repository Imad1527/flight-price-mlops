import streamlit as st
import requests
from datetime import date

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Flight Price Prediction",
    page_icon="✈️",
    layout="centered"
)

# -----------------------------
# LIGHT THEME CSS (NOT DARK)
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #F4F7FC;
}
.main {
    background-color: #F4F7FC;
}
.header {
    padding: 30px;
    border-radius: 16px;
    background: linear-gradient(90deg, #2563EB, #60A5FA);
    color: white;
    margin-bottom: 30px;
}
.card {
    background-color: #FFFFFF;
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.08);
    margin-bottom: 25px;
}
.result {
    background-color: #ECFDF5;
    padding: 20px;
    border-radius: 16px;
    font-size: 22px;
    color: #166534;
    text-align: center;
    border: 1px solid #BBF7D0;
}
.stButton>button {
    background-color: #2563EB;
    color: white;
    height: 50px;
    font-size: 16px;
    border-radius: 12px;
}
.stButton>button:hover {
    background-color: #1E40AF;
}
label {
    font-size: 14px !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div class="header">
    <h1>✈️ Flight Price Prediction</h1>
  
</div>
""", unsafe_allow_html=True)

# -----------------------------
# INPUT CARD
# -----------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    from_city = st.selectbox(
        "From",
        ["Aracaju", "Brasilia", "Campo_Grande", "Florianopolis",
         "Natal", "Recife", "Rio_de_Janeiro", "Salvador", "Sao_Paulo"]
    )

    flight_type = st.selectbox(
        "Flight Type",
        ["economic", "premium", "firstClass"]
    )

    st.text_input("Flight Time (minutes)", value="90", disabled=True)

    day = st.number_input("Day", min_value=1, max_value=31, value=15)

with col2:
    to_city = st.selectbox(
        "To",
        ["Aracaju", "Brasilia", "Campo_Grande", "Florianopolis",
         "Natal", "Recife", "Rio_de_Janeiro", "Salvador", "Sao_Paulo"]
    )

    agency = st.selectbox(
        "Agency",
        ["Rainbow", "CloudFy", "FlyingDrops"]
    )

    st.text_input("Distance (km)", value="360", disabled=True)

    month = st.number_input("Month", min_value=1, max_value=12, value=7)

year = st.number_input(
    "Year",
    min_value=2026,
    value=2026,
    step=1
)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# DERIVED VALUES
# -----------------------------
time = 90
distance = 360
weekday = date(year, month, day).weekday()

# -----------------------------
# PREDICTION
# -----------------------------
if st.button("Predict Flight Price", use_container_width=True):
    payload = {
        "from": from_city,
        "to": to_city,
        "flightType": flight_type,
        "time": time,
        "distance": distance,
        "agency": agency,
        "day": day,
        "month": month,
        "weekday": weekday
    }

    try:
        response = requests.post(
            "http://127.0.0.1:5000/predict",
            json=payload,
            timeout=5
        )

        if response.status_code == 200:
            result = response.json()
            st.markdown(
                f"""
                <div class="result">
                    💰 Estimated Ticket Price<br>
                    <strong>₹ {result['predicted_price']}</strong>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.error(f"API Error: {response.text}")

    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {e}")

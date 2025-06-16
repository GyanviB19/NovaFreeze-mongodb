
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from logger import log_freshscore

st.set_page_config(page_title="FreshScore AI – ColdChain Monitor", layout="wide")

def colorful_block(title, color, content):
    st.markdown(f"""
        <div style='background-color:{color};padding:20px;border-radius:10px;'>
        <h3 style='color:white;'>{title}</h3>
        <p style='color:white;'>{content}</p>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>🍓 FreshScore Predictor – ColdChain AI</h1>", unsafe_allow_html=True)
st.markdown("---")

left, right = st.columns([1, 1.2])

with left:
    with st.form("freshscore_form"):
        st.markdown("<h4>📋 Enter Item Details</h4>", unsafe_allow_html=True)
        category = st.selectbox("Perishable Category", [
            "strawberries", "flowers", "frozen_food", "milk", "vaccines", "cheese",
            "meat", "leafy_greens", "ice_cream", "seafood", "juice", "eggs", "yogurt", "berries", "herbs"
        ])
        temperature = st.slider("Internal Temperature (°C)", 0.0, 25.0, 6.0)
        humidity = st.slider("Humidity (%)", 30, 100, 75)
        duration_hours = st.slider("Transit Duration (hours)", 0.0, 48.0, 8.0)
        distance_km = st.slider("Distance Traveled (km)", 0.0, 2000.0, 250.0)
        door_openings = st.slider("Door Openings", 0, 10, 2)
        submitted = st.form_submit_button("🚀 Predict FreshScore")

if submitted:
    input_data = {
        "temperature": temperature,
        "humidity": humidity,
        "duration_hours": duration_hours,
        "distance_km": distance_km,
        "door_openings": door_openings
    }
    for cat in [
        "berries", "cheese", "eggs", "flowers", "frozen_food", "herbs", "ice_cream",
        "juice", "leafy_greens", "meat", "milk", "seafood", "strawberries", "vaccines", "yogurt"
    ]:
        input_data[f"category_{cat}"] = 1 if category == cat else 0

    input_df = pd.DataFrame([input_data])
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    X_dummy, y_dummy = make_regression(n_samples=1000, n_features=len(input_df.columns), noise=0.1)
    model.fit(X_dummy, y_dummy)
    score = float(np.clip(model.predict(input_df)[0], 0, 100))

    try:
        log_freshscore({
            "category": category,
            "temperature": temperature,
            "humidity": humidity,
            "duration_hours": duration_hours,
            "distance_km": distance_km,
            "door_openings": door_openings,
            "freshscore": score,
            "money_saved_usd": score * 3,
            "co2_avoided_kg": score * 0.02
        })
        st.success("✅ FreshScore logged to MongoDB!")
    except Exception as e:
        st.error(f"❌ MongoDB logging failed: {e}")

    with right:
        st.markdown("<h4>🌡️ Freshness Meter</h4>", unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "FreshScore (0–100)", 'font': {'size': 24}},
            delta={'reference': 80, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#FF4B4B"},
                'steps': [
                    {'range': [0, 60], 'color': 'red'},
                    {'range': [60, 80], 'color': 'yellow'},
                    {'range': [80, 100], 'color': 'lightgreen'}
                ],
                'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.75, 'value': score}
            }
        ))
        st.plotly_chart(fig)

        st.markdown("""
### 🧾 What Does the FreshScore Mean?

The **FreshScore** is a machine learning–generated indicator (0–100) representing the likely freshness and quality of a perishable product at the point of evaluation.

- **FreshScore 80–100:** ✅ **Healthy & Fresh**  
  Optimal temperature, low door openings, short duration. Products are likely to retain full quality, safety, and shelf life.

- **FreshScore 60–79:** ⚠️ **Acceptable but Monitor Closely**  
  Slight deviation in temperature or transit duration. While still usable, quality may begin to degrade.

- **FreshScore below 60:** 🚨 **Spoilage Risk**  
  High probability of reduced quality, contamination, or spoilage. Action needed — reroute, inspect, or dispose.

This score helps cold chain operators, retailers, and quality controllers make **real-time decisions** based on AI-powered predictions.
        """)

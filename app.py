import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

st.set_page_config(page_title="Context-Aware Driving Intelligence", page_icon="🚘", layout="wide")

# Custom Styles for UI Polish
st.markdown("""
<style>
.big-font {
    font-size: 60px !important;
    font-weight: bold;
    text-align: center;
}
.score-box {
    padding: 20px;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.05); /* Slight dark-mode friendly styling */
    text-align: center;
}
.smart-decision {
    color: #4CAF50;
}
.risky-behavior {
    color: #f44336;
}
</style>
""", unsafe_allow_html=True)

st.title("🚘 Context-Aware Driving Intelligence System")
st.markdown("Real-time behavioral analysis using simulated driving telemetry. It compares traditional rule-based scoring with intelligent context-aware scoring.")

# Session state initialization
if 'score' not in st.session_state:
    st.session_state.score = 100
if 'trad_score' not in st.session_state:
    st.session_state.trad_score = 100
if 'log' not in st.session_state:
    st.session_state.log = []
if 'accel_data' not in st.session_state:
    st.session_state.accel_data = [0] * 30
if 'speed' not in st.session_state:
    st.session_state.speed = 50
if 'turn_angle' not in st.session_state:
    st.session_state.turn_angle = 0
if 'status' not in st.session_state:
    st.session_state.status = "Monitoring... 🟢"

# Update random telemetry data
st.session_state.speed = np.random.randint(20, 81)
st.session_state.turn_angle = np.random.randint(-15, 16)
st.session_state.accel_data.append(np.random.uniform(-4.0, 4.0))
if len(st.session_state.accel_data) > 30:
    st.session_state.accel_data.pop(0)

# Layout configuration
col_controls, col_display, col_metrics = st.columns([1, 1.5, 1.5], gap="large")

with col_controls:
    st.subheader("🎛️ Simulation Controls")
    
    st.markdown("**Environment Context**")
    obstacle = st.checkbox("🚧 Obstacle Ahead", help="Simulates an obstacle abruptly crossing the path.")
    traffic = st.select_slider("🚦 Traffic Density", options=["Low", "Medium", "High"], value="Medium")
    
    st.markdown("---")
    st.markdown("**Driver Actions**")
    brake_button = st.button("🚨 Simulate Brake", use_container_width=True, type="primary")
    
    st.markdown("**Simulation Settings**")
    live_update = st.checkbox("🔄 Enable Live Telemetry", value=False)
    
    if st.button("♻️ Reset Simulation", use_container_width=True):
        st.session_state.score = 100
        st.session_state.trad_score = 100
        st.session_state.log = []
        st.session_state.status = "Monitoring... 🟢"
        st.rerun()

# Brake Logic & Event Detection
if brake_button:
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # Traditional systems simply penalize hard braking without context
    st.session_state.trad_score -= 10
    
    if obstacle:
        # Context-aware logic understands WHY the brake occurred
        st.session_state.score += 2
        st.session_state.status = "Smart Decision Detected! 🧠 (Obstacle Avoided)"
        log_entry = {
            "Time": timestamp, 
            "Event": "Context-Aware Brake ✅", 
            "Speed (km/h)": st.session_state.speed,
            "Context": f"Obstacle: Yes | Traffic: {traffic}", 
            "Score Change": "+2"
        }
    else:
        st.session_state.score -= 10
        st.session_state.status = "Risky Behavior! ⚠️ (Unnecessary Hard Brake)"
        log_entry = {
            "Time": timestamp, 
            "Event": "Risky Brake ❌", 
            "Speed (km/h)": st.session_state.speed,
            "Context": f"Obstacle: No | Traffic: {traffic}", 
            "Score Change": "-10"
        }
    st.session_state.log.insert(0, log_entry)

with col_display:
    st.subheader("📊 Live Telemetry")
    t_col1, t_col2 = st.columns(2)
    t_col1.metric(label="Speed", value=f"{st.session_state.speed} km/h", delta=f"{np.random.randint(-2, 3)} km/h")
    t_col2.metric(label="Steering Angle", value=f"{st.session_state.turn_angle}°", delta=f"{np.random.randint(-5, 6)}°", delta_color="off")
    
    st.markdown("**Acceleration (m/s²)**")
    chart_data = pd.DataFrame(st.session_state.accel_data, columns=["Acceleration"])
    st.line_chart(chart_data, height=250, use_container_width=True)

with col_metrics:
    st.subheader("🎯 Intelligence Module")
    
    # Status Message
    if "Smart" in st.session_state.status:
        st.success(st.session_state.status, icon="✅")
    elif "Risky" in st.session_state.status:
        st.error(st.session_state.status, icon="🚨")
    else:
        st.info(st.session_state.status, icon="ℹ️")
        
    st.markdown("---")
    
    # Score Comparison
    st.markdown("<div style='text-align: center'><h3>System Evaluation</h3></div>", unsafe_allow_html=True)
    
    sc_col1, sc_col2 = st.columns(2)
    with sc_col1:
        st.markdown("<div class='score-box'>", unsafe_allow_html=True)
        st.markdown("<b>Intelligent Score</b>", unsafe_allow_html=True)
        color = "smart-decision" if st.session_state.score >= 80 else "risky-behavior"
        st.markdown(f"<div class='big-font {color}'>{st.session_state.score}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with sc_col2:
        st.markdown("<div class='score-box'>", unsafe_allow_html=True)
        st.markdown("<b>Traditional Score</b>", unsafe_allow_html=True)
        t_color = "smart-decision" if st.session_state.trad_score >= 80 else "risky-behavior"
        st.markdown(f"<div class='big-font {t_color}'>{st.session_state.trad_score}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
st.markdown("---")
st.subheader("📋 Event Log")
if st.session_state.log:
    df_log = pd.DataFrame(st.session_state.log)
    st.dataframe(df_log, use_container_width=True, hide_index=True)
else:
    st.write("No events recorded yet. Configure the simulation and press **'Simulate Brake'** to log an event.")

# Handle Live Update Loop
if live_update:
    time.sleep(1)
    st.rerun()

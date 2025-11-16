import streamlit as st
import joblib
import numpy as np
import pandas as pd
import time
import base64
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load email settings
from email_config import EMAIL_ADDRESS, EMAIL_PASSWORD, TO_EMAIL

# Load ML models
navigation_model = joblib.load("models/navigation_model.joblib")
thermal_model = joblib.load("models/thermal_model.joblib")

# Streamlit setup with custom CSS
st.set_page_config(page_title="Autonomous AI Agent", page_icon="🤖", layout="wide")

# Custom CSS for attractive, responsive design
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Card styling */
    .sensor-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        color: white;
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
    }
    
    .sensor-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(0,0,0,0.3);
    }
    
    .thermal-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    
    .nav-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    /* Status badge */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.2rem;
        margin: 1rem 0;
        animation: pulse 2s infinite;
    }
    
    .status-safe {
        background: #10b981;
        color: white;
    }
    
    .status-alert {
        background: #ef4444;
        color: white;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 50%, 100% { opacity: 1; }
        25%, 75% { opacity: 0.5; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* Metric display */
    .metric-row {
        display: flex;
        flex-wrap: wrap;
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .metric-item {
        flex: 1;
        min-width: 150px;
        background: rgba(255,255,255,0.2);
        padding: 0.8rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 0.3rem;
    }
    
    .metric-value {
        font-size: 1.3rem;
        font-weight: bold;
    }
    
    /* Alert box */
    .alert-box {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1.5rem 0;
        box-shadow: 0 8px 16px rgba(255,0,0,0.3);
        animation: shake 0.5s;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-10px); }
        75% { transform: translateX(10px); }
    }
    
    /* Prediction section */
    .prediction-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-top: 2rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .prediction-title {
        color: white;
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    
    .prediction-content {
        display: flex;
        flex-wrap: wrap;
        gap: 2rem;
        justify-content: space-around;
    }
    
    .prediction-item {
        background: rgba(255,255,255,0.2);
        padding: 1.5rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
        flex: 1;
        min-width: 250px;
        text-align: center;
    }
    
    .prediction-label {
        color: rgba(255,255,255,0.9);
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .prediction-value {
        color: white;
        font-size: 2rem;
        font-weight: bold;
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .metric-item {
            min-width: 100%;
        }
        
        .prediction-item {
            min-width: 100%;
        }
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .header-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header-container">
    <div class="header-title">🤖 Autonomous AI Agent</div>
    <div class="header-subtitle">Real-Time Sensing System</div>
</div>
""", unsafe_allow_html=True)

# Initialize session state variables
if "last_alert" not in st.session_state:
    st.session_state.last_alert = None

if "last_heat_state" not in st.session_state:
    st.session_state.last_heat_state = 0

if "agent_status" not in st.session_state:
    st.session_state.agent_status = "SAFE"

EMAIL_COOLDOWN = 30
last_email_time = 0

# Status display
status_placeholder = st.empty()

# Create two columns for sensors
col1, col2 = st.columns(2)

# Placeholders for left and right columns
with col1:
    nav_placeholder = st.empty()

with col2:
    thermal_placeholder = st.empty()

# Prediction section below
prediction_placeholder = st.empty()

# Alert section
alert_placeholder = st.empty()

# Log section
log_placeholder = st.empty()


# ---------------------------------------------------------
# AUDIO ALERT
# ---------------------------------------------------------
def play_alert_sound():
    audio_file = "assets/robotic_beep.wav"
    try:
        with open(audio_file, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()

        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/wav;base64,{encoded}" type="audio/wav">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # Audio file not found, skip sound


# ---------------------------------------------------------
# SEND EMAIL ALERT
# ---------------------------------------------------------
def send_heat_alert_email(t):
    global last_email_time
    now = time.time()

    if now - last_email_time < EMAIL_COOLDOWN:
        return

    last_email_time = now

    subject = "🔥 ALERT: Heat Signature Detected!"
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    ambient = t['ambient_temp_c']
    surface = t['surface_temp_c']
    infrared = t['infrared_temp_c']

    body = f"""
    <div style="
        max-width: 520px;
        margin: auto;
        background: #ffffff;
        border-radius: 14px;
        box-shadow: 0 6px 18px rgba(0,0,0,0.15);
        padding: 24px;
        font-family: Arial, sans-serif;
    ">

        <!-- Header -->
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="
                font-size: 28px;
                font-weight: bold;
                color: #d9534f;
            ">
                🔥 ALERT: Heat Signature Detected!
            </div>
            <div style="font-size: 14px; color: #777;">
                {current_time}
            </div>
        </div>

        <!-- Description -->
        <p style="font-size: 15px; color: #333; line-height: 1.6; text-align:center;">
            A heat signature was detected by the autonomous agent.
        </p>

        <!-- Sensor Readings Card -->
        <div style="
            background: #fff5f5;
            border-left: 5px solid #ff4d4d;
            padding: 15px;
            border-radius: 10px;
            margin-top: 16px;
        ">
            <div style="font-weight: bold; font-size: 16px; margin-bottom: 10px;">
                🌡️ Sensor Readings at Detection
            </div>

            <!-- Responsive Grid -->
            <div style="
                display: flex;
                flex-wrap: wrap;
                gap: 12px;
            ">
                <div style="
                    flex: 1;
                    min-width: 140px;
                    background: #ffffff;
                    padding: 12px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                    text-align: center;
                ">
                    <div style="font-size: 13px; color:#555;">Ambient Temperature</div>
                    <div style="font-size: 20px; font-weight: bold; color:#d9534f;">
                        {ambient:.1f}°C
                    </div>
                </div>

                <div style="
                    flex: 1;
                    min-width: 140px;
                    background: #ffffff;
                    padding: 12px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                    text-align: center;
                ">
                    <div style="font-size: 13px; color:#555;">Surface Temperature</div>
                    <div style="font-size: 20px; font-weight: bold; color:#d9534f;">
                        {surface:.1f}°C
                    </div>
                </div>

                <div style="
                    flex: 1;
                    min-width: 140px;
                    background: #ffffff;
                    padding: 12px;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
                    text-align: center;
                ">
                    <div style="font-size: 13px; color:#555;">Infrared Temperature</div>
                    <div style="font-size: 20px; font-weight: bold; color:#d9534f;">
                        {infrared:.1f}°C
                    </div>
                </div>
            </div>
        </div>

    </div>
    """


    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
        print("📧 Email sent")
    except Exception as e:
        print("❌ Email failed:", e)

# ---------------------------------------------------------
# SYNTHETIC SENSOR GENERATORS
# ---------------------------------------------------------
def generate_navigation_signals():
    return {
        "accel_x": np.random.normal(0, 0.8),
        "accel_y": np.random.normal(0, 0.8),
        "accel_z": np.random.normal(9.8, 0.5),
        "gyro_x": np.random.normal(0, 0.05),
        "gyro_y": np.random.normal(0, 0.05),
        "gyro_z": np.random.normal(0, 0.05),
        "obstacle_distance_cm": np.clip(np.random.normal(50, 10), 5, 150),
        "speed_cm_per_s": np.clip(np.random.normal(5, 2), 0, 15)
    }


def generate_thermal_signals():
    return {
        "ambient_temp_c": np.clip(np.random.normal(30, 5), 23, 150),
        "surface_temp_c": np.clip(np.random.normal(40, 10), 23, 150),
        "infrared_temp_c": np.clip(np.random.normal(60, 20), 23, 150)
    }


# ---------------------------------------------------------
# MAIN AUTONOMOUS LOOP
# ---------------------------------------------------------
while True:
    
    # -------- NAVIGATION DATA --------
    nav_data = generate_navigation_signals()
    nav_input = pd.DataFrame([nav_data])
    nav_pred = navigation_model.predict(nav_input)[0]

    # -------- THERMAL DATA --------
    t = generate_thermal_signals()
    t_input = pd.DataFrame([t])
    heat_pred = thermal_model.predict(t_input)[0]

    # Update status
    if heat_pred == 1:
        if st.session_state.last_heat_state == 0:
            st.session_state.agent_status = "HEAT DETECTED"
            alert_msg = f"🔥 HEAT DETECTED at {datetime.now().strftime('%H:%M:%S')}"
            st.session_state.last_alert = alert_msg
            play_alert_sound()
            send_heat_alert_email(t)
        st.session_state.last_heat_state = 1
        status_class = "status-alert"
    else:
        if st.session_state.last_heat_state == 1:
            st.session_state.agent_status = "SAFE"
        st.session_state.last_heat_state = 0
        status_class = "status-safe"

    # Display status
    status_placeholder.markdown(f"""
    <div style="text-align: center;">
        <span class="status-badge {status_class}">
            {'🔴' if heat_pred == 1 else '🟢'} STATUS: {st.session_state.agent_status}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Display navigation (left column)
    nav_html = f"""
    <div class="sensor-card nav-card">
        <h2 style="margin-top:0;">🧭 Navigation System</h2>
        <div class="metric-row">
            <div class="metric-item">
                <div class="metric-label">Accel X</div>
                <div class="metric-value">{nav_data['accel_x']:.2f}</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Accel Y</div>
                <div class="metric-value">{nav_data['accel_y']:.2f}</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Accel Z</div>
                <div class="metric-value">{nav_data['accel_z']:.2f}</div>
            </div>
        </div>
        <div class="metric-row">
            <div class="metric-item">
                <div class="metric-label">Gyro X</div>
                <div class="metric-value">{nav_data['gyro_x']:.3f}</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Gyro Y</div>
                <div class="metric-value">{nav_data['gyro_y']:.3f}</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Gyro Z</div>
                <div class="metric-value">{nav_data['gyro_z']:.3f}</div>
            </div>
        </div>
        <div class="metric-row">
            <div class="metric-item">
                <div class="metric-label">Obstacle Distance</div>
                <div class="metric-value">{nav_data['obstacle_distance_cm']:.1f} cm</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Speed</div>
                <div class="metric-value">{nav_data['speed_cm_per_s']:.1f} cm/s</div>
            </div>
        </div>
    </div>
    """
    nav_placeholder.markdown(nav_html, unsafe_allow_html=True)

    # Display thermal (right column)
    thermal_status = "🔥 HEAT SIGNATURE DETECTED" if heat_pred == 1 else "✅ No Heat Detected"
    thermal_color = "red" if heat_pred == 1 else "#10b981"
    
    thermal_html = f"""
    <div class="sensor-card thermal-card">
        <h2 style="margin-top:0;">🔥 Thermal Detection</h2>
        <div style="text-align:center; font-size:1.3rem; font-weight:bold; margin:1rem 0; color:{thermal_color};">
            {thermal_status}
        </div>
        <div class="metric-row">
            <div class="metric-item">
                <div class="metric-label">Ambient Temp</div>
                <div class="metric-value">{t['ambient_temp_c']:.1f}°C</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Surface Temp</div>
                <div class="metric-value">{t['surface_temp_c']:.1f}°C</div>
            </div>
            <div class="metric-item">
                <div class="metric-label">Infrared Temp</div>
                <div class="metric-value">{t['infrared_temp_c']:.1f}°C</div>
            </div>
        </div>
    </div>
    """
    thermal_placeholder.markdown(thermal_html, unsafe_allow_html=True)

    # Display predictions below
    prediction_html = f"""
    <div class="prediction-section">
        <div class="prediction-title">🎯 AI Predictions</div>
        <div class="prediction-content">
            <div class="prediction-item">
                <div class="prediction-label">Navigation Direction</div>
                <div class="prediction-value">{nav_pred}</div>
            </div>
            <div class="prediction-item">
                <div class="prediction-label">Thermal Status</div>
                <div class="prediction-value">{'HEAT' if heat_pred == 1 else 'SAFE'}</div>
            </div>
        </div>
    </div>
    """
    prediction_placeholder.markdown(prediction_html, unsafe_allow_html=True)

    # Show alert if present
    if st.session_state.last_alert and heat_pred == 1:
        alert_html = f"""
        <div class="alert-box">
            <h3 style="margin:0 0 0.5rem 0;">🚨 ALERT</h3>
            <div style="font-size:1.1rem;">{st.session_state.last_alert}</div>
        </div>
        """
        alert_placeholder.markdown(alert_html, unsafe_allow_html=True)
    else:
        alert_placeholder.empty()

    time.sleep(1)

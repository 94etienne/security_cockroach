import streamlit as st
import numpy as np
import pandas as pd
import time
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
EMAIL_ADDRESS = "19etienne@gmail.com"
EMAIL_PASSWORD = "ojmh uvwb qrbo qpgy"   # Your Gmail App Password
TO_EMAIL = "ntambara94etienne@gmail.com"

# Page setup with mobile optimization
st.set_page_config(
    page_title="AI Agent Dashboard", 
    page_icon="🤖", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Advanced responsive CSS with mobile-first approach
st.markdown("""
<style>
    /* Base styles for all devices */
    .main-header {
        text-align: center;
        padding: 1rem 0;
    }
    
    .status-safe {
        background: #d4edda;
        color: #155724;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin: 0.5rem 0;
        border: 1px solid #c3e6cb;
    }
    
    .status-alert {
        background: #f8d7da;
        color: #721c24;
        padding: 0.75rem;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
        margin: 0.5rem 0;
        border: 1px solid #f5c6cb;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #007bff;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
    }
    
    .email-indicator {
        background: #fff3cd;
        color: #856404;
        padding: 0.5rem;
        border-radius: 5px;
        text-align: center;
        font-size: 0.9rem;
        margin: 0.5rem 0;
        border: 1px solid #ffeaa7;
    }
    
    /* Mobile devices (portrait phones, less than 576px) */
    @media (max-width: 576px) {
        .main-header h1 {
            font-size: 1.5rem !important;
        }
        
        .main-header h3 {
            font-size: 1rem !important;
        }
        
        .metric-card {
            padding: 0.75rem;
            margin: 0.25rem 0;
        }
        
        .section-header {
            padding: 0.75rem;
            font-size: 0.9rem;
        }
        
        /* Hide some secondary info on mobile */
        .mobile-hidden {
            display: none;
        }
    }
    
    /* Tablets (landscape phones, 576px and up) */
    @media (min-width: 576px) and (max-width: 768px) {
        .main-header h1 {
            font-size: 1.75rem !important;
        }
        
        .metric-card {
            padding: 0.9rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "last_heat_state" not in st.session_state:
    st.session_state.last_heat_state = 0
if "alert_msg" not in st.session_state:
    st.session_state.alert_msg = None
if "system_status" not in st.session_state:
    st.session_state.system_status = "ACTIVE"
if "last_email_sent" not in st.session_state:
    st.session_state.last_email_sent = None
if "email_cooldown" not in st.session_state:
    st.session_state.email_cooldown = 0

# Email function with cooldown to prevent spam
def send_heat_alert_email(temperature):
    """Send email alert only when heat is detected with cooldown period"""
    current_time = time.time()
    
    # Check cooldown (5 minutes between emails)
    if current_time - st.session_state.email_cooldown < 300:  # 300 seconds = 5 minutes
        return False
    
    try:
        # Create message
        subject = "🔥 HEAT DETECTION ALERT - AI Agent System"
        body = f"""
🚨 HEAT SIGNATURE DETECTED 🚨

AI Agent System has detected elevated temperatures:

• Detection Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
• Infrared Temperature: {temperature:.1f}°C
• System: Autonomous Exploration Agent
• Status: Investigation Required

The system will continue monitoring and provide updates.

---
AI Agent Dashboard
Autonomous Exploration System
        """
        
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        
        # Send email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
        
        # Update cooldown timer
        st.session_state.email_cooldown = current_time
        st.session_state.last_email_sent = datetime.now().strftime('%H:%M:%S')
        return True
        
    except Exception as e:
        st.error(f"Email failed: {str(e)}")
        return False

# Generate synthetic data functions
def generate_navigation():
    return {
        "accel_x": np.random.normal(0, 0.5),
        "accel_y": np.random.normal(0, 0.5),
        "accel_z": np.random.normal(9.8, 0.3),
        "gyro_x": np.random.normal(0, 0.03),
        "gyro_y": np.random.normal(0, 0.03),
        "gyro_z": np.random.normal(0, 0.03),
        "obstacle_distance_cm": np.clip(np.random.normal(50, 8), 5, 150),
        "speed_cm_per_s": np.clip(np.random.normal(6, 2), 0, 20),
        "battery_level": np.clip(np.random.normal(85, 5), 0, 100)
    }

def generate_thermal():
    heat_detected = np.random.random() > 0.85  # 15% chance for testing
    base_temp = 65 if heat_detected else 40
    return {
        "ambient_temp_c": np.clip(np.random.normal(30, 5), 23, 150),
        "surface_temp_c": np.clip(np.random.normal(base_temp, 10), 23, 150),
        "infrared_temp_c": np.clip(np.random.normal(base_temp + 20, 15), 23, 150),
        "heat_detected": heat_detected
    }

def generate_environment():
    return {
        "humidity": np.clip(np.random.normal(45, 10), 20, 80),
        "pressure": np.clip(np.random.normal(1013, 5), 1000, 1020),
        "light_level": np.clip(np.random.normal(500, 100), 0, 1000)
    }

# Mobile-optimized component functions
def display_navigation_mobile(nav_data):
    st.markdown('<div class="section-header">🧭 NAVIGATION SYSTEM</div>', unsafe_allow_html=True)
    
    # Critical metrics first
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Speed", f"{nav_data['speed_cm_per_s']:.1f} cm/s")
    with col2:
        st.metric("Obstacle", f"{nav_data['obstacle_distance_cm']:.1f} cm")
    
    # Battery with warning
    if nav_data['battery_level'] < 30:
        st.error(f"🔋 Battery: {nav_data['battery_level']:.1f}%")
    else:
        st.metric("Battery", f"{nav_data['battery_level']:.1f}%")
    
    # Acceleration in expander to save space
    with st.expander("Acceleration Data"):
        acc_col1, acc_col2, acc_col3 = st.columns(3)
        with acc_col1:
            st.metric("Accel X", f"{nav_data['accel_x']:.2f}")
        with acc_col2:
            st.metric("Accel Y", f"{nav_data['accel_y']:.2f}")
        with acc_col3:
            st.metric("Accel Z", f"{nav_data['accel_z']:.2f}")
    
    # Gyroscope in expander
    with st.expander("Gyroscope Data"):
        gyro_col1, gyro_col2, gyro_col3 = st.columns(3)
        with gyro_col1:
            st.metric("Gyro X", f"{nav_data['gyro_x']:.3f}")
        with gyro_col2:
            st.metric("Gyro Y", f"{nav_data['gyro_y']:.3f}")
        with gyro_col3:
            st.metric("Gyro Z", f"{nav_data['gyro_z']:.3f}")

def display_thermal_mobile(thermal_data):
    st.markdown('<div class="section-header">🔥 THERMAL DETECTION</div>', unsafe_allow_html=True)
    
    # Status first
    if thermal_data['heat_detected']:
        st.markdown('<div class="status-alert">🚨 HEAT SIGNATURE DETECTED</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-safe">✅ NO HEAT DETECTED</div>', unsafe_allow_html=True)
    
    # Critical temperature
    temp_col1, temp_col2 = st.columns(2)
    with temp_col1:
        st.metric("Infrared", f"{thermal_data['infrared_temp_c']:.1f}°C")
    with temp_col2:
        st.metric("Surface", f"{thermal_data['surface_temp_c']:.1f}°C")
    
    # Additional temps in expander
    with st.expander("All Temperature Readings"):
        st.metric("Ambient", f"{thermal_data['ambient_temp_c']:.1f}°C")
        if thermal_data['heat_detected']:
            st.progress(0.8, "High Temperature Alert")
        else:
            st.progress(0.3, "Normal Temperature Range")

def display_environment_mobile(env_data):
    st.markdown('<div class="section-header">🌡️ ENVIRONMENT</div>', unsafe_allow_html=True)
    
    env_col1, env_col2 = st.columns(2)
    with env_col1:
        st.metric("Humidity", f"{env_data['humidity']:.1f}%")
    with env_col2:
        st.metric("Pressure", f"{env_data['pressure']:.1f} hPa")
    
    # Environment status
    if env_data['humidity'] > 70:
        st.warning("High Humidity Detected")
    elif env_data['humidity'] < 30:
        st.warning("Low Humidity Detected")
    else:
        st.success("Optimal Conditions")

def display_predictions_mobile(nav_data, thermal_data):
    st.markdown('<div class="section-header">🎯 AI DECISIONS</div>', unsafe_allow_html=True)
    
    # Navigation decision
    if nav_data['obstacle_distance_cm'] < 20:
        nav_decision = "🔄 TURN RIGHT"
        st.warning(nav_decision)
    elif nav_data['obstacle_distance_cm'] < 40:
        nav_decision = "🔄 TURN LEFT"
        st.warning(nav_decision)
    else:
        nav_decision = "⬆️ FORWARD"
        st.success(nav_decision)
    
    # Thermal decision
    if thermal_data['heat_detected']:
        thermal_decision = "🚨 INVESTIGATE HEAT"
        st.error(thermal_decision)
    else:
        thermal_decision = "✅ CONTINUE EXPLORATION"
        st.success(thermal_decision)
    
    # System recommendations
    with st.expander("System Recommendations"):
        if nav_data['battery_level'] < 30:
            st.error("🔋 Low Battery - Return to base")
        elif thermal_data['heat_detected']:
            st.info("🔥 Heat source - Adjusting sensors")
        else:
            st.success("✅ All systems nominal")

# Desktop layout
def display_desktop_layout(nav_data, thermal_data, env_data):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🧭 Navigation System")
        
        nav_col1, nav_col2, nav_col3 = st.columns(3)
        with nav_col1:
            st.metric("Speed", f"{nav_data['speed_cm_per_s']:.1f} cm/s")
            st.metric("Accel X", f"{nav_data['accel_x']:.2f} m/s²")
        with nav_col2:
            st.metric("Obstacle", f"{nav_data['obstacle_distance_cm']:.1f} cm")
            st.metric("Accel Y", f"{nav_data['accel_y']:.2f} m/s²")
        with nav_col3:
            st.metric("Battery", f"{nav_data['battery_level']:.1f}%")
            st.metric("Accel Z", f"{nav_data['accel_z']:.2f} m/s²")
        
        st.markdown("**Gyroscope Data**")
        gyro_col1, gyro_col2, gyro_col3 = st.columns(3)
        with gyro_col1:
            st.metric("Gyro X", f"{nav_data['gyro_x']:.3f} rad/s")
        with gyro_col2:
            st.metric("Gyro Y", f"{nav_data['gyro_y']:.3f} rad/s")
        with gyro_col3:
            st.metric("Gyro Z", f"{nav_data['gyro_z']:.3f} rad/s")
    
    with col2:
        st.markdown("### 🔥 Thermal Detection")
        
        if thermal_data['heat_detected']:
            st.markdown('<div class="status-alert">🚨 HEAT SIGNATURE DETECTED</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-safe">✅ NO HEAT DETECTED</div>', unsafe_allow_html=True)
        
        temp_col1, temp_col2, temp_col3 = st.columns(3)
        with temp_col1:
            st.metric("Ambient", f"{thermal_data['ambient_temp_c']:.1f}°C")
        with temp_col2:
            st.metric("Surface", f"{thermal_data['surface_temp_c']:.1f}°C")
        with temp_col3:
            st.metric("Infrared", f"{thermal_data['infrared_temp_c']:.1f}°C")
        
        if thermal_data['heat_detected']:
            st.progress(0.8, "High Temperature Alert")
        else:
            st.progress(0.3, "Normal Temperature Range")
    
    st.markdown("---")
    
    # Second row for desktop
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 🌡️ Environment Sensors")
        
        env_col1, env_col2, env_col3 = st.columns(3)
        with env_col1:
            st.metric("Humidity", f"{env_data['humidity']:.1f}%")
        with env_col2:
            st.metric("Pressure", f"{env_data['pressure']:.1f} hPa")
        with env_col3:
            st.metric("Light Level", f"{env_data['light_level']:.0f} lux")
        
        if env_data['humidity'] > 70:
            st.warning("High Humidity Detected")
        elif env_data['humidity'] < 30:
            st.warning("Low Humidity Detected")
        else:
            st.success("Optimal Environment Conditions")
    
    with col4:
        st.markdown("### 🎯 AI Predictions & Decisions")
        
        # Navigation Prediction
        if nav_data['obstacle_distance_cm'] < 20:
            nav_decision = "🔄 TURN RIGHT"
            decision_color = "orange"
        elif nav_data['obstacle_distance_cm'] < 40:
            nav_decision = "🔄 TURN LEFT" 
            decision_color = "orange"
        else:
            nav_decision = "⬆️ FORWARD"
            decision_color = "green"
        
        # Thermal Decision
        if thermal_data['heat_detected']:
            thermal_decision = "🚨 INVESTIGATE HEAT SOURCE"
            thermal_color = "red"
        else:
            thermal_decision = "✅ CONTINUE EXPLORATION"
            thermal_color = "green"
        
        pred_col1, pred_col2 = st.columns(2)
        with pred_col1:
            st.markdown(f"**Navigation:**<br><span style='color:{decision_color}; font-weight:bold;'>{nav_decision}</span>", unsafe_allow_html=True)
        with pred_col2:
            st.markdown(f"**Thermal Action:**<br><span style='color:{thermal_color}; font-weight:bold;'>{thermal_decision}</span>", unsafe_allow_html=True)
        
        if nav_data['battery_level'] < 30:
            st.error("🔋 Low Battery - Consider returning to base")
        elif thermal_data['heat_detected']:
            st.info("🔥 Heat source detected - Adjusting sensor sensitivity")
        else:
            st.success("✅ All systems nominal - Continue mission")

# Mobile layout (stacked vertically)
def display_mobile_layout(nav_data, thermal_data, env_data):
    # Stack all sections vertically
    display_navigation_mobile(nav_data)
    st.markdown("---")
    display_thermal_mobile(thermal_data)
    st.markdown("---")
    display_environment_mobile(env_data)
    st.markdown("---")
    display_predictions_mobile(nav_data, thermal_data)

# Main Dashboard with responsive detection
def main_dashboard():
    # Header Section - Responsive
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown("# 🤖 AI Autonomous Exploration System")
    st.markdown("### Real-time Navigation & Thermal Detection Dashboard")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # System Status Bar - Responsive columns
    status_col1, status_col2, status_col3, status_col4 = st.columns(4)
    with status_col1:
        st.metric("System Status", st.session_state.system_status, "Online")
    with status_col2:
        st.metric("Last Update", datetime.now().strftime("%H:%M:%S"))
    with status_col3:
        st.metric("Uptime", "Continuous", "100%")
    with status_col4:
        cooldown_left = max(0, 300 - (time.time() - st.session_state.email_cooldown))
        if cooldown_left > 0:
            st.metric("Email Cooldown", f"{int(cooldown_left/60)}m {int(cooldown_left%60)}s")
        else:
            st.metric("Email Status", "Ready")
    
    st.markdown("---")
    
    # Generate all data
    nav_data = generate_navigation()
    thermal_data = generate_thermal()
    env_data = generate_environment()
    
    # Handle email alerts - ONLY when heat is detected
    if thermal_data['heat_detected'] and st.session_state.last_heat_state == 0:
        email_sent = send_heat_alert_email(thermal_data['infrared_temp_c'])
        if email_sent:
            st.session_state.alert_msg = f"🚨 HEAT DETECTED & EMAIL SENT at {datetime.now().strftime('%H:%M:%S')}"
        else:
            st.session_state.alert_msg = f"🚨 HEAT DETECTED at {datetime.now().strftime('%H:%M:%S')} (Email failed)"
    
    st.session_state.last_heat_state = 1 if thermal_data['heat_detected'] else 0
    
    # Device detection and layout selection
    use_mobile = st.checkbox("📱 Mobile View", value=False, help="Toggle mobile-optimized layout")
    
    if use_mobile:
        display_mobile_layout(nav_data, thermal_data, env_data)
    else:
        display_desktop_layout(nav_data, thermal_data, env_data)
    
    st.markdown("---")
    
    # Alert System (common to both layouts)
    st.markdown("### 📊 System Alerts & Status")
    
    # Display current alert
    if st.session_state.alert_msg and thermal_data['heat_detected']:
        st.error(st.session_state.alert_msg)
        if st.session_state.last_email_sent:
            st.markdown(f'<div class="email-indicator">📧 Last email sent: {st.session_state.last_email_sent}</div>', unsafe_allow_html=True)
    else:
        st.success("No active alerts - System operating normally")
    
    # Quick Stats - Responsive columns
    if use_mobile:
        stats_col1, stats_col2 = st.columns(2)
        with stats_col1:
            st.metric("Data Points", f"{np.random.randint(1000, 5000):,}")
        with stats_col2:
            st.metric("Sensor Accuracy", "98.7%")
    else:
        stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
        with stats_col1:
            st.metric("Data Points", f"{np.random.randint(1000, 5000):,}")
        with stats_col2:
            st.metric("Processing Speed", "Real-time")
        with stats_col3:
            st.metric("Sensor Accuracy", "79%")
        with stats_col4:
            st.metric("Mission Duration", "Continuous")

# Run the responsive dashboard
if __name__ == "__main__":
    main_dashboard()
    
    # Auto-refresh for real-time updates
    time.sleep(3)
    st.rerun()
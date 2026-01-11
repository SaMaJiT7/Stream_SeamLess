import streamlit as st
import time
import obsws_python as obs
import os
from dotenv import load_dotenv
from AI_Switcher import get_network_metrics, get_decision

# --- CONFIG ---
st.set_page_config(page_title="AI Stream Manager", page_icon="📡")

# --- UI LAYOUT ---
st.title("📡 AI Stream Sentinel")

# Create placeholders (Empty boxes we will fill later)
col1, col2 = st.columns(2)
with col1:
    ping_metric = st.empty()
with col2:
    status_banner = st.empty()
    
chart_placeholder = st.empty()
log_placeholder = st.empty() # For debug messages

# --- START BUTTON ---
if "running" not in st.session_state:
    st.session_state.running = False

if st.button("🔴 STOP AI" if st.session_state.running else "🟢 START AI"):
    st.session_state.running = not st.session_state.running
    # We don't rerun here, we just let the logic below take over

# --- THE CONTINUOUS LOOP ---
if st.session_state.running:
    
    # 1. Connect ONCE (This stays alive effectively)
    try:
        # No password needed since you disabled it
        client = obs.ReqClient(host="localhost", port=4455)
        st.toast("✅ OBS Connected and Locked In!")
    except Exception as e:
        st.error(f"❌ Could not connect to OBS: {e}")
        st.stop()

    ping_history = []
    current_scene = "Unknown"

    # 2. Loop Forever (No st.rerun calls!)
    while st.session_state.running:
        
        # A. Get Data
        ping_val, jitter, loss = get_network_metrics()
        ping_history.append(ping_val)
        if len(ping_history) > 100: ping_history.pop(0)

        # B. Get Decision
        target_scene, msg, color = get_decision(ping_val, jitter, loss)

        # C. Update UI (Update the placeholders, don't refresh page)
        ping_metric.metric("Live Ping", f"{ping_val:.1f} ms")
        
        if color == "success":
            status_banner.success(f"{msg}")
        elif color == "warning":
            status_banner.warning(f"{msg}")
        else:
            status_banner.error(f"{msg}")
            
        chart_placeholder.line_chart(ping_history)

        # D. SWITCH SCENE (Check Reality vs Target)
        try:
            # Ask OBS where we are
            real_scene = client.get_current_program_scene().current_program_scene_name # type: ignore
            
            # Update the debug log
            log_placeholder.code(f"OBS: {real_scene} | TARGET: {target_scene}")

            if real_scene != target_scene:
                client.set_current_program_scene(target_scene)
                print(f"Switched to {target_scene}")
                
        except Exception as e:
            log_placeholder.error(f"OBS Error: {e}")
            # Try to reconnect if connection drops
            try:
                client = obs.ReqClient(host="localhost", port=4455)
            except:
                pass

        # E. Wait a bit
        time.sleep(0.5)
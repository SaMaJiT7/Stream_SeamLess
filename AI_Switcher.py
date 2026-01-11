import time 
import joblib
import pandas as pd 
from ping3 import ping 
import obsws_python as obs # type: ignore
import os
from dotenv import load_dotenv

#--load environment variables from .env file--
load_dotenv()
OBS_PASSWORD = os.getenv("OBS_Password")


if not OBS_PASSWORD:
    print("Error: OBS_PASSWORD not set/present in .env file!")
    exit()


# --- CONFIG ---
OBS_HOST = "localhost"
OBS_PORT = 4455


SCENE_NORMAL = "Scene"
SCENE_PHONE = "Phone_Scene"
SCENE_ERROR = "BRB_Scene"

MODEL_FILE = "stream_model.pkl"
TARGET_HOST = "1.1.1.1"

#Loading the brain
print("Loading AI Model...")
try:
    model = joblib.load(MODEL_FILE)
    print("Model Loaded Successfully!")
except:
    model = None




def get_network_metrics():
    """Gets the raw numbers: Ping, Jitter, Loss"""
    try:
        latency = ping(TARGET_HOST, unit='ms')
        if latency is None:
            return 1000,100,1
        jitter = abs(latency - 20)
        return latency,jitter,  0
    except:
        return 1000,100,1



def get_decision(current_ping, jitter, pkt_loss):

    if model:
        df = pd.DataFrame([[current_ping, jitter, pkt_loss]], columns=['ping', 'jitter','pkt_loss'])
        prediction = model.predict(df)[0] # type: ignore
    # print(f"Predicted: {'NORMAL' if prediction == 0 else 'LAGGY'} | Metrics: {metrics}")
    else:
        prediction = 0 # Default to NORMAL if no model

    # Logic Tree
    if 200 < current_ping <= 300:
        return SCENE_PHONE, "⚠️ SWITCHING TO PHONE", "warning"
    elif prediction == 1 or current_ping > 300:
        return SCENE_ERROR, "🔴 CRITICAL FAILURE", "error"
    else:
        return SCENE_NORMAL, "✅ CONNECTION STABLE", "success"
        
    
if __name__ == "__main__":
    if not OBS_PASSWORD:
        print("Error: OBS_PASSWORD not set/present in .env file!")
        exit()
    
    #Connecting to OBS
    print("Connecting to OBS...")
    try:
        client = obs.ReqClient(host = OBS_HOST, port = OBS_PORT, password = OBS_PASSWORD)
        print("Connected to OBS successfully!")
    except Exception as e:
        print(f"Error: Could not connect to OBS. {e}")
        exit()

    print("\n🤖 AI STREAM MANAGER IS ACTIVE. Monitoring network...")
    # --- MAIN LOOP ---
    current_scene = SCENE_NORMAL

    while True:
        ping_val, jitter, pkt_loss = get_network_metrics()
        target_scene, status_message, result = get_decision(ping_val, jitter, pkt_loss)

        # Print Status
        if result != "success":
            print(f"{status_message} | Ping: {ping_val:.1f}ms")
        else:
            print(f"✅ Stable ({ping_val:.1f}ms)", end="\r")

        # Switching scenes if needed
        if current_scene != target_scene:
            try:
                print(f"\n   >>> SWITCHING: {current_scene} -> {target_scene}")
                client.set_current_program_scene(target_scene)
                current_scene = target_scene
            except Exception as e:
                print(f"Error: Could not switch scenes in OBS. {e}")
        
        time.sleep(0.6)
        


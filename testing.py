import obsws_python as obs
import time

print("--- 🩺 CONNECTION DOCTOR STARTING ---")

# 1. Try to connect WITHOUT a password (since you disabled auth)
try:
    print("1. Attempting connection to localhost:4455 (No Password)...")
    client = obs.ReqClient(host='localhost', port=4455)
    print("✅ SUCCESS! Connected to OBS.")
    
except Exception as e:
    print("\n❌ CONNECTION FAILED.")
    print(f"Error Details: {e}")
    
    # 2. Troubleshoot based on error
    if "refused" in str(e):
        print("\n👉 DIAGNOSIS: OBS is not listening.")
        print("   FIX: Go to Tools -> WebSocket Server Settings.")
        print("   FIX: Ensure 'Enable WebSocket server' is CHECKED.")
        print("   FIX: Ensure Port is 4455.")
    
    elif "authentication" in str(e):
        print("\n👉 DIAGNOSIS: OBS still expects a password.")
        print("   FIX: Go to Tools -> WebSocket Server Settings.")
        print("   FIX: UNCHECK 'Enable Authentication'.")
    
    exit() # Stop here if failed

# 3. If connected, list the scenes
print("\n--- 📋 YOUR SCENE LIST ---")
try:
    scenes = client.get_scene_list().scenes
    for s in scenes:
        print(f"   • '{s['sceneName']}'")
    print("-" * 30)
except Exception as e:
    print(f"❌ Could not list scenes: {e}")
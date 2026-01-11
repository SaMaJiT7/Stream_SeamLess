import time
from ping3 import ping
import pandas as pd

TARGET_HOST = "1.1.1.1"
PING_INTERVAL = 0.2
SAMPLE_SIZE = 500
OUTPUT_CSV = "high_dataloss_log.csv"


def log_ping_times(label):
    data = []
    print(f"\n>>> STARTING: {'NORMAL (0)' if label == 0 else 'LAGGY (1)'}")
    print(f"Collecting {SAMPLE_SIZE} samples...")

    for i in range(SAMPLE_SIZE):
        try:
            response_time = ping(TARGET_HOST, unit='ms')


            if response_time is None:
                response_time = 1000
                pkt_loss = 1
                jitter = 100
            else:
                pkt_loss = 0
                jitter = abs(response_time - 20)  # Assuming 20ms as a baseline for jitter calculation


                data.append({
                    "ping" : round(response_time,2),
                    "jitter": round(jitter, 2),
                    "pkt_loss": pkt_loss,
                    "label": label
                })

                if i % 10 == 0:
                    print(f"{i}/{SAMPLE_SIZE} | Ping: {response_time:.1f}ms")
        except:
            pass
        time.sleep(PING_INTERVAL)
    return data


if __name__ == "__main__":
    all_data = []
    
    # 1. NORMAL RUN
    input("Press Enter to record NORMAL data (Ensure Clumsy is STOPPED)...")
    all_data.extend(log_ping_times(0))
    
    
    # 2. LAGGY RUN
    print("\n" + "="*30)
    print("OPEN CLUMSY NOW.")
    print("1. Select 'Outbound'")
    print("2. Check 'Lag' -> Set to 300")
    print("3. Click 'Start' in Clumsy")
    input("Press Enter here when Clumsy is running...")
    all_data.extend(log_ping_times(1))

    # SAVE
    pd.DataFrame(all_data).to_csv(OUTPUT_CSV, index=False)
    print(f"\nDONE! Saved {len(all_data)} rows to {OUTPUT_CSV}")
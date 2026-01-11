import pandas as pd 
import numpy as np 
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib


# --- CONFIG ---
DATA_FILE = "training_data.csv"
MODEL_FILE = "stream_model.pkl"

def train():
    print("Step 1: Merging Data Files...")
    try:
        # 1. Load and Merge all your individual logs
        # Note: Make sure these files exist in the folder!
        df_list = [
            pd.read_csv('ping_log.csv'),
            pd.read_csv('dataloss_log.csv'),
            pd.read_csv('high_dataloss_log.csv'),
            pd.read_csv('mid_dataloss_log.csv')
        ]
        df = pd.concat(df_list, ignore_index=True)
        

        print(f"Original Row Count: {len(df)}")
        
        # Rule: If a row is labeled "Bad" (1), but the Ping is excellent (< 60ms) 
        # and there is No Loss, it's actually a "Good" packet.
        # Let's remove it so it doesn't confuse the AI.
        condition_to_remove = (df['label'] == 1) & (df['ping'] < 60) & (df['pkt_loss'] == 0)
        df = df.drop(df[condition_to_remove].index)
        
        print(f"Cleaned Row Count: {len(df)} (Removed confusing data points)")


        # Save it so you have a master record (Optional but good practice)
        df.to_csv(DATA_FILE, index=False)
        print(f" -> Successfully merged {len(df)} rows into '{DATA_FILE}'")
    except FileNotFoundError:
        print(f"Error: Could not find {DATA_FILE}. Did you run the logger?")
        return
    

    X = df[['ping', 'jitter', 'pkt_loss']]
    y = df['label']

    print(f"Training on {len(df)} data points...")


    X_train, X_test, y_train, y_test =  train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)


    model.fit(X_train, y_train)


    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    print("\n" + "="*30)
    print(f"MODEL ACCURACY: {accuracy * 100:.2f}%")
    print("="*30)
    print("\nDetailed Report:")
    print(classification_report(y_test, predictions))


    # 6. Save the Brain
    joblib.dump(model, MODEL_FILE)
    print(f"Saved model to '{MODEL_FILE}'")

if __name__ == "__main__":
    train()
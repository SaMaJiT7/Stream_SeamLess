# 📡 Stream SeamLess - AI-Powered Stream Manager

An intelligent streaming assistant that automatically switches OBS scenes based on network conditions using machine learning.

## 🌟 Features

- **Real-time Network Monitoring**: Continuously monitors ping, packet loss, and jitter
- **AI-Powered Scene Switching**: Machine learning model decides when to switch between scenes
- **Interactive Dashboard**: Streamlit-based web interface for monitoring and control
- **Data Logging**: Records network metrics for training and analysis
- **Training Mode**: Collect data and train custom models for your network

## 📋 Prerequisites

- Python 3.11 or higher
- OBS Studio with WebSocket plugin enabled
- FFmpeg (for media processing)
- **Clumsy** (optional - for testing/training with simulated network lag)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/SaMaJiT7/Stream_SeamLess.git
cd Stream_SeamLess
```

### 2. Install FFmpeg

**Windows:**
```bash
winget install ffmpeg
```
Or download from [ffmpeg.org](https://ffmpeg.org/download.html)

**Mac:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg
```

### 3. Install Clumsy (Optional - For Testing)

Clumsy is used to simulate network lag when collecting training data.

**Windows:**
Download from [jagt.github.io/clumsy](https://jagt.github.io/clumsy/)

**Note:** Clumsy is Windows-only. On Mac/Linux, you can use `tc` (traffic control) or similar tools.

### 4. Create Virtual Environment
```bash
python -m venv stream
```

**Activate the virtual environment:**

Windows:
```bash
stream\Scripts\activate
```

Mac/Linux:
```bash
source stream/bin/activate
```

### 5. Install Dependencies
```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, install these packages:
```bash
pip install streamlit obsws-python ping3 pandas numpy scikit-learn joblib python-dotenv altair
```

### 6. Configure OBS WebSocket

1. Open OBS Studio
2. Go to **Tools → WebSocket Server Settings**
3. Enable WebSocket server
4. Set port to **4455** (or note your custom port)
5. Set a password and remember it

### 7. Create Environment File

Create a `.env` file in the project root:
```env
OBS_Password=your_obs_websocket_password_here
```

Replace `your_obs_websocket_password_here` with your actual OBS WebSocket password.

### 8. Configure OBS Scenes

Make sure you have these scenes in OBS:
- **Scene** - Your normal streaming scene
- **Phone_Scene** - Backup scene when network is poor
- **BRB_Scene** - "Be Right Back" scene for severe issues

You can customize scene names in `AI_Switcher.py`:
```python
SCENE_NORMAL = "Scene"
SCENE_PHONE = "Phone_Scene"
SCENE_ERROR = "BRB_Scene"
```

## 🎮 Usage

### Running the Dashboard

```bash
streamlit run Dashboard.py
```

The dashboard will open in your browser at `http://localhost:8501`

### Training the Model (Optional)

If you want to train a custom model for your network:

1. **Collect Training Data** with simulated network conditions:
```bash
python data_Logger.py
```

Follow the prompts:
- First, it collects data under **normal** network conditions
- Then, use **Clumsy** to simulate lag:
  - Set "Outbound" mode
  - Enable "Lag" and set to 300ms
  - Click "Start"
- It then collects data under **laggy** conditions

2. **Train the Model:**
```bash
python train_mode.py
```

This creates `stream_model.pkl` which the AI uses for predictions.

### Manual AI Switcher

To run the AI switcher without the dashboard:
```bash
python AI_Switcher.py
```

## 📁 Project Structure

- `Dashboard.py` - Streamlit web interface
- `AI_Switcher.py` - Core AI logic and OBS control
- `data_Logger.py` - Network data collection
- `train_mode.py` - Model training script
- `testing.py` - Testing utilities
- `.env` - Environment variables (create this)
- `stream_model.pkl` - Trained ML model (generated)

## 🛠️ Troubleshooting

### OBS Connection Failed
- Ensure OBS is running
- Verify WebSocket is enabled in OBS
- Check password in `.env` file matches OBS
- Confirm port is 4455 (or update in code)

### Import Errors
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### Network Monitoring Issues
- Check internet connection
- Verify firewall isn't blocking ping
- Try changing `TARGET_HOST` in scripts (default: 1.1.1.1)

## 📊 How It Works

1. **Monitors Network**: Pings target host to measure latency and packet loss
2. **AI Prediction**: Machine learning model analyzes network metrics
3. **Scene Control**: Automatically switches OBS scenes based on network quality:
   - Good network → Normal Scene
   - Poor network → Phone Scene
   - Critical issues → BRB Scene

## 🤝 Contributing

Feel free to open issues or submit pull requests!

## 📄 License

MIT License - Feel free to use and modify for your projects.

## 👤 Author

SaMaJiT - [GitHub](https://github.com/SaMaJiT7)

---

**Note**: This tool requires a stable internet connection to monitor network metrics. Make sure your firewall allows ICMP (ping) requests.

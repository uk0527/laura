import requests
import os
from pydub import AudioSegment

# Ensure the static directory exists
AUDIO_DIR = "static"
os.makedirs(AUDIO_DIR, exist_ok=True)

def download_audio(audio_url):
    """Downloads audio from Twilio's Recording URL and saves it."""
    local_audio_path = os.path.join(AUDIO_DIR, "user_audio.wav")
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "audio/mpeg"
    }

    response = requests.get(audio_url, headers=headers, stream=True)

    if response.status_code == 200:
        with open(local_audio_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        print(f"✅ Audio downloaded: {local_audio_path}")
        return local_audio_path
    else:
        print(f"❌ Failed to download audio. Status code: {response.status_code}")
        return None

def convert_audio(audio_path):
    """Converts Twilio audio to WAV format (16kHz, mono)."""
    converted_path = os.path.join(AUDIO_DIR, "converted_audio.wav")
    
    try:
        audio = AudioSegment.from_file(audio_path)
        audio = audio.set_frame_rate(16000).set_channels(1)
        audio.export(converted_path, format="wav")
        print(f"🔄 Converted audio saved as {converted_path}")
        return converted_path
    except Exception as e:
        print(f"❌ Error converting audio: {e}")
        return None

def transcribe(audio_path):
    """Simulates transcription (replace with Whisper or OpenAI API call)."""
    print(f"🎤 Transcribing audio: {audio_path}")
    return "Hello Laura, I would like to schedule a meeting."


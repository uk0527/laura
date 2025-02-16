from gtts import gTTS
import os

def generate_audio():
    audio_dir = "static"
    os.makedirs(audio_dir, exist_ok=True)  # Ensure the folder exists
    audio_path = os.path.join(audio_dir, "response_audio.mp3")

    text = "Hello! This is Laura speaking."

    try:
        tts = gTTS(text, lang="en")
        tts.save(audio_path)
        print(f"✅ Audio file saved: {audio_path}")
    except Exception as e:
        print(f"❌ Error generating audio: {e}")

generate_audio()

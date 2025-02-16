from flask import Flask, request, send_from_directory, url_for
import os
import requests
from gtts import gTTS
from pydub import AudioSegment
from twilio.twiml.voice_response import VoiceResponse
from ai_response import generate_ai_response_with_memory  # AI processing
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

# Initialize Flask app
app = Flask(__name__, static_folder="static")

@app.route("/voice", methods=["POST"])
def voice():
    """Handles incoming Twilio calls and starts recording"""
    response = VoiceResponse()
    response.say("Hello! I am Laura, Uday's personal assistant. How can I assist you?", voice="alice")
    response.record(timeout=5, transcribe=True, transcribe_callback="/transcribe")
    return str(response)

def text_to_speech(text):
    """Converts AI response to Twilio-compatible speech in WAV format"""
    audio_dir = "static"
    os.makedirs(audio_dir, exist_ok=True)  # Ensure folder exists
    temp_audio_path = os.path.join(audio_dir, "temp.mp3")
    final_audio_path = os.path.join(audio_dir, "response_audio.wav")  # Use WAV format for Twilio

    try:
        # Generate initial MP3 using gTTS
        tts = gTTS(text, lang="en")
        tts.save(temp_audio_path)

        # Convert MP3 to Twilio-compatible WAV format (8kHz, mono)
        audio = AudioSegment.from_file(temp_audio_path, format="mp3")
        audio = audio.set_frame_rate(8000).set_channels(1)
        audio.export(final_audio_path, format="wav")

        print(f"✅ Twilio-compatible WAV saved: {final_audio_path}")

    except Exception as e:
        print(f"❌ Error generating audio: {e}")

    return final_audio_path

def download_audio(audio_url):
    """Downloads Twilio-recorded audio and saves it locally."""
    save_path = "static/user_audio.wav"
    try:
        # 🔹 Add Twilio authentication
        response = requests.get(audio_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))

        if response.status_code == 200:
            with open(save_path, "wb") as f:
                f.write(response.content)
            print(f"✅ Audio downloaded: {save_path}")
            return save_path
        else:
            print(f"❌ Failed to download audio. Status code: {response.status_code}, Message: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Error downloading audio: {e}")
        return None

@app.route("/transcribe", methods=["POST"])
def transcribe():
    """Processes Twilio voice recording, transcribes, generates AI response, and plays it"""
    user_id = request.form.get("From")
    audio_url = request.form.get("RecordingUrl")

    if not audio_url:
        return "Error: No audio received", 400

    print(f"🔗 Audio URL received: {audio_url}")

    # Download and transcribe the caller's voice message
    audio_path = download_audio(audio_url)
    if not audio_path:
        return "Error: Failed to download audio", 500

    # Generate AI response based on the transcribed caller's text
    response_text = generate_ai_response_with_memory("Hello, Laura!", user_id)
    print(f"🤖 AI Response: {response_text}")  # Debugging line

    # Convert AI response to speech
    text_to_speech(response_text)

    response = VoiceResponse()
    
    # Generate public URL for Twilio to access the WAV file
    public_audio_url = url_for('serve_audio', filename="response_audio.wav", _external=True)
    print(f"🔗 Audio URL for Twilio: {public_audio_url}")  # Debugging line
    
    response.play(public_audio_url)  # Play WAV response

    return str(response)

@app.route("/static/<filename>")
def serve_audio(filename):
    """Serves the generated audio file for Twilio to access"""
    return send_from_directory("static", filename, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(port=5000)

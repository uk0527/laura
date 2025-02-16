from gtts import gTTS
import os

def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    filename = "output.mp3"
    tts.save(filename)
    return filename

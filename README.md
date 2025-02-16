📞 Laura AI Call Assistant
🚀 Laura is an AI-powered voice assistant that integrates with Twilio to handle incoming calls, transcribe speech, generate AI responses, and play them back using Google TTS. The assistant can also schedule meetings, retrieve stored knowledge, and remember user interactions.

📜 Features
✅ Twilio Integration – Handles incoming calls & transcribes speech
✅ AI-Powered Responses – Uses OpenRouter AI to generate answers
✅ Meeting Scheduling – Checks availability & books meetings
✅ Memory Storage – Saves past user conversations
✅ Speech Synthesis – Converts AI responses to speech
✅ Knowledge Retrieval – Uses FAISS for relevant information

🛠️ Installation & Setup

1️⃣ Install Dependencies
sh
Copy
Edit
pip install -r requirements.txt

2️⃣ Set Up Environment Variables
Create a .env file in the root folder and add:

ini
Copy
Edit
OPENROUTER_API_KEY=your_openrouter_api_key
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

3️⃣ Initialize Database
sh
Copy
Edit
python calendar_local.py  # Creates meetings database
python ai_response.py     # Initializes user memory database

4️⃣ Start Flask Server
sh
Copy
Edit
python app.py

📞 How It Works
🚀 Call Flow
1️⃣ User calls Twilio number

2️⃣ Laura answers: "Hello! I am Laura. How can I assist you?"

3️⃣ User speaks

4️⃣ Twilio records & sends audio

5️⃣ Whisper transcribes speech

6️⃣ AI generates a response

7️⃣ Response is converted to speech & played back

🔗 API Endpoints
Method	Endpoint	Description
POST	/voice	Handles incoming Twilio calls
POST	/transcribe	Processes recorded speech & generates response
GET	/static/<filename>	Serves audio files for Twilio


⚠️ Troubleshooting

🔴 Issue: No AI response / blank playback
✔️ Fix: Check OPENROUTER_API_KEY in .env

🔴 Issue: Call hangs up after recording
✔️ Fix: Ensure whisper_stt.py correctly downloads audio.

🔴 Issue: "No such table: user_memory"
✔️ Fix: Run python ai_response.py to initialize the database.

📌 Future Improvements

🔹 Add GPT-4 integration for better responses

🔹 Improve meeting scheduling with Google Calendar

🔹 Implement multi-language support

🔹 Deploy to a cloud server for 24/7 availability
🎉 Enjoy your AI Call Assistant! 🚀

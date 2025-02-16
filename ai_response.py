import sqlite3
import json
import requests
import calendar_local
import datetime
import os
from dotenv import load_dotenv
from knowledge_base import retrieve_knowledge

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

def connect_db():
    """Connects to SQLite database."""
    return sqlite3.connect("database/user_memory.db")

def load_user_memory(user_id):
    """Loads user conversation history from SQLite."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT memory FROM user_memory WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return json.loads(result[0]) if result else {}

def save_user_memory(user_id, memory):
    """Saves user conversation history to SQLite."""
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO user_memory (user_id, memory) VALUES (?, ?)", (user_id, json.dumps(memory)))
    conn.commit()
    conn.close()

def process_meeting_request(user_input):
    """Detects meeting request and schedules if available."""
    if "schedule" in user_input.lower():
        now = datetime.datetime.now()
        start_time = (now + datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        end_time = (now + datetime.timedelta(days=1, hours=1)).strftime("%Y-%m-%d %H:%M:%S")

        if calendar_local.check_availability(start_time, end_time):
            return calendar_local.schedule_meeting("Meeting with Laura", start_time, end_time)
        else:
            return "Sorry, the requested time slot is already booked."
    return None

def generate_ai_response_with_memory(user_input, user_id):
    """Retrieves user memory and generates a personalized AI response."""
    if not OPENROUTER_API_KEY:
        return "❌ AI service is unavailable. Missing API key."

    user_memory = load_user_memory(user_id)
    retrieved_knowledge = retrieve_knowledge(user_input)

    prompt = f"""
    You are Laura, an AI assistant. The user previously mentioned:
    {user_memory.get('history', 'No prior conversations')}
    Use the following knowledge to respond:
    {retrieved_knowledge}
    
    User: {user_input}
    Laura:
    """

    payload = {
        "model": "deepseek-ai/deepseek-coder-1",
        "messages": [{"role": "system", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 200
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
            json=payload,
            timeout=10  # Prevent long response delays
        )

        if response.status_code == 200:
            ai_response = response.json().get("choices", [{}])[0].get("message", {}).get("content", "I'm sorry, I couldn't generate a response.")
        else:
            print(f"🔴 API Error: {response.status_code} - {response.text}")
            ai_response = "I'm having trouble generating a response right now. Please try again later."

    except requests.exceptions.RequestException as e:
        print(f"🔴 Request Exception: {e}")
        ai_response = "There was an issue connecting to the AI service."

    # Save memory and update conversation history
    user_memory["history"] = f"{user_memory.get('history', '')}\nUser: {user_input}\nLaura: {ai_response}"
    save_user_memory(user_id, user_memory)

    return ai_response

import sqlite3
import datetime

DB_FILE = "database/meetings.db"

# Initialize database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            summary TEXT,
            start_time TEXT,
            end_time TEXT
        )
    """)
    conn.commit()
    conn.close()

def schedule_meeting(summary, start_time, end_time):
    """Schedules a meeting in the local database"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Check for conflicts
    cursor.execute("""
        SELECT * FROM meetings WHERE 
        (start_time BETWEEN ? AND ?) OR (end_time BETWEEN ? AND ?)
    """, (start_time, end_time, start_time, end_time))
    
    if cursor.fetchone():
        conn.close()
        return "Sorry, the requested time slot is already booked."

    # Insert new meeting
    cursor.execute("INSERT INTO meetings (summary, start_time, end_time) VALUES (?, ?, ?)",
                   (summary, start_time, end_time))
    conn.commit()
    conn.close()
    
    return f"Meeting scheduled: {summary} from {start_time} to {end_time}"

def check_availability(start_time, end_time):
    """Checks if a time slot is available"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM meetings WHERE 
        (start_time BETWEEN ? AND ?) OR (end_time BETWEEN ? AND ?)
    """, (start_time, end_time, start_time, end_time))
    
    available = cursor.fetchone() is None
    conn.close()
    return available

# Run this function once to create the database
init_db()

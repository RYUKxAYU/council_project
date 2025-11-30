
import sqlite3, time, json, os

DB_PATH = os.path.join(os.path.dirname(__file__), "council.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user_input TEXT,
            final_verdict TEXT,
            full_json TEXT
        );
    """)
    conn.commit()
    conn.close()

def save_transcript(user_input, final_verdict, full_json):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO transcripts (timestamp, user_input, final_verdict, full_json) VALUES (?, ?, ?, ?)",
        (time.strftime("%Y-%m-%d %H:%M:%S"), user_input, final_verdict, json.dumps(full_json)),
    )
    conn.commit()
    conn.close()

init_db()

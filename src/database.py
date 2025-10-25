import sqlite3
import json
import time

DB_PATH = "typing_results.db"

def init_db():
    """Initialize database and table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL,
            wpm REAL,
            accuracy REAL,
            num_words INTEGER,
            expected_text TEXT,
            user_input TEXT,
            key_times TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_test_result(wpm, accuracy, num_words, expected_text, user_input, key_times):
    """Save test results into database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO test_results (
            timestamp, wpm, accuracy, num_words, expected_text, user_input, key_times
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        time.time(),
        wpm,
        accuracy,
        num_words,
        expected_text,
        json.dumps(user_input),
        json.dumps(key_times)
    ))
    conn.commit()
    conn.close()

def get_latest_test_result():
    """Fetch the most recent test result from the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT expected_text, user_input, key_times 
        FROM test_results 
        ORDER BY timestamp DESC 
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    expected_text, user_input_json, key_times_json = row
    return {
        "text": expected_text,
        "user_input": json.loads(user_input_json),
        "key_times": json.loads(key_times_json)
    }

import sqlite3
import json
import time
from collections import defaultdict

DB_PATH = "output/typing_results.db"

def init_db():
    """Initialize database and clear all existing data."""
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
    # Clear all rows
    # cursor.execute("DELETE FROM test_results")
    conn.commit()
    conn.close()

def save_test_result(wpm, accuracy, num_words, expected_text, user_input, key_times):
    """Save test results into database and return the new row ID."""
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
    new_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return new_id

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

def get_all_test_results():
    """Fetch all test results including ID for identifying specific entries."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, timestamp, wpm, accuracy, num_words
        FROM test_results
        ORDER BY timestamp DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_test_by_id(test_id):
    """Fetch a full test record by unique ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT expected_text, user_input, key_times 
        FROM test_results
        WHERE id = ?
        LIMIT 1
    """, (test_id,))
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

def generate_full_digraph_table_recent(n=None):
    """
    Builds a digraph timing table based on the 2 most recent times (not tests).
    Returns:
        table: dict[row_char][col_char] = avg of 2 most recent times (ms)
        chars: sorted list of unique characters
    """
    import string
    tests = get_all_full_tests()
    transitions = defaultdict(list)

    order_counter = 0  # To keep order of appearance
    for test in tests:
        chars = test["user_input"]
        times = test["key_times"]
        for i in range(len(chars) - 1):
            pair = chars[i] + chars[i + 1]
            # Store (order index, time in ms)
            transitions[pair].append((order_counter, times[i + 1] * 1000))
            order_counter += 1

    # Keep only 2 most recent times per digraph
    trimmed = {}
    for pair, entries in transitions.items():
        # sort by order descending (most recent last)
        recent_entries = sorted(entries, key=lambda x: x[0], reverse=True)[:2]
        recent_times = [t for _, t in recent_entries]
        trimmed[pair] = sum(recent_times) / len(recent_times)

    # Collect all characters seen
    all_chars = set(string.ascii_lowercase)
    for pair in trimmed.keys():
        all_chars.update(pair)

    # Build table
    table = {}
    for row_char in all_chars:
        table[row_char] = {}
        for col_char in all_chars:
            pair = row_char + col_char
            table[row_char][col_char] = trimmed.get(pair, None)

    return table, sorted(all_chars)


def get_all_full_tests():
    """
    Fetch all tests with user_input and key_times.
    Returns a list of dictionaries:
    [{"user_input": [...], "key_times": [...]}, ...]
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT user_input, key_times
        FROM test_results
        ORDER BY timestamp ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    return [
        {"user_input": json.loads(u), "key_times": json.loads(t)}
        for u, t in rows
    ]

def get_info(self):
    """Fetch basic info about the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM test_results")
    count = cursor.fetchone()[0]
    conn.close()
    return {
        "total_tests": count
    }
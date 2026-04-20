import hashlib
import os
import sqlite3

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'user_data.db'))


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS userdata (
        id INTEGER PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    )
    """)

    users = [
        ("SHILOHHH123", "SHILOOHHSSpassword"),
        ("buggs", "bunny123"),
        ("bob", "bobpass")
    ]
    for username, password in users:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cur.execute("INSERT OR IGNORE INTO userdata (username, password) VALUES (?, ?)", (username, hashed_password))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()


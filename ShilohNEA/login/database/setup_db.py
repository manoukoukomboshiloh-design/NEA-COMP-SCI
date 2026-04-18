import hashlib
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "userdata.db")
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
id INTEGER PRIMARY KEY,
username VARCHAR(255) NOT NULL,
password VARCHAR(255) NOT NULL
)
""")
# random guys in here
users = [
    ("SHILOHHH123", "SHILOOHHSSpassword"),
    ("buggs", "bunny123"),
    ("bob", "bobpass")
]
for username, password in users:
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username, hashed_password))
conn.commit()
conn.close()


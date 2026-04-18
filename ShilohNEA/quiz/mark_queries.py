import os
import sqlite3

DATABASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'user_data.db'))


def ensure_mark_query_table(db_path: str = DATABASE_PATH):
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS mark_queries (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                username TEXT NOT NULL,
                topic TEXT NOT NULL,
                question_text TEXT NOT NULL,
                expected_answer TEXT NOT NULL,
                user_answer TEXT NOT NULL,
                reason TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                admin_notes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reviewed_at TIMESTAMP
            )
            '''
        )
        con.commit()


def submit_mark_query(
    user_id: int,
    username: str,
    topic: str,
    question_text: str,
    expected_answer: str,
    user_answer: str,
    reason: str = "",
    db_path: str = DATABASE_PATH,
) -> int:
    ensure_mark_query_table(db_path)
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(
            '''
            INSERT INTO mark_queries (user_id, username, topic, question_text, expected_answer, user_answer, reason)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (user_id, username, topic, question_text, expected_answer, user_answer, reason.strip()),
        )
        con.commit()
        return cur.lastrowid


def get_pending_mark_queries(db_path: str = DATABASE_PATH) -> list[dict]:
    ensure_mark_query_table(db_path)
    with sqlite3.connect(db_path) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM mark_queries WHERE status = 'pending' ORDER BY created_at DESC")
        return [dict(row) for row in cur.fetchall()]


def resolve_mark_query(query_id: int, approved: bool, admin_notes: str = "", db_path: str = DATABASE_PATH):
    ensure_mark_query_table(db_path)
    status = "approved" if approved else "rejected"
    with sqlite3.connect(db_path) as con:
        cur = con.cursor()
        cur.execute(
            '''
            UPDATE mark_queries
            SET status = ?, admin_notes = ?, reviewed_at = CURRENT_TIMESTAMP
            WHERE id = ?
            ''',
            (status, admin_notes.strip(), query_id),
        )
        con.commit()

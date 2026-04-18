import os
import sqlite3

DATABASE_NAME = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'user_data.db'))


def ensure_progress_table(cur):
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='progress'")
    if cur.fetchone() is None:
        cur.execute('''
        CREATE TABLE progress (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            topic VARCHAR(255) NOT NULL,
            score INTEGER NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES userdata(id)
        )
        ''')
        return

    cur.execute("PRAGMA table_info(progress)")
    existing_columns = {row[1] for row in cur.fetchall()}
    required_columns = {'user_id', 'topic', 'score'}

    if required_columns.issubset(existing_columns):
        return

    cur.execute("ALTER TABLE progress RENAME TO progress_legacy")
    cur.execute('''
    CREATE TABLE progress (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        topic VARCHAR(255) NOT NULL,
        score INTEGER NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES userdata(id)
    )
    ''')

    cur.execute("PRAGMA table_info(progress_legacy)")
    legacy_columns = {row[1] for row in cur.fetchall()}
    if {'username', 'score'}.issubset(legacy_columns):
        cur.execute('''
        INSERT INTO progress (user_id, topic, score)
        SELECT COALESCE(u.id, 0), 'General', p.score
        FROM progress_legacy p
        LEFT JOIN userdata u ON u.username = p.username
        WHERE p.score IS NOT NULL
        ''')

    cur.execute("DROP TABLE progress_legacy")


def setup_full_database():
    con = sqlite3.connect(DATABASE_NAME)
    cur = con.cursor()

    # Users table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS userdata (
        id INTEGER PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    )
    ''')

    # Questions table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY,
        topic VARCHAR(255) NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
    ''')

    # Quizzes table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        topic VARCHAR(255) NOT NULL,
        start_time TIMESTAMP,
        end_time TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES userdata(id)
    )
    ''')

    # Results table (quiz results per question)
    cur.execute('''
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY,
        quiz_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        user_answer TEXT,
        correct INTEGER,
        FOREIGN KEY(quiz_id) REFERENCES quizzes(id),
        FOREIGN KEY(question_id) REFERENCES questions(id)
    )
    ''')

    # Progress table (summary)
    ensure_progress_table(cur)

    # Mark review requests table
    cur.execute('''
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
        reviewed_at TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES userdata(id)
    )
    ''')

    con.commit()
    con.close()

if __name__ == "__main__":
    setup_full_database()
    print("Database and tables created.")

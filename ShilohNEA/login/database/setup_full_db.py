import sqlite3

def setup_full_database():
    con = sqlite3.connect('user_data.db')
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
    cur.execute('''
    CREATE TABLE IF NOT EXISTS progress (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        topic VARCHAR(255) NOT NULL,
        score INTEGER NOT NULL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES userdata(id)
    )
    ''')

    con.commit()
    con.close()

if __name__ == "__main__":
    setup_full_database()
    print("Database and tables created.")

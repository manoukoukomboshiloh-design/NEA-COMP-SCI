import os
import sqlite3

DATABASE_NAME = os.path.abspath(os.path.join(os.path.dirname(__file__), 'user_data.db'))


def save_score(user_id, topic, score):
    con = sqlite3.connect(DATABASE_NAME)
    cur = con.cursor()

    cur.execute("""
        INSERT INTO progress (user_id, topic, score)
        VALUES (?, ?, ?)
    """, (user_id, topic, score))

    con.commit()
    con.close()


def show_dashboard(user_id):
    con = sqlite3.connect(DATABASE_NAME)
    cur = con.cursor()

    print("\n--- DASHBOARD ---")

    # Average per topic
    cur.execute("""
        SELECT topic, ROUND(AVG(score), 2)
        FROM progress
        WHERE user_id = ?
        GROUP BY topic
    """, (user_id,))
    
    averages = cur.fetchall()

    print("\nAverage Scores:")
    for topic, avg in averages:
        print(f"{topic}: {avg}")

    # Best score
    cur.execute("""
        SELECT MAX(score)
        FROM progress
        WHERE user_id = ?
    """, (user_id,))
    
    best = cur.fetchone()[0]
    print(f"\nBest Score: {best}")

    # Total quizzes
    cur.execute("""
        SELECT COUNT(*)
        FROM progress
        WHERE user_id = ?
    """, (user_id,))
    
    total = cur.fetchone()[0]
    print(f"Total Quizzes: {total}")

    con.close() 
    print()
    print()
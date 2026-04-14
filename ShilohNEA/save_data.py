import sqlite3

def save_score(user_id, topic, score):
    con = sqlite3.connect('user_data.db')
    cur = con.cursor()

    cur.execute("""
        INSERT INTO progress (user_id, topic, score)
        VALUES (?, ?, ?)
    """, (user_id, topic, score))

    con.commit()
    con.close()


def show_dashboard(user_id):
    con = sqlite3.connect('user_data.db')
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
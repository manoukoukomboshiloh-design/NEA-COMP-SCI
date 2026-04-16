import sqlite3


def get_topic_averages(user_id):
    try:
        with sqlite3.connect('user_data.db') as con:
            cur = con.cursor()
            cur.execute(
                """
                SELECT topic, AVG(score)
                FROM progress
                WHERE user_id = ?
                GROUP BY topic
                """,
                (user_id,),
            )
            return cur.fetchall()
    except sqlite3.Error:
        return []


def get_total_quizzes(user_id):
    try:
        with sqlite3.connect('user_data.db') as con:
            cur = con.cursor()
            cur.execute(
                """
                SELECT COUNT(*)
                FROM progress
                WHERE user_id = ?
                """,
                (user_id,),
            )
            result = cur.fetchone()
            return result[0] if result else 0
    except sqlite3.Error:
        return 0


def get_best_score(user_id):
    try:
        with sqlite3.connect('user_data.db') as con:
            cur = con.cursor()
            cur.execute(
                """
                SELECT MAX(score)
                FROM progress
                WHERE user_id = ?
                """,
                (user_id,),
            )
            result = cur.fetchone()
            return result[0] if result and result[0] is not None else 0
    except sqlite3.Error:
        return 0
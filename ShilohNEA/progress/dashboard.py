import os
import sqlite3

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'user_data.db'))


def _run_single_value_query(query: str, params: tuple) -> int:
    try:
        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute(query, params)
            result = cur.fetchone()
            return result[0] if result and result[0] is not None else 0
    except sqlite3.Error as exc:
        print(f"Dashboard query failed: {exc}")
        return 0


def get_topic_averages(user_id):
    try:
        with sqlite3.connect(DB_PATH) as con:
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
    except sqlite3.Error as exc:
        print(f"Could not load topic averages: {exc}")
        return []


def get_total_quizzes(user_id: int) -> int:
    return _run_single_value_query(
        """
        SELECT COUNT(*)
        FROM progress
        WHERE user_id = ?
        """,
        (user_id,),
    )


def get_best_score(user_id: int) -> int:
    return _run_single_value_query(
        """
        SELECT MAX(score)
        FROM progress
        WHERE user_id = ?
        """,
        (user_id,),
    )
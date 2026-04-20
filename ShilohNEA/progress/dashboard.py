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


def get_username(user_id: int) -> str | None:
    try:
        with sqlite3.connect(DB_PATH) as con:
            cur = con.cursor()
            cur.execute(
                """
                SELECT username
                FROM userdata
                WHERE id = ?
                """,
                (user_id,),
            )
            result = cur.fetchone()
            return result[0] if result else None
    except sqlite3.Error as exc:
        print(f"Could not load username: {exc}")
        return None


def show_user_dashboard(user_id: int, username: str | None = None) -> bool:
    if username is None:
        username = get_username(user_id)

    if not username:
        print(f"No user found with ID {user_id}.")
        return False

    separator = "~~~~~~~~~~~~~~~~~~~~~"
    print(f"\n{separator}")
    print("~~~~ DASHBOARD ~~~~")
    print(separator)
    print(f"User: {username} (ID: {user_id})")
    print(f"Total quizzes taken: {get_total_quizzes(user_id)}")
    print(f"Best score: {get_best_score(user_id)}")
    print(separator)
    print("Average scores by topic:")

    averages = get_topic_averages(user_id)
    if averages:
        for topic, avg in averages:
            print(f"- {topic}: {avg:.2f}")
    else:
        print("- No quiz data yet")

    print(separator)
    print()
    print()
    return True
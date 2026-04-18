def get_topic_averages(user_id):
    con = sqlite3.connect('user_data.db')
    cur = con.cursor()

    cur.execute("""
        SELECT topic, AVG(score)
        FROM progress
        WHERE user_id = ?
        GROUP BY topic
    """, (user_id,))

    results = cur.fetchall()
    con.close()
    return results

def get_total_quizzes(user_id: int) -> int:
    """Return the total number of quizzes completed by the user."""
    return _run_single_value_query(
        """
        SELECT COUNT(*)
        FROM progress
        WHERE user_id = ?
        """,
        user_id,
    )


def get_best_score(user_id: int) -> int:
    """Return the user's highest recorded quiz score."""
    return _run_single_value_query(
        """
        SELECT MAX(score)
        FROM progress
        WHERE user_id = ?
    """, (user_id,))

    result = cur.fetchone()[0]
    con.close()
    return result
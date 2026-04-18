"""Dashboard data helpers for displaying a user's quiz progress."""

import logging
import os
import sqlite3

DATABASE_NAME = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "user_data.db"))
LOGGER = logging.getLogger(__name__)


def _get_connection() -> sqlite3.Connection:
    """Return a connection to the dashboard database."""
    return sqlite3.connect(DATABASE_NAME)


def _run_single_value_query(query: str, user_id: int, default: int = 0) -> int:
    """Run a query that returns one numeric value for a given user."""
    try:
        with _get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()

            if not result or result[0] is None:
                return default

            return int(result[0])
    except sqlite3.Error as error:
        LOGGER.warning("Dashboard query failed for user %s: %s", user_id, error)
        return default


def get_topic_averages(user_id: int) -> list[tuple[str, float]]:
    """Return the average score achieved in each topic for a user."""
    try:
        with _get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT topic, AVG(score)
                FROM progress
                WHERE user_id = ?
                GROUP BY topic
                ORDER BY topic
                """,
                (user_id,),
            )
            return cursor.fetchall()
    except sqlite3.Error as error:
        LOGGER.warning("Unable to fetch topic averages for user %s: %s", user_id, error)
        return []


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
        """,
        user_id,
    )
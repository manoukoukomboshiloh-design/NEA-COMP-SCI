import os
import sqlite3

DATABASE_NAME = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'user_data.db'))


def get_user_progress(username):
    con = sqlite3.connect(DATABASE_NAME)
    cur = con.cursor()
    cur.execute("""
        SELECT userdata.username, progress.topic, progress.score
        FROM userdata
        JOIN progress ON userdata.id = progress.user_id
        WHERE userdata.username = ?
    """, (username,))
    result = cur.fetchall()
    con.close()
    return result




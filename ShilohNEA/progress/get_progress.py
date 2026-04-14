import sqlite3

def get_user_progress(username):
    con = sqlite3.connect('user_data.db')
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




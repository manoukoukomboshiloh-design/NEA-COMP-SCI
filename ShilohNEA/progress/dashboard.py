def get_topic_averages(user_id):
    con = sqlite3.connect('user_data.db')
    cur = con.cursor()

    cur.execute("""
        SELECT topic, AVG(score)   #calculates average score from topics
        FROM progress
        WHERE user_id = ?          #parameterised query for security
        GROUP BY topic             
        #uses 
    """, (user_id,))

    results = cur.fetchall()
    con.close()
    return results

def get_total_quizzes(user_id):
    con = sqlite3.connect('user_data.db')
    cur = con.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM progress
        WHERE user_id = ?
    """, (user_id,))

    result = cur.fetchone()[0]
    con.close()
    return result

def get_best_score(user_id):
    con = sqlite3.connect('user_data.db')
    cur = con.cursor()

    cur.execute("""
        SELECT MAX(score)
        FROM progress
        WHERE user_id = ?
    """, (user_id,))

    result = cur.fetchone()[0]
    con.close()
    return result

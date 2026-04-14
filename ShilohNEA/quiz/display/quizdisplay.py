def show_leaderboard():
    import sqlite3
    con = sqlite3.connect('user_data.db')
    cur = con.cursor()
    # Aggregate total score per user
    cur.execute('''
        SELECT u.username, SUM(p.score) as total_score, COUNT(p.id) as quizzes_taken
        FROM userdata u
        JOIN progress p ON u.id = p.user_id
        GROUP BY u.id
        ORDER BY total_score DESC, quizzes_taken DESC
        LIMIT 10
    ''')
    results = cur.fetchall()
    con.close()
    print("\n===== Leaderboard: Top Users =====")
    print(f"{'Rank':<5}{'User':<15}{'Total Score':<12}{'Quizzes Taken':<14}")
    for i, (username, total_score, quizzes_taken) in enumerate(results, start=1):
        print(f"{i:<5}{username:<15}{total_score:<12}{quizzes_taken:<14}")
    print("="*40)


import sys
import os
import time
# Ensure project root is in sys.path for imports
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from quiz.display.question_bank import question_data as data
from quiz.topic_graph import graph
from quiz.oop_quiz import User, Question, Quiz, Session



def display_menu(data):
    all_topics = list(data["topics"].keys())

    print("Welcome, please select a topic number")
    for i, topic in enumerate(all_topics, start=1):
        print(f"{i}. {topic}")
    print("L. Leaderboard")
    print("0. Exit")

    choice = input("Enter a topic number or 'L' for leaderboard: ")
    if choice.lower() == 'l':
        show_leaderboard()
        return display_menu(data)
    try:
        choice = int(choice)
        if choice == 0:
            print("Okie dokie see you soon..")
            return None
        elif 1 <= choice <= len(all_topics):
            return all_topics[choice - 1]
        else:
            print(f"Gotta be a number between 1 and {len(all_topics)}")
            return display_menu(data)
    except ValueError:
        print("Enter a valid whole number or 'L'")
        return display_menu(data)


def display_notes(selected_topic, data):
    topic_data = data["topics"][selected_topic]
    notes = topic_data["notes"]

    print(f"\n{'='*60}")
    print(f"TOPIC: {selected_topic}")
    print(f"{'='*60}\n")

    print("NOTES:")
    print("-" * 60)

    for i, note in enumerate(notes, start=1):
        print(f"{i}. {note}\n")

    print(f"{'='*60}\n")

def auto_timer_with_skip():
    print("You have 10 minutes to revise...")
    print("Press 's' then Enter at any time to skip to the quiz.")
    start = time.time()
    while True:
        elapsed = time.time() - start
        remaining = 600 - elapsed
        print(f"\rTime left: {int(remaining)}s ", end="")
        if elapsed > 600:
            print("\nTime's up!")
            return
        # Check for skip
        import select
        import sys
        import msvcrt
        if msvcrt.kbhit():
            key = msvcrt.getwch()
            if key.lower() == 's':
                print("\nSkipping revision timer...")
                return
        time.sleep(1)

def run_quiz(selected_topic, data, session):
    questions_data = data["topics"][selected_topic].get("questions", [])
    if not questions_data:
        print("No questions available for this topic.")
        return 0
    questions = [Question(q['id'], q['question'], q['answer']) for q in questions_data]
    quiz = Quiz(selected_topic, questions)
    session.start_quiz(quiz)
    return quiz.score


def auto_timer():
    print("You have 10 minutes to revise...")

    start = time.time()

    while True:
        elapsed = time.time() - start
        remaining = 600 - elapsed

        print(f"\rTime left: {int(remaining)}s", end="")

        if elapsed > 600:
            print("\nTime's up!")
            return

        time.sleep(1)


def recommend_next_topic(score, selected_topic, data):
    if score >= 4:
        next_topics = graph.get(selected_topic, [])
        if next_topics:
            print(f"Since you're so good, why don't you try: {next_topics[0]}?")
            answer = input("Enter yes to continue or no to return to menu: ")
            if answer.lower() == "yes":
                return next_topics[0]
    else:
        print("Ah that didn't go to plan but it's ok!")
        print("1. Stay on this topic")
        print("2. Switch topics")
        print("q. Quit")
        choice = input("The choice is yours...: ")
        if choice == "1":
            return selected_topic
        elif choice == "2":
            new_topic = display_menu(data)
            return new_topic
        elif choice == "q":
            print("We're in the learning phase, take a break and hit back stronger!")
            return None
        else:
            print("Not a valid response")
            return None



def login_flow():
    print("Welcome to the Quiz System! Please log in.")
    while True:
        username = input("Username: ")
        password = input("Password: ")
        user = User.authenticate(username, password)
        if user:
            print(f"Login successful. Welcome, {user.username}!")
            return user
        else:
            print("Login failed. Please try again.")

user = login_flow()
session = Session(user)

while True:
    selected_topic = display_menu(data)
    if selected_topic is None:
        print("Program ended")
        break
    while selected_topic:
        display_notes(selected_topic, data)
        try:
            auto_timer_with_skip()
        except Exception as e:
            print(f"Timer error: {e}\nProceeding to quiz...")
        score = run_quiz(selected_topic, data, session)
        next_topic = recommend_next_topic(score, selected_topic, data)
        if next_topic and next_topic != selected_topic:
            selected_topic = next_topic
        elif next_topic == selected_topic:
            continue
        else:
            break


import os
import sqlite3
import sys
import time


def show_leaderboard():
    try:
        with sqlite3.connect('user_data.db') as con:
            cur = con.cursor()
            cur.execute('''
                SELECT u.username, COALESCE(SUM(p.score), 0) as total_score, COUNT(p.id) as quizzes_taken
                FROM userdata u
                JOIN progress p ON u.id = p.user_id
                GROUP BY u.id
                ORDER BY total_score DESC, quizzes_taken DESC
                LIMIT 10
            ''')
            results = cur.fetchall()
    except sqlite3.Error as exc:
        print(f"Could not load leaderboard: {exc}")
        return

    print("\n===== Leaderboard: Top Users =====")
    print(f"{'Rank':<5}{'User':<15}{'Total Score':<12}{'Quizzes Taken':<14}")
    for i, (username, total_score, quizzes_taken) in enumerate(results, start=1):
        print(f"{i:<5}{username:<15}{total_score:<12}{quizzes_taken:<14}")
    print("=" * 40)


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from quiz.display.question_bank import question_data as data
from quiz.topic_graph import graph
from quiz.oop_quiz import Question, Quiz, RevisionPlanner, Session, TimedQuiz, User


def display_menu(data):
    all_topics = list(data["topics"].keys())

    while True:
        print("Welcome, please select a topic number")
        for i, topic in enumerate(all_topics, start=1):
            print(f"{i}. {topic}")
        print("L. Leaderboard")
        print("0. Exit")

        choice = input("Enter a topic number or 'L' for leaderboard: ").strip()
        if choice.lower() == 'l':
            show_leaderboard()
            continue

        try:
            choice_num = int(choice)
            if choice_num == 0:
                print("Okie dokie see you soon..")
                return None
            if 1 <= choice_num <= len(all_topics):
                return all_topics[choice_num - 1]
            print(f"Gotta be a number between 1 and {len(all_topics)}")
        except ValueError:
            print("Enter a valid whole number or 'L'")


def display_notes(selected_topic, data):
    topic_data = data["topics"].get(selected_topic)
    if not topic_data:
        print("Topic data could not be found.")
        return

    notes = topic_data.get("notes", [])

    print(f"\n{'=' * 60}")
    print(f"TOPIC: {selected_topic}")
    print(f"{'=' * 60}\n")
    print("NOTES:")
    print("-" * 60)

    for i, note in enumerate(notes, start=1):
        print(f"{i}. {note}\n")

    print(f"{'=' * 60}\n")


def auto_timer_with_skip():
    print("You have 10 minutes to revise...")
    answer = input("Type 'skip' to go straight to the quiz, or press Enter to start the timer: ").strip().lower()
    if answer == 'skip':
        print("Skipping revision timer...")
        return

    start = time.time()
    while True:
        elapsed = time.time() - start
        remaining = max(0, 600 - elapsed)
        print(f"\rTime left: {int(remaining)}s", end="")

        if remaining <= 0:
            print("\nTime's up!")
            return

        time.sleep(1)


def run_quiz(selected_topic, data, session):
    questions_data = data["topics"].get(selected_topic, {}).get("questions", [])
    if not questions_data:
        print("No questions available for this topic.")
        return 0

    questions = [Question(q['id'], q['question'], q['answer']) for q in questions_data]
    mode = input("Choose quiz mode: 1 for standard, 2 for timed: ").strip()

    if mode == "2":
        quiz = TimedQuiz(selected_topic, questions, time_limit=90, username=session.user.username)
    else:
        quiz = Quiz(selected_topic, questions, username=session.user.username)

    session.start_quiz(quiz)

    planner = RevisionPlanner(session.user)
    mastery = planner.calculate_topic_mastery()
    if selected_topic in mastery:
        print(f"Current mastery score for {selected_topic}: {mastery[selected_topic]['mastery_score']}%")

    return quiz.score


def recommend_next_topic(score, selected_topic, data, session):
    if score >= 4:
        session.build_recommendation_queue(graph, selected_topic)
        next_topic = session.get_next_recommendation()
        if next_topic:
            print(f"Since you're doing well, your next recommended topic is: {next_topic}")
            answer = input("Enter yes to continue or no to return to menu: ").strip().lower()
            if answer == "yes":
                return next_topic
    else:
        planner = RevisionPlanner(session.user)
        weakest_topics = planner.weakest_topics_first()
        if weakest_topics:
            weakest_topic = weakest_topics[0][0]
            print(f"You may want to revisit this weaker topic soon: {weakest_topic}")

        print("Ah that didn't go to plan but it's ok!")
        print("1. Stay on this topic")
        print("2. Switch topics")
        print("q. Quit")
        choice = input("The choice is yours...: ").strip().lower()

        if choice == "1":
            return selected_topic
        if choice == "2":
            return display_menu(data)
        if choice == "q":
            print("We're in the learning phase, take a break and hit back stronger!")
            return None

        print("Not a valid response")
    return None


def login_flow():
    print("Welcome to the Quiz System! Please log in.")
    while True:
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        if not username or not password:
            print("Username and password cannot be blank.")
            continue

        user = User.authenticate(username, password)
        if user:
            print(f"Login successful. Welcome, {user.username}!")
            return user

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
        next_topic = recommend_next_topic(score, selected_topic, data, session)

        if next_topic and next_topic != selected_topic:
            selected_topic = next_topic
        elif next_topic == selected_topic:
            continue
        else:
            break

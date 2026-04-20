import os
import sqlite3
import sys
import threading
import time

from progress.dashboard import show_user_dashboard


def show_leaderboard():
    while True:
        try:
            with sqlite3.connect(DB_PATH) as con:
                cur = con.cursor()
                cur.execute('''
                    SELECT u.id, u.username, COALESCE(SUM(p.score), 0) as total_score, COUNT(p.id) as quizzes_taken
                    FROM userdata u
                    JOIN progress p ON u.id = p.user_id
                    GROUP BY u.id
                    ORDER BY total_score DESC, quizzes_taken DESC
                    LIMIT 10
                ''')
                results = cur.fetchall()
        except sqlite3.Error as exc:
            print(f"Could not load leaderboard: {exc}")
            return 'back'

        if not results:
            print("\nNo leaderboard data yet.")
            return 'back'

        print("\n~~~~~ Leaderboard: Top Users ~~~~~")
        print(f"{'Rank':<5}{'ID':<5}{'User':<15}{'Total Score':<12}{'Quizzes Taken':<14}")
        for i, (user_id, username, total_score, quizzes_taken) in enumerate(results, start=1):
            print(f"{i:<5}{user_id:<5}{username:<15}{total_score:<12}{quizzes_taken:<14}")
        print("~" * 40)
        print()
        print()

        selected_user_id = input("Enter a user ID to view their dashboard, press 'b' to go back, or type 'exit' to quit: ").strip().lower()
        if selected_user_id == 'b':
            return 'back'
        if _is_exit_command(selected_user_id):
            return 'exit'

        try:
            show_user_dashboard(int(selected_user_id))
        except ValueError:
            print("Enter a valid whole number, 'b' or 'exit'.")


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
DB_PATH = os.path.join(PROJECT_ROOT, 'user_data.db')
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from quiz.display.question_bank import question_data as data, save_user_question
from quiz.topic_graph import graph
from quiz.oop_quiz import Question, Quiz, RevisionPlanner, Session, TimedQuiz, User


BACK_TO_DASHBOARD = "__back__"


def _return_to_main_menu():
    print("Returning to the main menu...")


def _is_exit_command(value):
    return value.strip().lower() == 'exit'


def prompt_add_question(data):
    print("\nAdd your own question to the shared JSON file")
    print("Type 'exit' at any prompt to return to the main menu.")
    topic = input("Topic: ").strip()
    if _is_exit_command(topic):
        _return_to_main_menu()
        return

    question = input("Question: ").strip()
    if _is_exit_command(question):
        _return_to_main_menu()
        return

    answer = input("Mark scheme answer: ").strip()
    if _is_exit_command(answer):
        _return_to_main_menu()
        return

    try:
        new_entry = save_user_question(topic, question, answer)
    except ValueError as exc:
        print(exc)
        return

    if topic not in data["topics"]:
        data["topics"][topic] = {"notes": [], "questions": []}

    existing_pairs = {
        (item.get("question", ""), item.get("answer", ""))
        for item in data["topics"][topic].get("questions", [])
    }
    if (question, answer) not in existing_pairs:
        data["topics"][topic].setdefault("questions", []).append(new_entry)

    print("Your question has been saved. Cheers for contributing.")


def prompt_delete_question(data):
    from quiz.display.question_bank import delete_user_question, get_user_questions

    stored_data = get_user_questions()
    saved_questions = []

    for topic, questions in stored_data.get("topics", {}).items():
        for entry in questions:
            saved_questions.append((topic, entry))

    if not saved_questions:
        print("There are no user-added questions to delete.")
        return

    print("\nDelete one of your saved questions")
    print("Type 'exit' to return to the main menu.")
    for index, (topic, entry) in enumerate(saved_questions, start=1):
        print(f"{index}. [{topic}] {entry.get('question', '')}")

    choice = input("Enter the number of the question to delete: ").strip()
    if _is_exit_command(choice):
        _return_to_main_menu()
        return

    try:
        choice_num = int(choice)
        if not 1 <= choice_num <= len(saved_questions):
            print(f"Gotta be a number between 1 and {len(saved_questions)}")
            return
    except ValueError:
        print("Enter a valid whole number or 'exit'")
        return

    topic, entry = saved_questions[choice_num - 1]

    try:
        deleted_entry = delete_user_question(topic, entry["id"])
    except ValueError as exc:
        print(exc)
        return

    topic_info = data["topics"].get(topic)
    if topic_info:
        topic_info["questions"] = [
            item for item in topic_info.get("questions", [])
            if int(item.get("id", 0)) != int(deleted_entry["id"])
        ]
        if not topic_info.get("notes") and not topic_info["questions"]:
            data["topics"].pop(topic, None)

    print("Question deleted.")


def display_menu(data, allow_back=False, allow_leaderboard=False):
    while True:
        all_topics = list(data["topics"].keys())

        print("Welcome, please select a topic number")
        for i, topic in enumerate(all_topics, start=1):
            print(f"{i}. {topic}")
        print("A. Add a question")
        print("D. Delete a question")
        if allow_back:
            print("B. Back")
        if allow_leaderboard:
            print("L. Leaderboard")
        print("0. Exit")

        choice = input("Enter a topic number, 'A' to add a question, 'D' to delete a question, 'B' to go back or '0' to exit: ").strip().lower()
        if allow_back and choice == 'b':
            return BACK_TO_DASHBOARD
        if allow_leaderboard and choice == 'l':
            leaderboard_action = show_leaderboard()
            if leaderboard_action == 'exit':
                return None
            continue
        if choice == 'a':
            prompt_add_question(data)
            continue
        if choice == 'd':
            prompt_delete_question(data)
            continue

        try:
            choice_num = int(choice)
            if choice_num == 0:
                return None
            if 1 <= choice_num <= len(all_topics):
                return all_topics[choice_num - 1]
            print(f"Gotta be a number between 1 and {len(all_topics)}")
        except ValueError:
            if allow_back:
                print("Enter a valid whole number, 'A', 'D', 'B' or '0'")
            else:
                print("Enter a valid whole number, 'A', 'D' or '0'")


def display_notes(selected_topic, data):
    topic_data = data["topics"].get(selected_topic)
    if not topic_data:
        print("Topic data could not be found.")
        return

    notes = topic_data.get("notes", [])

    print(f"\n{'~' * 60}")
    print(f"TOPIC: {selected_topic}")
    print(f"{'~' * 60}\n")
    print("NOTES:")
    print("-" * 60)

    for i, note in enumerate(notes, start=1):
        print(f"{i}. {note}\n")

    print(f"{'~' * 60}\n")
    print()


def auto_timer_with_skip():
    print("You have 10 minutes to revise...")
    print("Type 's' and press Enter at any time to skip straight to the quiz.\n")

    skip_flag = {"skip": False}

    def listen_for_skip():
        try:
            answer = input().strip().lower()
            if answer in {'s', 'skip'}:
                skip_flag["skip"] = True
        except (KeyboardInterrupt, EOFError):
            return

    threading.Thread(target=listen_for_skip, daemon=True).start()

    for remaining in range(600, 0, -1):
        if skip_flag["skip"]:
            print("\nSkipping revision timer...\n")
            return

        print(f"\rTime left: {remaining}s", end="", flush=True)
        time.sleep(1)

    print("\nTime's up!\n")


def run_quiz(selected_topic, data, session):
    questions_data = data["topics"].get(selected_topic, {}).get("questions", [])
    if not questions_data:
        print("No questions available for this topic.")
        return 0

    notes_context = " ".join(data["topics"].get(selected_topic, {}).get("notes", []))
    questions = [Question(q['id'], q['question'], q['answer'], notes_context=notes_context) for q in questions_data]
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


def recommend_next_topic(score, selected_topic, data, session, allow_back=False):
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
            return display_menu(data, allow_back=allow_back)
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
            show_user_dashboard(user.user_id, user.username)
            return user

        print("Login failed. Please try again.")


def main():
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


if __name__ == "__main__":
    main()

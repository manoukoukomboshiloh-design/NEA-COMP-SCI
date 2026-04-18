import os
import socket
import subprocess
import sys
import time

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
SERVER_SCRIPT = os.path.join(BASE_DIR, 'login', 'server', 'server.py')
SETUP_DB_SCRIPT = os.path.join(BASE_DIR, 'login', 'database', 'setup_db.py')

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from progress.dashboard import get_best_score, get_total_quizzes, get_topic_averages
from quiz.display.question_bank import question_data
from quiz.display.quizdisplay import display_menu, display_notes
from quiz.getquiz.getquestions import Quiz, User


def show_dashboard(user_id, username):
    print("\n~~~~ DASHBOARD ~~~~")
    print(f"User: {username} (ID: {user_id})")
    print(f"Total quizzes taken: {get_total_quizzes(user_id)}")
    print(f"Best score: {get_best_score(user_id)}")
    print("\nAverage scores by topic:")
    for topic, avg in get_topic_averages(user_id):
        print(f"- {topic}: {avg:.2f}")
    print("~~~~~~~~~~~~~~~~~~~~~\n")


def safe_input(prompt):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nRun cancelled.")
        return None


def ensure_server_running():
    probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        probe.connect(("localhost", 9999))
        probe.close()
        return True
    except OSError:
        probe.close()

    try:
        subprocess.run([sys.executable, SETUP_DB_SCRIPT], check=False)
        subprocess.Popen(
            [sys.executable, SERVER_SCRIPT],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(1)
    except OSError as exc:
        print(f"Could not start the login server automatically: {exc}")
        return False

    for _ in range(10):
        probe = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            probe.connect(("localhost", 9999))
            probe.close()
            return True
        except OSError:
            probe.close()
            time.sleep(0.2)

    print("The login server could not be started automatically.")
    return False


def main():
    if not ensure_server_running():
        return

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(("localhost", 9999))

        message = client.recv(1024).decode()
        action = safe_input(message)
        if action is None:
            return
        client.send(action.strip().encode())

        if action.strip().lower() in {"3", "exit", "quit"}:
            print(client.recv(1024).decode())
            return

        message = client.recv(1024).decode()
        username = safe_input(message)
        if username is None:
            return
        client.send(username.strip().encode())

        message = client.recv(1024).decode()
        password = safe_input(message)
        if password is None:
            return
        client.send(password.strip().encode())

        login_response = client.recv(1024).decode()
        parts = login_response.split("|")
        status_message = parts[0]
        print(status_message)

        if "successful" not in status_message.lower():
            return

        user_id = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1
        username = parts[2] if len(parts) > 2 else username.strip()
        show_dashboard(user_id, username)

        user = User(user_id, username)
        while True:
            selected_topic = display_menu(question_data)
            if not selected_topic:
                print("See you next time.")
                break

            display_notes(selected_topic, question_data)
            quiz = Quiz(user, question_data)
            quiz.run(selected_topic)

    except OSError as exc:
        print(f"Could not connect to the server: {exc}")
    finally:
        client.close()


if __name__ == "__main__":
    main()


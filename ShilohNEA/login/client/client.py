
import socket
import subprocess
import sys
import time
import os
# Need sys for python runtime interaction, these 3 libraries are the basis of networking and file management


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
SERVER_SCRIPT = os.path.join(BASE_DIR, 'login', 'server', 'server.py')
SETUP_DB_SCRIPT = os.path.join(BASE_DIR, 'login', 'database', 'setup_db.py')

# putting the project root on sys.path lets python find the other folders cleanly
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from progress.dashboard import get_topic_averages, get_total_quizzes, get_best_score
from quiz.display.quizdisplay import display_menu, display_notes
from quiz.display.question_bank import question_data
from quiz.getquiz.getquestions import Quiz, User

#Taking the functions and classes from my other folders so I can set up the dashboard, all thats missing is a leaderboard of all my users ordering them on how many questions they ahave answered INSTEAD of how many right as effort shall be rewarded (ts for later)
#OOP 
#data abstraction 
#use of modules 

def show_dashboard(user_id, username):
	print("\n~~~~ DASHBOARD ~~~~") #equals sign for nice layout
	print(f"User: {username} (ID: {user_id})") #Displays the username and user ID at the top of the dashboard for a personalized touch
	print(f"Total quizzes taken: {get_total_quizzes(user_id)}")
	print(f"Best score: {get_best_score(user_id)}")
	print("\nAverage scores by topic:")
	for topic, avg in get_topic_averages(user_id):
		print(f"- {topic}: {avg:.2f}")
		#Loops through list of (topic,average) pairs and displays them for the user
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
    except OSError as exc:
        print(f"Could not connect to the login server: {exc}")
        return
    # this is connecting the client to da server, which is running on the same machine (localhost) and listening on port 9999. This sets up the communication channel for sending and receiving data between the client and server.

    message = client.recv(1024).decode()
    action = safe_input(message)
    if action is None:
        client.close()
        return
    client.send(action.strip().encode())

    if action.strip().lower() in {"3", "exit", "quit"}:
        print(client.recv(1024).decode())
        client.close()
        return

    message = client.recv(1024).decode()
    username = safe_input(message)
    if username is None:
        client.close()
        return
    client.send(username.encode())

    message = client.recv(1024).decode()
    password = safe_input(message)
    if password is None:
        client.close()
        return
    client.send(password.encode())

    login_response = client.recv(1024).decode()
    status_message = login_response.split("|")[0]
    print(status_message)
    #max bytes the client can receive is 1024 
    #we have the decoding then turning those bytes into a string which is now stored in the variable message, which is then printed to the user as a prompt for their username and password. The client's responses are then sent back to the server for authentication, and the server's response is printed to the user to indicate whether the login was successful or not.

    if "successful" in login_response.lower():
        parts = login_response.split("|")
        user_id = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else 1
        username = parts[2] if len(parts) > 2 else username
        show_dashboard(user_id, username)

        selected_topic = display_menu(question_data)
        if selected_topic:
            from quiz.display.auto_timer_with_skip import auto_timer_with_skip
            display_notes(selected_topic, question_data)
            auto_timer_with_skip()
            user = User(user_id, username)
            quiz = Quiz(user, question_data)
            quiz.run(selected_topic)
            client.close()
            return
    else:
        print(f"This aint {username} lolol. byebye.")

    client.close()

if __name__ == "__main__":
	main()
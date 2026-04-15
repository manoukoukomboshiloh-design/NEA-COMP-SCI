
import socket
import sys
import os	
# Need sys for python runtime interaction, these 3 libraries are the basis of networking and file management


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
PROGRESS_DIR = os.path.join(BASE_DIR, 'progress')
QUIZ_DISPLAY_DIR = os.path.join(BASE_DIR, 'quiz', 'display')
QUIZ_GETQUIZ_DIR = os.path.join(BASE_DIR, 'quiz', 'getquiz')

#Sets up my directory paths for the various modules, and adds them to sys.path if not already present, allowing for imports from those directories.
#This is absically like the roots of my revision guide tree, and allows me to keep my code organized in different folders without import issues.


if PROGRESS_DIR not in sys.path:
	sys.path.insert(0, PROGRESS_DIR)
if QUIZ_DISPLAY_DIR not in sys.path:
	sys.path.insert(0, QUIZ_DISPLAY_DIR)
if QUIZ_GETQUIZ_DIR not in sys.path:
	sys.path.insert(0, QUIZ_GETQUIZ_DIR)

#Ts makes the whole program look nice ye with custom folders that python can import from


from dashboard import get_topic_averages, get_total_quizzes, get_best_score
from quizdisplay import display_menu, display_notes
from question_bank import question_data
from getquestions import Quiz, User

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

def main():
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(("localhost", 9999))  # this is connecting the client to da server, which is running on the same machine (localhost) and listening on port 9999. This sets up the communication channel for sending and receiving data between the client and server.

	message = client.recv(1024).decode()
	username = input(message)
	client.send(username.encode())
	message = client.recv(1024).decode()
	password = input(message)
	client.send(password.encode())
	login_response = client.recv(1024).decode()
	print(login_response)
	#max bytes the client can receive is 1024 
	#we have the decoding then turning those bytes into a string which is now stored in the variable message, which is then printed to the user as a prompt for their username and password. The client's responses are then sent back to the server for authentication, and the server's response is printed to the user to indicate whether the login was successful or not.

	if "successful" in login_response.lower():
		# Checks the users inputted username and passoword against the server side user and password
		# This lower part turns all letter to lowercase, making it case insensitive
		user_id = 1
		show_dashboard(user_id, username)         #assign fixed user id and passing it through the displaying dashboard according to id and the username
		selected_topic = display_menu(question_data)
		if selected_topic:
			import threading #lets part of the program run at the same time
			sys.path.append(QUIZ_DISPLAY_DIR) ~from the python import paths addind a folder and allowing imports from this directory (gonna be used in other parts of the program)
			from auto_timer_with_skip_flag import auto_timer_with_skip_flag # timer begins
			display_notes(selected_topic, question_data)
			skip_flag = {'skip': False}         #new dictionary storing a shared variable to be modifed in a threaad. we dont skip the timer until the request is made
			def ask_skip():
				answer = input("\nDo you want to skip the timer and go straight to the quiz? Please put 'yes' or 'no': ").strip().lower()
				if answer == 'yes':
					skip_flag['skip'] = True
					#skips timer if user requests
			t = threading.Thread(target=ask_skip)      #new thread created to run ask skip separately
			t.start()
			auto_timer_with_skip_flag(skip_flag)
			user = User(user_id, username)
			quiz = Quiz(user, question_data)
			quiz.run(selected_topic)
			#Running the quiz when the skip is true or when the timer expires
			return
	else:
		print("Login failed. Exiting.")

if __name__ == "__main__":
	main()                   makes sure main program only runs whne the file is executed directly and not whenm imported as a moduyle              

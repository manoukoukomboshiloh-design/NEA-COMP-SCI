import hashlib
import math      #calculations of score and mastery
import os        #for file path handling
import re        #for keyword extraction
import time
import sqlite3
import threading   #runing timer in backgrounmd for the timed quizzes
from collections import deque  #making queues for recommendations
from typing import Deque, Dict, List, Optional       #multiple imports for type hints

#This is database pathing for the user data, ensures database is created in the correct location and can be accessed by all modules without hardcoding paths.
DATABASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'user_data.db'))


#this class is basically just the blueprint for one quiz question
#it stores the id, the actual question, the answer and any notes context for marking
class Question:                      #represents a single quiz question topped off with validation
    #constructor for setting up one question object safely
    def __init__(self, qid: int, text: str, answer: str, notes_context: str = ""):
        if not isinstance(qid, int):               #qid should be an integer
            raise ValueError("Idk man your question id must be an integer!")  
        if not isinstance(text, str) or not text.strip():               #text should be a non-empty string
            raise ValueError("Idk man your question text cannot be empty!")
        if not isinstance(answer, str) or not answer.strip():           #answer should be a non-empty string
            raise ValueError("Idk man your question answer cannot be empty!")        #if wrong value error is raised
        #Each question object contains the 4 main features of a question  
        self.qid = qid
        self.text = text.strip()
        self.answer = answer.strip()
        self.notes_context = notes_context.strip()


#this is one node in the linked list used for quiz history
#each node stores one quiz result and a pointer to the next one
class QuizHistoryNode:                #LINKED LIST NODE FOR STORING QUIZ HISTORY IN USER OBJECT
    #constructor for one linked list node
    def __init__(self, quiz, next_node=None):
        self.quiz = quiz
        self.next = next_node        #the next node depends on the order of quizzes taken, new quizzes are added to the head of the list


#this is the main quiz class and it handles asking questions + keeping score
class Quiz:                              #main quiz class            
    #sets up the quiz topic, question list and tracking variables like score
    def __init__(self, topic: str, questions: List[Question], username: str = "Player"):
        if not isinstance(topic, str) or not topic.strip():                    #topic should be a non-empty string    
            raise ValueError("Idk man your quiz topic must be a non-empty string!")
        if not isinstance(questions, list) or not questions:                   #questions should be a non-empty list of Question objects
            raise ValueError("Idk man your quiz must contain at least one question!")
        #attributes of da quiz class
        self.topic = topic.strip()
        self.questions = questions
        self.score = 0
        self.responses = []
        self.username = username

    def ask_questions(self):              #3 prints statements for nice layout        
        print(f"\n{'~' * 60}")            
        print(f"THIS QUIZ IS ON: {self.topic}!!!")
        print(f"{'~' * 60}\n")
        #ts function is crash free
        for i, q in enumerate(self.questions, start=1):      #looping through the questions and asking them one by one, also handling user input (VALIDATION USED) and marking answers
            print(f"Q{i}: {q.text}")
            try:
                user_answer = input("Your answer: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nInput interrupted. Blank answer recorded.")            #means the user has entered ctrl+c or ctrl+d, so just record a blank answer and move on to the next question instead of crashing the program
                user_answer = ""

            correct = self.mark_answer(user_answer, q.answer, getattr(q, "notes_context", ""))       #calls function mark answer to check is answer is correct also passing in the notes context if it exists for better marking accuracy
            self.responses.append((q, user_answer, correct))

            if correct:
                print("Nice one, correct!")
                self.score += 1
            else:
                print("Not quite this time.")

            print(f"Correct answer: {q.answer}")
            print("-" * 40)

        print(
            f"Ayy good job on finishing the quiz, {self.username}! "
            f"Your score is: {self.score}/{len(self.questions)}\n"
        )

    #this helper is for the marking system
    #it strips out filler words and keeps the physics words that would actually get marks
    @classmethod
    def _extract_keywords(cls, text: str) -> set[str]:
        stop_words = {
            "the", "and", "are", "for", "with", "that", "this", "into", "from", "when",
            "what", "your", "have", "has", "had", "been", "their", "them", "then", "than",
            "each", "these", "those", "using", "used", "use", "give", "three", "does", "doesnt",
            "cant", "cannot", "about", "because", "whereas", "which", "would", "could", "should",
            "very", "more", "most", "much", "many", "some", "such", "through", "they",
            "onto", "over", "under", "between", "within", "also", "just", "too", "high", "low",
            "higher", "lower", "minimum", "maximum", "level", "levels", "time", "point",
            "points", "produce", "produces", "result", "results", "given", "describe",
            "describes", "called", "known", "individual", "other", "any", "can", "only",
            "one", "two", "how", "why", "it", "its", "than", "required", "need", "needed",
            "above", "below", "across", "while", "where", "there", "here", "theyre", "youre"
        }

        phrase_aliases = {
            "phase relationship": "phase_difference",
            "constant phase difference": "phase_difference",
            "constant phase relationship": "phase_difference",
            "in phase": "phase_difference",
            "work function": "work_function",
            "threshold frequency": "threshold_frequency",
            "line spectrum": "line_spectrum",
            "photoelectric effect": "photoelectric_effect",
            "resultant force": "resultant_force",
            "strong nuclear": "strong_nuclear",
            "weak nuclear": "weak_nuclear",
        }

        word_aliases = {
            "wavelengths": "wavelength",
            "frequencies": "frequency",
            "oscillations": "oscillation",
            "electrons": "electron",
            "photons": "photon",
            "particles": "particle",
            "energies": "energy",
            "metals": "metal",
            "nodes": "node",
            "antinodes": "antinode",
            "travelling": "travel",
            "travels": "travel",
            "emitted": "emit",
            "emission": "emit",
            "repeating": "repeat",
            "repeats": "repeat",
            "readings": "repeat",
            "calculated": "calculate",
            "calculating": "calculate",
            "find": "calculate",
            "proper": "appropriate",
            "suitable": "appropriate",
            "multiplied": "multiply",
            "times": "multiply",
            "velocity": "speed",
            "relationship": "difference",
        }

        #first we normalise the text so different ways of saying the same thing are treated the same
        cleaned = text.lower().replace("λ", " wavelength ").replace("μ", " micro ").replace("e.m.", " electromagnetic ")
        for phrase, replacement in phrase_aliases.items():
            cleaned = cleaned.replace(phrase, replacement)

        keywords = set()
        for raw_word in re.findall(r"[A-Za-z0-9_+-]+", cleaned):
            word = word_aliases.get(raw_word, raw_word)
            if word.endswith("ies") and len(word) > 4:
                word = word[:-3] + "y"
            elif word.endswith("s") and len(word) > 4 and not word.endswith("ss"):
                word = word[:-1]

            if len(word) <= 2 and not any(ch.isdigit() for ch in word):
                continue
            if word not in stop_words:
                keywords.add(word)
        return keywords

    #this is the actual marking method
    #idea is simple: if the student's answer contains most of the important physics words, give the mark
    @classmethod
    def mark_answer(cls, user_answer: str, correct_answer: str, notes_context: str = "") -> bool:
        if not user_answer.strip():
            return False

        user_keywords = cls._extract_keywords(user_answer)
        answer_keywords = cls._extract_keywords(correct_answer)
        notes_keywords = cls._extract_keywords(notes_context)

        if not answer_keywords and not notes_keywords:
            return user_answer.strip().lower() == correct_answer.strip().lower()

        physics_terms = {
            "precision", "accuracy", "uncertainty", "repeat", "mean", "datalogger", "equipment",
            "frequency", "wavelength", "phase_difference", "interference", "diffraction",
            "transverse", "longitudinal", "oscillation", "photoelectric_effect", "work_function",
            "threshold_frequency", "electron", "photon", "gamma", "energy", "radiation",
            "momentum", "mass", "speed", "acceleration", "force", "resultant_force",
            "line_spectrum", "proton", "neutron", "antineutrino", "excitation"
        }

        #this picks out the best marking words:
        #1) words that appear in both the official answer and the notes are probs important
        #2) then we also force in common physics terms we defo care about
        key_mark_words = answer_keywords & notes_keywords
        key_mark_words.update(word for word in (answer_keywords | notes_keywords) if word in physics_terms)

        if not key_mark_words:
            key_mark_words = answer_keywords | notes_keywords

        #majority rule happens here
        #if they got more than half of the key words, the answer counts as correct
        match_count = len(user_keywords & key_mark_words)
        required_matches = max(1, (len(key_mark_words) // 2) + 1)
        return match_count >= required_matches


#this class inherits from Quiz but adds a timer on top
class TimedQuiz(Quiz):
    #same idea as Quiz, but now we also store a time limit and a flag for when time runs out
    def __init__(self, topic: str, questions: List[Question], time_limit: int = 60, username: str = "Player"):
        super().__init__(topic, questions, username=username)
        self.time_limit = max(10, int(time_limit))
        self.time_up = False

    #this runs in the background while the quiz is happening
    def timer(self):
        time.sleep(self.time_limit)
        self.time_up = True
        print("\nTime's up!\n")

    #this version of ask_questions stops early if the timer finishes
    def ask_questions(self):
        print(f"\n{'=' * 60}")
        print(f"TIMED QUIZ: {self.topic} (Time limit: {self.time_limit}s)")
        print(f"{'=' * 60}\n")

        #daemon=True means the timer thread wont stop the whole program from closing
        timer_thread = threading.Thread(target=self.timer, daemon=True)
        timer_thread.start()

        for i, q in enumerate(self.questions, start=1):
            if self.time_up:
                break

            print(f"Q{i}: {q.text}")
            try:
                user_answer = input("Your answer: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nInput interrupted. Blank answer recorded.")
                user_answer = ""

            correct = self.mark_answer(user_answer, q.answer, getattr(q, "notes_context", ""))
            self.responses.append((q, user_answer, correct))

            if correct:
                print("Nice one, correct!")
                self.score += 1
            else:
                print("Not quite this time.")

            print(f"Correct answer: {q.answer}")
            print("-" * 40)

        print(
            f"Ayy good job on finishing the quiz, {self.username}! "
            f"Your score is: {self.score}/{len(self.questions)}\n"
        )
        self.time_up = False


#this class represents one logged in user and their saved quiz history
class User:
    #stores the core info for one user
    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username
        self.quiz_history_head = None

    #signup method - hashes the password and saves the new user in the database
    @staticmethod
    def create_user(username: str, password: str, db_path: str = DATABASE_PATH):
        if not username.strip() or not password.strip():
            return None

        try:
            with sqlite3.connect(db_path) as con:
                cur = con.cursor()
                cur.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS userdata (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL
                    )
                    '''
                )
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                cur.execute(
                    "INSERT INTO userdata (username, password) VALUES (?, ?)",
                    (username.strip(), hashed_password),
                )
                con.commit()
                return User(user_id=cur.lastrowid, username=username.strip())
        except sqlite3.IntegrityError:
            return None
        except sqlite3.Error as exc:
            print(f"Database error during signup: {exc}")
            return None

    #login method - hashes the entered password and checks if it matches the db
    @staticmethod
    def authenticate(username: str, password: str, db_path: str = DATABASE_PATH):
        if not username.strip() or not password.strip():
            return None

        try:
            with sqlite3.connect(db_path) as con:
                cur = con.cursor()
                cur.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS userdata (
                        id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL UNIQUE,
                        password TEXT NOT NULL
                    )
                    '''
                )
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                cur.execute(
                    "SELECT id, username FROM userdata WHERE username = ? AND password = ?",
                    (username.strip(), hashed_password),
                )
                row = cur.fetchone()
        except sqlite3.Error as exc:
            print(f"Database error during login: {exc}")
            return None

        if row:
            return User(user_id=row[0], username=row[1])
        return None

    #saves the finished quiz in 2 places: the linked list in memory and the sqlite progress table
    def add_quiz_result(self, quiz: Quiz):
        node = QuizHistoryNode((quiz.topic, quiz.score, time.time()), self.quiz_history_head)
        self.quiz_history_head = node

        try:
            with sqlite3.connect(DATABASE_PATH) as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO progress (user_id, topic, score) VALUES (?, ?, ?)",
                    (self.user_id, quiz.topic, quiz.score),
                )
                con.commit()
        except sqlite3.Error as exc:
            print(f"Could not save quiz summary: {exc}")

    #walks through the linked list from the newest result to the oldest one
    def print_quiz_history(self):
        print("\nYour Quiz History (most recent first):")
        node = self.quiz_history_head
        i = 1

        if node is None:
            print("No quiz history yet.")
            return

        while node:
            topic, score, ts = node.quiz
            print(f"{i}. {topic} | Score: {score} | Time: {time.ctime(ts)}")
            node = node.next
            i += 1


#this is just a recursive graph traversal to print linked topics nicely
#depth controls the indentation so you can see the branches more clearly
def recursive_topic_recommend(graph, current_topic, visited=None, depth=0):
    if visited is None:
        visited = set()

    visited.add(current_topic)
    print("  " * depth + f"- {current_topic}")

    for neighbor in graph.get(current_topic, []):
        if neighbor not in visited:
            recursive_topic_recommend(graph, neighbor, visited, depth + 1)


#this class looks at old quiz results and works out what topics need more revision
class RevisionPlanner:
    #planner is tied to one user because it uses their saved results
    def __init__(self, user: User):
        self.user = user

    #turns raw quiz scores into a mastery percentage for each topic
    def calculate_topic_mastery(self) -> Dict[str, Dict[str, float]]:
        mastery: Dict[str, Dict[str, float]] = {}

        try:
            with sqlite3.connect(DATABASE_PATH) as con:
                cur = con.cursor()
                cur.execute(
                    """
                    SELECT topic, COUNT(*), AVG(score), MAX(score)
                    FROM progress
                    WHERE user_id = ?
                    GROUP BY topic
                    """,
                    (self.user.user_id,),
                )
                rows = cur.fetchall()
        except sqlite3.Error as exc:
            print(f"Could not calculate mastery data: {exc}")
            return mastery

        for topic, attempts, avg_score, best_score in rows:
            #consistency factor rewards doing a topic multiple times instead of only once
            consistency_factor = min(attempts / 5, 1)
            mastery_score = round(
                ((avg_score / 5) * 0.6 + (best_score / 5) * 0.3 + consistency_factor * 0.1) * 100,
                2,
            )
            mastery[topic] = {
                "attempts": attempts,
                "average_score": round(avg_score, 2),
                "best_score": best_score,
                "mastery_score": mastery_score,
            }

        return mastery

    #sorts topics from weakest to strongest so revision can be targeted better
    def weakest_topics_first(self):
        mastery = self.calculate_topic_mastery()
        return sorted(mastery.items(), key=lambda item: item[1]["mastery_score"])


#this class manages what is going on while one user is actively using the quiz system
class Session:
    #sets up the live session data structures for the current user
    def __init__(self, user: User):
        if not isinstance(user, User):
            raise ValueError("Session requires a valid User object.")

        self.user = user
        self.active_quiz = None
        self.completed_quiz_stack: List[tuple[str, int, float]] = []
        self.recommendation_queue: Deque[str] = deque()

    #pushes a completed quiz onto the stack so the most recent one is on top
    def push_completed_quiz(self, quiz: Quiz):
        self.completed_quiz_stack.append((quiz.topic, quiz.score, time.time()))

    #classic stack behaviour - remove the last completed quiz if needed
    def undo_last_quiz(self) -> Optional[tuple[str, int, float]]:
        if not self.completed_quiz_stack:
            return None
        return self.completed_quiz_stack.pop()

    #builds a queue of recommended next topics using the topic graph
    def build_recommendation_queue(self, graph: Dict[str, List[str]], start_topic: str):
        self.recommendation_queue.clear()

        visited = {start_topic}
        pending = deque(graph.get(start_topic, []))

        #this is basically breadth first search using a queue
        while pending:
            topic = pending.popleft()
            if topic in visited:
                continue

            visited.add(topic)
            self.recommendation_queue.append(topic)

            for neighbour in graph.get(topic, []):
                if neighbour not in visited:
                    pending.append(neighbour)

    #gets the next topic from the front of the queue
    def get_next_recommendation(self) -> Optional[str]:
        if self.recommendation_queue:
            return self.recommendation_queue.popleft()gt
    def start_quiz(self, quiz: Quiz):
        import datetime

        if not isinstance(quiz, Quiz):
            raise ValueError("start_quiz expects a Quiz instance.")

        self.active_quiz = quiz
        quiz.username = self.user.username
        quiz_id = None

        try:
            with sqlite3.connect(DATABASE_PATH) as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO quizzes (user_id, topic, start_time) VALUES (?, ?, ?)",
                    (self.user.user_id, quiz.topic, datetime.datetime.now()),
                )
                quiz_id = cur.lastrowid
                con.commit()

            #this line actually runs the whole quiz interaction with the user
            quiz.ask_questions()

            #after the quiz finishes, each response gets saved to the results table
            if quiz_id is not None:
                with sqlite3.connect(DATABASE_PATH) as con:
                    cur = con.cursor()
                    for q, user_answer, correct in quiz.responses:
                        cur.execute(
                            "INSERT INTO results (quiz_id, question_id, user_answer, correct) VALUES (?, ?, ?, ?)",
                            (quiz_id, q.qid, user_answer, int(correct)),
                        )
                    cur.execute(
                        "UPDATE quizzes SET end_time = ? WHERE id = ?",
                        (datetime.datetime.now(), quiz_id),
                    )
                    con.commit()

            self.user.add_quiz_result(quiz)
            self.push_completed_quiz(quiz)
        except sqlite3.Error as exc:
            print(f"Database error while storing quiz results: {exc}")
        finally:
            self.active_quiz = None

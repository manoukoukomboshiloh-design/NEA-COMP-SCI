import time
from typing import List

import sqlite3

class Question:
    def __init__(self, qid: int, text: str, answer: str):
        self.qid = qid
        self.text = text
        self.answer = answer


# Linked list node for quiz history
class QuizHistoryNode:
    def __init__(self, quiz, next_node=None):
        self.quiz = quiz
        self.next = next_node

class Quiz:
    def __init__(self, topic: str, questions: List[Question]):
        self.topic = topic
        self.questions = questions
        self.score = 0
        self.responses = []

    def ask_questions(self):
        print(f"\n{'='*60}")
        print(f"QUIZ: {self.topic}")
        print(f"{'='*60}\n")
        for i, q in enumerate(self.questions, start=1):
            print(f"Q{i}: {q.text}")
            user_answer = input("Your answer: ")
            correct = self.mark_answer(user_answer, q.answer)
            self.responses.append((q, user_answer, correct))
            if correct:
                print(" Correct!")
                self.score += 1
            else:
                print("❌ Incorrect.")
            print(f"Correct answer: {q.answer}")
            print("-"*40)
        print(f"Quiz complete! Your score: {self.score}/{len(self.questions)}\n")

# OOP inheritance: TimedQuiz subclass
import threading
class TimedQuiz(Quiz):
    def __init__(self, topic: str, questions: List[Question], time_limit=60):
        super().__init__(topic, questions)
        self.time_limit = time_limit
        self.time_up = False

    def timer(self):
        time.sleep(self.time_limit)
        self.time_up = True
        print("\nTime's up!\n")

    def ask_questions(self):
        print(f"\n{'='*60}")
        print(f"TIMED QUIZ: {self.topic} (Time limit: {self.time_limit}s)")
        print(f"{'='*60}\n")
        timer_thread = threading.Thread(target=self.timer)
        timer_thread.start()
        for i, q in enumerate(self.questions, start=1):
            if self.time_up:
                break
            print(f"Q{i}: {q.text}")
            user_answer = input("Your answer: ")
            correct = self.mark_answer(user_answer, q.answer)
            self.responses.append((q, user_answer, correct))
            if correct:
                print(" Correct!")
                self.score += 1
            else:
                print("❌ Incorrect.")
            print(f"Correct answer: {q.answer}")
            print("-"*40)
        print(f"Quiz complete! Your score: {self.score}/{len(self.questions)}\n")
        self.time_up = False

    @staticmethod
    def mark_answer(user_answer: str, correct_answer: str) -> bool:
        import re
        answer_keywords = set(re.findall(r"\b\w{3,}\b", correct_answer.lower()))
        user_words = set(re.findall(r"\b\w{3,}\b", user_answer.lower()))
        if answer_keywords:
            match_count = len(answer_keywords & user_words)
            required = max(1, len(answer_keywords) // 2)
            return match_count >= required
        return False


class User:
    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username
        self.quiz_history_head = None  # Linked list head

    @staticmethod
    def authenticate(username: str, password: str):
        import hashlib
        con = sqlite3.connect('user_data.db')
        cur = con.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cur.execute("SELECT id, username FROM userdata WHERE username = ? AND password = ?", (username, hashed_password))
        row = cur.fetchone()
        con.close()
        if row:
            return User(user_id=row[0], username=row[1])
        return None

    def add_quiz_result(self, quiz: Quiz):
        # Add to linked list
        node = QuizHistoryNode((quiz.topic, quiz.score, time.time()), self.quiz_history_head)
        self.quiz_history_head = node
        # Store quiz summary in progress table
        con = sqlite3.connect('user_data.db')
        cur = con.cursor()
        cur.execute("INSERT INTO progress (user_id, topic, score) VALUES (?, ?, ?)", (self.user_id, quiz.topic, quiz.score))
        con.commit()
        con.close()

    def print_quiz_history(self):
        print("\nYour Quiz History (most recent first):")
        node = self.quiz_history_head
        i = 1
        while node:
            topic, score, ts = node.quiz
            print(f"{i}. {topic} | Score: {score} | Time: {time.ctime(ts)}")
            node = node.next
            i += 1
# --- Recursive graph traversal for topic recommendations ---
def recursive_topic_recommend(graph, current_topic, visited=None, depth=0):
    if visited is None:
        visited = set()
    visited.add(current_topic)
    print("  " * depth + f"- {current_topic}")
    for neighbor in graph.get(current_topic, []):
        if neighbor not in visited:
            recursive_topic_recommend(graph, neighbor, visited, depth+1)

class Session:
    def __init__(self, user: User):
        self.user = user
        self.active_quiz = None

    def start_quiz(self, quiz: Quiz):
        import datetime
        self.active_quiz = quiz
        # Store quiz start
        con = sqlite3.connect('user_data.db')
        cur = con.cursor()
        cur.execute("INSERT INTO quizzes (user_id, topic, start_time) VALUES (?, ?, ?)", (self.user.user_id, quiz.topic, datetime.datetime.now()))
        quiz_id = cur.lastrowid
        con.commit()
        con.close()
        quiz.ask_questions()
        # Store each question result
        con = sqlite3.connect('user_data.db')
        cur = con.cursor()
        for q, user_answer, correct in quiz.responses:
            cur.execute("INSERT INTO results (quiz_id, question_id, user_answer, correct) VALUES (?, ?, ?, ?)", (quiz_id, q.qid, user_answer, int(correct)))
        # Store quiz end time
        cur.execute("UPDATE quizzes SET end_time = ? WHERE id = ?", (datetime.datetime.now(), quiz_id))
        con.commit()
        con.close()
        self.user.add_quiz_result(quiz)
        self.active_quiz = None

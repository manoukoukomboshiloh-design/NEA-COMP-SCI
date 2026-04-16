import time
import sqlite3
import threading
from collections import deque
from typing import Deque, Dict, List, Optional


class Question:
    def __init__(self, qid: int, text: str, answer: str):
        if not isinstance(qid, int):
            raise ValueError("Question id must be an integer.")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Question text cannot be empty.")
        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("Question answer cannot be empty.")

        self.qid = qid
        self.text = text.strip()
        self.answer = answer.strip()


class QuizHistoryNode:
    def __init__(self, quiz, next_node=None):
        self.quiz = quiz
        self.next = next_node


class Quiz:
    def __init__(self, topic: str, questions: List[Question], username: str = "Player"):
        if not isinstance(topic, str) or not topic.strip():
            raise ValueError("Topic must be a non-empty string.")
        if not isinstance(questions, list) or not questions:
            raise ValueError("Quiz must contain at least one question.")

        self.topic = topic.strip()
        self.questions = questions
        self.score = 0
        self.responses = []
        self.username = username

    def ask_questions(self):
        print(f"\n{'=' * 60}")
        print(f"QUIZ: {self.topic}")
        print(f"{'=' * 60}\n")

        for i, q in enumerate(self.questions, start=1):
            print(f"Q{i}: {q.text}")
            try:
                user_answer = input("Your answer: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nInput interrupted. Blank answer recorded.")
                user_answer = ""

            correct = self.mark_answer(user_answer, q.answer)
            self.responses.append((q, user_answer, correct))

            if correct:
                print("Nice one, correct!")
                self.score += 1
            else:
                print("Not quite this time.")

            print(f"Correct answer: {q.answer}")
            print("-" * 40)

        print(
            f"Well done on finishing the quiz, {self.username}! "
            f"Your score is: {self.score}/{len(self.questions)}\n"
        )

    @staticmethod
    def mark_answer(user_answer: str, correct_answer: str) -> bool:
        import re

        if not user_answer.strip():
            return False

        answer_keywords = set(re.findall(r"\b\w{3,}\b", correct_answer.lower()))
        user_words = set(re.findall(r"\b\w{3,}\b", user_answer.lower()))

        if answer_keywords:
            match_count = len(answer_keywords & user_words)
            required = max(1, len(answer_keywords) // 2)
            return match_count >= required
        return False


class TimedQuiz(Quiz):
    def __init__(self, topic: str, questions: List[Question], time_limit: int = 60, username: str = "Player"):
        super().__init__(topic, questions, username=username)
        self.time_limit = max(10, int(time_limit))
        self.time_up = False

    def timer(self):
        time.sleep(self.time_limit)
        self.time_up = True
        print("\nTime's up!\n")

    def ask_questions(self):
        print(f"\n{'=' * 60}")
        print(f"TIMED QUIZ: {self.topic} (Time limit: {self.time_limit}s)")
        print(f"{'=' * 60}\n")

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

            correct = self.mark_answer(user_answer, q.answer)
            self.responses.append((q, user_answer, correct))

            if correct:
                print("Nice one, correct!")
                self.score += 1
            else:
                print("Not quite this time.")

            print(f"Correct answer: {q.answer}")
            print("-" * 40)

        print(
            f"Well done on finishing the quiz, {self.username}! "
            f"Your score is: {self.score}/{len(self.questions)}\n"
        )
        self.time_up = False


class User:
    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username
        self.quiz_history_head = None

    @staticmethod
    def authenticate(username: str, password: str):
        import hashlib

        if not username.strip() or not password.strip():
            return None

        try:
            with sqlite3.connect('user_data.db') as con:
                cur = con.cursor()
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

    def add_quiz_result(self, quiz: Quiz):
        node = QuizHistoryNode((quiz.topic, quiz.score, time.time()), self.quiz_history_head)
        self.quiz_history_head = node

        try:
            with sqlite3.connect('user_data.db') as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO progress (user_id, topic, score) VALUES (?, ?, ?)",
                    (self.user_id, quiz.topic, quiz.score),
                )
                con.commit()
        except sqlite3.Error as exc:
            print(f"Could not save quiz summary: {exc}")

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


def recursive_topic_recommend(graph, current_topic, visited=None, depth=0):
    if visited is None:
        visited = set()

    visited.add(current_topic)
    print("  " * depth + f"- {current_topic}")

    for neighbor in graph.get(current_topic, []):
        if neighbor not in visited:
            recursive_topic_recommend(graph, neighbor, visited, depth + 1)


class RevisionPlanner:
    def __init__(self, user: User):
        self.user = user

    def calculate_topic_mastery(self) -> Dict[str, Dict[str, float]]:
        mastery: Dict[str, Dict[str, float]] = {}

        try:
            with sqlite3.connect('user_data.db') as con:
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

    def weakest_topics_first(self):
        mastery = self.calculate_topic_mastery()
        return sorted(mastery.items(), key=lambda item: item[1]["mastery_score"])


class Session:
    def __init__(self, user: User):
        if not isinstance(user, User):
            raise ValueError("Session requires a valid User object.")

        self.user = user
        self.active_quiz = None
        self.completed_quiz_stack: List[tuple[str, int, float]] = []
        self.recommendation_queue: Deque[str] = deque()

    def push_completed_quiz(self, quiz: Quiz):
        self.completed_quiz_stack.append((quiz.topic, quiz.score, time.time()))

    def undo_last_quiz(self) -> Optional[tuple[str, int, float]]:
        if not self.completed_quiz_stack:
            return None
        return self.completed_quiz_stack.pop()

    def build_recommendation_queue(self, graph: Dict[str, List[str]], start_topic: str):
        self.recommendation_queue.clear()

        visited = {start_topic}
        pending = deque(graph.get(start_topic, []))

        while pending:
            topic = pending.popleft()
            if topic in visited:
                continue

            visited.add(topic)
            self.recommendation_queue.append(topic)

            for neighbour in graph.get(topic, []):
                if neighbour not in visited:
                    pending.append(neighbour)

    def get_next_recommendation(self) -> Optional[str]:
        if self.recommendation_queue:
            return self.recommendation_queue.popleft()
        return None

    def start_quiz(self, quiz: Quiz):
        import datetime

        if not isinstance(quiz, Quiz):
            raise ValueError("start_quiz expects a Quiz instance.")

        self.active_quiz = quiz
        quiz.username = self.user.username
        quiz_id = None

        try:
            with sqlite3.connect('user_data.db') as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO quizzes (user_id, topic, start_time) VALUES (?, ?, ?)",
                    (self.user.user_id, quiz.topic, datetime.datetime.now()),
                )
                quiz_id = cur.lastrowid
                con.commit()

            quiz.ask_questions()

            if quiz_id is not None:
                with sqlite3.connect('user_data.db') as con:
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

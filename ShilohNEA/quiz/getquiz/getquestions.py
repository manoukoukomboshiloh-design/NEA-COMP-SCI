import math
import os
import random
import re
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from save_data import save_score, show_dashboard
from quiz.mark_queries import submit_mark_query
from quiz.oop_quiz import Quiz as MarkingQuiz


class Node:
    def __init__(self, question):
        self.question = question
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, question):
        new_node = Node(question)

        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def display(self):
        current = self.head
        if not current:
            print("No wrong questions to review!")
            return

        while current:
            print(current.question["question"])
            current = current.next

    def to_list(self):
        current = self.head
        result = []

        while current:
            result.append(current.question)
            current = current.next

        return result


def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if len(left[i]["question"]) < len(right[j]["question"]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


class User:
    def __init__(self, user_id, username):
        self.user_id = user_id
        self.username = username

    def display_info(self):
        print(f"User: {self.username} (ID: {self.user_id})")


class Quiz:
    def __init__(self, user, data):
        self.user = user
        self.data = data
        self.score = 0
        self.exited_early = False

    @staticmethod
    def _extract_keywords(text):
        stop_words = {
            "the", "and", "are", "for", "with", "that", "this", "into", "from", "when",
            "what", "your", "have", "has", "had", "been", "their", "them", "then", "than",
            "each", "these", "those", "using", "used", "use", "give", "three", "does", "doesnt",
            "cant", "cannot", "about", "because", "whereas", "which", "would", "could", "should",
            "same", "very", "more", "most", "much", "many", "some", "such", "through", "they",
            "them", "onto", "over", "under", "between", "within", "also", "just", "than", "too",
            "high", "low", "higher", "lower", "minimum", "maximum", "level", "levels"
        }

        keywords = set()
        for word in re.findall(r"[A-Za-z0-9^+-]+", text.lower()):
            if len(word) <= 2 and not any(ch.isdigit() for ch in word):
                continue
            if word.endswith("ies") and len(word) > 4:
                word = word[:-3] + "y"
            elif word.endswith("s") and len(word) > 4:
                word = word[:-1]
            if word not in stop_words:
                keywords.add(word)
        return keywords

    def _is_correct(self, user_answer, expected_answer, notes_text):
        return MarkingQuiz.mark_answer(user_answer, expected_answer, notes_text)

    def run(self, selected_topic):
        topic_info = self.data["topics"][selected_topic]
        questions = list(topic_info["questions"])
        notes_text = " ".join(topic_info.get("notes", []))
        random.shuffle(questions)
        quiz_questions = questions[:5]

        wrong_questions = LinkedList()
        self.score = 0
        self.exited_early = False

        print("\n" * 25, end="")
        print(f"\n{'~' * 60}")
        print(f"SHILOH'S QUIZ FOR: {selected_topic}")
        print(f"{'~' * 60}\n")

        for q in quiz_questions:
            print(q["question"])

            options = q.get("options", [])
            for option in options:
                print(option)

            user_answer = input("Your answer (type ? to request a review or q to quit): ").strip()

            if user_answer.lower() in {"q", "quit", "exit"}:
                self.exited_early = True
                print("Leaving the quiz and returning to the main menu...\n")
                return self.score, wrong_questions

            if options and len(user_answer) == 1 and user_answer.upper() in "ABCD":
                option_index = ord(user_answer.upper()) - ord("A")
                if 0 <= option_index < len(options):
                    selected_option = options[option_index]
                    if ". " in selected_option:
                        user_answer = selected_option.split(". ", 1)[1]
                    elif ") " in selected_option:
                        user_answer = selected_option.split(") ", 1)[1]

            if user_answer == "?":
                proposed_answer = input("What answer do you want reviewed?: ").strip()
                reason = input("Why do you think it should get the mark?: ").strip()
                query_id = submit_mark_query(
                    user_id=self.user.user_id,
                    username=self.user.username,
                    topic=selected_topic,
                    question_text=q["question"],
                    expected_answer=q["answer"],
                    user_answer=proposed_answer or "[No answer provided]",
                    reason=reason,
                )
                print(f"Your mark review request has been saved for admin review. Query id: {query_id}\n")
                wrong_questions.add(q)
                continue

            if self._is_correct(user_answer, q["answer"], notes_text):
                print("heck yeah keep it up!\n")
                self.score += 1
            else:
                print(f"Chin up nephew, this was the right answer: {q['answer']}\n")
                wrong_questions.add(q)
                follow_up = input("Press Enter to continue, type ? for a review, or q to quit: ").strip()
                if follow_up.lower() in {"q", "quit", "exit"}:
                    self.exited_early = True
                    print("Leaving the quiz and returning to the main menu...\n")
                    return self.score, wrong_questions
                if follow_up == "?":
                    reason = input("Why do you think your answer should count?: ").strip()
                    query_id = submit_mark_query(
                        user_id=self.user.user_id,
                        username=self.user.username,
                        topic=selected_topic,
                        question_text=q["question"],
                        expected_answer=q["answer"],
                        user_answer=user_answer,
                        reason=reason,
                    )
                    print(f"Review request saved for admin review. Query id: {query_id}\n")

        total_questions = len(quiz_questions)
        pass_mark = max(1, math.ceil(total_questions * 0.8))
        print(f"You scored {self.score} out of {total_questions}")

        if self.score >= pass_mark:
            print("Ayyy Congrats, you passed the quiz!")
        else:
            print("Better luck next time g")

            review = input("Do you want to review your wrong questions? (yes/no): ")

            if review.lower() == "yes":
                print("\nYour weak questions:")

                weak_list = wrong_questions.to_list()
                sorted_questions = merge_sort(weak_list)

                for q in sorted_questions:
                    print(q["question"])

        save_score(self.user.user_id, selected_topic, self.score)
        show_dashboard(self.user.user_id)

        return self.score, wrong_questions

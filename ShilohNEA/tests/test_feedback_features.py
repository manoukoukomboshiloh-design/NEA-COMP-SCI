import io
import json
import os
import random
import sqlite3
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from quiz.mark_queries import get_pending_mark_queries, submit_mark_query
from quiz.display.question_bank import question_data, save_user_question
from quiz.getquiz.getquestions import Quiz, User


class FeedbackFeatureTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = os.path.join(self.temp_dir.name, 'user_data.db')
        self.json_path = os.path.join(self.temp_dir.name, 'user_questions.json')

        with sqlite3.connect(self.db_path) as con:
            con.execute(
                '''
                CREATE TABLE userdata (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
                '''
            )
            con.execute(
                "INSERT INTO userdata (username, password) VALUES (?, ?)",
                ('alice', 'hashed')
            )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_submit_mark_query_stores_pending_request(self):
        query_id = submit_mark_query(
            user_id=1,
            username='alice',
            topic='Waves',
            question_text='What is meant by coherent sources?',
            expected_answer='Same frequency and constant phase difference.',
            user_answer='same frequency and in phase',
            reason='This should still get the mark',
            db_path=self.db_path,
        )

        self.assertIsInstance(query_id, int)
        pending = get_pending_mark_queries(db_path=self.db_path)
        self.assertEqual(len(pending), 1)
        self.assertEqual(pending[0]['status'], 'pending')
        self.assertEqual(pending[0]['username'], 'alice')

    def test_save_user_question_writes_to_json_file(self):
        save_user_question(
            topic='Mechanics',
            question='What is impulse?',
            answer='Impulse is the change in momentum.',
            json_path=self.json_path,
        )

        with open(self.json_path, 'r', encoding='utf-8') as handle:
            data = json.load(handle)

        self.assertIn('Mechanics', data['topics'])
        self.assertEqual(data['topics']['Mechanics'][0]['question'], 'What is impulse?')

    def test_quiz_allows_exit_back_to_menu(self):
        random.seed(1)
        user = User(1, 'alice')
        quiz = Quiz(user, question_data)
        inputs = iter(['q'])

        output = io.StringIO()
        with patch('builtins.input', side_effect=lambda prompt='': next(inputs)):
            with redirect_stdout(output):
                score, wrong_questions = quiz.run('Waves')

        self.assertEqual(score, 0)
        self.assertIn('main menu', output.getvalue().lower())
        self.assertEqual(wrong_questions.to_list(), [])

    def test_quiz_accepts_multiple_choice_answer(self):
        user = User(1, 'alice')
        data = {
            'topics': {
                'Mini Topic': {
                    'notes': ['Force equals mass multiplied by acceleration.'],
                    'questions': [
                        {
                            'id': 1,
                            'question': 'What is Newton\'s second law?',
                            'answer': 'F = ma',
                            'options': ['A. F = ma', 'B. E = mc^2', 'C. V = IR', 'D. p = mv'],
                        }
                    ],
                }
            }
        }
        quiz = Quiz(user, data)
        inputs = iter(['A'])

        with patch('builtins.input', side_effect=lambda prompt='': next(inputs)):
            score, _ = quiz.run('Mini Topic')

        self.assertEqual(score, 1)


if __name__ == '__main__':
    unittest.main()

import os
import sys
import unittest

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from quiz.oop_quiz import Quiz


class QuizMarkingTests(unittest.TestCase):
    def test_accepts_majority_of_key_wave_terms(self):
        correct_answer = "Waves that maintain a constant phase relationship with each other over time."
        notes_context = "Coherent sources produce waves with a constant phase difference and the same frequency."
        user_answer = "Same frequency and in phase."

        self.assertTrue(Quiz.mark_answer(user_answer, correct_answer, notes_context))

    def test_accepts_measurements_keywords(self):
        correct_answer = "Take a minimum of 3 repeats and calculate a mean. Use computers, dataloggers or cameras. Use appropriate equipment."
        notes_context = "Random errors can be reduced by repeating measurements and calculating a mean, using digital equipment such as dataloggers or cameras, and using appropriate measuring instruments."
        user_answer = "Repeat the readings, find a mean, use dataloggers and proper equipment."

        self.assertTrue(Quiz.mark_answer(user_answer, correct_answer, notes_context))

    def test_accepts_particles_keywords(self):
        correct_answer = "When a particle and its antiparticle meet, they annihilate and produce two gamma photons moving in opposite directions to conserve momentum."
        notes_context = "Annihilation occurs when a particle and its antiparticle meet and convert their mass into energy, producing two gamma photons moving in opposite directions."
        user_answer = "A particle and antiparticle meet and make two gamma photons in opposite directions."

        self.assertTrue(Quiz.mark_answer(user_answer, correct_answer, notes_context))

    def test_accepts_em_radiation_keywords(self):
        correct_answer = "The emission of electrons from a metal surface when electromagnetic radiation of a high enough frequency is incident on it."
        notes_context = "The threshold frequency is the minimum frequency of electromagnetic radiation required to emit electrons from a metal surface."
        user_answer = "Electrons are emitted from a metal when radiation has enough frequency."

        self.assertTrue(Quiz.mark_answer(user_answer, correct_answer, notes_context))

    def test_accepts_mechanics_keywords(self):
        correct_answer = "The acceleration of an object is directly proportional to the resultant force acting on it and inversely proportional to its mass, F = ma."
        notes_context = "Newton's Second Law states that force equals mass multiplied by acceleration (F = ma)."
        user_answer = "Force equals mass times acceleration."

        self.assertTrue(Quiz.mark_answer(user_answer, correct_answer, notes_context))

    def test_accepts_single_keyword_answer_when_that_is_the_full_mark_point(self):
        correct_answer = "Estimation."
        notes_context = "Physicists must be able to estimate orders of magnitude and approximate values of physical quantities."
        user_answer = "Estimation"

        self.assertTrue(Quiz.mark_answer(user_answer, correct_answer, notes_context))

    def test_rejects_answer_missing_most_key_terms(self):
        correct_answer = "Waves that maintain a constant phase relationship with each other over time."
        notes_context = "Coherent sources produce waves with a constant phase difference and the same frequency."
        user_answer = "They are waves that travel together."

        self.assertFalse(Quiz.mark_answer(user_answer, correct_answer, notes_context))


if __name__ == '__main__':
    unittest.main()

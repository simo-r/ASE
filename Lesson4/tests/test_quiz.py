import unittest
from classes.quiz import Quiz, Answer, Question


class TestApp(unittest.TestCase):

    def test1(self):
        answer = Answer("test_answer", True)
        questions = Question("test_question", [answer])
        quiz = Quiz(1, [questions])
        result = quiz.isCompleted()
        self.assertEqual(result, False, "forte")


if __name__ == '__main__':
    unittest.main()

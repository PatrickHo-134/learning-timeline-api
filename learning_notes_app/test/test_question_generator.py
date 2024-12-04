import unittest
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from question_generator import QuestionGenerator

class TestQuestionGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = QuestionGenerator()

    def test_parse_questions(self):
        response = '<Question>: What is the primary characteristic of the WebSocket protocol compared to HTTP?\n<Options>:  \nA) WebSocket is unidirectional.  \nB) WebSocket is stateless.  \nC) WebSocket is bidirectional and stateful.  \nD) WebSocket only supports text data.  \n<Answer>: C) WebSocket is bidirectional and stateful.  \n\n---\n\n<Question>: In which scenario is WebSocket particularly beneficial?\n<Options>:  \nA) Fetching old data from the server.  \nB) Establishing multiple connections for each data request.  \nC) Real-time applications like trading or gaming.  \nD) Loading static web pages.  \n<Answer>: C) Real-time applications like trading or gaming.  \n\n---\n\n<Question>: When should WebSocket not be used?\n<Options>:  \nA) When continuous streams of data are needed.  \nB) When old data needs to be fetched only once.  \nC) When real-time updates are required.  \nD) When the application requires bidirectional communication.  \n<Answer>: B) When old data needs to be fetched only once.'
        parsed_questions = self.generator._parse_questions(response)
        expected = [{'question': 'What is the primary characteristic of the WebSocket protocol compared to HTTP?',
                     'options': ['A) WebSocket is unidirectional.  ',
                                 'B) WebSocket is stateless.  ',
                                 'C) WebSocket is bidirectional and stateful.  ',
                                 'D) WebSocket only supports text data.  '],
                     'answer': 'C) WebSocket is bidirectional and stateful.  '},
                    {'question': 'In which scenario is WebSocket particularly beneficial?',
                     'options': ['A) Fetching old data from the server.  ',
                                 'B) Establishing multiple connections for each data request.  ',
                                 'C) Real-time applications like trading or gaming.  ',
                                 'D) Loading static web pages.  '],
                     'answer': 'C) Real-time applications like trading or gaming.  '},
                    {'question': 'When should WebSocket not be used?',
                     'options': ['A) When continuous streams of data are needed.  ',
                                 'B) When old data needs to be fetched only once.  ',
                                 'C) When real-time updates are required.  ',
                                 'D) When the application requires bidirectional communication.  '],
                     'answer': 'B) When old data needs to be fetched only once.'}]
        self.assertEqual(parsed_questions, expected)

# Run the test
if __name__ == "__main__":
    unittest.main()

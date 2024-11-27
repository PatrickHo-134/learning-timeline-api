import sys
import os
import unittest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from question_generator import QuestionGenerator

class TestQuestionGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = QuestionGenerator()

    def test_parse_questions(self):
        response = """
        Question 1: What is the primary characteristic of WebSocket that differentiates it from HTTP?
        Options:
        - A) WebSocket is unidirectional.
        - B) WebSocket does not require a connection to be established.
        - C) WebSocket is a full-duplex protocol.
        - D) WebSocket uses a different transport layer protocol.
        Answer: C) WebSocket is a full-duplex protocol.

        ---

        Question 2: In which scenario is WebSocket particularly advantageous?
        Options:
        - A) Fetching old data.
        - B) Real-time web applications.
        - C) Sending large files.
        - D) Simple request-response interactions.
        Answer: B) Real-time web applications.

        ---

        Question 3: When should one avoid using WebSocket?
        Options:
        - A) When real-time data updates are needed.
        - B) When data needs to be pushed continuously.
        - C) When fetching old data that is not required frequently.
        - D) When maintaining a persistent connection is necessary.
        Answer: C) When fetching old data that is not required frequently.
        """
        parsed_questions = self.generator._parse_questions(response)
        expected = [
            {
                "question": "What is the primary characteristic of WebSocket that differentiates it from HTTP?",
                "options": {
                    "A": "WebSocket is unidirectional.",
                    "B": "WebSocket does not require a connection to be established.",
                    "C": "WebSocket is a full-duplex protocol.",
                    "D": "WebSocket uses a different transport layer protocol."
                },
                "answer": "C) WebSocket is a full-duplex protocol."
            },
            {
                "question": "In which scenario is WebSocket particularly advantageous?",
                "options": {
                    "A": "Fetching old data.",
                    "B": "Real-time web applications.",
                    "C": "Sending large files.",
                    "D": "Simple request-response interactions."
                },
                "answer": "B) Real-time web applications."
            },
            {
                "question": "When should one avoid using WebSocket?",
                "options": {
                    "A": "When real-time data updates are needed.",
                    "B": "When data needs to be pushed continuously.",
                    "C": "When fetching old data that is not required frequently.",
                    "D": "When maintaining a persistent connection is necessary."
                },
                "answer": "C) When fetching old data that is not required frequently."
            }
        ]
        self.assertEqual(parsed_questions, expected)

    def test_generate_questions(self):
        content = """<h2><strong>WebSocket</strong></h2><p>WebSocket is bidirectional, a full-duplex protocol that is used in the same scenario of client-server communication, unlike HTTP which starts from&nbsp;<strong>ws://</strong>&nbsp;or&nbsp;<strong>wss://</strong>. It is a stateful protocol, which means the connection between client and server will stay alive until it gets terminated by either party (client or server). After closing the connection by either of the client or server, the connection is terminated from both ends.&nbsp;</p><p><br></p><p>Let’s take an example of client-server communication, there is the client which is a web browser, and a server, whenever we initiate the connection between client and server, the client-server makes the handshaking and decides to create a new connection and this connection will keep alive until terminated by any of them. When the connection is established and alive the communication takes place using the same connection channel until it is terminated.&nbsp;</p><p><br></p><p>This is how after client-server handshaking, the client-server decides to keep a new connection alive, this new connection will be known as WebSocket. Once the communication link is established and the connections are opened, message exchange will take place in bidirectional mode until the connection persists between client-server. If anyone of them (client-server) dies or decide to close the connection then it is closed by both the party. The way in which the socket works is slightly different from how HTTP works, the status code 101 denotes the switching protocol in WebSocket.&nbsp;</p><p>&nbsp;</p><p><img src="https://media.geeksforgeeks.org/wp-content/uploads/20191203183648/WebSocket-Connection.png" height="inherit" width="inherit"></p><h2><strong>When can a web socket be used?</strong></h2><ul><li><strong>Real-time web application:</strong>&nbsp;Real-time web application uses a web socket to show the data at client end, which is continuously being sent by the backend server. In WebSocket, data is continuously pushed/transmitted into the same connection which is already open, that is why WebSocket is faster and improves the application performance.&nbsp;e.g. in a trading website or bitcoin trading, for displaying the price fluctuation and movement data is continuously pushed by the backend server to the client end by using a WebSocket channel.</li><li><strong>Gaming application:</strong>&nbsp;In a Gaming application, you might focus on that, data is continuously received by the server, and without refreshing the UI, it will take effect on the screen, UI gets automatically refreshed without even establishing the new connection, so it is very helpful in a Gaming application.</li><li><strong>Chat application:</strong>&nbsp;Chat applications use WebSockets to establish the connection only once for exchange, publishing, and broadcasting the message among the subscribers. It reuses the same WebSocket connection, for sending and receiving the message and for one-to-one message transfer.</li></ul><h2><strong>When not to use WebSocket?</strong></h2><p>WebSocket can be used if we want any real-time updated or continuous streams of data that are being transmitted over the network but if we want to fetch old data, or want to get the data only once to process it with an application we should go with&nbsp;<strong>HTTP protocol</strong>, old data which is not required very frequently or fetched only once can be queried by the simple HTTP request, so in this scenario, it’s better not use WebSocket.</p><p><br></p><p><a href="https://www.geeksforgeeks.org/what-is-web-socket-and-how-it-is-different-from-the-http/" rel="noopener noreferrer" target="_blank">Readmore</a></p>"""

        generator = QuestionGenerator()
        questions = generator.generate_questions(content, num_questions=3)

        self.assertEqual(len(questions), 3)

# Run the test
if __name__ == "__main__":
    unittest.main()
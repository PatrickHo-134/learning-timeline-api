from operator import truediv
from openai import OpenAI
from decouple import config
import re

# README: documentation of Openai's API https://platform.openai.com/docs/api-reference/chat/create


class QuestionGenerator:
     def __init__(self):
          self.api_key = config('OPENAI_API_KEY')
          self.engine = "gpt-4o-mini"
          self.max_tokens = 500
          self.temperature = 0.7  # Controls the creativity of the output

          self.client = OpenAI(
               organization=config('OPENAI_ORG_ID'),
               project=config('OPENAI_PROJECT_ID'),
               api_key=self.api_key
               )

     def _format_prompt(self, content, num_questions):
          """
          Formats the prompt for OpenAI to generate a multiple-choice question.

          :param content: The content for the prompt.
          :return: The formatted prompt string.
          """
          return f"""
          You are an expert Multiple-Choice Question maker.
          Create {num_questions} multiple-choice questions based on the following content:
          {content}

          Format:
          Question: [Your question]
          Options:
          - A) Option 1
          - B) Option 2
          - C) Option 3
          - D) Option 4
          Answer: [Correct answer]
          """

     def _parse_questions(self, text):
          """
          Parses multiple-choice questions from OpenAI's response text.

          :param text: The raw text returned by the OpenAI API.
          :return: A list of question dictionaries, each containing question, options, and answer.
          """
          questions = []
          sections = text.split("---")

          for section in sections:
               section = section.strip()
               if not section:
                    continue

               question_match = re.search(r'(?:\*\*Question|\bQuestion) \d+: (.+)', section)
               if not question_match:
                    continue
               question_text = question_match.group(1).strip()

               options = {}
               options_match = re.findall(r'- ([A-D])\) (.+)', section)
               for option in options_match:
                    options[option[0]] = option[1].strip()

               answer_match = re.search(r'Answer: ([A-D]\)) (.+)', section)
               if not answer_match:
                    continue
               answer_letter = answer_match.group(1).strip()
               answer_text = answer_match.group(2).strip()

               answer = f"{answer_letter} {answer_text}"

               questions.append({
                    "question": question_text,
                    "options": options,
                    "answer": answer
               })

          return questions

     def send_request(self, content, num_questions):
          prompt = self._format_prompt(content, num_questions)

          completion = self.client.chat.completions.create(
                         model=self.engine,
                         messages=[{"role": "user", "content": prompt}],
                         temperature=self.temperature,
                         max_tokens=self.max_tokens,
                         n=1
                         )

          return completion

     def generate_questions(self, content, num_questions=3):
          """
          Generates multiple multiple-choice questions based on the content of a learning note.

          :param content: The content from which to generate questions.
          :param num_questions: The number of questions to generate.
          :return: A list of dictionaries, each containing a question, options, and the correct answer.
          """
          try:
               response = self.send_request(content, num_questions)
               print(response.choices[0].message.content)
               questions = self._parse_questions(response.choices[0].message.content)

               return questions

          except Exception as e:
               return {"error": str(e)}


if __name__ == "__main__":
     content = """<h2><strong>WebSocket</strong></h2><p>WebSocket is bidirectional, a full-duplex protocol that is used in the same scenario of client-server communication, unlike HTTP which starts from&nbsp;<strong>ws://</strong>&nbsp;or&nbsp;<strong>wss://</strong>. It is a stateful protocol, which means the connection between client and server will stay alive until it gets terminated by either party (client or server). After closing the connection by either of the client or server, the connection is terminated from both ends.&nbsp;</p><p><br></p><p>Let’s take an example of client-server communication, there is the client which is a web browser, and a server, whenever we initiate the connection between client and server, the client-server makes the handshaking and decides to create a new connection and this connection will keep alive until terminated by any of them. When the connection is established and alive the communication takes place using the same connection channel until it is terminated.&nbsp;</p><p><br></p><p>This is how after client-server handshaking, the client-server decides to keep a new connection alive, this new connection will be known as WebSocket. Once the communication link is established and the connections are opened, message exchange will take place in bidirectional mode until the connection persists between client-server. If anyone of them (client-server) dies or decide to close the connection then it is closed by both the party. The way in which the socket works is slightly different from how HTTP works, the status code 101 denotes the switching protocol in WebSocket.&nbsp;</p><p>&nbsp;</p><p><img src="https://media.geeksforgeeks.org/wp-content/uploads/20191203183648/WebSocket-Connection.png" height="inherit" width="inherit"></p><h2><strong>When can a web socket be used?</strong></h2><ul><li><strong>Real-time web application:</strong>&nbsp;Real-time web application uses a web socket to show the data at client end, which is continuously being sent by the backend server. In WebSocket, data is continuously pushed/transmitted into the same connection which is already open, that is why WebSocket is faster and improves the application performance.&nbsp;e.g. in a trading website or bitcoin trading, for displaying the price fluctuation and movement data is continuously pushed by the backend server to the client end by using a WebSocket channel.</li><li><strong>Gaming application:</strong>&nbsp;In a Gaming application, you might focus on that, data is continuously received by the server, and without refreshing the UI, it will take effect on the screen, UI gets automatically refreshed without even establishing the new connection, so it is very helpful in a Gaming application.</li><li><strong>Chat application:</strong>&nbsp;Chat applications use WebSockets to establish the connection only once for exchange, publishing, and broadcasting the message among the subscribers. It reuses the same WebSocket connection, for sending and receiving the message and for one-to-one message transfer.</li></ul><h2><strong>When not to use WebSocket?</strong></h2><p>WebSocket can be used if we want any real-time updated or continuous streams of data that are being transmitted over the network but if we want to fetch old data, or want to get the data only once to process it with an application we should go with&nbsp;<strong>HTTP protocol</strong>, old data which is not required very frequently or fetched only once can be queried by the simple HTTP request, so in this scenario, it’s better not use WebSocket.</p><p><br></p><p><a href="https://www.geeksforgeeks.org/what-is-web-socket-and-how-it-is-different-from-the-http/" rel="noopener noreferrer" target="_blank">Readmore</a></p>"""

     generator = QuestionGenerator()
     questions = generator.generate_questions(content)
     print(questions)

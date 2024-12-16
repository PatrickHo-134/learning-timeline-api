from operator import truediv
from openai import OpenAI
from decouple import config
import logging

logger = logging.getLogger(__name__)

# README: documentation of Openai's API https://platform.openai.com/docs/api-reference/chat/create

def extract_question(lines):
     question_section = list(filter(lambda x: x.startswith("<Question>"), lines))[0]
     question = question_section.replace("<Question>: ", "")

     return question

def is_option(line):
     return line.startswith("A)") or line.startswith("B)") or line.startswith("C)") or line.startswith("D)")

def extract_options(lines):
     return list(filter(is_option, lines))

def extract_answer(lines):
     answer_section = list(filter(lambda x: x.startswith("<Answer>"), lines))[0]
     answer = answer_section.replace("<Answer>: ", "")

     return answer

def extract_question_content(section):
     lines = section.split("\n")

     question = extract_question(lines)
     options = extract_options(lines)
     answer = extract_answer(lines)

     return {"question": question, "options": options, "answer": answer}

class QuestionGenerator:
     def __init__(self):
          self.api_key = config('OPENAI_API_KEY')
          self.engine = "gpt-4o-mini"
          self.max_tokens = 1000
          self.temperature = 0.7  # Controls the creativity of the output

          logger.info(f"OpenAI API Key: {self.api_key}")

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
          <Question>: question generated from the content
          <Options>:
          A) Option 1
          B) Option 2
          C) Option 3
          D) Option 4
          <Answer>: A) option 1

          Each question should be seperated by ---
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
               section_content = extract_question_content(section)

               questions.append(section_content)

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
               questions = self._parse_questions(response.choices[0].message.content)

               return questions

          except Exception as e:
               return {"error": str(e)}

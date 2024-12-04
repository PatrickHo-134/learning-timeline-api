from bs4 import BeautifulSoup

def extract_text_from_html(html_content):
     """
     Extracts plain text from HTML content.

     :param html_content: A string containing HTML.
     :return: A string of plain text.
     """
     soup = BeautifulSoup(html_content, "html.parser")
     text = soup.get_text(separator=" ")
     cleaned_text = " ".join(text.split())

     return cleaned_text
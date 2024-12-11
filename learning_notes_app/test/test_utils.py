import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils import extract_text_from_html

class TestExtractTextFromHtml(unittest.TestCase):

    def test_extract_text_with_simple_html(self):
        html_content = "<h1>Welcome</h1><p>This is a test.</p>"
        expected_output = "Welcome This is a test."
        result = extract_text_from_html(html_content)
        self.assertEqual(result, expected_output)

    def test_extract_text_with_nested_html(self):
        html_content = "<div><h1>Title</h1><div><p>Some <b>bold</b> text here.</p></div></div>"
        expected_output = "Title Some bold text here."
        result = extract_text_from_html(html_content)
        self.assertEqual(result, expected_output)

    def test_extract_text_with_list_html(self):
        html_content = "<ul><li>Item 1</li><li>Item 2</li><li>Item 3</li></ul>"
        expected_output = "Item 1 Item 2 Item 3"
        result = extract_text_from_html(html_content)
        self.assertEqual(result, expected_output)

    def test_extract_text_with_extra_whitespace(self):
        html_content = "<p>   Lots    of   extra  whitespace    here.  </p>"
        expected_output = "Lots of extra whitespace here."
        result = extract_text_from_html(html_content)
        self.assertEqual(result, expected_output)

    def test_extract_text_with_empty_html(self):
        html_content = ""
        expected_output = ""
        result = extract_text_from_html(html_content)
        self.assertEqual(result, expected_output)

    def test_extract_text_with_no_tags(self):
        html_content = "Just plain text with no HTML tags."
        expected_output = "Just plain text with no HTML tags."
        result = extract_text_from_html(html_content)
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()

import unittest
from io import StringIO

from text_generator import file_line_generator


class TestFileinGenerator(unittest.TestCase):
    def test_search_words_found(self):
        file_content = StringIO(
            "а Роза упала на лапу Азора\n"
            "роза красивая\n"
            "лапа мягкая\n"
            "розы цветут\n"
            "лапы пушистые"
        )

        search_words = ["роза", "лапа"]
        stop_words = ["азора", "упала"]

        result = list(file_line_generator(file_content, search_words, stop_words))
        expected = ["роза красивая", "лапа мягкая"]
        self.assertEqual(result, expected)

    def test_stop_words_ignore(self):
        file_content = StringIO(
            "а Роза упала на лапу Азора\n"
            "роза красивая\n"
            "лапа мягкая\n"
            "розы цветут\n"
            "лапы пушистые"
        )

        search_words = ["роза", "лапа"]
        stop_words = ["азора", "упала"]

        result = list(file_line_generator(file_content, search_words, stop_words))
        self.assertNotIn("а Роза упала на лапу Азора", result)

    def test_no_search_words(self):
        file_content = StringIO("розы цветут\nлапы пушистые")
        search_words = ["роза"]
        stop_words = []

        result = list(file_line_generator(file_content, search_words, stop_words))
        self.assertEqual(result, [])

    def test_empty_file(self):
        file_content = StringIO("")
        search_words = ["роза"]
        stop_words = []

        result = list(file_line_generator(file_content, search_words, stop_words))
        self.assertEqual(result, [])

    def test_case_insensitivity(self):
        file_content = StringIO("Роза красивая\nроза цветет\nЛАПА мягкая")
        search_words = ["роза", "лапа"]
        stop_words = []

        result = list(file_line_generator(file_content, search_words, stop_words))
        expected = ["Роза красивая", "роза цветет", "ЛАПА мягкая"]
        self.assertEqual(result, expected)

    def test_multiple_matches_in_line(self):
        file_content = StringIO("роза и лапа\nрозы цветут\nлапы пушистые")
        search_words = ["роза", "лапа"]
        stop_words = []

        result = list(file_line_generator(file_content, search_words, stop_words))
        self.assertEqual(result, ["роза и лапа"])

    def test_string_in_search_words(self):
        file_content = StringIO("роза и лапа\nрозы цветут\nлапы пушистые")
        search_words = ["роза и лапа"]
        stop_words = ['лапы']

        result = list(file_line_generator(file_content, search_words, stop_words))
        self.assertEqual(result, [])

    def test_string_in_stop_words(self):
        file_content = StringIO("роза и лапа\nрозы цветут\nлапы пушистые")
        search_words = ["лапа"]
        stop_words = ["роза и лапа"]

        result = list(file_line_generator(file_content, search_words, stop_words))
        self.assertEqual(result, ["роза и лапа"])

    def test_char_in_search_words(self):
        file_content = StringIO("роза и лапа\nрозы цветут\nлапы пушистые")
        search_words = ["апа"]
        stop_words = []

        result = list(file_line_generator(file_content, search_words, stop_words))
        self.assertEqual(result, [])

    def test_char_in_stop_words(self):
        file_content = StringIO("роза и лапа\nрозы цветут\nлапы пушистые")
        search_words = ["роза"]
        stop_words = ["апа"]

        result = list(file_line_generator(file_content, search_words, stop_words))
        self.assertEqual(result, ["роза и лапа"])

    def test_file_path(self):
        with open("test_file.txt", "w", encoding="utf-8") as f:
            f.write("роза красивая\nлапа мягкая\nрозы цветут\nлапы пушистые")

        search_words = ["роза", "лапа"]
        stop_words = []

        result = list(file_line_generator("test_file.txt", search_words, stop_words))
        expected = ["роза красивая", "лапа мягкая"]
        self.assertEqual(result, expected)

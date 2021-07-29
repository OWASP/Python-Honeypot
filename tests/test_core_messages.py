import unittest
from core.messages import load_messages


class TestCoreMessagesModules(unittest.TestCase):

    def test_language_list(self):
        language_list = load_messages().languages_list
        languages = [
            "es_ES",
            "ru_RU",
            "en_US",
            "fr_FR",
            "de_DE"
        ]
        self.assertCountEqual(language_list, languages)

    def test_language_code(self):
        language_list = load_messages().languages_list
        self.assertIn("en_US", language_list)
        self.assertIn("es_ES", language_list)
        self.assertIn("ru_RU", language_list)
        self.assertIn("fr_FR", language_list)
        self.assertIn("de_DE", language_list)

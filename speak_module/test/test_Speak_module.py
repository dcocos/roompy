import unittest
from speak_module.Speak import Speak


class TestSpeakModule(unittest.TestCase):
    def test_speak(self):

        test_try = Speak()
        text_to_speak = 'Nevermore!'
        language = 'en'
        test_try.speak(text_to_speak, language)

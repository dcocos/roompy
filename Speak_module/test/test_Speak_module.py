import unittest
from Speak_module.SpeakManager import SpeakManager

class TestSpeakModule(unittest.TestCase):

    def test_speak(self):

        test_try = SpeakManager()
        text_to_speak = 'Nevermore!'
        language ="en"
        test_try.speak(text_to_speak, language)


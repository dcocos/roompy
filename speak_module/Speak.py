from gtts import gTTS
import hashlib
import os


class Speak:

    def create_MP3(self, text_to_speak: str, language: str, name_of_mp3: str):
        my_obj = gTTS(text=text_to_speak, lang=language, slow=False)
        my_obj.save(name_of_mp3)

    def obtain_hash(self, text_to_speak: str):
        text_bytes = bytes(text_to_speak, 'utf-8')
        hash_object = hashlib.sha1(text_bytes)
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def speak(self, text_to_read: str, language: str = 'en'):
        file_name = self.obtain_hash(text_to_read) + '.mp3'
        file_path = os.path.join(os.path.dirname(__file__), 'SoundRecordings', file_name)
        if not os.path.exists(file_path):
            self.create_MP3(text_to_read, language, file_path)
        os.system("mpg321 " + file_path)

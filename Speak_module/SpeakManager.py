from gtts import gTTS
import hashlib
import os

class SpeakManager:

    def create_MP3(self, text_to_read: str, language: str, name_of_mp3: str):
        my_obj = gTTS(text=text_to_read, lang=language, slow=False)
        my_obj.save(name_of_mp3)

    def obtain_hash(self, text_to_read: str):
        text = bytes(text_to_read, 'utf-8')
        hash_object = hashlib.sha512(text)
        hex_dig = hash_object.hexdigest()
        return hex_dig

    def verify_hash(self, hash_name: str):
        directory = os.fsencode("../../Speak_module/SoundRecordings/")
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename == hash_name:
                return True
            else:
                continue
        return False

    def speak(self, text_to_read: str, language: str):
        hex_dig = self.obtain_hash(text_to_read)+".mp3"
        name_of_mp3 = "../../Speak_module/SoundRecordings/" + hex_dig
        if(self.verify_hash(hex_dig) == False):
            self.create_MP3(text_to_read, language, name_of_mp3)
        os.system("mpg321 " + name_of_mp3)

import speech_recognition as sr
import googletrans as gt
from gtts import gTTS
import os

languages = ["English"]
#,"Portuguese","Italian","French","Latin","Greek","German","Russian","Hebrew","Arabic"]
keycodes = ["en"]
#,"pt","it","fr","la","el","de","ru","he","ar"]
#languages.remove("Hebrew")
#keycodes.remove("he")



def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    filename = "speech.mp3"
    tts.save(filename)
    os.system(f"afplay {filename}")
    
#recognizer = sr.Recognizer()
#translator = gt.Translator()
num = 0
while True:
    recognizer = sr.Recognizer()
    translator = gt.Translator()
    with sr.Microphone() as source:
        print("Speak Spanish word:")
        audio = recognizer.listen(source)

    try:

        spanish_word = recognizer.recognize_google(audio, language="es-MX")
        print(spanish_word)
            
        for i in range(len(languages)):
            translated_word = translator.translate(spanish_word, src='es', dest=keycodes[i]).text
            print(translated_word)
            if __name__ == "__main__":
                text_to_speech(translated_word, keycodes[i])
    except sr.UnknownValueError:
        print("Could not understand audio")
    

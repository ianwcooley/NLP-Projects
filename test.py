import speech_recognition as sr
import googletrans as gt
from gtts import gTTS
import os

languages = ["Spanish","Portuguese","Italian","French","Latin","Greek","German","Russian","Hebrew","Arabic"]
keycodes = ["es","pt","it","fr","la","el","de","ru","he","ar"]
languages.remove("Hebrew")
keycodes.remove("he")



def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    filename = "speech.mp3"
    tts.save(filename)
    os.system(f"afplay {filename}")
    
recognizer = sr.Recognizer()
translator = gt.Translator()

with sr.Microphone() as source:
    print("Speak English word:")
    audio = recognizer.listen(source)

try:

    english_word = recognizer.recognize_google(audio, lang="en-US")
    print("English word:", english_word)
    if __name__ == "__main__":
        text_to_speech("English", "en")
        text_to_speech(english_word, 'en')

    for i in range(len(languages)):
        translated_word = translator.translate(english_word, src='en', dest=keycodes[i]).text
        print(languages[i] + " translation:", translated_word)
        print("")
        if __name__ == "__main__":
            text_to_speech(languages[i], keycodes[i])
            text_to_speech(translated_word, keycodes[i])
except sr.UnknownValueError:
    print("Could not understand audio")
'''
    spanish_word = translator.translate(english_word, src='en', dest='es').text
    print("Spanish translation:", spanish_word)
    if __name__ == "__main__":
        text_to_speech(spanish_word, 'es')
        
    portuguese_word = translator.translate(english_word, src='en', dest='pt')
    print("Portuguese translation:", translated_word.text)
    
    
    italian_word = translator.translate(english_word, src='en', dest='it')
    print("Italian translation:", translated_word.text)
    translated_word = translator.translate(english_word, src='en', dest='fr')
    print("French translation:", translated_word.text)
    translated_word = translator.translate(english_word, src='en', dest='la')
    print("Latin translation:", translated_word.text)
    translated_word = translator.translate(english_word, src='en', dest='el')
    print("Greek translation:", translated_word.text)
    translated_word = translator.translate(english_word, src='en', dest='de')
    print("German translation:", translated_word.text)
    translated_word = translator.translate(english_word, src='en', dest='ru')
    print("Russian translation:", translated_word.text)
    translated_word = translator.translate(english_word, src='en', dest='he')
    print("Hebrew translation:", translated_word.text)
    translated_word = translator.translate(english_word, src='en', dest='ar')
    print("Arabic translation:", translated_word.text)
except sr.UnknownValueError:
    print("Could not understand audio")


'''

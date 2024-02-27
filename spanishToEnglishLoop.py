import speech_recognition as sr
import googletrans as gt
from gtts import gTTS
import os
import time

languages = ["English"]
keycodes = ["en"]



def text_to_speech(text, lang):
    tts = gTTS(text=text, lang=lang)
    filename = "speech.mp3"
    tts.save(filename)
    os.system(f"afplay {filename}")
    
#recognizer = sr.Recognizer()
translator = gt.Translator()

def callback(recognizer, audio):
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
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


r = sr.Recognizer()
m = sr.Microphone(sample_rate=8000)
with m as source:
    r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

# start listening in the background (note that we don't have to do this inside a `with` statement)
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some unrelated computations for 5 seconds
for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things

# calling this function requests that the background listener stop listening
#stop_listening(wait_for_stop=False)

# do some more unrelated things
while True:
    time.sleep(0.1)  # we're not listening anymore, even though the background thread might still be running for a second or two while cleaning up and stopping

    
'''
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
'''

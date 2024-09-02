import speech_recognition as sr
import googletrans as gt
import sys

# Initialize recognizer for speech recognition
recognizer = sr.Recognizer()

def capture_audio(audio_request_message):
    """Adjusts for background noise, prints audio_request_message that asks the
    user to speak, then records what the user says."""
    with sr.Microphone(sample_rate=8000) as source:
        print("...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(audio_request_message)
        audio = recognizer.listen(source)
        return audio


def convert_audio_to_text(audio, language="english"):
    """Converts a recorded audio message to text. If no language is given,
    defaults to English."""
    lang_code = gt.LANGCODES[language.lower()]
    try:
        text = recognizer.recognize_google(audio, language=lang_code)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        sys.exit()  # TODO: change this to loop back
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        sys.exit()  # TODO: change this to loop back

def get_language(direction):
    """Asks the user for the language they'd like to translate to or from, and returns
    that language if it is supported."""
    audio = capture_audio(f"Say the language you'd like to translate {direction}:")
    text = convert_audio_to_text(audio)
    if text.lower() in gt.LANGCODES:
        language = text.capitalize()
        print(f"You are translating {direction}: {text}")
        return language
    else:
        print(text + " is not a supported language.")
        sys.exit()  # TODO: change this to loop back

def get_word(language):
    """Asks the user to say a word in the given language, and returns the text
    of that word. If the user says more than one word, only the first word is
    returned."""
    audio = capture_audio(f"Say word in {language}:")
    words = convert_audio_to_text(audio, language).lower().split()
    return words[0]
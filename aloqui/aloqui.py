import speech_recognition as sr
import googletrans as gt
import pprint
import sys
import webbrowser
import requests
from bs4 import BeautifulSoup

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
    lang_code = gt.LANGCODES[language]
    try:
        text = recognizer.recognize_google(audio, language=lang_code)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
        sys.exit()  # TODO: change this to loop back
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        sys.exit()  # TODO: change this to loop back


def get_language_from():
    """Asks the user for the language they'd like to translate from, and returns
    that language if it is supported."""
    audio = capture_audio("Say the language you'd like to translate from:")
    text = convert_audio_to_text(audio)
    if text.lower() in gt.LANGCODES:
        language = text.lower()
        print("You are translating from: " + text)
        return language
    else:
        print(text + " is not a supported language.")
        sys.exit()  # TODO: change this to loop back


def get_language_to():
    """Asks the user for the language they'd like to translate to, and returns
    that language if it is supported."""
    audio = capture_audio("Say the language you'd like to translate to:")
    text = convert_audio_to_text(audio)
    if text.lower() in gt.LANGCODES:
        language = text.lower()
        print("You are translating to: " + text)
        return language
    else:
        print(text + " is not a supported language.")
        sys.exit()  # TODO: change this to loop back


def get_word(language):
    """Asks the user to say a word in the given language, and returns the text
    of that word. If the user says more than one word, only the first word is
    returned."""
    audio = capture_audio(f"Say word in {language.capitalize()}:")
    words = convert_audio_to_text(audio, language).split()
    return words[0]

def check_and_open_url(url):
    """Checks to see if url exists, and if so, opens the url in the user's default
    web browser. If not, prints an error message."""
    try:
        # Send a HEAD request to check if the URL exists
        response = requests.head(url, allow_redirects=True)
        if response.status_code == 200:
            webbrowser.open(url)
        else:
            print(f"URL does not exist or returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to reach the URL: {e}")

def get_soup(url):
    """Checks to see if url exists, and if so, gets the BeautifulSoup of the url.
    If not, prints an error message."""
    try:
        response = requests.get(url, allow_redirects=True)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # print(soup.prettify())
            print(soup.get_text())
        else:
            print(f"URL does not exist or returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to reach the URL: {e}")
    


def get_word_info(word, language):
    url = f"https://en.wiktionary.org/wiki/{word}#{language.capitalize()}"
    # check_and_open_url(url)
    get_soup(url)

# get_language_from()


def main():
    language_from = get_language_from()
    # language_to = get_language_to()
    # print(f'Translating from {language_from.capitalize()}'
    #       + f' to {language_to.capitalize()}')
    # print(f'Translating from {language_from.capitalize()}...')
    word = get_word(language_from)
    print(word)
    get_word_info(word, language_from)


if __name__ == "__main__":
    main()

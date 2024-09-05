import speech_recognition as sr
import googletrans as gt
import sys
from bs4 import BeautifulSoup
from gtts import gTTS
from pydub import AudioSegment
import os
import string
import pprint
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from word2number import w2n

# Initialize recognizer for speech recognition
recognizer = sr.Recognizer()
recognizer.pause_threshold = 0.5



def play_audio(file_path):
    """Play audio file using afplay on macOS"""
    os.system(f"afplay '{file_path}'")

def speak(text, lang_code):
    """Makes and plays an audio clip of the text in the given language"""
    # Text-to-speech function
    tts = gTTS(text=text, lang=lang_code, slow=False)
    tts.save("output.mp3")
    play_audio("output.mp3")

def is_language(text):
    return text.split()[0].lower() in gt.LANGCODES

def is_yes_or_no(text):
    return text.split()[0].lower() in ["yes", "no"]

def yes_or_no_error_message(text):
    return "Say yes or no."

def language_not_supported_message(text):
    return f"{text} is not a supported language."

def listen_for_input(prompt, lang_code, condition=None, error_message=None):
    """Prompts the user to say something, and returns
    what the user said as a string.
    
    lang_code sets the language to be listened for
    condition sets the condition to check the text against
    error_message returns the message to print if the condition is not met
    
    If condition is not met, prompts user again"""

    # with sr.Microphone(sample_rate=48000, chunk_size=512) as source:
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print(recognizer.energy_threshold)
        # print and speak prompt
        print(prompt)
        print(">>> ", end="", flush=True)
        speak(prompt, "en")
        while True:
            try:
                # audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                # listen for user input and discover if reco
                audio = recognizer.listen(source)
                # text = recognizer.recognize_google_cloud(audio, language=lang_code)
                text = recognizer.recognize_google(audio, language=lang_code)
                print("text: ", text)
                speak(text, lang_code)
                if condition == None or condition(text):
                    return text
                else:
                    if (error_message):
                        print("\n", error_message(text))
                        speak(error_message(text), "en")
                    print(prompt)
                    print(">>> ", end="", flush=True)
                    speak(prompt, "en")
            except sr.WaitTimeoutError:
                print("Timeout: No speech detected within the timeout period.")
            except sr.UnknownValueError:
                print("\nSorry, I did not understand.")
                speak("Sorry, I did not understand.", "en")
                print(prompt)
                print(">>> ", end="", flush=True)
                speak(prompt, "en")
            except sr.RequestError as e:
                print(f"Could not request results from Google Cloud Speech service; {e}")
                # text = recognizer.recognize_google(audio, language=lang_code)
def get_language():
    language = listen_for_input("Please say a language", "en-US", is_language, language_not_supported_message)
    return language.split()[0].capitalize()

def get_word(language):
    lang_code = gt.LANGCODES[language.lower()]
    words = listen_for_input("Please say a word", lang_code)
    word = words.split()[0]
    return word

def ask_for_flashcard():
    wants_to_make_flashcard = listen_for_input("Do you want to make a flashcard?", "en",  is_yes_or_no, yes_or_no_error_message)
    if wants_to_make_flashcard.split()[0].lower() == "yes":
        return True
    else:
        return False
    
def which_image():
    input_string = listen_for_input("Which image would you like to use?", "en")
    try:
        number = w2n.word_to_num(input_string)
    except ValueError as e:
        print()

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

# def get_language(direction):
#     """Asks the user for the language they'd like to translate to or from, and returns
#     that language if it is supported."""
#     audio = capture_audio(f"Say the language you'd like to translate {direction}:")
#     text = convert_audio_to_text(audio)
#     if text.lower() in gt.LANGCODES:
#         language = text.capitalize()
#         print(f"You are translating {direction}: {text}")
#         return language
#     else:
#         print(text + " is not a supported language.")
#         sys.exit()  # TODO: change this to loop back

# def get_word(language):
#     """Asks the user to say a word in the given language, and returns the text
#     of that word. If the user says more than one word, only the first word is
#     returned."""
#     audio = capture_audio(f"Say word in {language}:")
#     words = convert_audio_to_text(audio, language).lower().split()
#     return words[0]

def combine_fragments(text_fragments):
    # List to store the combined fragments
    combined_fragments = []

    # Initialize variables to keep track of the current fragment
    current_text = ""
    current_lang = None

    # Iterate through the text fragments
    for text, lang in text_fragments:
        # If the language matches the current block, append the text
        if lang == current_lang:
            current_text += " " + text  # Add space between combined text
        else:
            # If the language changes or it's the first block, save the previous block
            if current_text:
                combined_fragments.append((current_text.strip(), current_lang))
            # Start a new block
            current_text = text
            current_lang = lang

    # Append the last block if any
    if current_text:
        combined_fragments.append((current_text.strip(), current_lang))

    return combined_fragments

def find_language(element):
    # Check if the element itself has a 'lang' attribute
    if element.get('lang'):
        return element.get('lang')
    # Recursively check the parent elements
    elif element.parent:
        return find_language(element.parent)
    else:
        # Default to 'en' if no 'lang' attribute is found
        return 'en'

def get_multilingual_audio(html_content, audio_files, iteration):
    soup = BeautifulSoup(html_content, 'html.parser')

    # List to store text fragments with their respective languages
    text_fragments = []

    # Extract text fragments with language information
    for element in soup.find_all(text=True):
        if element.strip():  # Ensure the text is not empty
            lang = find_language(element.parent)
        text_fragments.append((element.strip(), lang))

    # print(text_fragments)
    combined_fragments = combine_fragments(text_fragments)

    # audio_files = []

    # Generate TTS for each fragment
    for i, (text, lang) in enumerate(combined_fragments):
        # Check if the fragment is not just punctuation
        # if any(char.isalnum() for char in text):  # At least one alphanumeric character
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            filename = f"fragment_{iteration}_{i}_{lang}.mp3"
            tts.save(filename)
            audio_files.append(filename)
        except Exception as e:
            print(f"Error generating TTS for fragment '{text}' with language '{lang}': {e}")
        # else:
            # print(f"Skipping punctuation-only fragment: '{text}'")
        
    # # Combine the audio fragments using pydub
    # combined_audio = AudioSegment.empty()

    # for audio_file in audio_files:
    #     audio_segment = AudioSegment.from_mp3(audio_file)
    #     combined_audio += audio_segment

    # # Save the combined audio file
    # combined_audio.export("combined_output.mp3", format="mp3")

    # # Clean up temporary files
    # for audio_file in audio_files:
    #     os.remove(audio_file)

    # # Play the final audio (this will depend on your OS)
    # os.system("open combined_output.mp3")  # For Windows; use "open combined_output.mp3" for macOS or "xdg-open combined_output.mp3" for Linux


def play_word_entry_audio(word_entry):
    audio_files = []
    iteration = 0
    for pos, defs in word_entry.definitions.items():
        if defs:  # Only play definitions for parts of speech with definitions
            # try:
            #     tts = gTTS(text=pos, lang='en', slow=False)
            #     filename = f"{pos}.mp3"
            #     tts.save(filename)
            #     audio_files.append(filename)
            # except Exception as e:
            #     print(f"Error generating TTS for fragment '{text}' with language '{lang}': {e}")
            for definition in defs:
                # pprint.pp(definition['text'])
                get_multilingual_audio(definition['html'], audio_files, iteration)
                
                iteration += 1

    # Combine the audio fragments using pydub
    combined_audio = AudioSegment.empty()

    for audio_file in audio_files:
        audio_segment = AudioSegment.from_mp3(audio_file)
        combined_audio += audio_segment

    # Save the combined audio file
    combined_audio.export("combined_output.mp3", format="mp3")

    # Clean up temporary files
    for audio_file in audio_files:
        os.remove(audio_file)

    # Play the final audio (this will depend on your OS)
    os.system("open combined_output.mp3")  # For Windows; use "open combined_output.mp3" for macOS or "xdg-open combined_output.mp3" for Linux


def say_multilingual_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # List to store text fragments with their respective languages
    text_fragments = []

    # Extract text fragments with language information
    for element in soup.find_all(text=True):
        if element.strip():  # Ensure the text is not empty
            lang = element.parent.get('lang', 'en')  # Default to English if no 'lang' attribute
            text_fragments.append((element.strip(), lang))

    # print(text_fragments)  # Example: [('Hello, this is an', 'en'), ('oración', 'es'), ('in English with a', 'en'), ('palabra', 'es'), ...]

    audio_files = []

    # Generate TTS for each fragment
    for i, (text, lang) in enumerate(text_fragments):
        # Check if the fragment is not just punctuation
        if any(char.isalnum() for char in text):  # At least one alphanumeric character
            try:
                tts = gTTS(text=text, lang=lang, slow=False)
                filename = f"fragment_{i}_{lang}.mp3"
                tts.save(filename)
                audio_files.append(filename)
            except Exception as e:
                print(f"Error generating TTS for fragment '{text}' with language '{lang}': {e}")
        # else:
            # print(f"Skipping punctuation-only fragment: '{text}'")

    # Combine the audio fragments using pydub
    combined_audio = AudioSegment.empty()

    for audio_file in audio_files:
        audio_segment = AudioSegment.from_mp3(audio_file)
        combined_audio += audio_segment

    # Save the combined audio file
    combined_audio.export("combined_output.mp3", format="mp3")

    # Clean up temporary files
    for audio_file in audio_files:
        os.remove(audio_file)

    # Play the final audio (this will depend on your OS)
    os.system("open combined_output.mp3")  # For Windows; use "open combined_output.mp3" for macOS or "xdg-open combined_output.mp3" for Linux

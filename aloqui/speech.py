import speech_recognition as sr
import googletrans as gt
import sys
from bs4 import BeautifulSoup
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
import string
import pprint
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
from word2number import w2n
import pyaudio
import wave
from google.cloud import speech
import utils
import constants

# Initialize recognizer for speech recognition
recognizer = sr.Recognizer()
# recognizer.pause_threshold = 0.5

def play_audio(file_path):
    """Play audio file using afplay on macOS"""
    os.system(f"afplay '{file_path}'")

def speak(text, lang_code):
    """Makes and plays an audio clip of the text in the given language"""
    # Text-to-speech function
    if utils.is_non_empty_string(text):
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save("output.mp3")
        play_audio("output.mp3")

def listen_for_input(prompt, lang_code, condition=None, error_message=None, contexts=[]):
    """Prompts the user to say something, and returns
    what the user said as a string.
    
    lang_code sets the language to be listened for
    condition sets the condition to check the text against
    error_message returns the message to print if the condition is not met
    
    If condition is not met, prompts user again"""

    # with sr.Microphone(sample_rate=48000, chunk_size=512) as source:
    with sr.Microphone(sample_rate=16000) as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        # print(recognizer.energy_threshold)
        # print and speak prompt
        print(prompt)
        print(">>> ", end="", flush=True)
        # speak(prompt, "en")
        while True:
            try:
                # audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)
                # listen for user input
                audio = recognizer.listen(source)
                
                ###
                print("Recording stopped. Processing...")
                # Convert audio to a format compatible with Google Cloud Speech-to-Text
                audio_data = audio.get_wav_data()

                # Convert the audio_data to an AudioSegment object
                audio_segment = AudioSegment(
                    data=audio_data,
                    sample_width=2,  # Assuming 16-bit audio
                    frame_rate=16000,  # Assuming a sample rate of 16000 Hz
                    channels=1  # Assuming mono audio
                )

                # Play back the audio using pydub
                # play(audio_segment)
                
                # Initialize the Google Cloud Speech Client
                client = speech.SpeechClient()
                # Configure the audio settings with phrase hints
                audio_google = speech.RecognitionAudio(content=audio_data)
                config = speech.RecognitionConfig(
                    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                    sample_rate_hertz=16000,
                    language_code=lang_code, # "en-US"
                    model="command_and_search",
                    speech_contexts=[speech.SpeechContext(phrases=contexts)],  # Add your target keywords here
                    max_alternatives=1 # NOTE: we're telling speech to only look for one word
                )

                # Call the API
                response = client.recognize(config=config, audio=audio_google)

                # Process and print the results
                try:
                # Attempt to access the desired index
                    text = response.results[0].alternatives[0].transcript
                except IndexError:
                    text = ""
                # for result in response.results:
                #     print("Transcript: {}".format(result.alternatives[0].transcript))
                ###
                
                # text = recognizer.recognize_google_cloud(audio, language=lang_code)
                # text = recognizer.recognize_google(audio, language=lang_code)
                print("text: ", text)
                speak(text, lang_code)
                # import pdb; pdb.set_trace()
                if utils.is_non_empty_string(text):    
                    if condition == None or condition(text):
                        return text
                    else:
                        if (error_message):
                            print("\n", error_message(text))
                            speak(error_message(text), "en")
                else:
                    print("\nSorry, I did not understand.")
                    # speak("Sorry, I did not understand.", "en")
                print(prompt)
                print(">>> ", end="", flush=True)
                # speak(prompt, "en")
            except sr.WaitTimeoutError:
                print("Timeout: No speech detected within the timeout period.")
            except sr.UnknownValueError:
                print("\nSorry, I did not understand.")
                # speak("Sorry, I did not understand.", "en")
                print(prompt)
                print(">>> ", end="", flush=True)
                # speak(prompt, "en")
            except sr.RequestError as e:
                print(f"Could not request results from Google Cloud Speech service; {e}")
                
def get_language():
    user_input = listen_for_input("Please say a language", "en-US", utils.is_supported_language, utils.language_not_supported_message, constants.LANGUAGES.values())
    language = utils.first_word(user_input).capitalize()
    return language

def get_word(language):
    lang_code = constants.LANGCODES[language.lower()]
    user_input = listen_for_input("Please say a word", lang_code)
    word = utils.first_word(user_input)
    return word

def ask_for_flashcard():
    wants_to_make_flashcard = listen_for_input("Do you want to make a flashcard?", "en",  utils.is_yes_or_no, utils.yes_or_no_error_message, ["yes", "no"])
    if utils.first_word(wants_to_make_flashcard).lower() == "yes":
        return True
    else:
        return False
    
def get_which_image():
    numbers = [str(number) for number in range(constants.NUMBER_OF_IMAGE_DOWNLOADS)]
    user_input = listen_for_input("Which image would you like to use?", "en-US", utils.is_valid_image, utils.invalid_image_error_message, numbers)
    try:
        number = w2n.word_to_num(utils.first_word(user_input))
        print(number)
        return number
    except ValueError as e:
        print(e)


#
#
#
#
#
#
#
###
### Unused code
###
#
#
#
#
#
#
#

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
    lang_code = constants.LANGCODES[language.lower()]
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
#     if text.lower() in constants.LANGCODES:
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


##
## practice
##

def recognize_yes_no():
    # Define your microphone as the audio source
    with sr.Microphone() as source:
        print("Say 'yes' or 'no'...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = recognizer.listen(source)  # Listen to the source

    # Define the grammar with limited vocabulary
    try:
        # Only recognize "yes" or "no"
        recognized_word = recognizer.recognize_sphinx(audio, grammar="yes_no.gram")
        print("You said:", recognized_word)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
            print(f"Sphinx error: {e}")


def record_audio(file_path, record_seconds=5):
    # Set up the microphone
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

    print("Recording...")
    frames = []

    for _ in range(0, int(16000 / 1024 * record_seconds)):
        data = stream.read(1024)
        frames.append(data)

    print("Recording completed.")

    # Save the recorded audio
    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)
        wf.writeframes(b''.join(frames))

def transcribe_audio_with_hints(file_path):
    client = speech.SpeechClient()

    # Read the audio file
    with open(file_path, "rb") as audio_file:
        content = audio_file.read()

    # Configure the audio settings with phrase hints
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        speech_contexts=[speech.SpeechContext(phrases=["yes", "no"])],  # Add your target keywords here
    )

    # Call the API
    response = client.recognize(config=config, audio=audio)

    # Process and print the results
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))

def record_and_transcribe():
    # Initialize recognizer and microphone
    # recognizer = sr.Recognizer()
    microphone = sr.Microphone(sample_rate=16000)

    # Adjust microphone settings and start recording
    with microphone as source:
        print("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source)
        print("Listening... Please speak.")

        # Listen until the user stops speaking
        audio = recognizer.listen(source)

    print("Recording stopped. Processing...")

    # Convert audio to a format compatible with Google Cloud Speech-to-Text
    audio_data = audio.get_wav_data()

    # Initialize the Google Cloud Speech Client
    client = speech.SpeechClient()

    # Configure the audio settings with phrase hints
    audio_google = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        speech_contexts=[speech.SpeechContext(phrases=["1", "2", "3", "15"])],  # Add your target keywords here
    )

    # Call the API
    response = client.recognize(config=config, audio=audio_google)

    # Process and print the results
    for result in response.results:
        print("Transcript: {}".format(result.alternatives[0].transcript))



def main():
    ask_for_flashcard()
    # recognize_yes_no()
    # Record audio and transcribe
    # record_audio("output.wav")
    # transcribe_audio_with_hints("output.wav")
    # record_and_transcribe()    
    pass


if __name__ == "__main__":
    main()
# Make sure you create a grammar file `yes_no.gram` with the following content:
# #JSGF V1.0;
# grammar yes_no;
# public <yesno> = yes | no ;


# Set up environment variable for credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service-account-file.json"
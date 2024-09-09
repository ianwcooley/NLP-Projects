import googletrans as gt
from word2number import w2n
import constants

def is_non_empty_string(value):
    """Check if a variable is a non-empty string."""
    return isinstance(value, str) and len(value) > 0

# def is_empty_string_or_none(value):
#     """Check if a variable is an empty string or None."""
#     return value == "" or value is None

def first_word(text):
    """Returns the first word in a given string."""
    return text.split()[0] if text else ''

def is_valid_image(text):
    try: 
        number = w2n.word_to_num(first_word(text))
        if number < constants.NUMBER_OF_IMAGE_DOWNLOADS:
            return True
        else:
            return False
    except ValueError:
        return False

def invalid_image_error_message(text):
    return f"{text} is not one of the images."

def is_supported_language(text):
    return first_word(text).lower() in gt.LANGUAGES.values()

def language_not_supported_message(text):
    return f"{text} is not a supported language."

def is_yes_or_no(text):
    return first_word(text).lower() in ["yes", "no"]

def yes_or_no_error_message(text):
    return "Say yes or no."


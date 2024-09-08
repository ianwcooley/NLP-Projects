import googletrans as gt

def is_non_empty_string(value):
    """Check if a variable is a non-empty string."""
    return isinstance(value, str) and len(value) > 0

# def is_empty_string_or_none(value):
#     """Check if a variable is an empty string or None."""
#     return value == "" or value is None

def is_language(text):
    return text.split()[0].lower() in gt.LANGCODES

def is_yes_or_no(text):
    return text.split()[0].lower() in ["yes", "no"]

def yes_or_no_error_message(text):
    return "Say yes or no."

def language_not_supported_message(text):
    return f"{text} is not a supported language."
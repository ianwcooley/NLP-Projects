import googletrans as gt
import gtts

PARTS_OF_SPEECH = [
    "Noun", "Pronoun", "Verb", "Adjective", "Adverb", "Preposition", "Conjunction", 
    "Interjection", "Article", "Determiner", "Numeral", "Participle", "Particle", 
    "Postposition", "Prefix", "Suffix", "Circumfix", "Infix", "Interfix", "Contraction", 
    "Phrase", "Proverb", "Idiom", "Abbreviation", "Initialism", "Symbol", "Letter", 
    "Diacritical_mark", "Romanization", "Affix", "Classificatory_particle", 
    "Auxiliary_verb", "Copula", "Proper_noun"
]

NUMBER_OF_IMAGE_DOWNLOADS = 20

# only supports languages that are recognized by both google translate and google text to speech
# format: {LANG_CODE: LANGUAGE,...}
LANGUAGES = {key: value for key, value in gt.LANGUAGES.items() if key in gtts.lang.tts_langs()}

# same as SUPPORTED_LANGUAGES but the keys and values are swapped
# format: {LANGUAGE: LANG_CODE,...}
LANGCODES = {value: key for key, value in LANGUAGES.items()}


def main():
    print(LANGUAGES)
    print(LANGCODES)

if __name__ == "__main__":
    main()

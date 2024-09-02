import pprint # NOTE: imported for testing purposes only
import speech
import wiki_parser

def main():
    language_from = speech.get_language("from")
    # language_to = get_language_to()
    # print(f'Translating from {language_from.capitalize()}'
    #       + f' to {language_to.capitalize()}')
    # print(f'Translating from {language_from.capitalize()}...')
    word = speech.get_word(language_from)
    print(word)
    wiki_parser.get_word_info(word, language_from)


if __name__ == "__main__":
    main()

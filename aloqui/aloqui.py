import pprint # NOTE: imported for testing purposes only
import speech
import wiki_parser
import googletrans as gt
import flashcard

def main():
    opened_page = False
    language = speech.get_language()
    while (opened_page == False):
        word = speech.get_word(language)
        opened_page = wiki_parser.open_wikitionary_page(word, language)    
        if opened_page == True:
            wants_to_make_flashcard = speech.ask_for_flashcard()
            if wants_to_make_flashcard:
                flashcard.get_images(word, language)
                pass
            else:
                opened_page = False
    




    # language_from = speech.get_language("from")
    # # language_to = get_language_to()
    # # print(f'Translating from {language_from.capitalize()}'
    # #       + f' to {language_to.capitalize()}')
    # # print(f'Translating from {language_from.capitalize()}...')
    # word = speech.get_word(language_from)
    # print(word)
    # html_content = wiki_parser.get_html(word, language_from)
    # parsed_entry = wiki_parser.parse_word_entry(html_content, word, language_from)
    # # wiki_parser.get_word_info(word, language_from)
    # # Access the parsed data
    
    # speech.play_word_entry_audio(parsed_entry)

    # print("Pronunciations:")
    # for pronunciation in parsed_entry.pronunciations:
    #     pprint.pp(pronunciation['text'])
    # print("Etymologies:")
    # for etymology in parsed_entry.etymologies:
    #     pprint.pp(etymology['text'])
    # for pos, defs in parsed_entry.definitions.items():
    #     if defs:  # Only print parts of speech with definitions
    #         print(f"Definitions for {pos}:") 
    #         for definition in defs:
    #             pprint.pp(definition['text'])
    #             speech.say_multilingual_html(definition['html'])

if __name__ == "__main__":
    main()

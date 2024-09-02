import webbrowser
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re
import constants
import pprint

# NOTE: This function is not called anywhere.
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
         # Send a HEAD request to check if the URL exists
        response = requests.get(url, allow_redirects=True)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            print(f"URL does not exist or returned status code: {response.status_code}")
            soup = None
    except requests.exceptions.RequestException as e:
        print(f"Failed to reach the URL: {e}")
    return soup

def get_html(word, language):
    """Goes to the wiktionary page for the given word, and writes to test.html
    only the section of the page's html code that corresponds to the given language"""
    encoded_word = quote(word)
    url = f"https://en.wiktionary.org/wiki/{encoded_word}#{language}"
    check_and_open_url(url) # NOTE: for testing purposes only
    soup = get_soup(url)
    if (soup):
        # Get div that contains heading with language name:
        start_element = soup.find(id=language.capitalize()).find_parent('div')
        # get that div's siblings until the div containing a heading with
        # the next language name is found, or the end of the page is found:        
        # Initialize a list to hold the desired elements:
        elements = [start_element]
        # Loop through the next siblings until the specific div with class="mw-headingheading2" is found
        for sibling in start_element.find_next_siblings():
            if sibling.name == 'div' and 'mw-heading2' in sibling.get('class', []):
                break
            elements.append(sibling)


        # Print the collected elements
        with open('test.html', 'w') as file:
            for element in elements:
                # file.write('ELEMENT\n')
                # for part_of_speech in constants.PARTS_OF_SPEECH:
                #     if element.find(lambda tag: tag.get('id', '').startswith(part_of_speech)):
                #         file.write('PART OF SPEECH\n')
                #         print(element.get_text())
                file.write(element.prettify() + '\n')

def get_plain_text(word, language):
    # MediaWiki API endpoint for English Wiktionary
    url = "https://en.wiktionary.org/w/api.php"

    # Define the parameters for the API request
    params = {
        "action": "query",
        "prop": "extracts",
        "titles": word,
        "format": "json",
        "explaintext": True  # Ensures the extract is plain text
    }

    # Make the API request
    response = requests.get(url, params=params)
    
    # Parse the JSON response
    data = response.json()

    # Regular expression for part of plain text corresponding to given language
    language_section_pattern = rf"(== {language} ==[\s\S]*?)(?=\n== [^\s=][^=]* ==|\Z)"

    # Extract the page content and write to file
    with open('test.txt', 'w') as file:
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_content in pages.items():
            extract = page_content.get("extract", "No content found.")
            match = re.search(language_section_pattern, extract, re.DOTALL)
            if match:
                language_section = match.group(1)  # Extract the content in the Spanish section
                return file.write(language_section)
            else:
                return "No Spanish section found in the text."


    # # Extract the page content
    # pages = data["query"]["pages"]
    # page_content = next(iter(pages.values()))["extract"]

def get_word_info(word, language):
    get_html(word, language)
    get_plain_text(word, language)

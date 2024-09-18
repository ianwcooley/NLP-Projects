import os
import requests
from duckduckgo_search import DDGS
import json
import base64
import threading

def search_duckduckgo_images(keyword):
    """Search for images on DuckDuckGo and return the results."""
    results = DDGS().images(
        keywords=keyword,
        region="wt-wt",
        # safesearch="off",
        size=None,
        # color="Monochrome",
        type_image=None,
        layout=None,
        license_image=None,
        max_results=20,
    )
    return results

def download_image(url, folder_path, index):
    """Download an image from a URL and save it to the specified folder."""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(folder_path, f"image_{index}.jpg")
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"Downloaded: {file_path}")
        else:
            print(f"Failed to download {url}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def get_images(word):
    """Download images concurrently using threading."""
    
    images = search_duckduckgo_images(word)
    # Folder to save downloaded images
    folder_path = "images"
    os.makedirs(folder_path, exist_ok=True)

    threads = []  # List to keep track of all threads

    # Create and start a thread for each image download
    for index, image in enumerate(images):
        image_url = image['image']
        thread = threading.Thread(target=download_image, args=(image_url, folder_path, index))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()


def store_image_in_anki(image_path, image_name):
    """
    Stores an image in Anki's media collection.

    Args:
    - image_path (str): The local path to the image file.
    - image_name (str): The name to store the image as in Anki's media collection.

    Returns:
    - str: Response from AnkiConnect.
    """
    # Read the image file and encode it in base64
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    # Define the request payload to store the media file
    payload = {
        "action": "storeMediaFile",
        "version": 6,
        "params": {
            "filename": image_name,
            "data": image_data
        }
    }

    # Send the request to AnkiConnect
    response = requests.post("http://localhost:8765", json=payload)

    # Parse and return the response
    return json.loads(response.text)

def add_card_with_image(deck_name, text, image_name, image_side, tags=None):
    """
    Adds a new card with an image to an Anki deck.

    Args:
    - deck_name (str): The name of the Anki deck.
    - front (str): The front text of the card.
    - back (str): The back text of the card.
    - image_name (str): The name of the stored image to include in the card.
    - tags (list, optional): A list of tags to assign to the card.

    Returns:
    - str: Response from AnkiConnect.
    """
    # Define the HTML image tag for the stored image
    image_tag = f'<img src="{image_name}">'

    # # Include the image in the front or back field
    # front_with_image = f"{front} {image_tag}"

    # Define the request payload to add the card
    payload = {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": deck_name,
                "modelName": "Basic",
                "fields": {
                    "Front": text if image_side == "back" else f"{image_tag}",
                    "Back": f"{image_tag}" if image_side == "back" else text
                },
                "tags": tags or [],
                "options": {
                    "allowDuplicate": False
                }
            }
        }
    }

    # Send the request to AnkiConnect
    response = requests.post("http://localhost:8765", json=payload)

    # Parse and return the response
    return json.loads(response.text)

def add_flashcard(image_number, word, language):
    image_name = f"image_{str(image_number)}.jpg"
    anki_image_name = f"{word}_{language}"
    store_response = store_image_in_anki(f"images/{image_name}", anki_image_name)
    print("Image Store Response:", store_response)

    # Step 2: Add the cards with the image on one side, text on the other (both directions)
    add_card_response_1 = add_card_with_image("Spanish-New", word, anki_image_name, "front", ["sample", "image"])
    print("Add Card Response:", add_card_response_1)
    add_card_response_2 = add_card_with_image("Spanish-New", word, anki_image_name, "back", ["sample", "image"])
    print("Add Card Response:", add_card_response_2)

# # Example usage
# deck_name = "Test"  # Replace with your deck name
# front_text = "Look at the cute lil kitty cat"
# back_text = "Isn't he cute?"
# image_path = "./kitty_cat.jpg"  # Replace with the actual path to your image file
# image_name = "kitty_cat.jpg"  # The name to store the image as in Anki
# tags = ["sample", "image"]

# # Step 1: Store the image in Anki's media collection
# store_response = store_image_in_anki(image_path, image_name)
# print("Image Store Response:", store_response)

# # Step 2: Add the card with the image
# add_card_response = add_card_with_image(deck_name, front_text, back_text, image_name, tags)
# print("Add Card Response:", add_card_response)

# def main():
#     images = search_duckduckgo_images()

#     # Folder to save downloaded images
#     folder_path = "images"
#     os.makedirs(folder_path, exist_ok=True)

#     # Download each image
#     for index, image in enumerate(images):
#         image_url = image['image']
#         download_image(image_url, folder_path, index)

# if __name__ == "__main__":
#     main()

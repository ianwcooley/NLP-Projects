import os
import requests
from duckduckgo_search import DDGS

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
        max_results=10,
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
    images = search_duckduckgo_images(word)
    # Folder to save downloaded images
    folder_path = "images"
    os.makedirs(folder_path, exist_ok=True)

    # Download each image
    for index, image in enumerate(images):
        image_url = image['image']
        download_image(image_url, folder_path, index)


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

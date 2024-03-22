import requests
from urllib.parse import unquote

def download_wikipedia_pages(urls, directory):
    for url in urls:
        try:
            # Extract the page title from the URL and unquote it
            page_title = unquote(url.split("/wiki/")[-1])
            # Construct the save path
            save_path = f"{directory}/{page_title}.html"
            # Send a GET request to the Wikipedia page
            response = requests.get(url)
            # Check if the request was successful
            if response.status_code == 200:
                # Open a file in binary write mode and write the page content to it
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                print(f"Page downloaded successfully and saved at '{save_path}'")
            else:
                print(f"Failed to download page '{url}'. Status code: {response.status_code}")
        except Exception as e:
            print(f"An error occurred while downloading page '{url}': {e}")

# Example usage:
urls = [
    "https://en.wikipedia.org/wiki/Shanghai",
    "https://en.wikipedia.org/wiki/Rio_de_Janeiro",
    "https://en.wikipedia.org/wiki/Chicago"
]
directory = "./city"
download_wikipedia_pages(urls, directory)

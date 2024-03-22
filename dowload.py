import os 
import requests
from urllib.parse import unquote
from bs4 import BeautifulSoup

cities_table = []

def download_table_data(url, selector):
    try:
        # Send a GET request to the Wikipedia page
        response = requests.get(url)
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # Find the table element using the provided selector
            table = soup.select(selector)
            # Extract and print the table data
            if table:
                cities_table = []
                # Extract data from each row of the table
                for row in table[2:]: #last row is 468 or 467
                    html_content = str(row.contents)
                    start_index = html_content.find('href="') + len('href="')
                    end_index = html_content.find('"', start_index)
                    href_value = html_content[start_index:end_index]
                    city = href_value.split("/wiki/")[-1]
                    # print (city)
                    cities_table.append(city)
                    if city == "Quetta":
                        print (cities_table)
                        break
                return cities_table
            else:
                print("Table not found on the page.")
                return None
        else:
            print(f"Failed to download page. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
url = "https://en.wikipedia.org/wiki/List_of_cities_with_over_one_million_inhabitants"
# #mw-content-text > div.mw-content-ltr.mw-parser-output > table:nth-child(10) > tbody > tr:nth-child(1)
selector = "tr"

cities_table = download_table_data(url, selector)

def download_wikipedia_pages(cities_table, save_directory):
    # Create the directory if it doesn't exist
    os.makedirs(save_directory, exist_ok=True)

    # Base URL
    base_url = "https://en.wikipedia.org/wiki/"

    # Iterate through each city
    for city in cities_table:
        # Construct the URL
        url = base_url + city

        # Fetch the page
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Generate the file path
            file_path = os.path.join(save_directory, f"{city}.html")

            # Save the HTML content to a file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(response.text)
            
            print(f"Page for {city} saved successfully.")
        else:
            print(f"Failed to download page for {city}. Status code: {response.status_code}")

# Example usage:
# cities_table = [] listed above!
save_directory = "./city"
download_wikipedia_pages(cities_table, save_directory)

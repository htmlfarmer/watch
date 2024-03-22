import requests
from bs4 import BeautifulSoup

url = "https://simple.wikipedia.org/wiki/List_of_countries"

res = requests.get(url)
soup = BeautifulSoup(res.text,"lxml")
for items in soup.find(class_="wikitable").find_all("tr")[1:]:
    data = items.find("td").get_text(strip=True)
    print(data)
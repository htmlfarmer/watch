"""
General News:

BBC News: https://feeds.bbci.co.uk/news/rss.xml
CNN: http://rss.cnn.com/rss/edition.rss
The New York Times: https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml
Reuters: https://feeds.reuters.com/reuters/topNews
Technology News:

TechCrunch: https://feeds.feedburner.com/TechCrunch
Wired: https://www.wired.com/feed/rss
The Verge: https://www.theverge.com/rss/index.xml
Ars Technica: https://arstechnica.com/feed/
Business News:

Bloomberg: https://www.bloomberg.com/feed/news/
CNBC: https://www.cnbc.com/id/100003114/device/rss/rss.html
Financial Times: https://www.ft.com/?format=rss
Forbes: https://www.forbes.com/business/feed/
Science News:

Scientific American: https://www.scientificamerican.com/feed/rss.cfm
National Geographic: https://www.nationalgeographic.com/rss.xml
Popular Science: https://www.popsci.com/rss.xml
Science Daily: https://www.sciencedaily.com/rss.xml
Sports News:

ESPN: http://www.espn.com/espn/rss/news
BBC Sport: https://feeds.bbci.co.uk/sport/rss.xml
The Guardian Sport: https://www.theguardian.com/uk/sport/rss
Entertainment News:

E! Online: https://www.eonline.com/news/rss.xml
Entertainment Weekly: https://ew.com/feed/
Variety: https://variety.com/feed/
World News:

Al Jazeera: https://www.aljazeera.com/xml/rss/all.xml
The Guardian: https://www.theguardian.com/world/rss
Associated Press: https://apnews.com/rss
Health News:

WebMD: https://www.webmd.com/rss/feeds
Healthline: https://www.healthline.com/rss
"""

import feedparser

rss_feeds = {
    # error with something? 'Reuters': 'https://www.reutersagency.com/en/reutersbest/reuters-best-rss-feeds/',
    """ 'TechCrunch': 'https://feeds.feedburner.com/TechCrunch',
    'Wired': 'https://www.wired.com/feed/rss',
    'The Verge': 'https://www.theverge.com/rss/index.xml',
    'Ars Technica': 'https://arstechnica.com/feed/',
    'Bloomberg': 'https://www.bloomberg.com/feed/news/',
    'CNBC': 'https://www.cnbc.com/id/100003114/device/rss/rss.html',
    'Financial Times': 'https://www.ft.com/?format=rss',
    'Forbes': 'https://www.forbes.com/business/feed/',
    'Scientific American': 'https://www.scientificamerican.com/feed/rss.cfm',
    'National Geographic': 'https://www.nationalgeographic.com/rss.xml',
    'Popular Science': 'https://www.popsci.com/rss.xml',
    'Science Daily': 'https://www.sciencedaily.com/rss.xml',
    'ESPN': 'http://www.espn.com/espn/rss/news',
    'BBC Sport': 'https://feeds.bbci.co.uk/sport/rss.xml',
    'The Guardian Sport': 'https://www.theguardian.com/uk/sport/rss',
    'E! Online': 'https://www.eonline.com/news/rss.xml',
    'Entertainment Weekly': 'https://ew.com/feed/',
    'Variety': 'https://variety.com/feed/',
    'Al Jazeera': 'https://www.aljazeera.com/xml/rss/all.xml',
    'The Guardian': 'https://www.theguardian.com/world/rss',
    'Associated Press': 'https://apnews.com/rss',
    'WebMD': 'https://www.webmd.com/rss/feeds',
    'Healthline': 'https://www.healthline.com/rss', 
    'BBC News': 'https://feeds.bbci.co.uk/news/rss.xml',
    'CNN': 'http://rss.cnn.com/rss/edition.rss',
    'The New York Times': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml', """
    'WSJ World News' : 'https://feeds.a.dj.com/rss/RSSWorldNews.xml'
}

for rss in rss_feeds:
    rss_feed_url = (rss_feeds[rss])

    # Fetch the RSS feed
    feed = feedparser.parse(rss_feed_url)

    # Check if the feed was successfully fetched
    if feed.get('bozo_exception') is not None:
        print("Error fetching RSS feed:", feed['bozo_exception'])
    else:
        # Print feed title and its entries
        print("Feed Title:", feed.feed.title)
        print("Feed Description:", feed.feed.description)
        print("Feed URL:", feed.feed.link)
        print("\nEntries:")
        for entry in feed.entries:
            print("- Title:", entry.title)
            #print("  Link:", entry.link)
            #print("  Published Date:", entry.published)
            
            # Check if summary exists
            if hasattr(entry, 'summary') and entry.summary:
                print("  Summary:", entry.summary)
            # Check if description exists
            elif hasattr(entry, 'description') and entry.description:
                print("  Description:", entry.description)
            else:
                print("  No summary or description available")
            
            print()

import os
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Function to extract text from HTML file
def extract_text_from_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
        # Extract text from HTML excluding scripts and styles
        text = ' '.join([p.get_text() for p in soup.find_all('p')])
    return text

# Function to preprocess text
def preprocess_text(text):
    # Add more preprocessing steps if needed (e.g., lowercase, remove punctuation)
    return text.lower()

# RSS feed value
rss_feed_value = "Stocks Take a Breather, Slipping at the End of a Red-Hot Week The Dow led stock indexes lower as results from Nike and Lululemon made some investors worry about consumer demand."

# Directory containing HTML files
html_directory = "./watch/city"

# Calculate TF-IDF vectors
vectorizer = TfidfVectorizer()

# Preprocess RSS feed value
rss_feed_value_processed = preprocess_text(rss_feed_value)

# Initialize variables to store the most similar city and its similarity score
most_similar_city = None
max_similarity_score = -1

city_similarity_scores = {}

for filename in os.listdir(html_directory):
    if filename.endswith(".html"):
        html_file_path = os.path.join(html_directory, filename)
        city_name = os.path.splitext(filename)[0]

        # Extract text from HTML file
        city_text = extract_text_from_html(html_file_path)

        # Preprocess city text
        city_text_processed = preprocess_text(city_text)

        # Calculate TF-IDF vectors
        tfidf_matrix = vectorizer.fit_transform([rss_feed_value_processed, city_text_processed])

        # Calculate cosine similarity between the RSS feed value and city text
        similarity_score = cosine_similarity(tfidf_matrix)[0][1]
        print(f"City: {city_name}, Similarity Score: {similarity_score}")

        # Update most similar city if similarity score is higher
        if similarity_score > max_similarity_score:
            max_similarity_score = similarity_score
            most_similar_city = city_name

        # Store city name and similarity score in the dictionary
        city_similarity_scores[city_name] = similarity_score

        for city, score in sorted(city_similarity_scores.items(), key=lambda x: x[1], reverse=True):
            print(f"City: {city}, Similarity Score: {score}")

print("Most similar city to the news:", most_similar_city)
print("Similarity score:", max_similarity_score)

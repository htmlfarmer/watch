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
    'Healthline': 'https://www.healthline.com/rss', """
    'BBC News': 'https://feeds.bbci.co.uk/news/rss.xml',
    'CNN': 'http://rss.cnn.com/rss/edition.rss',
    'The New York Times': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
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
            print("  Link:", entry.link)
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
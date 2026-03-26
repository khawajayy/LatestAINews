import requests
from bs4 import BeautifulSoup
import json

def scrape_hn_ai():
    try:
        # Using Algolia API for HN search which is more reliable than scraping the search page
        url = "https://hn.algolia.com/api/v1/search?query=AI&tags=story&numericFilters=created_at_i>0"
        # Let's get stories from the last 24 hours (approx)
        import time
        yesterday = int(time.time()) - 86400
        url = f"https://hn.algolia.com/api/v1/search?query=AI&tags=story&numericFilters=created_at_i>{yesterday}"
        
        response = requests.get(url)
        data = response.json()
        
        articles = []
        for hit in data.get('hits', []):
            articles.append({
                "title": hit.get('title'),
                "url": hit.get('url'),
                "source": "Hacker News",
                "created_at": hit.get('created_at')
            })
            if len(articles) >= 10:
                break
        return articles
    except Exception as e:
        print(f"Error scraping HN: {e}")
        return []

if __name__ == "__main__":
    results = scrape_hn_ai()
    print(json.dumps(results, indent=2))

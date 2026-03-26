import os
import json
from scrapers.hn_scraper import scrape_hn
from scrapers.arxiv_scraper import scrape_arxiv
from scrapers.blog_scraper import scrape_blogs
from scrapers.x_scraper import scrape_x
from brain.processor import process_article
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase Client
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def run_pipeline():
    print("🚀 Starting AI Pulse Pipeline...")
    
    # 1. Scrape
    all_articles = []
    
    print("Scraping Hacker News...")
    all_articles.extend(scrape_hn())
    
    print("Scraping ArXiv...")
    all_articles.extend(scrape_arxiv())
    
    print("Scraping Blogs...")
    all_articles.extend(scrape_blogs())
    
    # print("Scraping X...")
    # all_articles.extend(scrape_x()) # X scraping might require special handling in Docker
    
    print(f"Total raw articles: {len(all_articles)}")
    
    # 2. Process & Deduplicate (Simple uniqueness check by URL)
    processed_count = 0
    for article in all_articles:
        # Check if already in Supabase
        existing = supabase.table("articles").select("url").eq("url", article['url']).execute()
        if existing.data:
            continue
            
        print(f"Processing: {article['title'][:50]}...")
        enriched = process_article(article)
        
        # 3. Save to Supabase
        try:
            supabase.table("articles").insert({
                "title": enriched['title'],
                "summary": enriched.get('summary', ''),
                "category": enriched.get('category', 'Unknown'),
                "hype_score": enriched.get('hype_score', 5),
                "hype_label": enriched.get('hype_label', 'Balanced'),
                "source": enriched['source'],
                "url": enriched['url'],
                "content": enriched.get('content', '')
            }).execute()
            processed_count += 1
        except Exception as e:
            print(f"Error saving to database: {e}")

    print(f"✅ Pipeline complete. Processed {processed_count} new articles.")

if __name__ == "__main__":
    run_pipeline()

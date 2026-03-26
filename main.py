import asyncio
from scrapers.hn_scraper import scrape_hn_ai
from scrapers.arxiv_scraper import scrape_arxiv_ai
from scrapers.blog_scraper import scrape_lab_blogs
from scrapers.x_scraper import scrape_x_profile
from brain.processor import process_article
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    print("⚠️ Warning: GEMINI_API_KEY is missing. AI processing will likely fail.")

# Initialize Supabase Client
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("❌ Error: SUPABASE_URL or SUPABASE_KEY environment variables are missing!")
    exit(1)

print(f"Connecting to Supabase at: {url}")
try:
    supabase: Client = create_client(url, key)
    print("✅ Supabase client initialized.")
except Exception as e:
    print(f"❌ Failed to initialize Supabase client: {e}")
    exit(1)

async def run_pipeline():
    print("🚀 Starting AI Pulse Pipeline...")
    
    # 1. Scrape
    all_articles = []
    
    print("Scraping Hacker News...")
    all_articles.extend(scrape_hn_ai())
    
    print("Scraping ArXiv...")
    all_articles.extend(scrape_arxiv_ai())
    
    print("Scraping Blogs...")
    blog_articles = await scrape_lab_blogs()
    all_articles.extend(blog_articles)
    
    # print("Scraping X...")
    # x_handles = ['rowancheung', 'GoogleDeepMind', 'OpenAI']
    # for handle in x_handles:
    #     x_articles = await scrape_x_profile(handle)
    #     all_articles.extend(x_articles)
    
    print(f"Total raw articles: {len(all_articles)}")
    
    # 2. Process & Deduplicate
    processed_count = 0
    for article in all_articles:
        # Check if already in Supabase
        # We use URL as unique identifier
        try:
            existing = supabase.table("articles").select("url").eq("url", article['url']).execute()
            if existing.data:
                continue
        except Exception as e:
            print(f"Error checking existence: {e}")
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
    asyncio.run(run_pipeline())

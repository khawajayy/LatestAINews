import asyncio
from playwright.async_api import async_playwright
import json

async def scrape_x_profile(profile_handle):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # Navigate to a specific profile known for AI news
        url = f"https://x.com/{profile_handle}"
        await page.goto(url)
        
        # Wait for tweets to load
        try:
            await page.wait_for_selector('article', timeout=10000)
        except:
            print(f"Timeout waiting for tweets on {profile_handle}")
        
        # Extract tweets
        tweets = await page.query_selector_all('article')
        results = []
        
        for tweet in tweets[:5]: # Get latest 5
            text_element = await tweet.query_selector('[data-testid="tweetText"]')
            if text_element:
                text = await text_element.inner_text()
                # Simple check for AI content
                if any(term in text.lower() for term in ['ai', 'llm', 'gpt', 'model', 'robot', 'agent']):
                    # Find links
                    links = await text_element.query_selector_all('a')
                    hrefs = [await link.get_attribute('href') for link in links]
                    
                    results.append({
                        "title": text[:100] + "...", # Use start of text as title
                        "url": f"https://x.com{hrefs[0]}" if hrefs else url,
                        "source": f"X (@{profile_handle})"
                    })
        
        await browser.close()
        return results

async def main():
    handles = ['rowancheung', 'GoogleDeepMind', 'OpenAI']
    all_results = []
    for handle in handles:
        print(f"Scraping X profile: {handle}")
        res = await scrape_x_profile(handle)
        all_results.extend(res)
    print(json.dumps(all_results, indent=2))

if __name__ == "__main__":
    asyncio.run(main())

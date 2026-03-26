import requests
from bs4 import BeautifulSoup
import json

import asyncio
from playwright.async_api import async_playwright
import json

async def scrape_lab_blogs():
    results = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # OpenAI
        try:
            await page.goto("https://openai.com/news/", timeout=30000)
            links = await page.query_selector_all('a[href*="/news/"]')
            for link in links[:3]:
                title = await link.inner_text()
                href = await link.get_attribute('href')
                if title and href:
                    results.append({
                        "title": title.strip(),
                        "url": "https://openai.com" + href if href.startswith('/') else href,
                        "source": "OpenAI Blog"
                    })
        except Exception as e: print(f"OpenAI error: {e}")

        # Anthropic
        try:
            await page.goto("https://www.anthropic.com/news", timeout=30000)
            # Find all links in the news section that look like articles
            items = await page.query_selector_all('a[href^="/news/"]')
            for item in items:
                title_el = await item.query_selector('h3, h2, span:not([class*="tag"])')
                if not title_el: continue
                
                title = await title_el.inner_text()
                href = await item.get_attribute('href')
                
                # Filter out generic tags or short strings
                if title and len(title.strip()) > 10 and href:
                    results.append({
                        "title": title.strip(),
                        "url": "https://www.anthropic.com" + href,
                        "source": "Anthropic Blog"
                    })
                if len(results) >= 10: break
        except Exception as e: print(f"Anthropic error: {e}")

        await browser.close()
    return results

if __name__ == "__main__":
    results = asyncio.run(scrape_lab_blogs())
    print(json.dumps(results, indent=2))

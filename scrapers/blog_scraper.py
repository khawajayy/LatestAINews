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
            # Using specific attribute selectors as found by browser agent
            items = await page.query_selector_all('a[class*="listItem"]')
            for item in items[:3]:
                title_span = await item.query_selector('span:last-child')
                title = await title_span.inner_text() if title_span else await item.inner_text()
                href = await item.get_attribute('href')
                if title and href:
                    results.append({
                        "title": title.strip(),
                        "url": "https://www.anthropic.com" + href if href.startswith('/') else href,
                        "source": "Anthropic Blog"
                    })
        except Exception as e: print(f"Anthropic error: {e}")

        await browser.close()
    return results

if __name__ == "__main__":
    results = asyncio.run(scrape_lab_blogs())
    print(json.dumps(results, indent=2))

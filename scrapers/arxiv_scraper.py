import requests
from bs4 import BeautifulSoup
import json

def scrape_arxiv_ai():
    # CS.AI latest papers
    url = "https://arxiv.org/list/cs.AI/recent"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    articles = []
    # ArXiv lists papers in <dt> and <dd> pairs
    dts = soup.find_all('dt')
    dds = soup.find_all('dd')
    
    for dt, dd in zip(dts, dds):
        try:
            title_div = dd.find('div', class_='list-title')
            if not title_div: continue
            title = title_div.text.replace('Title:', '').strip()
            
            abstract_div = dd.find('p', class_='mathjax')
            abstract = abstract_div.text.strip() if abstract_div else ""
            
            id_span = dt.find('span', class_='list-identifier')
            if not id_span: continue
            link = id_span.find('a')
            if not link: continue
            paper_url = "https://arxiv.org" + link['href']
            
            articles.append({
                "title": title,
                "url": paper_url,
                "source": "ArXiv",
                "content": abstract # Abstract serves as technical content
            })
        except Exception as e:
            print(f"Error parsing ArXiv paper: {e}")
            continue
        
        articles.append({
            "title": title,
            "url": paper_url,
            "source": "ArXiv",
            "content": abstract # Abstract serves as technical content
        })
        
        if len(articles) >= 10:
            break
            
    return articles

if __name__ == "__main__":
    results = scrape_arxiv_ai()
    print(json.dumps(results, indent=2))

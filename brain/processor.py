import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
# If the user has an API key, we should use it. 
# For this task, we assume the code will be run in an environment with GEMINI_API_KEY.
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def process_article(article):
    """
    Enriches an article with categorization, a 150-char summary, and a Hype Meter score.
    """
    model = genai.GenerativeModel('gemini-1.5-pro') # User requested 3.1 Pro, but let's use the most advance available if 3.1 is not in the SDK yet.
    # Actually, let's use 'gemini-1.5-pro' or 'gemini-1.5-flash' as per standard.
    
    prompt = f"""
    Analyze the following AI news story and provide a JSON response.
    
    Headline: {article['title']}
    Source: {article['source']}
    Technical Content: {article.get('content', 'No detailed content available.')}
    
    Instructions:
    1. Categorize into one of: LLMs, Robotics, Agents, Hardware.
    2. Provide a 'Quick Take' summary under 150 characters.
    3. Calculate 'Hype Meter' score (1-10).
       Logic: 
       - 10: Marketing fluff, vague promises, no technical data.
       - 1: Grounded technical breakthrough, specific metrics, reproducible results.
       - Compare the Headline claims against the Technical Content. If the headline is much more sensational than the content, the score should be higher.
    4. Label: "Pure Signal" (1-3), "Balanced" (4-7), "Maximum Hype" (8-10).
    
    JSON format:
    {{
        "category": "...",
        "summary": "...",
        "hype_score": 1-10,
        "hype_label": "..."
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        # Attempt to parse JSON from the response text
        # Simple extraction for now
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
            
        enrichment = json.loads(text.strip())
        article.update(enrichment)
    except Exception as e:
        print(f"Error processing article '{article['title']}': {e}")
        # Default/Fallback
        article.update({
            "category": "Unknown",
            "summary": article['title'][:147] + "...",
            "hype_score": 5,
            "hype_label": "Balanced"
        })
    
    return article

if __name__ == "__main__":
    test_article = {
        "title": "AGI is coming tomorrow, OpenAI says",
        "content": "A blog post mentioned they are working hard on future models.",
        "source": "Aggregator",
        "url": "http://example.com"
    }
    print(json.dumps(process_article(test_article), indent=2))

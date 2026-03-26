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
    model = genai.GenerativeModel('gemini-2.0-flash-lite')
    
    prompt = f"""
    Analyze the following AI news story and provide a JSON response.
    
    Headline: {article['title']}
    Source: {article['source']}
    Technical Content: {article.get('content', 'No detailed content available.')}
    
    Instructions:
    1. Categorize into EXACTLY one of: LLMs, Robotics, Agents, Hardware.
    2. Provide a 'Quick Take' summary under 150 characters.
    3. Calculate 'Hype Meter' score (1-10).
    4. Label: "Pure Signal" (1-3), "Balanced" (4-7), "Maximum Hype" (8-10).
    
    Return ONLY a valid JSON object.
    
    JSON format:
    {{
        "category": "One of [LLMs, Robotics, Agents, Hardware]",
        "summary": "...",
        "hype_score": 1-10,
        "hype_label": "..."
    }}
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text
        
        # More robust JSON extraction
        import re
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            enrichment = json.loads(json_str)
            
            # Ensure category is one of the valid ones
            valid_categories = ["LLMs", "Robotics", "Agents", "Hardware"]
            if enrichment.get("category") not in valid_categories:
                enrichment["category"] = "LLMs" 
                
            article.update(enrichment)
        else:
            raise ValueError("No JSON found in response")
            
    except Exception as e:
        print(f"❌ Error processing article '{article['title']}': {e}")
        # Default/Fallback
        article.update({
            "category": "LLMs",
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

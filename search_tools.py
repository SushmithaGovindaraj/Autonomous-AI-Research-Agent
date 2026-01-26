from duckduckgo_search import DDGS
import wikipediaapi
import time

def search_wikipedia(query: str):
    """Fallback to Wikipedia for reliable factual data."""
    wiki = wikipediaapi.Wikipedia('ResearchAgent/1.0', 'en')
    
    # Extract key terms for Wikipedia search
    search_terms = query.replace("Search and extract", "").replace("comprehensive data for:", "").strip()
    
    # Try to find relevant Wikipedia pages
    results = []
    keywords = ["electric vehicle", "EV battery", "battery market", "lithium-ion battery"]
    
    for keyword in keywords:
        page = wiki.page(keyword)
        if page.exists():
            # Get summary and key sections
            summary = page.summary[:1000]
            results.append(f"Title: {page.title}\nContent: {summary}\nSource: {page.fullurl}\n")
    
    return "\n---\n".join(results) if results else ""

def search_query(query: str, max_retries=2):
    """Hybrid search: Try DuckDuckGo first, fallback to Wikipedia if it fails."""
    results_text = []
    
    # Enhanced query for better results
    enhanced_query = query
    if any(kw in query.lower() for kw in ["ev", "battery", "market", "electric"]):
        enhanced_query = f"{query} market size statistics 2024 billion"
    
    # Try DuckDuckGo first
    for attempt in range(max_retries):
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(enhanced_query, max_results=15))
                
                if results:
                    # Filter out help pages
                    skip_keywords = ['support.google', 'help.', 'tutorial', 'faq', 'search console']
                    filtered_results = []
                    
                    for r in results:
                        if not any(skip in r['href'].lower() or skip in r['title'].lower() for skip in skip_keywords):
                            if any(kw in r['body'].lower() for kw in ['billion', 'market', 'growth', 'data', 'report']):
                                filtered_results.append(r)
                    
                    if filtered_results:
                        for r in filtered_results[:8]:
                            results_text.append(f"Title: {r['title']}\nSnippet: {r['body']}\nSource: {r['href']}\n")
                        print(f"✓ DuckDuckGo search successful: {len(filtered_results)} relevant results")
                        break
            
            if not results_text:
                time.sleep(2)
        except Exception as e:
            print(f"⚠️ DuckDuckGo attempt {attempt + 1} failed: {str(e)}")
            time.sleep(3)
    
    # If DuckDuckGo failed, use Wikipedia as backup
    if not results_text:
        print("⚠️ DuckDuckGo failed. Trying Wikipedia...")
        wiki_results = search_wikipedia(query)
        if wiki_results:
            print("✓ Wikipedia search successful")
            return wiki_results
        else:
            print("⚠️ Both DuckDuckGo and Wikipedia failed")
            return ""
    
    return "\n---\n".join(results_text)

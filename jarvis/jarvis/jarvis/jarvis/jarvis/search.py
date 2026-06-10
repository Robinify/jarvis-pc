"""
Web Search Integration
"""

import logging
import requests
from typing import Dict, List, Optional
from urllib.parse import quote

logger = logging.getLogger(__name__)


class WebSearch:
    """Web search functionality using DuckDuckGo"""
    
    def __init__(self, config: Dict):
        """Initialize web search"""
        self.enabled = config.get("enabled", True)
        self.engine = config.get("engine", "duckduckgo")
        self.max_results = config.get("max_results", 5)
        self.timeout = 10
        
        logger.info(f"Web search initialized with engine: {self.engine}")
    
    def search(self, query: str) -> List[Dict]:
        """Search the web using DuckDuckGo"""
        if not self.enabled:
            return []
        
        try:
            # Use DuckDuckGo API (no key required)
            url = "https://api.duckduckgo.com/"
            params = {
                "q": query,
                "format": "json",
                "no_html": 1
            }
            
            logger.info(f"Searching for: {query}")
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract results from AbstractResults and RelatedTopics
            results = []
            
            # Add abstract result if available
            if data.get("AbstractText"):
                results.append({
                    "title": data.get("Heading", "Search Result"),
                    "snippet": data.get("AbstractText"),
                    "link": data.get("AbstractURL", "")
                })
            
            # Add related topics
            for topic in data.get("RelatedTopics", [])[:self.max_results]:
                if "Result" in topic:
                    results.append({
                        "title": topic.get("Text", "Result"),
                        "snippet": topic.get("Result", ""),
                        "link": topic.get("FirstURL", "")
                    })
            
            logger.debug(f"Found {len(results)} results")
            return results[:self.max_results]
        
        except requests.RequestException as e:
            logger.error(f"Search request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error in search: {e}")
            return []
    
    def format_results(self, results: List[Dict]) -> str:
        """Format search results as readable text"""
        if not results:
            return "No results found."
        
        formatted = "Search Results:\n\n"
        for i, result in enumerate(results[:5], 1):
            formatted += f"{i}. {result.get('title', 'No title')}\n"
            formatted += f"   {result.get('snippet', 'No description')}\n"
            if result.get('link'):
                formatted += f"   Link: {result.get('link')}\n"
            formatted += "\n"
        
        return formatted

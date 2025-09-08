# Simplified semantic search for UI integration
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_Handler import DbHandler

def semantic_search_listings(query: str, limit: int = 20):
    """
    Simple semantic search function for UI integration
    Args:
        query: User search query
        limit: Maximum number of results
    Returns:
        List of matching listings
    """
    try:
        if not query.strip():
            return []
            
        db = DbHandler()
        similar_listing_ids = db.query_try(query, limit)
        
        if similar_listing_ids:
            return db.get_listings(ids=similar_listing_ids)
        else:
            return []
            
    except Exception as e:
        print(f"Semantic search error: {e}")
        return []
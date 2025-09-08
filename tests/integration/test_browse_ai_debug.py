"""
Debug test for browse AI database access
"""
from ui.browse_ai import generate_ai_response
from db_Handler import DbHandler

def test_browse_ai_debug():
    print("=== Testing Browse AI Database Access ===")
    
    # Check database listings first
    db = DbHandler()
    listings = db.get_listings()
    print(f"Database has {len(listings)} listings")
    
    if listings:
        print("Sample listing:")
        print(f"- {listings[0].get('title', 'No title')}: ${listings[0].get('price', 0)}")
    
    # Test vector search directly
    print("\n=== Testing Vector Search ====")
    test_query = "electronics"
    top_k_ids = db.query_try(test_query, 10)
    print(f"Vector search returned {len(top_k_ids) if top_k_ids else 0} IDs: {top_k_ids}")
    
    if top_k_ids:
        filtered_listings = db.get_listings(top_k_ids)
        print(f"Filtered listings: {len(filtered_listings)}")
        for item in filtered_listings[:3]:
            print(f"- {item.get('title', 'No title')}: {item.get('category', 'No category')}")
    
    # Test AI response
    print("\n=== Testing AI Response ===")
    test_query = "I'm looking for electronics"
    response = generate_ai_response(test_query)
    print(f"User query: {test_query}")
    print(f"AI response: {response}")

if __name__ == "__main__":
    test_browse_ai_debug()
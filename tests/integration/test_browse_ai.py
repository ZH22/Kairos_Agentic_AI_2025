"""
Test script to check if browse AI has access to database listings
"""
from ui.browse_ai import generate_ai_response
from db_Handler import DbHandler

def test_browse_ai_db_access():
    print("=== Testing Browse AI Database Access ===")
    

    
    # Test AI response
    print("\n=== Testing AI Response ===")
    test_query = "I'm looking for electronics"
    response = generate_ai_response(test_query)
    print(f"User query: {test_query}")
    print(f"AI response: {response}")

if __name__ == "__main__":
    test_browse_ai_db_access()
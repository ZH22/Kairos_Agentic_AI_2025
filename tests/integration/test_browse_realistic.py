"""
Test browse AI with realistic query
"""
from Buyer_Workflow.browse_ai import generate_ai_response

def test_realistic_query():
    print("=== Testing Browse AI with Realistic Query ===")
    
    # Test with a realistic query
    test_query = "looking for textbooks"
    print(f"Test query: {test_query}")
    print("\n" + "-"*50 + "\n")
    
    try:
        response = generate_ai_response(test_query)
        print("AI Response:")
        print(response)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_realistic_query()
"""
Test browse AI with no results scenario
"""
from Buyer_Workflow.browse_ai import generate_ai_response

def test_no_results():
    print("=== Testing Browse AI No Results Response ===")
    
    # Test with a query that should return no results
    test_query = "flying car spaceship rocket"
    print(f"Test query: {test_query}")
    print("\n" + "-"*50 + "\n")
    
    response = generate_ai_response(test_query)
    print("AI Response:")
    print(response)

if __name__ == "__main__":
    test_no_results()
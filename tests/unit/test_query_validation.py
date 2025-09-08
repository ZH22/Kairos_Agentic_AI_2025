"""
Test the new query validation system
"""
from Buyer_Workflow.search_agents import validate_query

def test_validation():
    print("=== Testing Query Validation System ===")
    
    # Test cases
    test_cases = [
        "I want a laptop",  # Should need more info
        "Looking for a MacBook Air M2, under $800, good condition, pickup at NUS",  # Should be sufficient
        "water bottle",  # Should need more info
        "Need a portable air conditioner, budget $200, used condition okay, NUS pickup"  # Should be sufficient
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Query: {query}")
        print("-" * 40)
        
        try:
            result = validate_query(query)
            print(f"Status: {result['status']}")
            
            if result['status'] == 'SUFFICIENT':
                print("Structured Query:")
                print(result['structured_query'])
            else:
                print("Clarification Request:")
                print(result['clarification_request'])
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_validation()
"""
Test the improved query validation system with fallback logic
"""
from Buyer_Workflow.search_agents import validate_query

def test_improved_validation():
    print("=== Testing Improved Query Validation System ===")
    
    # Test cases
    test_cases = [
        "laptop",  # Should trigger fallback for laptop category
        "I want a phone",  # Should trigger fallback for phone category
        "textbook",  # Should trigger fallback for textbook category
        "chair",  # Should trigger fallback for furniture category
        "something random",  # Should trigger default fallback
        "Looking for a MacBook Air M2, under $800, good condition, pickup at NUS",  # Should be sufficient
    ]
    
    for i, query in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Query: '{query}'")
        print("-" * 50)
        
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
    test_improved_validation()
"""
Simple test for buyer workflow without Unicode characters
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from Buyer_Workflow.search_agents import buyer_search_workflow

def test_aircon_search():
    user_preferences = """Portable Air Conditioner
I want an aircon that has good condition while not exceeding budget SGD200
Prefer brands like Midea or similar
Condition: Used is acceptable if well-maintained
University: NUS for easy pickup
Age: Less than 1 year preferred"""
    
    print("Starting Air Conditioner Search...")
    print(f"User Input:\n{user_preferences}")
    print("\n" + "-"*40 + "\n")
    
    try:
        recommendations = buyer_search_workflow(user_preferences)
        print("Search Results:")
        print(recommendations)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_aircon_search()
# Test script for buyer search workflow
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Buyer_Workflow.search_agents import buyer_search_workflow

def test_search_workflow():
    """Test the buyer search workflow with sample preferences"""
    
    # Test case 1: Specific item with budget constraint
    print("=== Test Case 1: Air Conditioner ===")
    test_aircon_search()
    
    print("\n" + "="*60 + "\n")
    
    # Test case 2: Laptop search
    print("=== Test Case 2: Laptop ===")
    test_laptop_search()

def test_aircon_search():
    
    # Sample user preferences in specified format
    user_preferences = """Portable Air Conditioner
I want an aircon that has good condition while not exceeding budget SGD200
Prefer brands like Midea or similar
Condition: Used is acceptable if well-maintained
University: NUS for easy pickup
Age: Less than 1 year preferred"""
    
    print("🔍 Starting Air Conditioner Search...")
    print(f"User Input:\n{user_preferences}")
    print("\n" + "-"*40 + "\n")
    
    try:
        recommendations = buyer_search_workflow(user_preferences)
        print("📋 Search Results:")
        print(recommendations)
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_laptop_search():
    """Test laptop search with broad preferences"""
    
    user_preferences = """Laptop
Looking for a good laptop under $800
Condition: Used or Like New is fine
Brand: Prefer Apple MacBook or high-end Windows laptops
University: NUS preferred for easy pickup
Usage: Programming, research, note-taking"""
    
    print("🔍 Starting Laptop Search...")
    print(f"User Input:\n{user_preferences}")
    print("\n" + "-"*40 + "\n")
    
    try:
        recommendations = buyer_search_workflow(user_preferences)
        print("📋 Search Results:")
        print(recommendations)
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_search_workflow()
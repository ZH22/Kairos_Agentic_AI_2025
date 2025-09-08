# Test script for 3-agent buyer search workflow
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Buyer_Workflow.search_agents import buyer_search_workflow

def test_workflow():
    """Test the 3-agent workflow with different user scenarios"""
    
    test_cases = [
        {
            "name": "Budget-Conscious Student",
            "query": """I'm a university student looking for a laptop for my computer science studies. 
            My budget is tight - around $600-700 maximum. I need something that can handle programming, 
            running IDEs, and some light gaming. Used condition is totally fine as long as it works well. 
            I'm at NUS so pickup from campus would be ideal."""
        },
        {
            "name": "Quick Air Conditioner Need",
            "query": """Air conditioner
            Need something for my dorm room ASAP since it's getting really hot
            Budget under $300
            Don't care about brand as long as it cools well
            Used is fine if it's in good working condition"""
        },
        {
            "name": "Specific Brand Preference",
            "query": """Looking for a MacBook for design work
            Prefer MacBook Pro but Air is okay too
            Budget up to $1200
            Condition should be Like New or excellent Used
            Need it for Adobe Creative Suite"""
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*60}")
        print(f"TEST CASE {i}: {test_case['name']}")
        print(f"{'='*60}")
        print(f"User Query:\n{test_case['query']}")
        print(f"\n{'-'*40}")
        print("AI Processing...")
        
        try:
            result = buyer_search_workflow(test_case['query'])
            print(f"\nAI Recommendations:\n{result}")
            
            # User evaluation prompts
            print(f"\n{'-'*40}")
            print("USER EVALUATION:")
            print("1. Did the AI understand what I was looking for?")
            print("2. Are the recommendations relevant to my needs?")
            print("3. Do the explanations make sense?")
            print("4. Would I click 'View Original' on any of these?")
            print("5. Overall satisfaction: ***** (rate 1-5 stars)")
            
        except Exception as e:
            print(f"Error: {str(e)}")
        
        print(f"\n{'='*60}\n")

if __name__ == "__main__":
    print("Testing 3-Agent Buyer Search Workflow")
    print("This test simulates different buyer scenarios and evaluates AI responses")
    test_workflow()
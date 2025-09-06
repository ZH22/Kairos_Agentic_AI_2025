"""
Test script for Deal Evaluation Workflow
"""
from deal_evaluation_workflow import deal_evaluation_workflow

# Test user info
test_user_info = {
    'title': 'Sony WH-1000XM4 Wireless Headphones',
    'brand': 'Sony',
    'category': 'Electronics',
    'condition': 'Like New',
    'age': 6,
    'original_price': 400.00,
    'price': 120.00,
    'reason': 'Upgraded to a new model',
    'price_negotiable': 'Yes'
}

def main():
    print("=== Testing Deal Evaluation Workflow ===")
    try:
        final_report = deal_evaluation_workflow(test_user_info)
        print("Workflow completed successfully!")
        print("\nFinal Report:")
        print(final_report)
    except Exception as e:
        print(f"Error in workflow: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
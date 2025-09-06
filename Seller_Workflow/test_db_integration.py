"""
Test script for database integration with Seller_Workflow
Tests the InternalDBSearchAgent functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_internal_db_tool():
    """Test internal_db_search tool functionality"""
    print("=== Testing internal_db_search Tool Integration ===")
    
    try:
        from market_agents import internal_db_search
        
        print("Testing internal_db_search tool...")
        result = internal_db_search(
            category="Tech and Gadgets",
            brand="Sony",
            price_range="100-150"
        )
        
        print("✅ internal_db_search tool executed successfully")
        print("\n--- Tool Results ---")
        print(result)
        
        return True
        
    except Exception as e:
        print(f"❌ internal_db_search tool test failed: {e}")
        return False

def test_workflow_integration():
    """Test full workflow with database integration"""
    print("\n=== Testing Full Workflow Integration ===")
    
    try:
        from deal_evaluation_workflow import deal_evaluation_workflow
        
        # Test user info
        test_user_info = {
            "title": "Sony Wireless Headphones",
            "brand": "Sony", 
            "category": "Tech and Gadgets",
            "condition": "Like New",
            "age": 6,
            "price": 120.0,
            "reason": "Upgraded to a new model",
            "price_negotiable": "Yes"
        }
        
        print("Running deal evaluation workflow...")
        result = deal_evaluation_workflow(test_user_info)
        
        print("✅ Workflow completed successfully")
        print("\n--- Workflow Results ---")
        print(result)
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow integration test failed: {e}")
        return False

def main():
    """Run integration tests"""
    print("🧪 Starting Seller_Workflow Database Integration Tests\n")
    
    # Test internal DB tool
    tool_success = test_internal_db_tool()
    
    # Test full workflow
    workflow_success = test_workflow_integration()
    
    if tool_success and workflow_success:
        print("\n🎉 All integration tests passed!")
    else:
        print("\n⚠️ Some tests failed - check output above")

if __name__ == "__main__":
    main()
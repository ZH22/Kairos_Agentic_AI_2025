#!/usr/bin/env python3
"""
Comprehensive AI Workflow Test Suite
Tests all AI-involved functions on the platform to ensure workflows work after updates
"""

import sys
import os
import traceback
from datetime import datetime

# Add paths for imports
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_seller_workflows():
    """Test all seller AI workflows"""
    print("🔧 TESTING SELLER WORKFLOWS")
    print("=" * 50)
    
    # Test 1: Description Writer
    try:
        from src.ai_workflows.seller.description_writer import Writer
        
        test_item = {
            'title': 'MacBook Pro 13-inch',
            'category': 'Tech and Gadgets',
            'condition': 'Like New',
            'price': 1200,
            'age': 6,
            'reason': 'Upgrading to newer model',
            'brand': 'Apple',
            'price_negotiable': 'Yes',
            'university': 'NUS',
            'address': 'Kent Ridge',
            'delivery_option': 'Pickup',
            'description': 'Barely used laptop'
        }
        
        writer = Writer()
        prompt = writer.fill_prompt(test_item, "Make it sound appealing for students")
        result = writer.write(prompt)
        
        assert len(result) > 50, "Description too short"
        print("✅ Description Writer: PASS")
        
    except Exception as e:
        print(f"❌ Description Writer: FAIL - {str(e)}")
    
    # Test 2: Market Agents
    try:
        from src.ai_workflows.seller.market_agents import WebsearchAgent, MarketAnalyzer
        
        test_info = """
Item: MacBook Pro 13-inch
Brand: Apple
Category: Tech and Gadgets
Condition: Like New
Age: 6 months
Asking Price: $1200.00 SGD
Reason for Selling: Upgrading
Price Negotiable: Yes
"""
        
        # Test WebsearchAgent
        web_agent = WebsearchAgent()
        web_result = web_agent.search(test_info)
        assert web_result is not None, "Web search returned None"
        
        # Test MarketAnalyzer
        analyzer = MarketAnalyzer()
        analysis_result = analyzer.analyze(str(web_result), test_info)
        assert analysis_result is not None, "Market analysis returned None"
        
        print("✅ Market Agents: PASS")
        
    except Exception as e:
        print(f"❌ Market Agents: FAIL - {str(e)}")
    
    # Test 3: Deal Evaluation Workflow
    try:
        from src.ai_workflows.seller.deal_evaluation_workflow import deal_evaluation_workflow
        
        test_user_info = {
            'title': 'iPhone 14',
            'brand': 'Apple',
            'category': 'Tech and Gadgets',
            'condition': 'Used',
            'age': 12,
            'price': 800,
            'reason': 'Switching to Android',
            'price_negotiable': 'No'
        }
        
        result = deal_evaluation_workflow(test_user_info)
        assert result is not None and len(str(result)) > 100, "Deal evaluation too short"
        print("✅ Deal Evaluation Workflow: PASS")
        
    except Exception as e:
        print(f"❌ Deal Evaluation Workflow: FAIL - {str(e)}")

def test_buyer_workflows():
    """Test all buyer AI workflows"""
    print("\n🛒 TESTING BUYER WORKFLOWS")
    print("=" * 50)
    
    # Test 1: Query Validation
    try:
        from src.ai_workflows.buyer.search_agents import validate_query
        
        # Test sufficient query
        sufficient_query = "Looking for MacBook Pro under $1000, used condition is fine, prefer 13-inch for programming"
        result = validate_query(sufficient_query)
        assert result['status'] in ['SUFFICIENT', 'NEEDS_MORE_INFO'], "Invalid validation status"
        
        # Test insufficient query
        insufficient_query = "laptop"
        result2 = validate_query(insufficient_query)
        assert result2['status'] == 'NEEDS_MORE_INFO', "Should need more info"
        
        print("✅ Query Validation: PASS")
        
    except Exception as e:
        print(f"❌ Query Validation: FAIL - {str(e)}")
    
    # Test 2: Buyer Search Workflow
    try:
        from src.ai_workflows.buyer.search_agents import buyer_search_workflow
        
        structured_query = """
**Item Title:** Laptop

**Preferences:**
- Budget under $800
- Used condition acceptable
- Prefer Apple MacBook or high-end Windows
- For programming and study
- NUS pickup preferred
"""
        
        result = buyer_search_workflow(structured_query)
        assert result is not None and len(str(result)) > 50, "Search result too short"
        print("✅ Buyer Search Workflow: PASS")
        
    except Exception as e:
        print(f"❌ Buyer Search Workflow: FAIL - {str(e)}")

def test_database_ai_functions():
    """Test AI functions that interact with database"""
    print("\n💾 TESTING DATABASE AI FUNCTIONS")
    print("=" * 50)
    
    # Test 1: Semantic Search
    try:
        from src.core.db_handler import DbHandler
        
        db = DbHandler()
        
        # Test semantic search
        results = db.query_try("laptop computer programming", 3)
        assert isinstance(results, list), "Query should return list"
        print("✅ Semantic Search: PASS")
        
    except Exception as e:
        print(f"❌ Semantic Search: FAIL - {str(e)}")
    
    # Test 2: Vector Store Operations
    try:
        # Test adding to vector store (if listings exist)
        listings = db.get_listings()
        if listings:
            test_listing = listings[0]
            db._add_to_vector_store(test_listing, test_listing.get('id'))
            print("✅ Vector Store Operations: PASS")
        else:
            print("⚠️ Vector Store Operations: SKIP - No listings to test")
            
    except Exception as e:
        print(f"❌ Vector Store Operations: FAIL - {str(e)}")

def test_ui_ai_integrations():
    """Test AI integrations in UI components"""
    print("\n🖥️ TESTING UI AI INTEGRATIONS")
    print("=" * 50)
    
    # Test 1: Browse AI (if exists)
    try:
        # Check if browse AI exists in UI
        if os.path.exists("ui/browse_ai.py"):
            from ui.browse_ai import generate_ai_response
            
            test_query = "I'm looking for electronics under $500"
            response = generate_ai_response(test_query)
            assert response is not None and len(response) > 20, "AI response too short"
            print("✅ Browse AI Integration: PASS")
        else:
            print("⚠️ Browse AI Integration: SKIP - File not found")
            
    except Exception as e:
        print(f"❌ Browse AI Integration: FAIL - {str(e)}")

def run_comprehensive_test():
    """Run all AI workflow tests"""
    print("🤖 KAIROS AI WORKFLOW COMPREHENSIVE TEST")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        test_seller_workflows()
        test_buyer_workflows() 
        test_database_ai_functions()
        test_ui_ai_integrations()
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS COMPLETED")
        print("=" * 60)
        print("✅ = Test passed")
        print("❌ = Test failed (check error messages)")
        print("⚠️ = Test skipped (missing components)")
        print("\nIf any tests failed, check the error messages above.")
        print("Run this script after major updates to verify AI workflows.")
        
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {str(e)}")
        print(traceback.format_exc())

if __name__ == "__main__":
    run_comprehensive_test()
"""
Test script for db_Handler.py
Tests database connections, user operations, listing operations, and vector search
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db_Handler import DbHandler

def test_initialization():
    """Test DbHandler initialization and connections"""
    print("=== Testing DbHandler Initialization ===")
    try:
        db = DbHandler()
        print("✅ DbHandler initialized successfully")
        
        # Test if clients are properly initialized
        assert db.llm_client is not None, "AWS Bedrock client not initialized"
        assert db.vec_client is not None, "Vector client not initialized" 
        assert db.db_client is not None, "Supabase client not initialized"
        print("✅ All database clients initialized")
        return db
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        return None

def test_user_operations(db):
    """Test user-related operations"""
    print("\n=== Testing User Operations ===")
    try:
        # Test get_users
        users = db.get_users()
        print(f"✅ Retrieved {len(users)} users")
        
        if users:
            # Test user ID/username conversion
            first_user = users[0]
            username = first_user['username']
            user_id = first_user['id']
            
            # Test get_userid_from_username
            retrieved_id = db.get_userid_from_username(username)
            assert retrieved_id == user_id, f"User ID mismatch: {retrieved_id} != {user_id}"
            print(f"✅ get_userid_from_username works for '{username}'")
            
            # Test get_username_from_id
            retrieved_username = db.get_username_from_id(user_id)
            assert retrieved_username == username, f"Username mismatch: {retrieved_username} != {username}"
            print(f"✅ get_username_from_id works for ID {user_id}")
        else:
            print("⚠️ No users found in database")
            
    except Exception as e:
        print(f"❌ User operations failed: {e}")

def test_listings_operations(db):
    """Test listing-related operations"""
    print("\n=== Testing Listings Operations ===")
    try:
        # Test get_listings
        listings = db.get_listings()
        print(f"✅ Retrieved {len(listings)} listings")
        
        if listings:
            # Verify listing structure
            first_listing = listings[0]
            required_fields = ['user', 'title', 'price', 'category', 'condition', 'date_posted']
            
            for field in required_fields:
                assert field in first_listing, f"Missing field: {field}"
            print("✅ Listing structure validation passed")
            
            # Check data formatting
            assert isinstance(first_listing['price'], (int, float)), "Price should be numeric"
            assert first_listing['price_negotiable'] in ['Yes', 'No'], "price_negotiable should be Yes/No"
            print("✅ Listing data formatting validation passed")
        else:
            print("⚠️ No listings found in database")
            
    except Exception as e:
        print(f"❌ Listings operations failed: {e}")

def test_vector_search(db):
    """Test vector search functionality"""
    print("\n=== Testing Vector Search ===")
    try:
        # Test query_try with a sample query
        test_query = "electronics laptop computer"
        limit = 3
        
        print(f"Searching for: '{test_query}' (limit: {limit})")
        results = db.query_try(test_query, limit)
        
        print(f"✅ Vector search completed, returned {len(results) if results else 0} results")
        
        if results:
            print("✅ Vector search functionality working")
            # Show sample results
            for i, result in enumerate(results[:2]):
                metadata = result.get('metadata', {})
                print(f"  Result {i+1}: {metadata.get('title', 'No title')} (similarity: {1-result.get('distance', 1):.3f})")
        else:
            print("⚠️ No results returned - vector store may be empty")
            print("  Run 'python populate_vector_store.py' to populate with existing listings")
            
    except Exception as e:
        print(f"❌ Vector search failed: {e}")

def test_vector_store_population(db):
    """Test vector store population functionality"""
    print("\n=== Testing Vector Store Population ===")
    try:
        # Test the population function
        print("Testing vector store population...")
        success = db.populate_vector_store_from_existing()
        
        if success:
            print("✅ Vector store population function works")
        else:
            print("❌ Vector store population failed")
            
    except Exception as e:
        print(f"❌ Vector store population test failed: {e}")

def test_delete_operations(db):
    """Test delete functionality with safety checks"""
    print("\n=== Testing Delete Operations ===")
    try:
        # Get current listings
        listings = db.get_listings()
        
        if not listings:
            print("⚠️ No listings available to test deletion")
            return
            
        # Test with invalid listing ID
        result = db.delete_listing_by_id(99999, "testuser")
        assert result == False, "Should fail for non-existent listing"
        print("✅ Invalid listing ID rejection works")
        
        # Test with valid listing but wrong user
        first_listing = listings[0]
        listing_id = first_listing.get('id')
        if listing_id:
            result = db.delete_listing_by_id(listing_id, "wronguser")
            assert result == False, "Should fail for unauthorized user"
            print("✅ Ownership validation works")
        
        print("✅ Delete operation safety checks passed")
        print("⚠️ Actual deletion not tested to preserve data")
        
    except Exception as e:
        print(f"❌ Delete operations test failed: {e}")

def test_environment_variables():
    """Test if required environment variables are set"""
    print("\n=== Testing Environment Variables ===")
    required_vars = [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY", 
        "AWS_REGION",
        "DB_CONNECTION",
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "EMBED_MODEL_SMALL"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def main():
    """Run all tests"""
    print("🧪 Starting db_Handler Tests\n")
    
    # Load environment variables
    load_dotenv()
    
    # Test environment variables first
    if not test_environment_variables():
        print("\n❌ Cannot proceed without required environment variables")
        return
    
    # Test initialization
    db = test_initialization()
    if not db:
        print("\n❌ Cannot proceed without successful initialization")
        return
    
    # Run all tests
    test_user_operations(db)
    test_listings_operations(db)
    test_vector_search(db)
    test_delete_operations(db)
    test_vector_store_population(db)
    
    print("\n🎉 All tests completed!")

if __name__ == "__main__":
    main()
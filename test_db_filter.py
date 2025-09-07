"""
Test database filtering by IDs
"""
from db_Handler import DbHandler

def test_db_filter():
    db = DbHandler()
    
    # Test vector search
    test_query = "electronics"
    top_k_ids = db.query_try(test_query, 10)
    print(f"Vector search returned: {top_k_ids}")
    print(f"Type of IDs: {type(top_k_ids[0]) if top_k_ids else 'None'}")
    
    # Test direct database query with these IDs
    try:
        res = (db.db_client.table("listing").select("id, title, category")
               .in_("id", top_k_ids)
               .execute())
        print(f"Direct query returned {len(res.data)} results:")
        for item in res.data[:3]:
            print(f"- ID {item['id']}: {item['title']} ({item['category']})")
    except Exception as e:
        print(f"Direct query error: {e}")
    
    # Test get_listings method
    filtered_listings = db.get_listings(top_k_ids)
    print(f"get_listings returned {len(filtered_listings)} results")

if __name__ == "__main__":
    test_db_filter()
"""
Sync vector store with current database listings
"""
from db_Handler import DbHandler
import json
import os

def sync_vector_store():
    """Rebuild vector store from current database listings"""
    print("=== Syncing Vector Store with Database ===")
    
    db = DbHandler()
    
    # Get all current listings from database
    all_listings = db.get_listings()
    print(f"Found {len(all_listings)} listings in database")
    
    # Clear existing vector store
    try:
        docs = db.vec_client.get_collection(name="listing")
        # Delete all existing vectors
        print("Clearing existing vector store...")
    except:
        print("Creating new vector collection...")
    
    # Recreate collection
    docs = db.vec_client.get_or_create_collection(name="listing", dimension=1536)
    
    # Add each listing to vector store
    success_count = 0
    for listing in all_listings:
        try:
            listing_id = listing.get('id')
            
            # Create searchable text
            searchable_text = f'''
              Title: {listing.get('title', '')} 
              Listing Description: {listing.get('description', '')} 
              Brand: {listing.get('brand', '')} 
              Condition: {listing.get('condition', '')}
              Category: {listing.get('category', '')}
              Reason for sale: {listing.get('reason', '')}
              age (in months): {listing.get('age', '')}
              price is negotiable: {listing.get('price_negotiable', '')}
              '''.strip()
            
            # Generate embedding
            response = db.llm_client.invoke_model(
                body=json.dumps({"inputText": searchable_text}),
                modelId=os.getenv("EMBED_MODEL_SMALL"),
                accept="application/json",
                contentType="application/json"
            )
            
            response_body = json.loads(response["body"].read())
            embedding = response_body.get("embedding")
            
            if embedding:
                # Add to vector store
                record = [(str(listing_id), embedding, {})]
                docs.upsert(record)
                success_count += 1
                print(f"Added listing {listing_id}: {listing.get('title', 'No title')}")
            
        except Exception as e:
            print(f"Failed to add listing {listing_id}: {e}")
    
    print(f"\n=== Sync Complete ===")
    print(f"Successfully added {success_count}/{len(all_listings)} listings to vector store")
    
    # Test the sync
    print("\n=== Testing Sync ===")
    test_queries = ["laptop computer", "air conditioner aircon"]
    
    for query in test_queries:
        ids = db.query_try(query, 5)
        if ids:
            listings = db.get_listings(ids)
            print(f"Query '{query}' found {len(listings)} results:")
            for listing in listings[:3]:
                print(f"  - {listing.get('title')} (ID: {listing.get('id')})")
        else:
            print(f"Query '{query}' found no results")

if __name__ == "__main__":
    sync_vector_store()
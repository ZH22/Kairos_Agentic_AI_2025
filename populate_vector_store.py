#!/usr/bin/env python3
"""
Populate Vector Store Script
One-time setup to populate vector store with existing listings
"""

from db_Handler import DbHandler

def main():
    """Populate vector store with existing listings"""
    print("Populating vector store...")
    
    db = DbHandler()
    
    # Get all listings
    listings = db.get_listings()
    print(f"Found {len(listings)} listings to process")
    
    # Add each to vector store
    for listing in listings:
        if listing.get('id'):
            try:
                db._add_to_vector_store(listing, listing['id'])
                print(f"Added listing {listing['id']}: {listing.get('title', 'Unknown')}")
            except Exception as e:
                print(f"Error adding listing {listing['id']}: {e}")
    
    print("Vector store population complete!")

if __name__ == "__main__":
    main()
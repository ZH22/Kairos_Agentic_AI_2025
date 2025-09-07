"""
Debug test for buyer workflow semantic search
"""
from db_Handler import DbHandler

def test_buyer_debug():
    print("=== Testing Buyer Workflow Database Access ===")
    
    db = DbHandler()
    
    # Check total listings
    all_listings = db.get_listings()
    print(f"Total listings in database: {len(all_listings)}")
    
    # Check for aircon/computer listings
    aircon_count = 0
    computer_count = 0
    for listing in all_listings:
        title = listing.get('title', '').lower()
        category = listing.get('category', '').lower()
        if 'aircon' in title or 'air conditioner' in title or 'air conditioning' in title:
            aircon_count += 1
            print(f"Found aircon: {listing.get('title')} (ID: {listing.get('id')})")
        if 'laptop' in title or 'computer' in title or 'macbook' in title:
            computer_count += 1
            print(f"Found computer: {listing.get('title')} (ID: {listing.get('id')})")
    
    print(f"\nAircon listings found: {aircon_count}")
    print(f"Computer listings found: {computer_count}")
    
    # Test vector search for aircon
    print("\n=== Testing Vector Search for Aircon ===")
    aircon_query = "portable air conditioner aircon cooling"
    aircon_ids = db.query_try(aircon_query, 10)
    print(f"Vector search returned {len(aircon_ids) if aircon_ids else 0} IDs: {aircon_ids}")
    
    if aircon_ids:
        aircon_listings = db.get_listings(aircon_ids)
        print(f"Actual listings retrieved: {len(aircon_listings)}")
        for listing in aircon_listings[:3]:
            print(f"- {listing.get('title')} (ID: {listing.get('id')})")
    
    # Test vector search for laptop
    print("\n=== Testing Vector Search for Laptop ===")
    laptop_query = "laptop computer macbook programming"
    laptop_ids = db.query_try(laptop_query, 10)
    print(f"Vector search returned {len(laptop_ids) if laptop_ids else 0} IDs: {laptop_ids}")
    
    if laptop_ids:
        laptop_listings = db.get_listings(laptop_ids)
        print(f"Actual listings retrieved: {len(laptop_listings)}")
        for listing in laptop_listings[:3]:
            print(f"- {listing.get('title')} (ID: {listing.get('id')})")

if __name__ == "__main__":
    test_buyer_debug()
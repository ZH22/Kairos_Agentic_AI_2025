"""
One-time script to populate vector store with existing listings
Run this to enable semantic search for existing data
"""

from db_Handler import DbHandler
from dotenv import load_dotenv

def main():
    print("🚀 Starting Vector Store Population...")
    
    # Load environment variables
    load_dotenv()
    
    # Initialize database handler
    db = DbHandler()
    
    # Populate vector store with existing listings
    success = db.populate_vector_store_from_existing()
    
    if success:
        print("✅ Vector store population completed successfully!")
        print("🔍 Semantic search is now enabled for all listings")
    else:
        print("❌ Vector store population failed - check logs above")

if __name__ == "__main__":
    main()
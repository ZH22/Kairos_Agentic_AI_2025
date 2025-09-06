#!/usr/bin/env python3
"""
Test script for Writer class performance on description generation.
"""

import os
from dotenv import load_dotenv
from description_writer import Writer

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

def test_writer_performance():
    """Test the Writer class with placeholder data."""
    
    # Placeholder user_info dict - to be filled later
    user_info = {
        'title': 'Portable Aircon',
        'category': 'Electronics',
        'condition': 'Used',
        'price': 100,
        'original_price': 200,
        'age': 12,
        'reason': 'Moving out of hostel, no longer needs it',
        'brand': 'Do not remember',
        'price_negotiable': 'Yes',
        'university': 'NUS',
        'address': 'PGP Blk8',
        'delivery_option': 'Buyer Pickup',
        'description': ""
    }
    
    # Placeholder user_prompt - to be filled later
    user_prompt = "Generate a compelling description for this item listing."
    
    # Initialize Writer
    writer = Writer()
    
    # Test description generation
    print("Testing Writer performance...")
    print("=" * 50)
    
    try:
        # Fill prompt with user data
        complete_prompt = writer.fill_prompt(user_info, user_prompt)
        print("Complete prompt generated successfully")
        
        # Generate description
        description = writer.write(complete_prompt)
        print("\nGenerated Description:")
        print("-" * 30)
        print(description)
        print("-" * 30)
        
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {e}")

if __name__ == "__main__":
    test_writer_performance()
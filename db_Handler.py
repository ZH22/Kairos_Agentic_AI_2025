import boto3
import vecs
import json
from dotenv import load_dotenv
import os
import supabase
import streamlit as st
from helper_scripts.image_helper import image_to_base64
from datetime import datetime
import base64

@st.cache_resource
class DbHandler:
  def __init__(self):
    # Load Environment variables for use
    load_dotenv()

    # Initialise Amazon Bedrock Client 
    self.llm_client = boto3.client(
      'bedrock-runtime',
      region_name = os.getenv("AWS_REGION"),
      aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
      aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    )

    # Initialise Supabase Vector Store Client
    self.vec_client = vecs.Client(os.getenv("DB_CONNECTION"))

    # Initialise Supabase Main Database Client
    self.db_client = supabase.create_client(
      os.getenv("SUPABASE_URL"), 
      os.getenv("SUPABASE_KEY")
    )

  def save_listing_to_db(self, listing_object):
    # Create a copy for use
    data = listing_object.copy()

    # Get user id
    username = listing_object["user"]
    userid = self.get_userid_from_username(username)

    # Change image to base64 
    image = listing_object["image"]
    if image is not None:
        b64_img = image_to_base64(image).decode('utf-8')
    else:
        b64_img = None

    # Change boolean values
    data['price_negotiable'] = data['price_negotiable'] == 'Yes'

    # Change Enum Values (format by lowercased, underscore seperated)
    data['university'] = data['university'].lower().replace(" ", "_")
    data['category'] = data['category'].lower().replace(" ", "_")
    data['condition'] = data['condition'].lower().replace(" ", "_")
    data['delivery_option'] = data['delivery_option'].lower().replace(" ", "_")


    # Remove image, date_posted, user fields
    del data['image']
    del data['date_posted']
    data['user'] = userid
    data['image_base64'] = b64_img 

    # Save to main database
    response = (self.db_client.table("listing")
                .insert(data)
                .execute())
    
    # Add to vector store for semantic search
    if response.data:
        listing_id = response.data[0]['id']
        self._add_to_vector_store(listing_object, listing_id)

  def get_userid_from_username(self, username):
    resp = self.db_client.table("user_profile").select("id").eq("username", username).execute()

    if resp.data:
        user_id = resp.data[0]["id"]
        print(f"User ID for {username}: {user_id}")
        return user_id
    else:
        print(f"User with username '{username}' not found.")
    
  def get_username_from_id(self, user_id):
    res = self.db_client.table("user_profile").select("username").eq("id", user_id).execute()
    return res.data[0]["username"]

  def get_listings(self):
    res = (self.db_client.table("listing").select("*").execute())
    listings = res.data

    # Convert back to session state style
    for item in listings:
      item['user'] = self.get_username_from_id(item['user']).title()
      item['date_posted'] = datetime.fromisoformat(item['created_at']).strftime("%d %B %Y, %H:%M")
      del item['created_at']
      item['price_negotiable'] = "Yes" if item['price_negotiable'] else "No"
      item['university'] = item['university'].title()
      item['delivery_option'] = item['delivery_option'].replace('_', ' ').title()
      if item['image_base64']:
          item['image'] = base64.b64decode(item['image_base64'])
      else:
          item['image'] = None
      del item['image_base64']

    return listings

  def delete_listing_by_id(self, listing_id, current_user):
    """Delete a listing from database by ID with ownership validation"""
    try:
        # First verify ownership
        listing_check = (self.db_client.table("listing")
                        .select("user")
                        .eq("id", listing_id)
                        .execute())
        
        if not listing_check.data:
            print(f"Listing {listing_id} not found")
            return False
            
        # Get listing owner's user ID
        listing_owner_id = listing_check.data[0]["user"]
        current_user_id = self.get_userid_from_username(current_user)
        
        # Verify ownership
        if listing_owner_id != current_user_id:
            print(f"User {current_user} not authorized to delete listing {listing_id}")
            return False
            
        # Delete the listing
        response = (self.db_client.table("listing")
                   .delete()
                   .eq("id", listing_id)
                   .execute())
        
        # Also remove from vector store
        self._remove_from_vector_store(listing_id)
        
        print(f"Listing {listing_id} deleted successfully")
        return True
        
    except Exception as e:
        print(f"Error deleting listing {listing_id}: {e}")
        return False
  
  def _add_to_vector_store(self, listing_object, listing_id):
    """Add listing to vector store for semantic search"""
    try:
        # Create searchable text from listing
        searchable_text = f"{listing_object.get('title', '')} {listing_object.get('description', '')} {listing_object.get('brand', '')} {listing_object.get('category', '')}".strip()
        
        if not searchable_text:
            print(f"No searchable text for listing {listing_id}")
            return
        
        # Generate embedding
        response = self.llm_client.invoke_model(
            body=json.dumps({"inputText": searchable_text}),
            modelId=os.getenv("EMBED_MODEL_SMALL"),
            accept="application/json",
            contentType="application/json"
        )
        
        response_body = json.loads(response["body"].read())
        embedding = response_body.get("embedding")
        
        if embedding:
            # Add to vector collection
            sentencesDB = self.vec_client.get_or_create_collection(name="sentences", dimension=1536)
            sentencesDB.upsert(
                records=[
                    {
                        "id": f"listing_{listing_id}",
                        "vec": embedding,
                        "metadata": {
                            "listing_id": listing_id,
                            "text": searchable_text,
                            "title": listing_object.get('title', ''),
                            "category": listing_object.get('category', ''),
                            "price": listing_object.get('price', 0)
                        }
                    }
                ]
            )
            print(f"Added listing {listing_id} to vector store")
        
    except Exception as e:
        print(f"Error adding listing {listing_id} to vector store: {e}")
  
  def _remove_from_vector_store(self, listing_id):
    """Remove listing from vector store"""
    try:
        sentencesDB = self.vec_client.get_or_create_collection(name="sentences", dimension=1536)
        sentencesDB.delete(ids=[f"listing_{listing_id}"])
        print(f"Removed listing {listing_id} from vector store")
    except Exception as e:
        print(f"Error removing listing {listing_id} from vector store: {e}")
  
  # *****************************
  # Returns an array of the top k similar sentences to query 
  # *****************************
  def get_users(self):
    response = (self.db_client.table("user_profile")
                .select("id, username")
                .execute()
                .model_dump_json())
    
    data = json.loads(response)["data"] 
    return data

  # *****************************
  # Returns an array of the top k similar sentences to query 
  # *****************************
  def query_try(self, query_sentence, limit_num):
    # Generate Embeddings for input query string
    print("Generating Input Query Embedding...")
    response = self.llm_client.invoke_model(
        body= json.dumps({"inputText": query_sentence}),
        modelId= os.getenv("EMBED_MODEL_SMALL"),
        accept = "application/json",
        contentType = "application/json"
    )

    response_body = json.loads(response["body"].read())
    query_embedding = response_body.get("embedding")
    print("Query Embedding: SUCCESS")

    print("Querying Vector Store for k nearest...")
    # Query Vector store for Top k Similar Items
    sentencesDB = self.vec_client.get_or_create_collection(name="sentences", dimension=1536)
    results = sentencesDB.query(
      data=query_embedding,
      limit=limit_num,
      include_value = True
    )
    print("Queried Results! Returning as array")

    return results
  
  def populate_vector_store_from_existing(self):
    """Populate vector store with existing listings (one-time setup)"""
    try:
        # Get all existing listings
        response = self.db_client.table("listing").select("*").execute()
        listings = response.data
        
        print(f"Populating vector store with {len(listings)} existing listings...")
        
        for listing in listings:
            # Convert back to original format for processing
            listing_object = {
                'title': listing.get('title', ''),
                'description': listing.get('description', ''),
                'brand': listing.get('brand', ''),
                'category': listing.get('category', '').replace('_', ' ').title(),
                'price': listing.get('price', 0)
            }
            
            # Add to vector store
            self._add_to_vector_store(listing_object, listing['id'])
        
        print(f"Vector store population completed!")
        return True
        
    except Exception as e:
        print(f"Error populating vector store: {e}")
        return False
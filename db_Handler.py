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
    b64_img = image_to_base64(image).decode('utf-8')

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

    # Modify to image_base64, user -> userid
    response = (self.db_client.table("listing")
                .insert(data)
                .execute())

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
      item['image'] = base64.b64decode(item['image_base64'])
      del item['image_base64']

    return listings
  
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
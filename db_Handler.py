import boto3
import vecs
import json
from dotenv import load_dotenv
import os


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


if __name__ == "__main__":
  db = DbHandler()

  res = db.query_try("money", 10)
  for r in res:
    print(r)
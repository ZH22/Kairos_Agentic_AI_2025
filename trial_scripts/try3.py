import boto3
import vecs
import json
from dotenv import load_dotenv
import os

# Load Environment variables
print("loading Environment variables")
load_dotenv()

client = boto3.client(
  'bedrock-runtime',
  region_name = os.getenv("AWS_REGION"),
  aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID"),
  aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
)

query_sentence = "Plants"


# create vector store client
vx = vecs.Client(os.getenv("DB_CONNECTION"))
# create an embedding for the query sentence
response = client.invoke_model(
        body= json.dumps({"inputText": query_sentence}),
        modelId= "amazon.titan-embed-text-v1",
        accept = "application/json",
        contentType = "application/json"
    )
response_body = json.loads(response["body"].read())
query_embedding = response_body.get("embedding")
# query the 'sentences' collection for the most similar sentences

sentences = vx.get_or_create_collection(name="sentences", dimension=1536)

results = sentences.query(
    data=query_embedding,
    limit=3,
    include_value = True
)
# print the results
for result in results:
    print(result)
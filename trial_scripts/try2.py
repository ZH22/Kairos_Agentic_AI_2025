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

dataset = [
  "All roads lead to Rome.",
    "Time flies when you're having fun.",
    "Silence is golden.",
    "Practice makes perfect.",
    "Knowledge is power.",
    "Honesty is the best policy.",
    "Fortune favors the bold.",
    "Curiosity killed the cat.",
    "Beggars can't be choosers.",
    "Birds of a feather flock together.",
    "The early bird catches the worm.",
    "Look before you leap.",
    "A picture is worth a thousand words.",
    "No pain, no gain.",
    "When in Rome, do as the Romans do.",
    "Necessity is the mother of invention.",
    "You can't judge a book by its cover.",
    "The squeaky wheel gets the grease.",
    "Strike while the iron is hot.",
    "Money doesn't grow on trees.",
    "Hope for the best, prepare for the worst.",
    "Too many cooks spoil the broth.",
    "Rome wasn't built in a day.",
    "A watched pot never boils.",
    "Every rose has its thorn.",
    "Lightning never strikes twice in the same place.",
    "The grass is always greener on the other side.",
    "Absence makes the heart grow fonder.",
    "Actions speak louder than words.",
    "Better safe than sorry."
]
embeddings = []


print("Generating Embeddings")
for sentence in dataset:
  response = client.invoke_model(
    body= json.dumps({"inputText": sentence}),
    modelId= os.getenv("EMBED_MODEL_SMALL"),
    accept = "application/json",
    contentType = "application/json"
  )

  response_body = json.loads(response["body"].read())

  # add the embedding to the embedding list
  embeddings.append((sentence, response_body.get("embedding"), {}))


print("Creating/Updating Vector Store")
# Create vector store client
vx = vecs.Client(os.getenv("DB_CONNECTION"))
sentences = vx.get_or_create_collection(name="sentences", dimension=1536)

sentences.upsert(records=embeddings)
# create an index for the 'sentences' collection
sentences.create_index()

print("Completed Successfully")
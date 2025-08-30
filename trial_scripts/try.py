from dotenv import load_dotenv

from strands import Agent

# Load Environment variables from file
print("Loading Environment variables....")
load_dotenv()


# Create Agent Instance
agent = Agent(model="us.anthropic.claude-3-5-haiku-20241022-v1:0")


# Trial Run
agent("Hello World");

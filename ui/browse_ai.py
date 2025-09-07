import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Seller_Workflow')))
from strands import Agent
from strands.models import BedrockModel

CHAT_SYSTEM_PROMPT = """
You are Kairos AI, a helpful assistant for a university marketplace app. Help users find items they're looking for by:

1. Understanding what they want to buy
2. Suggesting relevant items from available listings
3. Providing helpful shopping advice
4. Answering questions about items

Be friendly, concise, and helpful. Focus on connecting buyers with sellers.
"""

def generate_ai_response(user_message, listings):
    """Generate AI response for chat using available listings context"""
    try:
        model = BedrockModel(
            model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
            temperature=0.7,
        )

        # Get k-nearest listings using vector embeddings semantic search
        
        # Format listings for context
        listings_context = "\n".join([
            f"- {item.get('title', 'No title')}: ${item.get('price', 0)} ({item.get('condition', 'Unknown condition')}, {item.get('category', 'No category')})"
            for item in listings[:10]  # Limit to first 10 items
        ]) if listings else "No items currently available."
        
        context_prompt = f"""
            Available listings:
            {listings_context}

            User message: {user_message}

            Help the user with their request based on the available listings.
            """
        
        agent = Agent(
            model=model,
            system_prompt=CHAT_SYSTEM_PROMPT
        )
        
        response = agent(context_prompt)
        return str(response)
    
    except Exception as e:
        return f"I'm having trouble right now. Please try again later. ({str(e)})"
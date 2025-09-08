import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from strands import Agent
from strands.models import BedrockModel
from src.core.db_handler import DbHandler

CHAT_SYSTEM_PROMPT = """
You are Kairos AI, a need clarification specialist for a university marketplace. Your role is to:

1. **Identify Vague Requests** - Detect when users have unclear or incomplete needs
2. **Ask Clarifying Questions** - Guide users to be more specific about their requirements
3. **Suggest Considerations** - Help users think about important factors they might miss
4. **Provide Quick Answers** - Answer simple questions about the marketplace

## When User Needs Are Vague:
Ask targeted questions like:
- "What's your budget range?"
- "What condition are you looking for?"
- "Any preferred brands?"
- "When do you need it by?"
- "Where would you prefer to pick it up?"

## When User Needs Are Clear:
Respond: "It sounds like you know exactly what you want! Try the 'Smart Search' tab above for personalized AI recommendations based on your specific requirements."

## Examples:
- User: "I want a water bottle" → Ask about size, material, budget, insulation needs
- User: "Looking for a MacBook Air M2, under $800, good condition, pickup at NUS" → Direct to Smart Search

Be friendly and conversational. Focus on helping users clarify their needs rather than searching for items.
"""

def generate_ai_response(user_message, chat_history=None):
    """Generate AI response for chat using conversation history and listings context"""
    try:
        model = BedrockModel(
            model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
            temperature=0.7,
        )

        # Build conversation context from history
        conversation_context = ""
        if chat_history:
            conversation_context = "\n\nPrevious conversation:\n"
            for role, msg in chat_history[-6:]:  # Last 6 messages for context
                conversation_context += f"{role.title()}: {msg}\n"
        
        context_prompt = f"""
            Current user message: {user_message}{conversation_context}

            Help the user clarify their needs or answer their question about the marketplace.
            If they have specific, detailed requirements, direct them to use Smart Search.
            If they have vague needs, ask clarifying questions to help them be more specific.
            Use the conversation history to provide contextual responses and avoid repeating questions.
            """
        
        agent = Agent(
            model=model,
            system_prompt=CHAT_SYSTEM_PROMPT
        )
        
        response = agent(context_prompt)
        return str(response)
    
    except Exception as e:
        return f"I'm having trouble right now. Please try again later. ({str(e)})"
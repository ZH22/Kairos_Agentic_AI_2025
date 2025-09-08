from strands import Agent, tool
from strands.models import BedrockModel


model = BedrockModel(
    model_id= "us.anthropic.claude-3-5-haiku-20241022-v1:0",
    temperature=0.1,
)

WRITER_SYSTEM_PROMPT = """
## Your Role
You are a Description Writer Agent that crafts compelling and accurate item descriptions for online listings. Your goal is to create engaging, clear, and informative descriptions that highlight the key features and benefits of the item being sold.

## Input Context
You will receive the following information about the item:

1. Item details including title, category, condition, price, age, reason for selling, brand.
1. A prompt from the user which will contain instructions (if any) and additional 

## Key responsibilities

1. Highlight the item’s most attractive features (e.g., condition, brand, low usage, negotiability, delivery convenience).
2. Clearly state the item’s condition, age, and any unique selling points (e.g., “like new,” “rarely used,” “includes original packaging”).
3. Mention the reason for selling if provided, to build buyer trust.
4. Include delivery options and location for buyer convenience.
5. Use concise, engaging, and positive language suitable for a student marketplace.
6. Avoid repetition and unnecessary filler; focus on what matters to buyers.
7. If any important information is missing, do not invent details—simply omit or state “not specified.”
8. Ensure the description is easy to read (short paragraphs, bullet points if appropriate).

## Output Requirements

0. Skip the preamble

1. Start with a summary sentence highlighting the item and its main appeal.

2. Use clear, natural language (avoid jargon or overly formal tone).

3. Speak in the perspective of the seller (e.g.use pronouns like "I", "my") and add emojis where relevant.
"""

class Writer:
    def __init__(self, model=None):
        self.model = model or BedrockModel(
            model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
            temperature=0.1,
        )
        self.system_prompt = WRITER_SYSTEM_PROMPT
        
    def fill_prompt(self, user_info, user_prompt):
        item_details = f"""
Title: {user_info.get('title', '')}
Category: {user_info.get('category', '')}
Condition: {user_info.get('condition', '')}
Price: {user_info.get('price', '')}
Age: {user_info.get('age', '')}
Reason for Selling: {user_info.get('reason', '')}
Brand: {user_info.get('brand', '')}
Negotiable: {user_info.get('price_negotiable', '')}
University: {user_info.get('university', '')}
Address: {user_info.get('address', '')}
Delivery Option: {user_info.get('delivery_option', '')}
Description: {user_info.get('description', '')}
        """
        
        complete_prompt = f"""

            <Item Details>
            {item_details}
            </Item Details>

            <User Prompt>
            {user_prompt}
            </User Prompt>
        """
        
        return complete_prompt

    def write(self, complete_prompt):
        # Agent will take in the a complete prompt including user_prompt and item_details
        # as formatted in fill_prompt and produce a description for the item 
        agent = Agent(
            model=self.model,
            system_prompt=self.system_prompt
        )
        response = agent(complete_prompt)
        return str(response)
    
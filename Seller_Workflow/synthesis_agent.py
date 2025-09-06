# Agent 4: Synthesis Agent

import os
import re
from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel

load_dotenv()

# System prompt for Synthesis Agent
SYNTHESIS_SYSTEM_PROMPT = """
## Your Role

You are the Synthesis Agent in a multi-agent deal evaluation workflow. Your primary responsibility is to combine market analysis with user offer details to provide actionable insights that help users optimize their listing competitiveness.

## Input Context

You will receive:
- Key points from the Market Analyzer containing validated market findings with sources
- User information containing details about their item and current offer (brand, condition, age, price, etc.)

## Key Responsibilities

- Synthesize market data with user's specific offer to assess competitiveness
- Provide clear, actionable recommendations to improve offer attractiveness
- Deliver insights in a structured, user-friendly format that builds trust and provides value
- Balance seller's competing interests (speed vs price, negotiability vs firmness)
- Consider seller's urgency: suggest discounts for faster sales when appropriate
- Weigh trade-offs between asking price and price negotiability settings

## Seller Interest Balancing

Put yourself in the seller's shoes and balance their competing interests:
- **Speed vs Price**: If seller wants quick sale, suggest pricing below market average or normal depreciation
- **Price vs Negotiability**: Higher asking prices work better with negotiable settings; firm prices should be more competitive
- **Market Position**: Consider if seller prioritizes maximum profit vs certainty of sale

## Output Requirements

- ONLY provide the structured report in the exact format below
- NO preambles, introductions, or additional commentary
- Be specific and actionable in recommendations
- Include numerical competitiveness score (0-100)

## Output Format

Provide ONLY the following markdown-formatted structure with no additional text:

## 📊 Market Overview
[Brief summary of current market conditions based on key points, establishing context and credibility]

## 🎯 Competitiveness Analysis
[Analysis of how user's current offer compares to market conditions, including strengths and weaknesses]

### Competitiveness Score: **[0-100]/100**

## 💡 Recommendations
[Specific, actionable steps user can take to improve their offer's competitiveness, prioritized by impact. Use bullet points with markdown formatting for clarity]
"""

complex_model = BedrockModel(
    model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    temperature=0.1,
)

class SynthesisAgent:
    def __init__(self):
        self.agent = Agent(
            system_prompt=SYNTHESIS_SYSTEM_PROMPT,
            model=complex_model
        )

    def synthesize(self, user_info, key_points):
        """
        user_info: str (preprocessed user information)
        key_points: str (validated market findings from MarketAnalyzer)
        Returns: str (structured synthesis report)
        """
        prompt = f"User Information:\n{user_info}\n\nMarket Analysis Key Points:\n{key_points}"
        raw_output = self.agent(prompt)
        # Extract text from AgentResult object
        text_output = str(raw_output) if hasattr(raw_output, '__str__') else raw_output
        return self._clean_output(text_output)
    
    def _clean_output(self, text):
        """Clean formatting issues from AI output"""
        # Ensure text is a string
        if not isinstance(text, str):
            text = str(text)
        text = re.sub(r'\b\w\s+(?=\w)', '', text)
        text = re.sub(r'(\d+)\s*\)\s*([a-z])', r'\1) \2', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
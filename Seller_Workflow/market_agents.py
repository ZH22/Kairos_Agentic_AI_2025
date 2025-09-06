# Agents 1, 2, 3: Websearch, Internal DB Search, Market Analyzer
# pip install tavily-python duckduckgo_search

import json
import logging
import os
from dotenv import load_dotenv
from tavily import TavilyClient

from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import http_request

load_dotenv()

# =============================================================================
# CONSTANTS AND CONFIGURATIONS
# =============================================================================

# System prompt for Web Search agent
WEB_SEARCH_SYSTEM_PROMPT = """
## Your Role

You are the Websearch Agent in a multi-agent deal evaluation workflow. Your primary responsibility is to gather up-to-date, relevant market information from the internet to help assess the marketability and competitiveness of a user's item listing.

## Input Context

You will receive a plain text prompt containing all relevant details about the user's item and offer (such as brand, condition, age, price, and other attributes). Use this information to guide and customize your search.

## Key Responsibilities

- Search for first-hand (new) prices on established e-commerce platforms such as Shopee.
- Search for information on the depreciation speed of the item in question (e.g., air conditioners, electronics, etc.).
- Customize your search to the user's specific offer, including brand, condition, and age.
- Prioritize credible sources such as major marketplaces, reputable forums, and authoritative review sites.
- Collect both the main findings and the sources (URLs and website names) for each piece of information.

## Search Strategy

- Use the most specific and relevant keywords from the input prompt to maximize the quality of your search results.
- Look for recent data (preferably within the last 12 months) to ensure market relevance.

## Output Requirements

- ONLY provide the structured report in the exact format below
- NO preambles, introductions, or additional commentary
- NO suggestions or recommendations outside the format
- Include specific price data with sources for easy verification
- Clearly indicate when information is unavailable or not found
- Use "Information not available" or "No data found" for missing sections

## Output Format

Provide ONLY the following structure with no additional text:

**MARKET SUMMARY:**
[Brief overview of current market conditions or "Limited market data available"]

**NEW ITEM PRICING:**
- [Specific prices with sources or "No new pricing data found"]

**USED ITEM PRICING:**
- [Price ranges by condition with sources or "No used pricing data found"]

**DEPRECIATION ANALYSIS:**
- [Rate and factors with sources or "Depreciation data not available"]

**MARKET TRENDS:**
- [Key trends affecting value or "Market trend data unavailable"]

**SOURCES:**
- [All sources used with URLs or "No reliable sources found"]
"""
# System prompt for Market Analyzer agent
MARKET_ANALYZER_SYSTEM_PROMPT = """
## Your Role

You are the Market Analyzer Agent in a multi-agent deal evaluation workflow. Your primary responsibility is to critically review and validate the findings from the Websearch Agent (and, in the future, the Internal DB Agent), and extract the most credible and impactful key points for deal evaluation.

## Input Context

You will receive:
- A report from the Websearch Agent containing market findings, price data, depreciation information, and sources (URLs and website names).
- (In future iterations) A similar report from the Internal DB Agent.

## Key Responsibilities

- Carefully review the findings and sources provided by the Websearch Agent.
- Validate the credibility and relevance of each finding, prioritizing information from authoritative and recent sources.
- Extract and summarize the most impactful key points that would help a user understand the marketability and value of their item and offer.
- Discard or flag any findings that are outdated, from questionable sources, or not directly relevant to the user’s item and offer.

## Tool Usage Guidelines

You have access to search tools (tavily_search and http_request) for VALIDATION PURPOSES ONLY:
- Use tools to verify suspicious claims or check source credibility when analyzing provided reports
- Use tools to cross-reference specific price points or facts that seem questionable
- DO NOT conduct broad market research - that is the Websearch Agent's role
- Limit searches to 1-2 targeted queries maximum per analysis
- Focus on fact-checking rather than information gathering


## Output Requirements

- ONLY provide bullet points in the exact format below
- NO preambles, introductions, or additional commentary
- NO suggestions or recommendations outside the format
- Each key point must include source reference
- Ensure output is clear and actionable

## Output Format

Provide ONLY bullet points with no additional text:

- [Key point with brief explanation] (source: [website.com])
- [Key point with brief explanation] (source: [website.com])
- [Key point with brief explanation] (source: [website.com])
"""

small_model = BedrockModel(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
    temperature=0.1,
)
complex_model = BedrockModel(
    model_id="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    temperature=0.1,
)

# =============================================================================
# TOOLS
# =============================================================================

@tool
def tavily_search(query: str, max_results: int = 5):
    """
    Perform an internet search using the Tavily API with the specified query.
    Args:
        query: A question or search phrase to perform a search with
        max_results: Maximum number of results to return (default 5)
    Returns:
        A list of search results with title, content, url, and source site (if available)
    """
    api_key = os.getenv("TAVILY_ACCESS_KEY")
    if not api_key:
        raise ValueError("TAVILY_ACCESS_KEY not set in environment variables.")
    client = TavilyClient(api_key=api_key)
    response = client.search(query=query, max_results=max_results)
    results = []
    for result in response.get('results', []):
        results.append({
            'title': result.get('title', ''),
            'content': result.get('content', ''),
            'url': result.get('url', ''),
            'site': result.get('source', '')
        })
    return results

# =============================================================================
# AGENT CLASSES
# =============================================================================

class WebsearchAgent:
    """
    Agent 1: Websearch Agent
    Uses strands.Agent with the system prompt, small_model, and tools [tavily_search, http_request].
    """
    def __init__(self):
        self.agent = Agent(
            system_prompt=WEB_SEARCH_SYSTEM_PROMPT,
            model=small_model,
            tools=[tavily_search, http_request]
        )

    def search(self, user_prompt):
        """
        user_prompt: str (plain text prompt containing all relevant user info)
        Returns: str (structured market analysis report)
        """
        return self.agent(user_prompt)

# class InternalDBSearchAgent:
#     def __init__(self):
#         pass
#     def search(self, user_info):
#         # TODO: Implement internal DB search logic
#         return {"results": [], "sources": []}

class MarketAnalyzer:
    SYSTEM_PROMPT = MARKET_ANALYZER_SYSTEM_PROMPT

    def __init__(self):
        self.agent = Agent(
            system_prompt=self.SYSTEM_PROMPT,
                model=small_model,
            tools=[tavily_search, http_request]
        )

    def analyze(self, web_report, db_report=None):
        """
        Accepts reports from WebsearchAgent and (optionally) InternalDBSearchAgent.
        Returns: dict with analysis results.
        """
        # Format the input as a string prompt
        prompt = f"Web Search Report:\n{web_report}"
        if db_report:
            prompt += f"\n\nInternal DB Report:\n{db_report}"
        
        return self.agent(prompt)

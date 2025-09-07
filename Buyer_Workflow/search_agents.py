# Buyer Workflow: Intelligent Search Agents
import os
import sys
import json
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models import BedrockModel

load_dotenv()

# Add parent directory to path for db_Handler import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db_Handler import DbHandler

# =============================================================================
# SYSTEM PROMPTS
# =============================================================================

SEARCH_ANALYZER_SYSTEM_PROMPT = """
## Your Role

You are the Search Analyzer Agent in a buyer workflow. Your primary responsibility is to analyze listings retrieved from semantic search and evaluate how well each matches the user's preferences.

## Input Context

You will receive:
- User's search preferences and requirements (semi-structured prompt)
- Listings retrieved from semantic search via query_try tool

## Key Responsibilities

- Use the semantic_search_tool to find relevant listings based on user preferences
- Analyze each retrieved listing against user's specific requirements
- Evaluate match quality considering price, condition, category, location, etc.
- Provide a concise summary for each listing explaining the match quality

## Output Requirements

For each listing found, provide ONLY the following format:

**Listing ID: [listing_id]**
[2-3 sentence summary explaining how this listing matches or doesn't match user preferences, highlighting key strengths and potential concerns]

---

If no listings found, state: "No matching listings found."
"""

RANKING_AGENT_SYSTEM_PROMPT = """
## Your Role

You are the Ranking Agent in a buyer workflow. Your primary responsibility is to rank listings analyzed by the Search Analyzer and recommend the top 3 candidates.

## Input Context

You will receive:
- User's original search preferences
- Analysis summaries from Search Analyzer Agent for each listing

## Key Responsibilities

- Compare and rank all analyzed listings based on user preferences
- Select up to top 3 best matches
- Provide detailed recommendations explaining why each listing fits user needs

## Output Requirements

Provide ONLY the following format:

## 🏆 Top Recommendations

### 1. [Listing Title] (ID: [listing_id])
[Detailed paragraph explaining why this is the best match, how it fits user preferences, and what makes it stand out]

**[View Original]**

### 2. [Listing Title] (ID: [listing_id])
[Detailed paragraph explaining why this is recommended and how it meets user needs]

**[View Original]**

### 3. [Listing Title] (ID: [listing_id])
[Detailed paragraph explaining the recommendation rationale]

**[View Original]**

If fewer than 3 suitable listings, only show the good matches.
"""

# =============================================================================
# MODELS
# =============================================================================

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
def semantic_search_tool(user_query: str, limit: int = 10):
    """
    Search listings database using semantic similarity based on user preferences.
    Args:
        user_query: User's search preferences and requirements
        limit: Maximum number of listings to return (default 10)
    Returns:
        List of matching listings with full details
    """
    try:
        db = DbHandler()
        
        # Get similar listing IDs using semantic search
        similar_listing_ids = db.query_try(user_query, limit)
        
        # Get full listing details
        if similar_listing_ids:
            listings = db.get_listings(ids=similar_listing_ids)
            return listings
        else:
            return []
            
    except Exception as e:
        return {"error": f"Search failed: {str(e)}"}

# =============================================================================
# AGENT CLASSES
# =============================================================================

class SearchAnalyzerAgent:
    """
    Agent 1: Analyzes listings from semantic search against user preferences
    """
    def __init__(self):
        self.agent = Agent(
            system_prompt=SEARCH_ANALYZER_SYSTEM_PROMPT,
            model=small_model,
            tools=[semantic_search_tool]
        )

    def analyze(self, user_preferences: str):
        """
        Analyze listings based on user preferences
        Args:
            user_preferences: Semi-structured prompt with user requirements
        Returns:
            Analysis summaries for each listing
        """
        prompt = f"User Preferences:\n{user_preferences}\n\nUse semantic_search_tool to find relevant listings and analyze each one."
        return self.agent(prompt)

class RankingAgent:
    """
    Agent 2: Ranks analyzed listings and provides top 3 recommendations
    """
    def __init__(self):
        self.agent = Agent(
            system_prompt=RANKING_AGENT_SYSTEM_PROMPT,
            model=complex_model
        )

    def rank(self, user_preferences: str, analysis_summaries: str):
        """
        Rank listings and provide top 3 recommendations
        Args:
            user_preferences: Original user search preferences
            analysis_summaries: Analysis results from SearchAnalyzerAgent
        Returns:
            Top 3 ranked recommendations
        """
        prompt = f"User Preferences:\n{user_preferences}\n\nListing Analysis:\n{analysis_summaries}"
        return self.agent(prompt)

# =============================================================================
# WORKFLOW ORCHESTRATION
# =============================================================================

def buyer_search_workflow(user_preferences: str):
    """
    Orchestrates the buyer search workflow
    Args:
        user_preferences: Semi-structured prompt with user search requirements
    Returns:
        Top 3 listing recommendations
    """
    # Step 1: Search and analyze listings
    search_analyzer = SearchAnalyzerAgent()
    analysis_results = search_analyzer.analyze(user_preferences)
    analysis_text = str(analysis_results) if hasattr(analysis_results, '__str__') else analysis_results
    
    # Step 2: Rank and recommend top 3
    ranking_agent = RankingAgent()
    recommendations = ranking_agent.rank(user_preferences, analysis_text)
    final_recommendations = str(recommendations) if hasattr(recommendations, '__str__') else recommendations
    
    return final_recommendations
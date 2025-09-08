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
from src.core.db_handler import DbHandler

# =============================================================================
# SYSTEM PROMPTS
# =============================================================================

QUERY_PROCESSOR_SYSTEM_PROMPT = """
## Your Role

You are the Query Processor Agent. Your primary responsibility is to evaluate if user queries have sufficient detail for precision matching, and either structure them or request more information.

## Input Context

You will receive raw user queries in natural language describing what they're looking for.

## Key Responsibilities

- Evaluate if the query has enough specificity for effective matching
- For sufficient queries: structure into standardized format
- For insufficient queries: identify what information is missing and ask for it

## Decision Criteria for Sufficient Queries

A query is SUFFICIENT if it includes:
- Clear item type/category
- At least 2 of: budget/price range, condition preference, brand preference, specific requirements

## Output Requirements

**For SUFFICIENT queries, provide:**
STATUS: SUFFICIENT

**Item Title:** [Main item type user is looking for]

**Preferences:**
- [Specific requirement 1]
- [Specific requirement 2]
- [Specific requirement 3]
- [etc.]

**For INSUFFICIENT queries, provide:**
STATUS: NEEDS_MORE_INFO

**Missing Information:**
To help you find the perfect match, could you please specify:
- What's your budget range? (e.g., under $500, $200-800)
- What condition are you looking for? (new, like new, used, any condition)
- Any preferred brands or specific features?
- Where would you prefer pickup? (NUS, NTU, etc.)

**Examples:**
Query: "I want a laptop" → Ask: Budget range? Gaming/work/study use? Brand preference? Condition?
Query: "water bottle" → Ask: What size? Insulated or regular? Budget range? Material preference?
Query: "textbook" → Ask: What subject? Specific title/author? Budget? Condition acceptable?

Always provide 3-4 specific, actionable questions relevant to the item type.
"""

SEARCH_ANALYZER_SYSTEM_PROMPT = """
## Your Role

You are the Search Analyzer Agent in a buyer workflow. Your primary responsibility is to analyze listings retrieved from semantic search and evaluate how well each matches the user's preferences.

## Input Context

You will receive:
- Structured user preferences with Item Title and Preferences list
- Access to semantic_search_tool for finding relevant listings

## Key Responsibilities

- Use the Item Title for targeted semantic search via semantic_search_tool
- Analyze each retrieved listing against the specific user preferences
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
# FALLBACK QUESTIONS
# =============================================================================

FALLBACK_QUESTIONS = {
    "laptop": [
        "What's your budget range? (e.g., under $800, $500-1000)",
        "What will you use it for? (gaming, work, study, programming)",
        "Any preferred brands? (Apple, Dell, HP, Lenovo, etc.)",
        "What condition are you looking for? (new, like new, used)"
    ],
    "phone": [
        "What's your budget range?",
        "Any preferred brands? (iPhone, Samsung, Google, etc.)",
        "What condition are you looking for?",
        "Any specific features needed? (camera quality, storage, etc.)"
    ],
    "furniture": [
        "What's your budget range?",
        "What size/dimensions do you need?",
        "What condition are you looking for?",
        "Where would you prefer pickup? (NUS, NTU, etc.)"
    ],
    "textbook": [
        "What subject are you looking for?",
        "Do you need a specific title or author?",
        "What's your budget range?",
        "What condition is acceptable? (new, used, any condition)"
    ],
    "electronics": [
        "What's your budget range?",
        "What condition are you looking for?",
        "Any preferred brands?",
        "Where would you prefer pickup?"
    ],
    "clothing": [
        "What size do you need?",
        "What's your budget range?",
        "Any preferred brands or styles?",
        "What condition are you looking for?"
    ],
    "default": [
        "What's your budget range?",
        "What condition are you looking for? (new, like new, used)",
        "Any specific requirements or preferences?",
        "Where would you prefer pickup? (NUS, NTU, etc.)"
    ]
}

def detect_item_category(query):
    """Detect item category from user query for fallback questions"""
    query_lower = query.lower()
    
    # Electronics
    if any(word in query_lower for word in ['laptop', 'macbook', 'computer', 'pc']):
        return 'laptop'
    if any(word in query_lower for word in ['phone', 'iphone', 'samsung', 'mobile']):
        return 'phone'
    if any(word in query_lower for word in ['tv', 'monitor', 'speaker', 'headphone', 'camera']):
        return 'electronics'
    
    # Furniture
    if any(word in query_lower for word in ['chair', 'table', 'desk', 'bed', 'sofa', 'furniture']):
        return 'furniture'
    
    # Books
    if any(word in query_lower for word in ['textbook', 'book', 'novel', 'manual']):
        return 'textbook'
    
    # Clothing
    if any(word in query_lower for word in ['shirt', 'pants', 'dress', 'jacket', 'shoes', 'clothing']):
        return 'clothing'
    
    return 'default'

def generate_fallback_questions(query):
    """Generate fallback questions based on item category"""
    category = detect_item_category(query)
    questions = FALLBACK_QUESTIONS.get(category, FALLBACK_QUESTIONS['default'])
    
    formatted_questions = "To help you find the perfect match, could you please specify:\n"
    for question in questions:
        formatted_questions += f"- {question}\n"
    
    return formatted_questions.strip()

# =============================================================================
# AGENT CLASSES
# =============================================================================

class QueryProcessorAgent:
    """
    Agent 1: Processes raw user queries into structured format
    """
    def __init__(self):
        self.agent = Agent(
            system_prompt=QUERY_PROCESSOR_SYSTEM_PROMPT,
            model=small_model
        )

    def process(self, raw_query: str):
        """
        Process raw user query and evaluate specificity
        Args:
            raw_query: Natural language user query
        Returns:
            Dict with status and either structured_query or clarification_request
        """
        try:
            response = str(self.agent(raw_query))
            
            if "STATUS: SUFFICIENT" in response:
                return {
                    "status": "SUFFICIENT",
                    "structured_query": response.replace("STATUS: SUFFICIENT\n\n", "")
                }
            elif "STATUS: NEEDS_MORE_INFO" in response:
                # AI agent successfully identified insufficient query - use its response
                if "**Missing Information:**" in response:
                    missing_info_section = response.split("**Missing Information:**\n")[1]
                    return {
                        "status": "NEEDS_MORE_INFO",
                        "clarification_request": missing_info_section.strip()
                    }
                else:
                    # AI provided NEEDS_MORE_INFO but no proper format - use its full response
                    return {
                        "status": "NEEDS_MORE_INFO",
                        "clarification_request": response.replace("STATUS: NEEDS_MORE_INFO\n\n", "")
                    }
            else:
                # AI response doesn't match expected format - this is an AI failure
                # Use fallback only in this case
                return {
                    "status": "NEEDS_MORE_INFO",
                    "clarification_request": generate_fallback_questions(raw_query)
                }
                
        except Exception as e:
            # AI agent completely failed - use fallback
            return {
                "status": "NEEDS_MORE_INFO",
                "clarification_request": generate_fallback_questions(raw_query)
            }

class SearchAnalyzerAgent:
    """
    Agent 2: Analyzes listings from semantic search against user preferences
    """
    def __init__(self):
        self.agent = Agent(
            system_prompt=SEARCH_ANALYZER_SYSTEM_PROMPT,
            model=small_model,
            tools=[semantic_search_tool]
        )

    def analyze(self, structured_preferences: str):
        """
        Analyze listings based on structured user preferences
        Args:
            structured_preferences: Structured query from QueryProcessor
        Returns:
            Analysis summaries for each listing
        """
        prompt = f"Structured User Query:\n{structured_preferences}\n\nUse semantic_search_tool with the Item Title to find relevant listings and analyze each against the Preferences."
        return self.agent(prompt)

class RankingAgent:
    """
    Agent 3: Ranks analyzed listings and provides top 3 recommendations
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

def validate_query(raw_user_query: str):
    """
    Validates if user query has sufficient detail for precision matching
    Args:
        raw_user_query: Natural language user query
    Returns:
        Dict with validation result and either structured_query or clarification_request
    """
    query_processor = QueryProcessorAgent()
    return query_processor.process(raw_user_query)

def buyer_search_workflow(structured_query: str):
    """
    Orchestrates the 2-agent buyer search workflow (assumes query is already validated)
    Args:
        structured_query: Pre-validated and structured user query
    Returns:
        Top 3 listing recommendations
    """
    # Step 1: Search and analyze listings using structured query
    search_analyzer = SearchAnalyzerAgent()
    analysis_results = search_analyzer.analyze(structured_query)
    analysis_text = str(analysis_results) if hasattr(analysis_results, '__str__') else analysis_results
    
    # Step 2: Rank and recommend top 3
    ranking_agent = RankingAgent()
    recommendations = ranking_agent.rank(structured_query, analysis_text)
    final_recommendations = str(recommendations) if hasattr(recommendations, '__str__') else recommendations
    
    return final_recommendations
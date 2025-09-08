# Buyer Workflow: Intelligent Buying Guide Agent
import os
import sys
import re
from dotenv import load_dotenv
from strands import Agent
from strands.models import BedrockModel

load_dotenv()

# =============================================================================
# SYSTEM PROMPT
# =============================================================================

BUYING_GUIDE_SYSTEM_PROMPT = """
## Your Role

You are a quick, helpful discovery guide for Kairos campus connector. Help students find exactly what they need and connect with fellow student sellers through short, focused conversations.

## Response Style - CRITICAL

**KEEP RESPONSES SHORT & CONVERSATIONAL:**
- Maximum 3-4 sentences per response
- Ask 1-2 focused questions max
- Use simple, friendly language
- Avoid long lists or detailed explanations
- Get to the point quickly

## Core Process

1. **Identify** what they want
2. **Ask** 1-2 key questions about their needs
3. **Clarify** their priorities quickly
4. **Transition** to search when ready

## Response Format

🎯 **[Item]** - [Quick insight/question]

**Examples:**

"🎯 **Laptop** - What's your main use? Gaming, work, or just browsing? And what's your budget range?"

"🎯 **Standing Fan** - For a dorm room or larger space? Noise level important for studying?"

"🎯 **Phone** - iPhone or Android preference? What's your budget looking like?"

## Transition Signal

When ready: "🚀 **Ready for Search!** You've got clear preferences now. Want me to find students selling what you need?"

## Keep It Simple
- No long explanations
- No bullet point lists
- Quick back-and-forth conversation
- Focus on 2-3 key factors max
"""

# =============================================================================
# MODELS
# =============================================================================

guide_model = BedrockModel(
    model_id="us.anthropic.claude-3-5-haiku-20241022-v1:0",
    temperature=0.3,
)

# =============================================================================
# ITEM CATEGORIES
# =============================================================================

ITEM_CATEGORIES = {
    # Electronics
    'laptop', 'computer', 'macbook', 'pc', 'notebook',
    'phone', 'iphone', 'samsung', 'mobile', 'smartphone',
    'tablet', 'ipad', 'monitor', 'screen', 'display',
    'headphones', 'earbuds', 'speaker', 'audio',
    'camera', 'webcam', 'microphone',
    
    # Appliances
    'fan', 'standing fan', 'ceiling fan', 'air conditioner', 'ac',
    'heater', 'humidifier', 'dehumidifier',
    'refrigerator', 'fridge', 'microwave',
    'rice cooker', 'kettle', 'blender',
    
    # Furniture
    'chair', 'desk', 'table', 'bed', 'mattress',
    'sofa', 'couch', 'bookshelf', 'wardrobe', 'dresser',
    'lamp', 'lighting',
    
    # Study Materials
    'textbook', 'book', 'notebook', 'calculator',
    'stationery', 'pen', 'pencil',
    
    # Personal Items
    'bag', 'backpack', 'wallet', 'watch',
    'clothing', 'shirt', 'pants', 'shoes',
    'water bottle', 'tumbler', 'mug',
    
    # Sports & Recreation
    'bicycle', 'bike', 'skateboard', 'sports equipment',
    'gym equipment', 'yoga mat',
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def extract_item_category(message):
    """Extract item category from user message"""
    message_lower = message.lower()
    
    # Look for item categories in the message
    found_categories = []
    for category in ITEM_CATEGORIES:
        if category in message_lower:
            found_categories.append(category)
    
    # Return the longest match (most specific)
    if found_categories:
        return max(found_categories, key=len)
    
    return None

def detect_topic_change(new_message, current_context):
    """Detect if user is switching to a different item category"""
    if not current_context.get("current_item"):
        return False, None
    
    new_category = extract_item_category(new_message)
    current_category = current_context.get("current_item")
    
    if new_category and new_category != current_category:
        # Check if it's a significant change (not just related terms)
        if not _are_related_categories(new_category, current_category):
            return True, new_category
    
    return False, None

def _are_related_categories(cat1, cat2):
    """Check if two categories are related (e.g., 'laptop' and 'computer')"""
    related_groups = [
        {'laptop', 'computer', 'macbook', 'pc', 'notebook'},
        {'phone', 'iphone', 'samsung', 'mobile', 'smartphone'},
        {'fan', 'standing fan', 'ceiling fan'},
        {'chair', 'desk chair', 'office chair', 'study chair'},
        {'bag', 'backpack'},
        {'water bottle', 'tumbler', 'bottle'},
    ]
    
    for group in related_groups:
        if cat1 in group and cat2 in group:
            return True
    
    return False

# =============================================================================
# AGENT CLASS
# =============================================================================

class BuyingGuideAgent:
    """
    Intelligent buying guide that helps users discover their preferences
    with memory and topic change detection
    """
    
    def __init__(self):
        self.agent = Agent(
            system_prompt=BUYING_GUIDE_SYSTEM_PROMPT,
            model=guide_model
        )
    
    def guide_conversation(self, user_message, conversation_context):
        """
        Main conversation handler with memory (no automatic topic change detection)
        
        Args:
            user_message: User's current message
            conversation_context: Current conversation state
            
        Returns:
            dict: {
                'response': agent response,
                'context': updated context,
                'ready_for_search': bool
            }
        """
        
        # Build conversation prompt with context
        conversation_prompt = self._build_conversation_prompt(user_message, conversation_context)
        
        # Get agent response
        response = str(self.agent(conversation_prompt))
        
        # Update context
        updated_context = self._update_context(user_message, response, conversation_context)
        
        # Check if ready for search
        ready_for_search = self._is_ready_for_search(response, updated_context)
        
        return {
            'response': response,
            'context': updated_context,
            'ready_for_search': ready_for_search
        }
    
    def start_fresh_conversation(self, new_message, conversation_context):
        """Start fresh conversation (used when user clicks Start Over)"""
        # Extract item from new message
        new_item = extract_item_category(new_message)
        
        # Reset context for new conversation
        new_context = {
            'current_item': new_item,
            'conversation_stage': 'initial',
            'chat_history': [],
            'discovered_preferences': {},
            'previous_items': conversation_context.get('previous_items', [])
        }
        
        # Add previous item to history if exists
        if conversation_context.get('current_item'):
            new_context['previous_items'].append(conversation_context['current_item'])
        
        # Get fresh response
        if new_item:
            fresh_prompt = f"User wants guidance for: {new_item}. Provide an engaging introduction and initial questions."
        else:
            fresh_prompt = f"User message: {new_message}. Help them discover what they're looking for."
            
        response = str(self.agent(fresh_prompt))
        
        # Update context with first interaction
        new_context['chat_history'].append(('user', new_message))
        new_context['chat_history'].append(('assistant', response))
        
        return {
            'response': response,
            'context': new_context,
            'ready_for_search': False
        }
    

    
    def _build_conversation_prompt(self, user_message, context):
        """Build prompt with conversation context"""
        prompt_parts = []
        
        # Add current focus
        if context.get('current_item'):
            prompt_parts.append(f"Current Focus: {context['current_item']}")
        
        # Add conversation history (last 6 messages to avoid token limits)
        if context.get('chat_history'):
            prompt_parts.append("Recent Conversation:")
            recent_history = context['chat_history'][-6:]
            for role, message in recent_history:
                prompt_parts.append(f"{role}: {message}")
        
        # Add discovered preferences
        if context.get('discovered_preferences'):
            prompt_parts.append(f"Discovered Preferences: {context['discovered_preferences']}")
        
        # Add current message
        prompt_parts.append(f"User's Current Message: {user_message}")
        
        return "\n\n".join(prompt_parts)
    
    def _update_context(self, user_message, response, context):
        """Update conversation context"""
        updated_context = context.copy()
        
        # Update chat history
        if 'chat_history' not in updated_context:
            updated_context['chat_history'] = []
        
        updated_context['chat_history'].append(('user', user_message))
        updated_context['chat_history'].append(('assistant', response))
        
        # Extract item category if not set
        if not updated_context.get('current_item'):
            item_category = extract_item_category(user_message)
            if item_category:
                updated_context['current_item'] = item_category
        
        # Update conversation stage based on response content
        if 'Ready for Search' in response:
            updated_context['conversation_stage'] = 'ready_for_search'
        elif updated_context.get('conversation_stage') == 'initial':
            updated_context['conversation_stage'] = 'discovery'
        
        return updated_context
    
    def _is_ready_for_search(self, response, context):
        """Check if user is ready to transition to search"""
        ready_indicators = [
            'Ready for Search',
            'sufficient preferences',
            'help you find specific listings',
            'transition to search'
        ]
        
        return any(indicator in response for indicator in ready_indicators)

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def initialize_guide_context():
    """Initialize empty conversation context"""
    return {
        'current_item': None,
        'conversation_stage': 'initial',
        'chat_history': [],
        'discovered_preferences': {},
        'previous_items': []
    }

def extract_preferences_for_search(context):
    """Extract discovered preferences in format suitable for AI Search"""
    if not context.get('current_item') or not context.get('discovered_preferences'):
        return None
    
    item = context['current_item']
    prefs = context['discovered_preferences']
    
    # Build structured query format
    structured_query = f"**Item Title:** {item}\n\n**Preferences:**\n"
    
    for key, value in prefs.items():
        structured_query += f"- {key}: {value}\n"
    
    return structured_query
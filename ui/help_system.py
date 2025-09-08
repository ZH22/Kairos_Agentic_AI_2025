import streamlit as st

# Help content for different pages
HELP_CONTENT = {
    "home": {
        "title": "🏠 Welcome to Kairos!",
        "content": """
        **What makes Kairos different?**
        - 🤖 **AI-Powered Search**: Find exactly what you need using natural language
        - 🎯 **Smart Matching**: Get personalized recommendations based on your preferences
        - 💬 **Conversational Discovery**: Chat with AI to discover what you really want
        - 🔒 **Campus-Safe**: Connect directly with fellow students for secure transactions
        
        **Quick Start:**
        1. Select your user profile (Adam, Bob, or Charlie)
        2. Try browsing items or posting something new
        3. Use AI Chat for the best search experience!
        
        **💡 Pro Tip:** Unlike traditional marketplaces, Kairos learns your preferences to find better matches over time.
        """
    },
    "browse": {
        "title": "🔍 Smart Item Discovery",
        "content": """
        **🎯 RECOMMENDED WORKFLOW:**
        
        **Step 1: Start with AI Chat** 💬
        - Tell AI what you're looking for in natural language
        - AI helps you discover your real needs and preferences
        - Learns your budget, condition preferences, and priorities
        
        **Step 2: Use AI Search** 🤖
        - Get personalized, ranked recommendations
        - AI validates your requirements and asks clarifying questions
        - Receive detailed analysis of why each item matches
        
        **Alternative: Basic Search** 🔍
        - Use only when you know exactly what you want
        - Quick keyword search for specific items
        - Best for browsing or simple searches
        
        **💡 Best Practice:** Chat → AI Search → Contact Seller. This workflow gives you the most personalized and accurate results!
        """
    },
    "post": {
        "title": "📝 Smart Item Posting",
        "content": """
        **🎯 RECOMMENDED WORKFLOW:**
        
        **Step 1: Fill Basic Details** 📋
        - Enter item title, price, category, condition
        - Add photos and basic information
        - Use "Fill Demo Data" to explore features quickly
        
        **Step 2: Generate AI Description** 🤖
        - Toggle "Use AI Write up" for compelling copy
        - AI creates engaging descriptions that sell faster
        - Edit the generated text to match your style
        
        **Step 3: Evaluate Your Deal** 📊
        - Click "Evaluate Your Deal!" for market analysis
        - AI analyzes web + campus market data
        - Adjust your price based on AI recommendations
        
        **Step 4: Post Your Item** ✅
        - Review all details and post to marketplace
        - Item appears in search results immediately
        
        **💡 Best Practice:** Fill Details → AI Description → Evaluate Deal → Post. This workflow maximizes your selling success!
        """
    },
    "mylistings": {
        "title": "📋 Manage Your Listings",
        "content": """
        **Your personal marketplace dashboard:**
        
        **✏️ Edit Listings**
        - Update prices, descriptions, and details anytime
        - Changes sync automatically across the platform
        - Preview descriptions before saving
        
        **🗑️ Delete Listings**
        - Secure deletion with ownership validation
        - Confirmation dialog prevents accidental removal
        - Items removed from all search results instantly
        
        **🔄 Auto-Sync**
        - Page automatically refreshes with latest data
        - No manual refresh needed
        - See updates from other pages immediately
        
        **💡 Pro Tip:** Keep your listings updated with current prices and availability for better visibility!
        """
    },
    "evaluation": {
        "title": "📊 AI Deal Evaluation",
        "content": """
        **Get smart pricing insights:**
        
        **🌐 Market Analysis**
        - AI searches web for similar items and pricing
        - Compares against internal campus marketplace data
        - Provides comprehensive market overview
        
        **💰 Price Recommendations**
        - Data-driven pricing suggestions
        - Considers item condition, age, and market trends
        - Helps you price competitively
        
        **📈 Deal Insights**
        - Understand if your price is fair
        - See how your item compares to alternatives
        - Make informed pricing decisions
        
        **💡 Pro Tip:** Use evaluation before posting to optimize your pricing strategy!
        """
    }
}

def show_floating_help_button():
    """Display floating help button in bottom left corner"""
    # CSS for floating button
    st.markdown("""
    <style>
    .floating-help-btn {
        position: fixed;
        bottom: 20px;
        left: 20px;
        z-index: 999;
        background-color: #FF6B6B;
        color: white;
        border: none;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 24px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    .floating-help-btn:hover {
        background-color: #FF5252;
        transform: scale(1.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize help state
    if "show_help_dialog" not in st.session_state:
        st.session_state.show_help_dialog = False
    
    # Help button (using columns to position it)
    col1, col2, col3 = st.columns([1, 8, 1])
    with col1:
        if st.button("❓", key="help_btn", help="Get help for this page"):
            st.session_state.show_help_dialog = True

def show_help_dialog(page_key):
    """Show help dialog for specific page"""
    if st.session_state.get("show_help_dialog", False):
        help_data = HELP_CONTENT.get(page_key, {
            "title": "❓ Help",
            "content": "Help content not available for this page."
        })
        
        # Create help dialog
        with st.container():
            st.markdown("---")
            st.markdown(f"### {help_data['title']}")
            st.markdown(help_data['content'])
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("✅ Got it!", key="close_help"):
                    st.session_state.show_help_dialog = False
                    st.rerun()

def contextual_help_system(page_key):
    """Main function to add contextual help to any page"""
    # Add floating help button
    show_floating_help_button()
    
    # Show help dialog if requested
    show_help_dialog(page_key)

def track_user_engagement(action, page):
    """Track user actions for progressive disclosure"""
    if "user_engagement" not in st.session_state:
        st.session_state.user_engagement = {}
    
    if page not in st.session_state.user_engagement:
        st.session_state.user_engagement[page] = []
    
    st.session_state.user_engagement[page].append(action)

def show_progressive_tip(page, feature, tip_text, trigger_count=3):
    """Show advanced tips after user engagement"""
    if "user_engagement" not in st.session_state:
        return
    
    page_actions = st.session_state.user_engagement.get(page, [])
    feature_count = page_actions.count(feature)
    
    if feature_count >= trigger_count:
        tip_key = f"tip_shown_{page}_{feature}"
        if not st.session_state.get(tip_key, False):
            st.info(f"💡 **Did you know?** {tip_text}")
            st.session_state[tip_key] = True
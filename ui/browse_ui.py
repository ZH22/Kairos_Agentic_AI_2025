import streamlit as st
from commons import categories_list
from Buyer_Workflow.browse_ai import generate_ai_response
from Buyer_Workflow.search_agents import validate_query, buyer_search_workflow
from db_Handler import DbHandler
import re

@st.dialog("Item Details")
def popup_dial(item):
    st.subheader(item["title"])
    if item["image"]:
        st.image(item["image"], width=200)
    st.write(f"**Price:** ${item['price']}")
    st.write(f"**Category:** {item['category']}")
    st.write(f"**Condition:** {item['condition']}")
    st.write(f"**Description:** {item['description']}")



def display():
    # Initialize database handler
    db = DbHandler()
    st.set_page_config(layout="wide")
    
    # Auto-refresh on page load
    if "page_loaded_browse" not in st.session_state:
        st.session_state.listings = db.get_listings()
        st.session_state.page_loaded_browse = True

    tab1, tab2, tab3 = st.tabs(["💬 Chat", "🔍 Basic Search", "🤖 AI Search"])
    
    with tab1:
        st.subheader("Chat with Kairos AI")
        st.caption("This is an AI-assisted search. Chat with AI to improve search. Click search when done.")   
        prompt = st.chat_input("Ask me anything...")
        with st.container(height = 300):
            # Full-width chat
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            for role, msg in st.session_state.chat_history:
                with st.chat_message(role):
                    st.write(msg)

            if prompt:
                st.session_state.chat_history.append(("user", prompt))
                with st.chat_message("user"):
                    st.write(prompt)

                ai_reply = generate_ai_response(prompt)
                st.session_state.chat_history.append(("assistant", ai_reply))
                with st.chat_message("assistant"):
                    st.write(ai_reply)

    with tab2:
        st.subheader("Browse All Listings")
        search_query = st.text_input("Search for items", placeholder="e.g., 'laptop', 'air conditioner', 'good condition'")

        listings = st.session_state["listings"]
        if not listings:
            st.info("No items available yet.")
        else:
            # Simple text search in title and description
            if search_query:
                filtered = [item for item in listings 
                           if search_query.lower() in item["title"].lower() 
                           or search_query.lower() in item["description"].lower()]
            else:
                filtered = listings

            if not filtered:
                st.warning("No items match your search.")
            else:
                st.write(f"Found {len(filtered)} items")
                cols = st.columns(2)
                for idx, item in enumerate(filtered):
                    with cols[idx % 2]:
                        if st.button(f"{item['title']}", key=f"basic_search_{idx}"):
                            popup_dial(item)
                        st.markdown(
                            f"""
                            <div style='border: 1px solid #ddd; padding: 10px; margin: 5px; border-radius: 5px;'>
                                <h4>{item['title']}</h4>
                                <p><b>${item['price']}</b></p>
                                <p>{item['category']} | {item['condition']}</p>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

    with tab3:
        st.subheader("🎯 Smart Search")
        st.caption("AI-powered precision matching. Describe your needs and get personalized recommendations.")
        
        # Initialize session state for validation
        if "validation_result" not in st.session_state:
            st.session_state.validation_result = None
        if "show_question_form" not in st.session_state:
            st.session_state.show_question_form = False
        
        ai_query = st.text_area(
            "What are you looking for?", 
            placeholder="Example: Looking for a MacBook Air M2, under $800, good condition, pickup at NUS",
            height=100
        )
        
        # Determine if Smart Search should be enabled
        search_enabled = (
            st.session_state.validation_result is None or 
            st.session_state.validation_result.get("status") == "SUFFICIENT"
        )
        
        if st.button("🔍 Smart Search", type="primary", disabled=not search_enabled):
            if ai_query.strip():
                with st.spinner("🤖 Analyzing your request..."):
                    try:
                        st.session_state.validation_result = validate_query(ai_query)
                        st.session_state.user_query = ai_query
                    except Exception as e:
                        st.error(f"Query analysis failed: {str(e)}")
            else:
                st.warning("Please describe what you're looking for.")
        
        # Display validation results
        if st.session_state.validation_result:
            result = st.session_state.validation_result
            
            if result["status"] == "NEEDS_MORE_INFO":
                # Show clarification request in colored section
                st.markdown("---")
                with st.container():
                    st.markdown(
                        """
                        <div style="background-color: #FFF3CD; border: 1px solid #FFEAA7; border-radius: 8px; padding: 16px; margin: 16px 0;">
                            <h4 style="color: #856404; margin-top: 0;">🤔 Need More Details</h4>
                            <div style="color: #856404;">
                    """, unsafe_allow_html=True)
                    
                    st.markdown(result["clarification_request"])
                    
                    st.markdown("</div></div>", unsafe_allow_html=True)
                
                # Action buttons
                st.markdown("**Choose your next step:**")
                col1, col2, col3 = st.columns([1, 1, 1])
                
                with col1:
                    if st.button("✏️ Refine Query", key="refine_btn"):
                        # Clear results and let user modify input
                        st.session_state.validation_result = None
                        st.rerun()
                
                with col2:
                    if st.button("📝 Answer Questions", key="answer_btn"):
                        # Show form for answering clarification questions
                        st.session_state.show_question_form = True
                        st.rerun()
                
                with col3:
                    if st.button("🚀 Search Anyway", key="override_btn"):
                        # Proceed with current query
                        with st.spinner("🤖 Searching listings..."):
                            try:
                                # Create a basic structured query for override
                                override_query = f"**Item Title:** {st.session_state.user_query}\n**Preferences:**\n- User provided limited details"
                                recommendations = buyer_search_workflow(override_query)
                                st.session_state["ai_recommendations"] = recommendations
                                st.session_state.validation_result = {"status": "COMPLETED"}
                            except Exception as e:
                                st.error(f"Search failed: {str(e)}")
            
                # Show question form if requested
                if st.session_state.get("show_question_form", False):
                    st.markdown("---")
                    with st.form("question_form"):
                        st.markdown("**📝 Provide Additional Details**")
                        additional_details = st.text_area(
                            "Please provide the requested information:",
                            placeholder="Answer the questions above to help us find better matches...",
                            height=100
                        )
                        
                        if st.form_submit_button("🔄 Re-validate Query"):
                            if additional_details.strip():
                                # Combine original query with additional details
                                combined_query = f"{st.session_state.user_query}\n\nAdditional details: {additional_details}"
                                
                                with st.spinner("🤖 Re-analyzing your request..."):
                                    try:
                                        st.session_state.validation_result = validate_query(combined_query)
                                        st.session_state.user_query = combined_query
                                        st.session_state.show_question_form = False
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"Re-validation failed: {str(e)}")
                            else:
                                st.warning("Please provide additional details.")
            
            elif result["status"] == "SUFFICIENT":
                # Proceed with full search workflow
                with st.spinner("🤖 Finding your perfect matches..."):
                    try:
                        recommendations = buyer_search_workflow(result["structured_query"])
                        st.session_state["ai_recommendations"] = recommendations
                        st.session_state.validation_result = {"status": "COMPLETED"}
                    except Exception as e:
                        st.error(f"Search failed: {str(e)}")
        
        # Display AI recommendations with inline buttons
        if (st.session_state.validation_result and 
            st.session_state.validation_result.get("status") == "COMPLETED" and 
            "ai_recommendations" in st.session_state):
            
            # New Search button at top right
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("---")
            with col2:
                if st.button("🔄 New Search", key="new_search_btn"):
                    # Clear all search-related session state
                    st.session_state.validation_result = None
                    st.session_state.show_question_form = False
                    if "ai_recommendations" in st.session_state:
                        del st.session_state["ai_recommendations"]
                    if "user_query" in st.session_state:
                        del st.session_state["user_query"]
                    st.rerun()
            
            # Parse recommendations and display with inline buttons
            recommendation_text = st.session_state["ai_recommendations"]
            
            # Split by recommendation sections (looking for ### numbered recommendations)
            sections = re.split(r'(### \d+\.[^\n]+)', recommendation_text)
            
            current_listing_id = None
            for section in sections:
                if section.strip():
                    st.markdown(section)
                    
                    # Check if this section contains a listing ID
                    listing_id_match = re.search(r'ID: (\d+)', section)
                    if listing_id_match:
                        current_listing_id = int(listing_id_match.group(1))
                    
                    # If we see "**[View Original]**" and have a current listing ID, add button
                    if "**[View Original]**" in section and current_listing_id:
                        # Find the listing in current listings
                        matching_listing = next((item for item in st.session_state["listings"] if item.get('id') == current_listing_id), None)
                        if matching_listing:
                            with st.expander(f"📋 View {matching_listing['title']}", expanded=False):
                                col1, col2 = st.columns([2, 1])
                                
                                with col1:
                                    st.markdown(f"### ${matching_listing['price']}")
                                    
                                    # Key details in organized format
                                    st.markdown(f"**Condition:** {matching_listing['condition']} | **Brand:** {matching_listing.get('brand', 'N/A')}")
                                    st.markdown(f"**Category:** {matching_listing['category']} | **Age:** {matching_listing.get('age', 'N/A')} months")
                                    st.markdown(f"**Location:** {matching_listing.get('university', 'N/A')} | **Seller:** {matching_listing.get('user', 'N/A')}")
                                
                                with col2:
                                    if matching_listing.get("image"):
                                        st.image(matching_listing["image"], width=150)
                                    else:
                                        st.info("No image available")
                                
                                # Description in full width below
                                if matching_listing.get('description'):
                                    st.markdown("**Description:**")
                                    st.markdown(matching_listing['description'])
                        current_listing_id = None  # Reset after using


    #Keep this in view first
    '''
    # Mandatory fix: Ensure listings is initialized
    if "listings" not in st.session_state:
        st.session_state["listings"] = []

    st.title("Browse Listings")

    if len(st.session_state.listings) == 0:
        st.info("No items available yet. Try posting one!")
    else:
        # Search + Filters
        search = st.text_input("Search items")
        category_filter = st.selectbox("Filter by Category", ["All"] + categories_list)
        condition_filter = st.selectbox("Filter by Condition", ["All", "New", "Like New", "Used", "Heavily Used"])

        # Price filter
        prices = [item.get("price", 0.0) for item in st.session_state.listings]
        if prices:
            min_price, max_price = min(prices), max(prices)
            # Prevent slider issue when only one price available
            max_price = min_price + 1 if min_price == max_price else max_price
            price_range = st.slider("Filter by Price Range ($)", min_value=float(min_price), max_value=float(max_price), value=(float(min_price), float(max_price)))
        else:
            price_range = (0.0, float("inf"))

        # Sorting option
        sort_option = st.selectbox("Sort by", ["Default", "Price: Low to High", "Price: High to Low", "Newest", "Oldest"])

        filtered_items = [item for item in st.session_state.listings if (
            (search.lower() in item.get("title", "").lower()) and 
            (category_filter == "All" or item.get("category", "") == category_filter) and 
            (condition_filter == "All" or item.get("condition", "") == condition_filter) and
            (price_range[0] <= item.get("price", 0.0) <= price_range[1])
        )]

        if sort_option == "Price: Low to High":
            filtered_items = sorted(filtered_items, key=lambda x: x.get("price", 0.0))
        elif sort_option == "Price: High to Low":
            filtered_items = sorted(filtered_items, key=lambda x: x.get("price", 0.0), reverse=True)
        elif sort_option == "Newest":
            filtered_items = sorted(filtered_items, key=lambda x: x.get("date_posted", 0), reverse=True)
        elif sort_option == "Oldest":
            filtered_items = sorted(filtered_items, key=lambda x: x.get("date_posted", 0))

        for item in filtered_items:
            # Image handling
            if item.get("image"):
                st.image(item["image"], width=150)
            else:
                st.write("No image available")
            # Title and price
            st.subheader(f"{item.get('title', 'No title')} - ${item.get('price', 0.0)}")
            st.caption(f"Category: {item.get('category', 'N/A')}")
            st.caption(f"Condition: {item.get('condition', 'Not specified')}")
            # Date formatting
            date_posted = item.get("date_posted")
            if date_posted:
                try:
                    import datetime
                    if isinstance(date_posted, datetime.datetime):
                        date_posted = date_posted.strftime("%Y-%m-%d %H:%M:%S")
                except Exception:
                    pass
                st.caption(f"Posted on: {date_posted}")
            st.caption(f"by: {item.get('user', 'Unknown')}")
            # Description handling (consistent label and spacing)
            st.markdown("**Description:**")
            st.markdown(item.get("description") or "No description provided")
            st.markdown("---")
    '''



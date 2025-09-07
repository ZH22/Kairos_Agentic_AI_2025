import streamlit as st
from commons import categories_list
from browse_ai import generate_ai_response
from db_Handler import DbHandler


def display():
    # Initialize database handler
    db = DbHandler()
    st.set_page_config(layout="wide")
    
    # Auto-refresh on page load
    if "page_loaded_browse" not in st.session_state:
        st.session_state.listings = db.get_listings()
        st.session_state.page_loaded_browse = True

    tab1, tab2 = st.tabs(["💬 Chat", "🔍 Search"])
    
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

        st.subheader("Available Listings")
        listings = st.session_state["listings"]
        if not listings:
            st.info("No items available yet.")
        else:
            cols = st.columns(2)
            for idx, item in enumerate(listings):
                with cols[idx % 2]:
                    if st.button(f"{item['title']}", key=f"card_{idx}"):
                        st.session_state["selected_item"] = idx
                    st.markdown(
                        f"""
                        <div class='listing-card'>
                            <h4>{item['title']}</h4>
                            <p><b>${item['price']}</b></p>
                            <p>{item['category']} | {item['condition']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            if "selected_item" in st.session_state:
                sel = st.session_state["selected_item"]
                st.markdown("---")
                st.subheader(listings[sel]["title"])
                if listings[sel]["image"] is not None:
                    st.image(listings[sel]["image"], width=200)
                st.write(f"Price: ${listings[sel]['price']}")
                st.write(f"Category: {listings[sel]['category']}")
                st.write(f"Condition: {listings[sel]['condition']}")
                st.write(f"Description: {listings[sel]['description']}")




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



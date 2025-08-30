import streamlit as st
from commons import categories_list

def display():
    st.title("Browse Listings")

    if len(st.session_state.listings) == 0:
        st.info("No items available yet. Try posting one!")
    else:
        # Search + Filters
        search = st.text_input("Search items")
        category_filter = st.selectbox("Filter by Category", ["All"] + categories_list)
        condition_filter = st.selectbox("Filter by Condition", ["All", "New", "Like New", "Used", "Heavily Used"])

        # Price filter
        prices = [item["price"] for item in st.session_state.listings]
        if prices:
            min_price, max_price = min(prices), max(prices)
            price_range = st.slider("Filter by Price Range ($)", min_value=float(min_price), max_value=float(max_price), value=(float(min_price), float(max_price)))
        else:
            price_range = (0.0, float("inf"))

        # Sorting option
        sort_option = st.selectbox("Sort by", ["Default", "Price: Low to High", "Price: High to Low", "Newest", "Oldest"])

        filtered_items = [item for item in st.session_state.listings if (
            (search.lower() in item["title"].lower()) and 
            (category_filter == "All" or item["category"] == category_filter) and 
            (condition_filter == "All" or item["condition"] == condition_filter) and
            (price_range[0] <= item["price"] <= price_range[1])
        )]

        if sort_option == "Price: Low to High":
            filtered_items = sorted(filtered_items, key=lambda x: x["price"])
        elif sort_option == "Price: High to Low":
            filtered_items = sorted(filtered_items, key=lambda x: x["price"], reverse=True)
        elif sort_option == "Newest":
            filtered_items = sorted(filtered_items, key=lambda x: x["date_posted"], reverse=True)
        elif sort_option == "Oldest":
            filtered_items = sorted(filtered_items, key=lambda x: x["date_posted"])

        for item in filtered_items:
            st.image(item["image"], width=150)
            st.subheader(f"{item['title']} - ${item['price']}")
            st.caption(f"Category: {item['category']}")
            st.caption(f"Condition: {item.get('condition', 'Not specified')}")
            st.caption(f"Posted on: {item['date_posted'].strftime('%Y-%m-%d %H:%M:%S')}")
            st.write(item["description"])
            st.markdown("---")



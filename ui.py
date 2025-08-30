import streamlit as st
import pandas as pd
from io import BytesIO
import datetime

# Initialize session state storage if not exists
if "listings" not in st.session_state:
    st.session_state.listings = []  # Each listing: dict with keys

# Sidebar navigation
st.sidebar.title("E-Commerce App")
page = st.sidebar.radio("Go to", ["Home", "Browse", "Post Item", "My Listings"])

# Predefined categories
categories_list = [
    "Accomodation",
    "Clothing and Accessories",
    "Everything Else",
    "Food and Drink Containers",
    "Furniture and Appliances",
    "Sports and Fitness",
    "Tech and Gadgets",
    "Textbooks and Study Materials"
]

# --- Home ---
if page == "Home":
    st.title("Welcome to Kairos 🛍️")
    st.write("A simple e-commerce prototype built with Streamlit.")

# --- Browse ---
elif page == "Browse":
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

# --- Post Item ---
elif page == "Post Item":
    st.title("Post a New Item")
    title = st.text_input("Item Title")
    image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])
    if image:
        st.image(image, width=150)
    condition = st.selectbox("Condition", ["New", "Like New", "Used", "Heavily Used"])
    category = st.selectbox("Category", categories_list)

    use_ai = st.toggle("Use AI Write up")

    description = ""
    if use_ai:
        st.info("AI Write up Mode: Type a short prompt and the AI will generate a description.")
        ai_prompt = st.text_input("Enter a prompt for AI description")
        if ai_prompt:
            # Placeholder AI generation logic
            description = f"AI generated description based on: {ai_prompt}"
            st.write(description)
    else:
        description = st.text_area("Description")

    price = st.number_input("Price ($)", min_value=0.0, format="%.2f")

    submitted = st.button("Post Item")

    if submitted:
        if title and price and category and image:
            st.session_state.listings.append({
                "title": title,
                "price": price,
                "category": category,
                "condition": condition,
                "description": description,
                "image": image,
                "date_posted": datetime.datetime.now()
            })
            st.success("Item posted successfully!")
        else:
            st.error("Please fill all fields and upload an image.")

# --- My Listings ---
elif page == "My Listings":
    st.title("My Listings")
    if len(st.session_state.listings) == 0:
        st.info("You haven't posted anything yet.")
    else:
        for idx, item in enumerate(st.session_state.listings):
            st.image(item["image"], width=150)
            title_edit = st.text_input("Title", value=item["title"], key=f"title_{idx}")
            price_edit = st.number_input("Price ($)", min_value=0.0, value=float(item["price"]), format="%.2f", key=f"price_{idx}")
            category_edit = st.selectbox("Category", categories_list, index=categories_list.index(item["category"]), key=f"cat_{idx}")
            condition_edit = st.selectbox("Condition", ["New", "Like New", "Used", "Heavily Used"], index=["New", "Like New", "Used", "Heavily Used"].index(item["condition"]), key=f"cond_{idx}")
            description_edit = st.text_area("Description", value=item["description"], key=f"desc_{idx}")
            new_image = st.file_uploader("Update Image", type=["png", "jpg", "jpeg"], key=f"img_{idx}")
            if new_image:
                st.image(new_image, width=150)

            # Save edits
            if st.button(f"Save {item['title']}", key=f"save_{idx}"):
                item["title"] = title_edit
                item["price"] = price_edit
                item["category"] = category_edit
                item["condition"] = condition_edit
                item["description"] = description_edit
                if new_image:
                    item["image"] = new_image
                st.success("Item updated successfully!")

            # Delete option
            if st.button(f"Delete {item['title']}", key=f"del_{idx}"):
                st.session_state.listings.pop(idx)
                st.success("Item deleted.")
                st.experimental_rerun()

            st.markdown("---")

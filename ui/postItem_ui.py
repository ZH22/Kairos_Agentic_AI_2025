import streamlit as st
from commons import categories_list
import datetime

def display():
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

    price = st.number_input("Price ($SGD)", min_value=0.0, format="%.2f")

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


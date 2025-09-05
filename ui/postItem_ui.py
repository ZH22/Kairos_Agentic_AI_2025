import streamlit as st
from commons import categories_list

import datetime
from commons import categories_list, condition_list
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Seller_Workflow')))
# from Collector_Polisher import Collector
from Seller_Workflow.description_writer import Writer
def display():

    st.title("Post a New Item")



    user = st.text_input("User", value=st.session_state.get("user"), disabled=True)
    title = st.text_input("Item Title", help="Enter a clear, descriptive title for your item.")
    image = st.file_uploader("Upload Image (optional)", type=["png", "jpg", "jpeg"], help="Max 5MB. JPG, PNG only.")
    if image:
        if image.size > 5 * 1024 * 1024:
            st.warning("Image file is too large (max 5MB). Please upload a smaller image.")
            image = None
        else:
            st.image(image, width=150)
    category = st.selectbox("Category", categories_list, help="Select the most relevant category.")
    condition = st.selectbox("Condition", condition_list, help="Describe the item's condition.")
    original_price = st.number_input("Original Price ($SGD)", min_value=0.0, format="%.2f", help="What did you pay for this item when new?")
    price = st.number_input("Price ($SGD)", min_value=0.0, format="%.2f", help="Your asking price.")
    age = st.number_input("Age (in months)", min_value=0, step=1, format="%d", help="How long have you used this item?")
    brand = st.text_input("Brand (optional)", help="Brand or manufacturer (if relevant).")
    reason = st.text_area("Reason for Selling (optional)", help="Why are you selling this item?")
    price_negotiable = st.selectbox("Is the price negotiable?", ["Yes", "No"], help="Are you open to offers?")
    university = st.selectbox("University/Campus", ["NUS", "NTU", "SMU", "Off campus"], help="Select your university or campus.")
    address = st.text_input("Specific Location (Block/Room)", help="E.g., Block 12, Room 101, or area on campus.")
    delivery_option = st.selectbox("Delivery Option", ["Buyer Pickup", "Seller Delivery", "Third-party Delivery", "Other"], help="How will the item be delivered?")
    custom_delivery_option = ""
    if delivery_option == "Other":
        custom_delivery_option = st.text_input("Please describe your delivery option", help="Describe your custom delivery arrangement.")

    # Store all data fields in a dictionary before Item Description
    item_data_for_writer = {
        "user": user,
        "title": title,
        "price": price,
        "original_price": original_price,
        "age": age,
        "reason": reason,
        "brand": brand,
        "price_negotiable": price_negotiable,
        "university": university,
        "address": address,
        "delivery_option": custom_delivery_option if delivery_option == "Other" else delivery_option,
        "category": category,
        "condition": condition,
        "description": "",  # Let AI generate this
        "image": image if image else None,
        "date_posted": datetime.datetime.now()
    }

    st.markdown("---")
    st.subheader("Item Description")
    use_ai = st.toggle("Use AI Write up")
    description = ""
    def get_missing_fields():
        missing = []
        if not title:
            missing.append("Item Title")
        if not price:
            missing.append("Price")
        if not category:
            missing.append("Category")
        if not user:
            missing.append("User")
        if not condition:
            missing.append("Condition")
        if not original_price:
            missing.append("Original Price")
        if not age:
            missing.append("Age")
        return missing

    if use_ai:
        st.info(
            "AI Write up Mode: You can use the default prompt or enter your own. "
            "The default prompt is: 'Generate a compelling description for this item listing.' "
            "You may leave the prompt unchanged to use the default, or modify it as you wish."
        )
        ai_prompt = st.text_input(
            "Enter a prompt for AI description (or use the default below)",
            value="Generate a compelling description for this item listing."
        )
        missing_fields = get_missing_fields()
        generate_ai = st.button("Generate Description with AI")
        if 'ai_description' not in st.session_state:
            st.session_state['ai_description'] = ""
        if generate_ai:
            if missing_fields:
                st.warning(f"Please fill all required fields before generating an AI description. Missing: {', '.join(missing_fields)}")
            elif ai_prompt:
                writer_agent = Writer()  # Use new class definition
                complete_prompt = writer_agent.fill_prompt(item_data_for_writer, ai_prompt)
                with st.spinner("Generating AI description..."):
                    st.session_state['ai_description'] = writer_agent.write(complete_prompt)
        # Show the AI-generated description in a single editable text area after generation
        if st.session_state['ai_description']:
            description = st.text_area(
                "AI Generated Description (you can edit before posting)",
                value=st.session_state['ai_description'],
                key="editable_description"
            )
        else:
            description = ""
    else:
        description = st.text_area("Description")
    
    submitted = st.button("Post Item")
    
    if submitted:
        missing_fields = get_missing_fields()
        if delivery_option == "Other" and not custom_delivery_option.strip():
            st.error("Please describe your delivery option if you select 'Other'.")
        elif missing_fields:
            st.error(f"Please fill all required fields. Missing: {', '.join(missing_fields)}")
            if(not user):
                print(user)
                st.error("User not defined. Please head to home to select")
        else:
            item_data = {
                "user": user,
                "title": title,
                "price": price,
                "original_price": original_price,
                "age": age,
                "reason": reason,
                "brand": brand,
                "price_negotiable": price_negotiable,
                "university": university,
                "address": address,
                "delivery_option": custom_delivery_option if delivery_option == "Other" else delivery_option,
                "category": category,
                "condition": condition,
                "description": description,
                "image": image if image else None,
                "date_posted": datetime.datetime.now()
            }
            st.session_state.listings.append(item_data)
            st.success("Item posted successfully!")


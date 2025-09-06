import streamlit as st
from commons import categories_list
from demo_data import get_demo_data

import datetime
from commons import categories_list
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Seller_Workflow')))
# from Collector_Polisher import Collector
from Seller_Workflow.description_writer import Writer
def display():

    st.title("Post a New Item")
    
    # Demo button
    if st.button("🎯 Fill Demo Data (Portable Aircon)", help="Click to fill all fields with sample data for testing"):
        demo_data = get_demo_data()
        for key, value in demo_data.items():
            st.session_state[f"demo_{key}"] = value
        st.rerun()

    user = st.text_input("User", value=st.session_state.get("user"), disabled=True)
    title = st.text_input("Item Title", value=st.session_state.get("demo_title", ""), help="Enter a clear, descriptive title for your item.")
    image = st.file_uploader("Upload Image (optional)", type=["png", "jpg", "jpeg"], help="Max 5MB. JPG, PNG only.")
    if image:
        if image.size > 5 * 1024 * 1024:
            st.warning("Image file is too large (max 5MB). Please upload a smaller image.")
            image = None
        else:
            st.image(image, width=150)
    demo_category = st.session_state.get("demo_category", categories_list[0])
    category_index = categories_list.index(demo_category) if demo_category in categories_list else 0
    category = st.selectbox("Category", categories_list, index=category_index, help="Select the most relevant category.")
    condition_options = ["New", "Like New", "Used", "Heavily Used"]
    demo_condition = st.session_state.get("demo_condition", "New")
    condition_index = condition_options.index(demo_condition) if demo_condition in condition_options else 0
    condition = st.selectbox("Condition", condition_options, index=condition_index, help="Describe the item's condition.")
    original_price = st.number_input("Original Price ($SGD)", min_value=0.0, value=st.session_state.get("demo_original_price", 0.0), format="%.2f", help="What did you pay for this item when new?")
    price = st.number_input("Price ($SGD)", min_value=0.0, value=st.session_state.get("demo_price", 0.0), format="%.2f", help="Your asking price.")
    age = st.number_input("Age (in months)", min_value=0, value=st.session_state.get("demo_age", 0), step=1, format="%d", help="How long have you used this item?")
    brand = st.text_input("Brand (optional)", value=st.session_state.get("demo_brand", ""), help="Brand or manufacturer (if relevant).")
    reason = st.text_area("Reason for Selling (optional)", value=st.session_state.get("demo_reason", ""), help="Why are you selling this item?")
    negotiable_options = ["Yes", "No"]
    demo_negotiable = st.session_state.get("demo_price_negotiable", "Yes")
    negotiable_index = negotiable_options.index(demo_negotiable) if demo_negotiable in negotiable_options else 0
    price_negotiable = st.selectbox("Is the price negotiable?", negotiable_options, index=negotiable_index, help="Are you open to offers?")
    
    university_options = ["NUS", "NTU", "SMU", "Off campus"]
    demo_university = st.session_state.get("demo_university", "NUS")
    university_index = university_options.index(demo_university) if demo_university in university_options else 0
    university = st.selectbox("University/Campus", university_options, index=university_index, help="Select your university or campus.")
    
    address = st.text_input("Specific Location (Block/Room)", value=st.session_state.get("demo_address", ""), help="E.g., Block 12, Room 101, or area on campus.")
    
    delivery_options = ["Buyer Pickup", "Seller Delivery", "Third-party Delivery", "Other"]
    demo_delivery = st.session_state.get("demo_delivery_option", "Buyer Pickup")
    delivery_index = delivery_options.index(demo_delivery) if demo_delivery in delivery_options else 0
    delivery_option = st.selectbox("Delivery Option", delivery_options, index=delivery_index, help="How will the item be delivered?")
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
    
    if st.button("Evaluate Your Deal!"):
        missing_fields = get_missing_fields()
        if missing_fields:
            st.error(f"Please fill all required fields before evaluation. Missing: {', '.join(missing_fields)}")
        else:
            # Store user_info in session state for DE_ui to use
            st.session_state.user_info = {
                "title": title,
                "brand": brand,
                "category": category,
                "condition": condition,
                "age": age,
                "original_price": original_price,
                "price": price,
                "reason": reason,
                "price_negotiable": price_negotiable
            }
            st.session_state.page = "evaluation"
            st.rerun()
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


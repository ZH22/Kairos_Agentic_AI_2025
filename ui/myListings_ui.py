import streamlit as st
from commons import categories_list
from db_Handler import DbHandler

def display():
    # Initialize database handler
    db = DbHandler()
    
    # Always sync with database on page load
    st.session_state.listings = db.get_listings()
    
    current_user = st.session_state.get("user")
    if (not current_user):
        st.error("No User selected. Head to Home to select")

    st.title("My Listings")
    # Filter listings for current user
    print(current_user)
    user_listings = [item for item in st.session_state.listings if item.get("user") == current_user]
    
    if len(user_listings) == 0:
        st.info("You haven't posted anything yet.")
    else:
        listing_count = 0
        cols = st.columns(2)

        for idx, item in enumerate(user_listings):
            with cols[idx % 2]:
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
                if item.get("image"):
                    st.image(item["image"], width=150)
                else:
                    st.write("No image available")

                if st.button(f"Edit {item['title']}", key=f"edit_{idx}"):
                    title_edit = st.text_input("Title", value=item.get("title", ""), key=f"title_{idx}")
                    price_edit = st.number_input("Price ($)", min_value=0.0, value=float(item.get("price", 0.0)), format="%.2f", key=f"price_{idx}")
                    category_edit = st.selectbox("Category", categories_list, index=categories_list.index(item.get("category", categories_list[0])), key=f"cat_{idx}")
                    condition_edit = st.selectbox("Condition", ["New", "Like New", "Used", "Heavily Used"], index=["New", "Like New", "Used", "Heavily Used"].index(item.get("condition", "New")), key=f"cond_{idx}")
                    description_edit = st.text_area("Description", value=item.get("description", "No description provided"), key=f"desc_{idx}")
                    new_image = st.file_uploader("Re-upload Image", type=["png", "jpg", "jpeg"], key=f"image_{idx}")
                    if new_image:
                        st.image(new_image, width=150)
                    if st.button("Save Changes", key=f"save_{idx}"):
                        user_listings[idx]["title"] = new_title
                        user_listings[idx]["price"] = new_price
                        user_listings[idx]["category"] = new_category
                        user_listings[idx]["condition"] = new_condition
                        user_listings[idx]["description"] = new_description
                        if new_image:
                            user_listings[idx]["image"] = new_image

                        # Update in database
                        db = DbHandler()
                        db.update_listing_in_db(item, item['id'])
                        # Reset page flags to trigger refresh
                        if "page_loaded_browse" in st.session_state:
                            del st.session_state.page_loaded_browse
                        st.success("Item updated in database!")

                # Delete option with confirmation
                delete_key = f"delete_confirm_{idx}"
                if delete_key not in st.session_state:
                    st.session_state[delete_key] = False
                    
                if not st.session_state[delete_key]:
                    if st.button(f"Delete {item.get('title', 'Item')}", key=f"del_{idx}"):
                        st.session_state[delete_key] = True
                        st.rerun()
                else:
                    st.warning(f"⚠️ Are you sure you want to delete '{item.get('title', 'Item')}'? This cannot be undone.")
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("✅ Yes, Delete", key=f"confirm_{idx}"):
                            db = DbHandler()
                            listing_id = item.get('id')
                            if listing_id and db.delete_listing_by_id(listing_id, current_user):
                                # Refresh from database
                                st.session_state.listings = db.get_listings()
                                # Reset page flags
                                if "page_loaded_browse" in st.session_state:
                                    del st.session_state.page_loaded_browse
                                st.success("Item deleted successfully!")
                            else:
                                st.error("Failed to delete item. You may not have permission.")
                            st.session_state[delete_key] = False
                            st.rerun()
                    with col2:
                        if st.button("❌ Cancel", key=f"cancel_{idx}"):
                            st.session_state[delete_key] = False
                            st.rerun()

                # Date formatting
                date_posted = item.get("date_posted")
                if date_posted:
                    try:
                        import datetime
                        if isinstance(date_posted, datetime.datetime):
                            date_posted = date_posted.strftime("%Y-%m-%d %H:%M")
                    except Exception:
                        pass
                    st.write(f"**Posted:** {date_posted}")

                st.markdown("---")

                listing_count += 1

        if listing_count == 0:
            st.info("You don't have any listings")
            
'''
            # Image handling
            if item.get("image"):
                st.image(item["image"], width=150)
            else:
                st.write("No image available")
            title_edit = st.text_input("Title", value=item.get("title", ""), key=f"title_{idx}")
            price_edit = st.number_input("Price ($)", min_value=0.0, value=float(item.get("price", 0.0)), format="%.2f", key=f"price_{idx}")
            category_edit = st.selectbox("Category", categories_list, index=categories_list.index(item.get("category", categories_list[0])), key=f"cat_{idx}")
            condition_edit = st.selectbox("Condition", ["New", "Like New", "Used", "Heavily Used"], index=["New", "Like New", "Used", "Heavily Used"].index(item.get("condition", "New")), key=f"cond_{idx}")
            description_edit = st.text_area("Description", value=item.get("description", "No description provided"), key=f"desc_{idx}")
            # Preview formatted description
            st.markdown("**Preview:**")
            st.markdown(description_edit or "No description provided")
            new_image = st.file_uploader("Update Image", type=["png", "jpg", "jpeg"], key=f"img_{idx}")
            if new_image:
                st.image(new_image, width=150)

            # Save edits
            if st.button(f"Save {item.get('title', 'Item')}", key=f"save_{idx}"):
                item["title"] = title_edit
                item["price"] = price_edit
                item["category"] = category_edit
                item["condition"] = condition_edit
                item["description"] = description_edit
                if new_image:
                    item["image"] = new_image
'''
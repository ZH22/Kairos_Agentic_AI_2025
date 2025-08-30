import streamlit as st
from commons import categories_list

def display():
    current_user = st.session_state.get("user")
    if (not current_user):
        st.error("No User selected. Head to Home to select")

    st.title("My Listings")
    if len(st.session_state.listings) == 0:
        st.info("You haven't posted anything yet.")
    else:
        # Count number of listings for that user (To change to database call after this)
        listing_count = 0

        for idx, item in enumerate(st.session_state.listings):
            if(item["user"] != st.session_state.get("user")):
                continue
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

            listing_count += 1

        if (listing_count == 0):
            st.info("You don't have any listings")
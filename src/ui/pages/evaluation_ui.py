import streamlit as st
import sys
import os
import time
from src.ai_workflows.seller.market_agents import WebsearchAgent, MarketAnalyzer
from src.ai_workflows.seller.synthesis_agent import SynthesisAgent
from contextlib import contextmanager

def display():
    # Hide sidebar for evaluation page
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

    # 1. Header with Home button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("Deal Evaluation")
    with col2:
        if st.button("🏠 Home"):
            st.session_state.show_home_confirm = True
            st.rerun()
    
    # Confirmation dialog
    if st.session_state.get("show_home_confirm", False):
        st.warning("⚠️ Are you sure you want to go home? All unsaved changes will be lost.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Go Home"):
                st.session_state.active_page = "Home"
                st.session_state.show_home_confirm = False
                st.rerun()
        with col2:
            if st.button("❌ Cancel"):
                st.session_state.show_home_confirm = False
                st.rerun()

    # 2. Explaining text
    st.markdown("""
    This page helps you assess how marketable your item is, and whether your offer is competitive in the current market.

    When you click **Start Evaluation**, an agentic workflow will search the web for similar listings, analyze your offer, and generate a detailed report to help you make informed decisions.
    """)

    # 3. Start Evaluation button
    if st.button("Start Evaluation"):
        user_info = st.session_state.get("user_info")
        if not user_info:
            st.error("No item data found. Please go back to Post Item and fill out the form first.")
        else:
            # Progress bar container
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Convert user_info dict to formatted prompt
                user_info_prompt = f"""
Item: {user_info.get('title', 'N/A')}
Brand: {user_info.get('brand', 'N/A')}
Category: {user_info.get('category', 'N/A')}
Condition: {user_info.get('condition', 'N/A')}
Age: {user_info.get('age', 0)} months
Asking Price: ${user_info.get('price', 0):.2f} SGD
Reason for Selling: {user_info.get('reason', 'N/A')}
Price Negotiable: {user_info.get('price_negotiable', 'N/A')}
"""
                
                # Step 1: Web Search (0-33%)
                status_text.text("🔍 Searching for similar listings...")
                progress_bar.progress(10)
                
                @contextmanager
                def suppress_output():
                    with open(os.devnull, 'w') as devnull:
                        old_stdout = sys.stdout
                        old_stderr = sys.stderr
                        try:
                            sys.stdout = devnull
                            sys.stderr = devnull
                            yield
                        finally:
                            sys.stdout = old_stdout
                            sys.stderr = old_stderr
                
                with suppress_output():
                    web_agent = WebsearchAgent()
                    web_report = web_agent.search(user_info_prompt)
                
                progress_bar.progress(33)
                
                # Step 2: Market Analysis (33-66%)
                status_text.text("📊 Analyzing market data...")
                time.sleep(0.5)
                
                with suppress_output():
                    analyzer = MarketAnalyzer()
                    key_points = analyzer.analyze(web_report)
                
                progress_bar.progress(66)
                
                # Step 3: Synthesis (66-100%)
                status_text.text("💡 Generating recommendations...")
                time.sleep(0.5)
                
                synthesis = SynthesisAgent()
                final_report = synthesis.synthesize(user_info_prompt, key_points)
                
                progress_bar.progress(100)
                status_text.text("✅ Evaluation complete!")
                
                st.session_state["de_report"] = final_report
                
            except Exception as e:
                st.session_state["de_report"] = f"Error during evaluation: {str(e)}"
                status_text.text("❌ Evaluation failed")
                progress_bar.progress(0)

    # 4. Analysis Report and Edit section after evaluation
    report = st.session_state.get("de_report", "")
    if report:
        # Initialize edit mode state
        if "edit_mode" not in st.session_state:
            st.session_state.edit_mode = False
        if "changes_saved" not in st.session_state:
            st.session_state.changes_saved = True
        
        # Analysis Report
        st.subheader("📊 Analysis Report")
        
        # Report display
        with st.container():
            st.markdown(
                f"""
                <div style="
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 4px solid #4CAF50;
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    line-height: 1.6;
                    max-height: 400px;
                    overflow-y: auto;
                    margin-bottom: 20px;
                ">
                {report}
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Edit Offer button below report
        if st.button("✏️ Edit Offer"):
            st.session_state.edit_mode = True
            st.rerun()
        
        # Edit Your Offer section below
        st.subheader("📝 Edit Your Offer")
        user_info = st.session_state.get("user_info", {})
        
        col1, col2 = st.columns(2)
        with col1:
            new_title = st.text_input("Item Title", value=user_info.get('title', ''), disabled=not st.session_state.edit_mode)
            new_price = st.number_input("Asking Price ($SGD)", min_value=0.0, value=user_info.get('price', 0.0), format="%.2f", disabled=not st.session_state.edit_mode)
            new_condition = st.selectbox("Condition", ["New", "Like New", "Used", "Heavily Used"], 
                                       index=["New", "Like New", "Used", "Heavily Used"].index(user_info.get('condition', 'New')), disabled=not st.session_state.edit_mode)
        
        with col2:
            new_age = st.number_input("Age (months)", min_value=0, value=user_info.get('age', 0), step=1, disabled=not st.session_state.edit_mode)
            new_negotiable = st.selectbox("Price Negotiable?", ["Yes", "No"], 
                                        index=["Yes", "No"].index(user_info.get('price_negotiable', 'Yes')), disabled=not st.session_state.edit_mode)
        
        new_reason = st.text_area("Reason for Selling", value=user_info.get('reason', ''), disabled=not st.session_state.edit_mode)
        
        # Action buttons at bottom
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Save button (only show in edit mode)
            if st.session_state.edit_mode:
                if st.button("💾 Save Changes", use_container_width=True):
                    updated_info = user_info.copy()
                    updated_info.update({
                        'title': new_title,
                        'price': new_price,
                        'condition': new_condition,
                        'age': new_age,
                        'price_negotiable': new_negotiable,
                        'reason': new_reason
                    })
                    st.session_state.user_info = updated_info
                    st.session_state.edit_mode = False
                    st.session_state.changes_saved = True
                    st.success("Changes saved!")
                    st.rerun()
        
        with col2:
            # Update Analysis button
            update_disabled = st.session_state.edit_mode or not st.session_state.changes_saved
            if st.button("🔄 Update Analysis", disabled=update_disabled, use_container_width=True):
                if update_disabled:
                    if st.session_state.edit_mode:
                        st.warning("Please save changes first")
                    else:
                        st.warning("No changes to analyze")
                else:
                    # Re-run evaluation logic here (same as before)
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        user_info_prompt = f"""
Item: {user_info.get('title', 'N/A')}
Brand: {user_info.get('brand', 'N/A')}
Category: {user_info.get('category', 'N/A')}
Condition: {user_info.get('condition', 'N/A')}
Age: {user_info.get('age', 0)} months
Asking Price: ${user_info.get('price', 0):.2f} SGD
Reason for Selling: {user_info.get('reason', 'N/A')}
Price Negotiable: {user_info.get('price_negotiable', 'N/A')}
"""
                        
                        status_text.text("🔍 Re-analyzing...")
                        progress_bar.progress(33)
                        
                        @contextmanager
                        def suppress_output():
                            with open(os.devnull, 'w') as devnull:
                                old_stdout = sys.stdout
                                old_stderr = sys.stderr
                                try:
                                    sys.stdout = devnull
                                    sys.stderr = devnull
                                    yield
                                finally:
                                    sys.stdout = old_stdout
                                    sys.stderr = old_stderr
                        
                        with suppress_output():
                            web_agent = WebsearchAgent()
                            web_report = web_agent.search(user_info_prompt)
                            analyzer = MarketAnalyzer()
                            key_points = analyzer.analyze(web_report)
                        
                        progress_bar.progress(66)
                        synthesis = SynthesisAgent()
                        final_report = synthesis.synthesize(user_info_prompt, key_points)
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Analysis updated!")
                        st.session_state["de_report"] = final_report
                        st.session_state.changes_saved = False
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Update failed: {str(e)}")
        
        with col3:
            # Post Item button
            if st.button("📤 Post This Item", use_container_width=True):
                import datetime
                from src.core.db_handler import DbHandler
                
                item_data = st.session_state.user_info.copy()
                item_data.update({
                    "user": st.session_state.get("user", "Unknown"),
                    "university": "NUS",
                    "address": "",
                    "delivery_option": "Buyer Pickup",
                    "description": "Item posted from evaluation page",
                    "image": None,
                    "date_posted": datetime.datetime.now()
                })
                
                # Save to database
                try:
                    db = DbHandler()
                    db.save_listing_to_db(item_data)
                    
                    # Refresh listings and reset page flags
                    st.session_state.listings = db.get_listings()
                    if "page_loaded_mylistings" in st.session_state:
                        del st.session_state.page_loaded_mylistings
                    if "page_loaded_browse" in st.session_state:
                        del st.session_state.page_loaded_browse
                    
                    st.success("Item posted successfully!")
                    st.balloons()
                    
                    # Navigate back to home page
                    st.session_state.active_page = "Home"
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Failed to post item: {str(e)}")
    else:
        # Initial state - show original layout
        st.write("Click 'Start Evaluation' to begin the analysis.")

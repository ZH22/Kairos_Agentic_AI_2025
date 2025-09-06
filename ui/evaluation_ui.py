import streamlit as st
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Seller_Workflow')))
from market_agents import WebsearchAgent, MarketAnalyzer
from synthesis_agent import SynthesisAgent
from contextlib import contextmanager

def display():
    # Hide sidebar for evaluation page
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {display: none;}
        </style>
    """, unsafe_allow_html=True)

    # 1. Header
    st.title("Deal Evaluation")

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
                    web_result = web_agent.search(user_info_prompt)
                    web_report = str(web_result) if hasattr(web_result, '__str__') else web_result
                
                progress_bar.progress(33)
                
                # Step 2: Market Analysis (33-66%)
                status_text.text("📊 Analyzing market data...")
                time.sleep(0.5)
                
                with suppress_output():
                    analyzer = MarketAnalyzer()
                    key_result = analyzer.analyze(web_report)
                    key_points = str(key_result) if hasattr(key_result, '__str__') else key_result
                
                progress_bar.progress(66)
                
                # Step 3: Synthesis (66-100%)
                status_text.text("💡 Generating recommendations...")
                time.sleep(0.5)
                
                synthesis = SynthesisAgent()
                final_result = synthesis.synthesize(user_info_prompt, key_points)
                final_report = str(final_result) if hasattr(final_result, '__str__') else final_result
                
                progress_bar.progress(100)
                status_text.text("✅ Evaluation complete!")
                
                st.session_state["de_report"] = final_report
                
            except Exception as e:
                st.session_state["de_report"] = f"Error during evaluation: {str(e)}"
                status_text.text("❌ Evaluation failed")
                progress_bar.progress(0)

    # 4. Side-by-side layout after evaluation
    report = st.session_state.get("de_report", "")
    if report:
        col1, col2 = st.columns([1, 2])
        
        # Initialize edit mode state
        if "edit_mode" not in st.session_state:
            st.session_state.edit_mode = False
        if "changes_saved" not in st.session_state:
            st.session_state.changes_saved = True
            
        with col1:
            st.subheader("📝 Edit Your Offer")
            user_info = st.session_state.get("user_info", {})
            
            # Editable fields (disabled unless in edit mode)
            new_title = st.text_input("Item Title", value=user_info.get('title', ''), disabled=not st.session_state.edit_mode)
            new_price = st.number_input("Asking Price ($SGD)", min_value=0.0, value=user_info.get('price', 0.0), format="%.2f", disabled=not st.session_state.edit_mode)
            new_condition = st.selectbox("Condition", ["New", "Like New", "Used", "Heavily Used"], 
                                       index=["New", "Like New", "Used", "Heavily Used"].index(user_info.get('condition', 'New')), disabled=not st.session_state.edit_mode)
            new_age = st.number_input("Age (months)", min_value=0, value=user_info.get('age', 0), step=1, disabled=not st.session_state.edit_mode)
            new_negotiable = st.selectbox("Price Negotiable?", ["Yes", "No"], 
                                        index=["Yes", "No"].index(user_info.get('price_negotiable', 'Yes')), disabled=not st.session_state.edit_mode)
            new_reason = st.text_area("Reason for Selling", value=user_info.get('reason', ''), disabled=not st.session_state.edit_mode)
            
            # Save button (only show in edit mode)
            if st.session_state.edit_mode:
                if st.button("💾 Save Changes"):
                    # Update user_info with new values
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
            
            # Update Analysis button (only enabled if changes are saved and not in edit mode)
            update_disabled = st.session_state.edit_mode or not st.session_state.changes_saved
            if st.button("🔄 Update Analysis", disabled=update_disabled):
                if update_disabled:
                    if st.session_state.edit_mode:
                        st.warning("Please save changes first")
                    else:
                        st.warning("No changes to analyze")
                else:
                    # Re-run evaluation with saved info
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        user_info_prompt = f"""
Item: {updated_info.get('title', 'N/A')}
Brand: {updated_info.get('brand', 'N/A')}
Category: {updated_info.get('category', 'N/A')}
Condition: {updated_info.get('condition', 'N/A')}
Age: {updated_info.get('age', 0)} months
Asking Price: ${updated_info.get('price', 0):.2f} SGD
Reason for Selling: {updated_info.get('reason', 'N/A')}
Price Negotiable: {updated_info.get('price_negotiable', 'N/A')}
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
                            web_result = web_agent.search(user_info_prompt)
                            web_report = str(web_result) if hasattr(web_result, '__str__') else web_result
                            analyzer = MarketAnalyzer()
                            key_result = analyzer.analyze(web_report)
                            key_points = str(key_result) if hasattr(key_result, '__str__') else key_result
                        
                        progress_bar.progress(66)
                        synthesis = SynthesisAgent()
                        final_result = synthesis.synthesize(user_info_prompt, key_points)
                        final_report = str(final_result) if hasattr(final_result, '__str__') else final_result
                        
                        progress_bar.progress(100)
                        status_text.text("✅ Analysis updated!")
                        st.session_state["de_report"] = final_report
                        st.session_state.changes_saved = False  # Mark as analyzed
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Update failed: {str(e)}")
        
        with col2:
            # Edit Offer button at top of right column
            if st.button("✏️ Edit Offer"):
                st.session_state.edit_mode = True
                st.rerun()
                
            st.subheader("📊 Analysis Report")
            st.markdown("""
                <div style='border: 2px solid #4CAF50; border-radius: 8px; min-height: 400px; padding: 16px; background-color: #f8fff8;'>
            """, unsafe_allow_html=True)
            st.markdown(report)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Post Item button at bottom of right column
            if st.button("📤 Post This Item"):
                # Add current offer to listings
                import datetime
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
                if "listings" not in st.session_state:
                    st.session_state.listings = []
                st.session_state.listings.append(item_data)
                st.success("Item posted successfully!")
                st.balloons()
    else:
        # Initial state - show original layout
        st.markdown("""
            <div style='border: 2px solid #4CAF50; border-radius: 8px; min-height: 200px; padding: 16px; margin-top: 24px; background-color: #f8fff8;'>
        """, unsafe_allow_html=True)
        st.write("Click 'Start Evaluation' to begin the analysis.")
        st.markdown("</div>", unsafe_allow_html=True)

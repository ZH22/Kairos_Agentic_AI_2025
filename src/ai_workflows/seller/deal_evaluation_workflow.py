"""
Deal Evaluation Workflow Orchestration
- Runs the multi-agent workflow for evaluating a user's item sale offer.
- Agents: WebsearchAgent, MarketAnalyzer, SynthesisAgent
"""

import sys
import os
from contextlib import contextmanager
from market_agents import WebsearchAgent, MarketAnalyzer
from synthesis_agent import SynthesisAgent

@contextmanager
def suppress_output():
    """Context manager to suppress stdout and stderr during agent execution"""
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


def deal_evaluation_workflow(user_info: dict):
    """
    Orchestrates the deal evaluation workflow.
    Args:
        user_info: dict, user's item data from postItem_ui
    Returns:
        final_report: str, the synthesized evaluation report for the user
    """
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

    # 1. Websearch Agent (silent execution)
    with suppress_output():
        web_agent = WebsearchAgent()
        web_result = web_agent.search(user_info_prompt)
        web_report = str(web_result) if hasattr(web_result, '__str__') else web_result

    # 2. Market Analyzer with internal DB tool access (silent execution)
    with suppress_output():
        analyzer = MarketAnalyzer()
        key_result = analyzer.analyze(web_report, user_info_prompt)
        key_points = str(key_result) if hasattr(key_result, '__str__') else key_result

    # 3. Synthesis Agent (only this output is returned to user)
    synthesis = SynthesisAgent()
    final_result = synthesis.synthesize(user_info_prompt, key_points)
    final_report = str(final_result) if hasattr(final_result, '__str__') else final_result

    return final_report

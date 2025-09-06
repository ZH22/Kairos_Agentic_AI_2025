"""
Test script for Market Agents (WebsearchAgent and MarketAnalyzer with internal_db_search tool)

'Callback = True' here, so you can see results from each stage
"""
from market_agents import WebsearchAgent, MarketAnalyzer

# Example fake user_info prompt (plain text)
fake_user_info_prompt = """
Brand: Sony
Product: Wireless Headphones
Condition: Like New
Age: 6 months
Price: $120
Category: Electronics
Reason for Selling: Upgraded to a new model
University: NUS
Delivery Option: Buyer Pickup
"""

def main():
    print("=== Testing WebsearchAgent ===")
    web_agent = WebsearchAgent()
    web_report = web_agent.search(fake_user_info_prompt)
    print("WebsearchAgent Output:")
    print(web_report)

    print("\n=== Testing MarketAnalyzer with internal_db_search tool ===")
    analyzer = MarketAnalyzer()
    key_points = analyzer.analyze(web_report, fake_user_info_prompt)
    print("MarketAnalyzer Output (with internal DB tool access):")
    print(key_points)

if __name__ == "__main__":
    main()

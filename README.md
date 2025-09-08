# Kairos Agentic AI Campus Connector 2025

AI-powered university marketplace connector with semantic search, market analysis, and direct student-to-student connections.

## Features

### 🤖 AI-Powered Workflows
- **Deal Evaluation**: Multi-agent system analyzing external + internal market data
- **Smart Description Writer**: AI-generated compelling listing descriptions
- **Semantic Search**: Vector-based similarity matching for listings
- **Market Analysis**: Web search + internal database comparison

### 💾 Database Integration
- **Persistent Storage**: Supabase database with cross-session data persistence
- **Vector Search**: AWS Bedrock embeddings for semantic listing discovery
- **Auto-Sync**: Real-time synchronization across all pages
- **Secure Operations**: Ownership validation for edit/delete actions

### 🎯 User Experience
- **Multi-User Support**: Switch between Adam, Bob, Charlie profiles
- **Auto-Refresh**: Seamless data updates without manual refresh
- **Direct Contact**: Connect students with sellers for safe campus transactions
- **Demo Data**: Quick-fill functionality for testing

## Setup

### Prerequisites
- Python 3.12+
- Supabase account
- AWS account with Bedrock access
- Tavily API key (for web search)

### Database Setup
1. Create new Supabase project
2. Enable 'vector' extension in Database settings
3. Run database migrations (tables created automatically)

### Installation
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables
Create `.env` file:
```env
# AWS Credentials
AWS_ACCESS_KEY_ID=<your_aws_key>
AWS_SECRET_ACCESS_KEY=<your_aws_secret>
AWS_REGION=us-east-1

# Supabase
SUPABASE_URL=<your_supabase_url>
SUPABASE_KEY=<your_supabase_anon_key>
DB_CONNECTION=<your_supabase_db_connection_string>

# AI Models
EMBED_MODEL_SMALL=amazon.titan-embed-text-v1
TAVILY_ACCESS_KEY=<your_tavily_key>
```

### First-Time Setup
```bash
# Populate vector store with existing data (if any)
python populate_vector_store.py

# Run the application
streamlit run ui.py
```

## Usage

### Core Workflows
1. **Discover Items**: Find what you need with AI-powered semantic search
2. **List Items**: Share what you're offering with AI description generation
3. **My Listings**: Manage your posted items with edit/delete capabilities
4. **Market Analysis**: Get AI-powered insights for fair pricing decisions

### AI Features
- **Smart Descriptions**: Toggle AI writeup when listing items
- **Market Intelligence**: Compare your item against web + campus market data
- **Semantic Discovery**: Find exactly what you need using natural language
- **Fair Pricing**: AI-suggested pricing based on market analysis

## Architecture

### Database Layer (`db_Handler.py`)
- Supabase integration for persistent storage
- Vector store management for semantic search
- CRUD operations with ownership validation

### AI Workflow (`Seller_Workflow/`)
- **Market Agents**: Web search + internal database analysis
- **Description Writer**: AI-powered listing generation
- **Deal Evaluation**: Multi-agent workflow for pricing decisions

### UI Components (`ui/`)
- **Modular Design**: Separate files for each page
- **Auto-Sync**: Database integration across all components
- **Real-time Updates**: Seamless data synchronization

## Testing

```bash
# Test database operations
python test_db_handler.py

# Test AI workflows
python Seller_Workflow/test_market_agents.py
```

## Project Structure

```
Kairos_Agentic_AI_2025/
├── db_Handler.py              # Database integration
├── ui.py                      # Main Streamlit app
├── ui/                        # UI components
│   ├── browse_ui.py          # Browse listings page
│   ├── postItem_ui.py        # Post new items
│   ├── myListings_ui.py      # Manage user listings
│   └── evaluation_ui.py      # Deal evaluation page
├── Seller_Workflow/          # AI agent workflows
│   ├── market_agents.py      # Market analysis agents
│   ├── description_writer.py # AI description generation
│   └── deal_evaluation_workflow.py # Multi-agent evaluation
├── helper_scripts/           # Utility functions
└── test_*.py                 # Test suites
```


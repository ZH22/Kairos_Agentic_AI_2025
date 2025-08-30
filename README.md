### Setting up
(Assumes your system has python3.12 installed
1. Create virtual environment
2. Activate virtual environment

(Supabase Portion)
- Create new Project 
- Enable 'vector' option in Database

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```
3. Add credentials
```
AWS_ACCESS_KEY_ID=<token>
AWS_SECRET_ACCESS_KEY=<token>
AWS_REGION=us-east-1
```

### Running Project Locally
```bash
streamlit run ui.py

```


import os

folders = [
    "agents",
    "scrapers",
    "prompts",
    "data",
    "output"
]

files = {
    "app.py": "",
    ".env": "# Add your OpenAI API key here\nOPENAI_API_KEY=your-key",
    "requirements.txt": "streamlit\nopenai\npython-dotenv\nbeautifulsoup4\nrequests",
    "README.md": "# BizzBot: AI Agent for D2C Strategy in Eco-FMCG",
    
    # Agents
    "agents/pricing_agent.py": "# Logic for pricing strategy",
    "agents/gtm_agent.py": "# Logic for GTM strategy",
    "agents/analysis_agent.py": "# Competitor positioning and review analysis",

    # Scrapers
    "scrapers/amazon_scraper.py": "# Scrapes product info from Amazon",
    "scrapers/flipkart_scraper.py": "# (Optional) Add Flipkart scraping",
    "scrapers/review_scraper.py": "# Extract reviews for sentiment analysis",

    # Prompts
    "prompts/pricing.txt": "",
    "prompts/gtm.txt": "",
    "prompts/positioning.txt": "",

    # Data
    "data/competitor_data.json": "[]",
    "data/reviews_raw.json": "[]",

    # Output
    "output/report_formatter.py": "# Format output for dashboard or sheets",
    "output/google_sheets_export.py": "# Google Sheets integration (optional)",
    "output/dashboard.py": "# Optional modular dashboard UI",
}

def create_bizzbot_project():
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
    for filepath, content in files.items():
        with open(filepath, "w") as f:
            f.write(content)
    print("✅ BizzBot folder structure created successfully.")

if __name__ == "__main__":
    create_bizzbot_project()
    
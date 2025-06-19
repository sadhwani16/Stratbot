import requests
import os
from dotenv import load_dotenv
import re
load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def extract_brand_from_title(title):
    if not title:
        return "Unknown"
    match = re.match(r"^([A-Z][a-zA-Z0-9&\-\s]+?)\s", title)
    if match:
        brand = match.group(1).strip()
        # Filter generic phrases like "Biodegradable", "Sea Turtle", etc.
        generic_keywords = ["Biodegradable", "Eco", "Sea Turtle", "Bamboo", "Natural"]
        if any(word in brand for word in generic_keywords):
            return "Unknown"
        return brand
    return "Unknown"

def fetch_amazon_realtime_products(query, api_key, page=1, country="IN", max_results=10):
    url = "https://real-time-amazon-data.p.rapidapi.com/search"
    headers = {
        "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com",
        "x-rapidapi-key": api_key
    }
    params = {
        "query": query, 
        "page": page,
        "country": country,
        "sort_by": "RELEVANCE",
        "product_condition": "ALL",
        "is_prime": "false",
        "deals_and_discounts": "NONE"
    }

    response = requests.get(url, headers=headers, params=params)
    try:
        data = response.json()
    except Exception as e:
        print("❌ Failed to parse JSON from search response:", e)
        return []

    print("🔍 Raw Search Response:", data)
    results = []
    products = data.get("data", {}).get("products", [])[:max_results]

    for p in products:
        results.append({
            "site": "Amazon",
            "asin": p.get("asin"),
            "title": p.get("product_title", "No title"),
            "brand": extract_brand_from_title(p.get("product_title")),

            "price": p.get("unit_price", "₹ Not Available"),
            "rating": p.get("product_star_rating", "N/A"),
            "link": p.get("product_url", "#"),
            "image": p.get("product_photo", "")
        })

    return results


# ----------- Test Execution ----------- #
if __name__ == "__main__":
    query = "bamboo toothbrush"
    results = fetch_amazon_realtime_products(query, api_key=RAPIDAPI_KEY, country="IN", max_results=3)

    from pprint import pprint
    pprint(results) 

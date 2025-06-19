# scrapers/review_scraper.py
import requests
import os
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def fetch_amazon_reviews(asin, page=1, country="IN", max_reviews=10):
    """
    Fetch Amazon reviews for a given ASIN
    Returns list of review strings
    """
    if not RAPIDAPI_KEY:
        print("❌ RAPIDAPI_KEY not found in environment variables")
        return []
        
    if not asin:
        print("❌ No ASIN provided")
        return []

    url = "https://real-time-amazon-data.p.rapidapi.com/product-reviews"
    headers = {
        "x-rapidapi-host": "real-time-amazon-data.p.rapidapi.com",
        "x-rapidapi-key": RAPIDAPI_KEY
    }
    params = {
        "asin": asin,
        "country": country,
        "page": page,
        "sort_by": "TOP_REVIEWS",
        "star_rating": "ALL",
        "verified_purchases_only": "false",
        "images_or_videos_only": "false",
        "current_format_only": "false"
    }

    print(f"📦 Fetching reviews for ASIN: {asin}, Country: {country}, Page: {page}")
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ API request failed with status code: {response.status_code}")
            print("Response text:", response.text[:500])  # Limit output
            return []

        response_json = response.json()
        print("✅ API Response Status: Success")
        
        # Navigate the JSON structure more carefully
        data = response_json.get("data", {})
        if not data:
            print("❌ No 'data' field in response")
            return []
            
        reviews = data.get("reviews", [])
        if not reviews:
            print("❌ No 'reviews' field in data")
            return []
            
        print(f"📋 Found {len(reviews)} reviews")
        
        # Extract reviews with better error handling
        extracted_reviews = []
        for i, review in enumerate(reviews[:max_reviews]):
            try:
                # Handle the actual API response format
                title = review.get('review_title', '').strip()
                review_text = review.get('review_comment', '').strip()
                rating = review.get('review_star_rating', review.get('rating', 'N/A'))
                
                # Combine title and review text
                if title and review_text:
                    combined_review = f"[{rating}⭐] {title}: {review_text}"
                elif title:
                    combined_review = f"[{rating}⭐] {title}"
                elif review_text:
                    combined_review = f"[{rating}⭐] {review_text}"
                else:
                    continue  # Skip empty reviews
                    
                extracted_reviews.append(combined_review)
                print(f"✅ Processed review {i+1}: {title[:50]}...")
                
            except Exception as e:
                print(f"⚠️ Error processing review {i}: {e}")
                continue
        
        print(f"✅ Successfully extracted {len(extracted_reviews)} reviews")
        return extracted_reviews
        
    except requests.exceptions.Timeout:
        print("❌ Request timeout - API took too long to respond")
        return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return []
    except Exception as e:
        print(f"❌ Error parsing reviews JSON: {e}")
        return []

def test_review_scraper():
    """Test function to verify review scraper works"""
    # Test with a known ASIN (you can replace this)
    test_asin = "B08N5WRWNW"  # Example ASIN
    reviews = fetch_amazon_reviews(test_asin, max_reviews=3)
    
    if reviews:
        print("✅ Review scraper test successful!")
        for i, review in enumerate(reviews):
            print(f"{i+1}. {review[:100]}...")
    else:
        print("❌ Review scraper test failed!")
    
    return reviews

if __name__ == "__main__":
    test_review_scraper()
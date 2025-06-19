import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scrapers.amazon_realtime_scraper import fetch_amazon_realtime_products
from agents.pricing_agent import PricingAgent
from agents.gtm_agent import GTMAgent
from agents.analysis_agent import AnalysisAgent

# Load environment variables
load_dotenv()
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Page config
st.set_page_config(
    page_title="BizzBot Consultant",
    page_icon="📊",
    layout="wide"
)

# Clean CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .header {
        text-align: center;
        background: linear-gradient(90deg, #2E86AB, #A23B72);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .section-box {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin: 1rem 0;
        border-left: 4px solid #2E86AB;
    }
    .metric-box {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 6px;
        text-align: center;
        margin: 0.5rem 0;
    }
    .insight-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="header">
    <h1>📊 BizzBot Consultant</h1>
    <p>Get strategic insights in 2 minutes</p>
</div>
""", unsafe_allow_html=True)

# Two-column layout for input
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 🎯 Business Basics")
    product = st.text_input("Product/Service", "bamboo toothbrush")
    current_price = st.number_input("Current Selling Price (₹)", value=45, step=5)
    monthly_units = st.number_input("Monthly Units Sold", value=500, step=50)
    cost_per_unit = st.number_input("Cost per Unit (₹)", value=25, step=1)

with col2:
    st.markdown("### 📈 Objectives")
    primary_goal = st.selectbox("Primary Goal", 
        ["Increase Profit Margin", "Increase Sales Volume", "Market Penetration"])
    target_market = st.selectbox("Target Market", 
        ["Mass Market (₹20-50)", "Mid-Premium (₹50-150)", "Premium (₹150+)"])
    current_channels = st.multiselect("Current Sales Channels",
        ["Amazon", "Instagram", "D2C Website", "Retail Stores", "Flipkart"],
        default=["Amazon", "Instagram"])

# Calculate basic metrics
monthly_revenue = current_price * monthly_units
monthly_profit = (current_price - cost_per_unit) * monthly_units
profit_margin = ((current_price - cost_per_unit) / current_price) * 100

# Display current metrics
st.markdown("### 📊 Current Business Snapshot")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-box">
        <h3>₹{monthly_revenue:,.0f}</h3>
        <p>Monthly Revenue</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-box">
        <h3>₹{monthly_profit:,.0f}</h3>
        <p>Monthly Profit</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-box">
        <h3>{profit_margin:.1f}%</h3>
        <p>Profit Margin</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-box">
        <h3>₹{current_price}</h3>
        <p>Unit Price</p>
    </div>
    """, unsafe_allow_html=True)

# Generate Strategy Button
if st.button("🚀 Generate Strategy Report", type="primary", use_container_width=True):
    st.markdown("---")
    
    # Fetch competitor data
    with st.spinner("Analyzing market..."):
        competitors = fetch_amazon_realtime_products(product, api_key=RAPIDAPI_KEY, country="IN", max_results=3)
    
    # Extract competitor prices
    competitor_prices = []
    for comp in competitors:
        price_str = comp.get('price', '₹0')
        import re
        price_match = re.search(r'₹?\s*(\d+(?:,\d+)*(?:\.\d+)?)', str(price_str))
        if price_match:
            price_val = float(price_match.group(1).replace(',', ''))
            competitor_prices.append(price_val)
    
    # Calculate market positioning
    if competitor_prices:
        avg_market_price = np.mean(competitor_prices)
        min_market_price = min(competitor_prices)
        max_market_price = max(competitor_prices)
        
        # Price positioning
        if current_price < avg_market_price * 0.8:
            price_position = "Budget"
        elif current_price > avg_market_price * 1.2:
            price_position = "Premium"
        else:
            price_position = "Competitive"
    else:
        avg_market_price = current_price
        price_position = "Unknown"
    
    # Strategy Report
    st.markdown("## 📋 Strategic Analysis Report")
    
    # Two main sections
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown("### 💰 AI Pricing Strategy")
        
        # Use your Pricing Agent
        with st.spinner("🤖 AI analyzing pricing strategy..."):
            competitors_text = "\n".join([f"- {comp['title'][:50]}: {comp['price']}" for comp in competitors]) if competitors else "No competitor data available"
            
            pricing_agent = PricingAgent()
            pricing_inputs = {
                "product": product,
                "revenue": monthly_revenue,
                "cost": {
                    "raw": 60,  # Estimated breakdown
                    "labor": 25,
                    "delivery": 15
                },
                "competitors": competitors_text,
                "sales_volume": monthly_units,
                "usp": f"Eco-friendly {product} targeting {target_market}",
                "segment": target_market,
                "goal": primary_goal
            }
            
            pricing_result = pricing_agent.run(pricing_inputs)
            st.markdown(pricing_result)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown("### 🎯 AI Go-to-Market Strategy")
        
        # Use your GTM Agent
        with st.spinner("🤖 AI crafting GTM strategy..."):
            gtm_agent = GTMAgent()
            gtm_inputs = {
                "product": product,
                "usp": f"Eco-friendly {product} with premium quality",
                "segment": target_market,
                "channels": current_channels,
                "goal": primary_goal
            }
            
            gtm_result = gtm_agent.run(gtm_inputs)
            st.markdown(gtm_result)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Market Analysis
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown("### 🧠 AI Market Analysis & Positioning")
    
    with st.spinner("🤖 AI analyzing market positioning..."):
        analysis_agent = AnalysisAgent()
        competitors_text = "\n".join([f"- {comp['title'][:50]}: {comp['price']} (Rating: {comp['rating']})" for comp in competitors]) if competitors else "No competitor data available"
        
        analysis_inputs = {
            "product": product,
            "usp": f"Eco-friendly {product} with sustainable materials",
            "competitors": competitors_text,
            "segment": target_market,
            "goal": primary_goal
        }
        
        analysis_result = analysis_agent.run(analysis_inputs)
        st.markdown(analysis_result)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Competitive Landscape Table
    if competitors:
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.markdown("### 🏆 Competitive Landscape")
        
        # Simple competitor table
        comp_data = []
        for comp in competitors:
            comp_data.append({
                'Product': comp.get('title', 'Unknown')[:50] + "...",
                'Price': comp.get('price', 'N/A'),
                'Rating': comp.get('rating', 'N/A'),
                'Brand': comp.get('brand', 'Unknown')
            })
        
        if comp_data:
            comp_df = pd.DataFrame(comp_data)
            st.dataframe(comp_df, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Customer Sentiment Analysis
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown("### 😊 AI Customer Sentiment Analysis")
    
    with st.spinner("🤖 AI analyzing customer reviews..."):
        if competitors and len(competitors) > 0:
            # Get ASIN from first competitor
            asin = competitors[0].get("asin")
            if asin:
                from scrapers.review_scraper import fetch_amazon_reviews
                from agents.analysis_agent import SentimentAnalysisAgent
                
                reviews = fetch_amazon_reviews(asin, max_reviews=5)
                if reviews:
                    sentiment_agent = SentimentAnalysisAgent()
                    sentiment_result = sentiment_agent.run(product, reviews)
                    st.markdown(sentiment_result)
                else:
                    st.warning("⚠️ No reviews found for sentiment analysis")
            else:
                st.warning("⚠️ No product ASIN available for review analysis")
        else:
            st.info("ℹ️ Competitor data needed for customer sentiment analysis")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # ROI Calculator
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.markdown("### 📈 Strategy ROI Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        strategy_investment = st.number_input("Strategy Implementation Cost (₹)", value=25000, step=5000)
    
    with col2:
        expected_uplift = st.slider("Expected Revenue Uplift (%)", 10, 50, 25)
    
    with col3:
        timeline = st.slider("Timeline (Months)", 3, 12, 6)
    
    # Calculate ROI
    current_6m_profit = monthly_profit * timeline
    uplifted_6m_profit = monthly_profit * (1 + expected_uplift/100) * timeline
    additional_profit = uplifted_6m_profit - current_6m_profit
    net_benefit = additional_profit - strategy_investment
    roi_percentage = (net_benefit / strategy_investment) * 100
    
    st.write(f"**Investment**: ₹{strategy_investment:,.0f}")
    st.write(f"**Additional Profit**: ₹{additional_profit:,.0f}")
    st.write(f"**Net Benefit**: ₹{net_benefit:,.0f}")
    st.write(f"**ROI**: {roi_percentage:.1f}%")
    
    if roi_percentage > 100:
        st.success("🎯 High ROI Strategy - Recommended to proceed!")
    elif roi_percentage > 50:
        st.info("📊 Moderate ROI - Consider optimizing the approach")
    else:
        st.warning("⚠️ Low ROI - May need to reconsider strategy or reduce investment")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>📊 BizzBot Consultant • Quick Strategic Insights</p>
</div>
""", unsafe_allow_html=True)
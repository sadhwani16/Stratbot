# agents/analysis_agent.py - Minimal fix using your existing gemini.py

from gemini import chat_with_gemini

class AnalysisAgent:
    def run(self, inputs):
        prompt = f"""
        You're a D2C brand strategist analyzing positioning.

        Product: {inputs['product']}
        USP: {inputs['usp']}
        Target Segment: {inputs['segment']}
        Business Goal: {inputs['goal']}

        Competitor Summary:
        {inputs['competitors']}

        Analyze and return:
        1. **Product Positioning** (relative to market)
        2. **Perceived Value**
        3. **Suggestions to Differentiate**
        4. **Potential Pricing Premium Justification**
        5. **Key Risk Factors**

        Use bullet points and be concise. Format in markdown.
        """
        return chat_with_gemini(prompt)

class SentimentAnalysisAgent:
    def __init__(self):
        # Remove CrewAI - just use a simple class
        pass
    
    def run(self, product, reviews):
        """Analyze customer sentiment from reviews"""
        
        # Handle empty reviews
        if not reviews:
            return "⚠️ **No reviews available for sentiment analysis.**"
        
        # Convert reviews to string if it's a list
        if isinstance(reviews, list):
            if len(reviews) == 0:
                return "⚠️ **No reviews available for sentiment analysis.**"
            reviews_text = "\n".join(reviews)
        else:
            reviews_text = str(reviews)
        
        # Check if we have meaningful content
        if len(reviews_text.strip()) < 10:
            return "⚠️ **Insufficient review content for analysis.**"
        
        prompt = f"""
        You are an expert customer sentiment analyst. Analyze the following reviews for "{product}":

        **Customer Reviews:**
        {reviews_text}

        Provide analysis in this format:

        ## 📊 Sentiment Analysis Report

        ### 🎯 Overall Sentiment
        - **Score**: [Positive/Mixed/Negative] (X/10)
        - **Summary**: Brief overall assessment

        ### 👍 Top Praised Features
        - Most mentioned positive aspects
        - Customer satisfaction points

        ### 👎 Common Complaints
        - Frequent issues mentioned
        - Areas of concern

        ### 💡 Improvement Suggestions
        - Actionable recommendations
        - Priority fixes

        ### 📈 D2C Strategy Insights
        - **Marketing Focus**: What to highlight
        - **Product Development**: Priority improvements
        - **Competitive Advantage**: Unique strengths
        """
        
        try:
            result = chat_with_gemini(prompt)
            return result if result else "❌ **Failed to generate analysis**"
        except Exception as e:
            print(f"❌ Sentiment Analysis Error: {e}")
            return f"❌ **Error**: {str(e)}"
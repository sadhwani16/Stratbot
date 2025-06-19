# Logic for GTM strategy
from gemini import chat_with_gemini

class GTMAgent:
    def run(self, inputs):
        prompt = f"""
        You're a go-to-market (GTM) strategist for Indian D2C brands.

        Product: {inputs['product']}
        Unique Selling Proposition (USP): {inputs['usp']}
        Target Segment: {inputs['segment']}
        Current Channels: {", ".join(inputs['channels'])}
        Business Goal: {inputs['goal']}

        Recommend a GTM plan with:
        1. Ideal Primary Channel
        2. Messaging Angle (based on USP)
        3. Promotional Tactics (paid + organic)
        4. Influencer/Partner ideas
        5. Timeline & Metrics to track

        Be actionable and India-specific.
        """
        return chat_with_gemini(prompt)

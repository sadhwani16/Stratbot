from crewai import Agent
from gemini import chat_with_gemini

class PricingAgent:
    def __init__(self):
        self.agent = Agent(
            role="Pricing Strategy Agent",
            goal="Recommend a pricing strategy for eco-conscious D2C products in India",
            backstory="You are a pricing consultant with expertise in sustainable FMCG brands.",
            verbose=True
        )

    def run(self, inputs):
        prompt = f"""
You're a pricing strategy consultant for eco-friendly consumer products.

Create a detailed pricing report in markdown format based on the following inputs:

**Product**: {inputs['product']}
**Monthly Revenue**: ₹{inputs['revenue']}
**Monthly Sales Volume (Units)**: {inputs['sales_volume']}
**Unique Selling Proposition (USP)**: {inputs['usp']}
**Target Segment**: {inputs['segment']}
**Primary Goal**: {inputs['goal']}

**Cost Breakdown (%):**
- Raw Material: {inputs['cost']['raw']}%
- Labor: {inputs['cost']['labor']}%
- Delivery: {inputs['cost']['delivery']}%

**Competitor Prices (USD, to be converted to INR):**
{inputs['competitors']}

---

### 🎯 Output Format (Markdown)
Structure the report as follows:
1. **Cost Analysis**
   - Use sales volume to estimate unit costs
   - Break down each cost component
2. **Competitor Benchmarking**
   - Table with product name and price (converted to INR)
   - Position our product on this scale
3. **Recommended Price Range**
   - Provide minimum, maximum, and suggested price in INR
4. **Justification**
   - Explain rationale based on USP, target segment, and goal
5. **Strategic Next Steps**
   - Recommend 2-3 practical steps to refine pricing strategy

Ensure the report feels professional and actionable. Use bullet points and headings where needed.
        """
        return chat_with_gemini(prompt)

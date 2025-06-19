# gemini.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def chat_with_gemini(prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")  # or gemini-pro if needed
    response = model.generate_content(prompt)
    return response.text

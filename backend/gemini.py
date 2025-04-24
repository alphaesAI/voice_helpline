import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def gemini_response(user_input: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(user_input)
        return response.text.strip()  
    except Exception as e:
        return f"Error with Gemini API: {str(e)}"

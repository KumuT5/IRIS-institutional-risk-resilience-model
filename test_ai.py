import google.generativeai as genai
import os
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))


model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content("hello")

print(response.text)

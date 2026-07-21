import google.generativeai as genai

genai.configure(api_key="AIzaSyDK_wMErEbEr0wEuBwQLznIVcT-vaE8Po0")

model = genai.GenerativeModel("gemini-2.0-flash")

response = model.generate_content("hello")

print(response.text)

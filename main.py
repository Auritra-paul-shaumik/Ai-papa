import os
from flask import Flask
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is missing in your .env file.")
genai.configure(api_key=api_key)

# Load Gemini model
model = genai.GenerativeModel("gemini-pro")

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to your Gemini-powered chatbot! Ask a question via the URL: /your-question"

@app.route("/<query>")
def ask_gemini(query):
    try:
        prompt = f"{query} - reply under 200 characters and don't say how many characters you used."
        response = model.generate_content(prompt)
        return response.text.strip()[:256]
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/ping")
def ping():
    return "pong", 200

if __name__ == "__main__":
    app.run(port=11223, host="0.0.0.0", debug=True)

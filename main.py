import os
from flask import Flask
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

# Flask app setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Gemini AI is ready! Ask something in the URL."

@app.route('/<query>')
def query(query):
    try:
        prompt = f"{query} - reply under 200 characters and don't say how many characters you used."
        response = model.generate_content(prompt)
        return response.text.strip()[:256]
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/ping')
def ping():
    return "pong", 200

if __name__ == '__main__':
    app.run(port=11223, host="0.0.0.0", debug=True)

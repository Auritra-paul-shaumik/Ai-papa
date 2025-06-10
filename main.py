# How to Add AI to Your Live Stream Chat using HuggingFace API
# File Provided by EXPOSUREEE - Abhishek Mishra

from flask import Flask
from huggingface_hub import InferenceClient

# Initialize the client with your Hugging Face API token
client = InferenceClient(api_key="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")

# Define the initial conversation
messages = [
    {"role": "assistant", "content": "Hello! I'm here to assist you. Feel free to ask anything."}
]

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "hello chat"

@app.route("/<query>")
def query(query):
    # Append the condition to the user's query
    query_with_condition = f"{query} - reply under 200 characters in total and don't tell me how many characters you used in your response."
    
    messages.append({"role": "user", "content": query_with_condition})
    stream = client.chat.completions.create(
            model="Qwen/Qwen2.5-72B-Instruct", 
            messages=messages, 
            temperature=0.5,
            max_tokens=2048,
            top_p=0.7,
            stream=True
        )
    assistant_reply = ""
    for chunk in stream:
        if chunk.choices[0].delta.get("content"):
            part = chunk.choices[0].delta["content"]
            assistant_reply += part
    messages.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply[:256]

if __name__ == '__main__':
    app.run(port=11223, host="0.0.0.0", debug=True)

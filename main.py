# How to Add AI to Your Live Stream Chat using HuggingFace API
# File Provided by EXPOSUREEE - Abhishek Mishra

import os
from flask import Flask
from huggingface_hub import InferenceClient

client = InferenceClient(api_key=os.getenv("HF_TOKEN"))


# Define the initial conversation
messages = [
    {"role": "assistant", "content": "Hello! I'm here to assist you. Feel free to ask anything."}
]

app = Flask(__name__)


@app.route('/')
def hello_world():
    return "Hello friend, What can I help with? Ask me anything....."

@app.route("/<query>")
def query(query):
    # Append the condition to the user's query
    query_with_condition = f"{query} - reply under 200 characters in total and don't tell me how many characters you used in your response."
    
    stream = client.chat.completions.create(
    model="mistralai/Mistral-7B-Instruct-v0.1", 
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

@app.route('/ping')
def ping():
    return "pong", 200


if __name__ == '__main__':
    app.run(port=11223, host="0.0.0.0", debug=True)

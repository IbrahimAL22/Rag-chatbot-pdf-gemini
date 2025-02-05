import google.generativeai as genai
import time
import os

# Set up the API key from an environment variable
api_key = "AIzaSyC-sBXY8Jsg758ypFm-BgVKsumypNjpLu4"
if not api_key:
    raise ValueError("API key not found. Please set the GOOGLE_GENERATIVEAI_API_KEY environment variable.")

genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-pro")

# Function to send a request and handle rate limiting
def send_request(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return None

# Send the request 100 times with error handling and rate limiting

response = send_request("what is the capital of France")
if response:
    print(f"Response : {response}")

import google.generativeai as genai

# Set up the API key
api_key = "AIzaSyC-sBXY8Jsg758ypFm-BgVKsumypNjpLu4"
if not api_key:
    raise ValueError("API key not found. Please set the GOOGLE_GENERATIVEAI_API_KEY environment variable.")

genai.configure(api_key=api_key)

# Initialize the model with temperature
model = genai.GenerativeModel("gemini-pro", generation_config={"temperature": 0.7})

# Function to send a request
def send_request(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return None

# Send a request
response = send_request("What is the capital of France?")
if response:
    print(f"Response: {response}")

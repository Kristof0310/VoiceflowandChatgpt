from flask import Flask, request
import requests

app = Flask(__name__)

# Endpoint to receive data from Voiceflow
@app.route('/to_chatgpt', methods=['POST'])
def to_chatgpt():
    data = request.json
    user_responses = [data['field1'], data['field2'], data['field3'], data['field4']]

    # Create Custom Script
    custom_prompt = f"Your custom prompt here with variables: {user_responses[0]}, {user_responses[1]}, {user_responses[2]}, {user_responses[3]}"

    # Send the prompt to GPT API
    gpt_response = send_to_gpt(custom_prompt)

    # Send the GPT response back to Voiceflow
    return send_to_voiceflow(gpt_response)

def send_to_gpt(prompt):
    # Replace with your actual GPT API endpoint and key
    gpt_api_endpoint = "https://api.openai.com/v1/engines/davinci-codex/completions"
    headers = {
        "Authorization": "Bearer YOUR_GPT_API_KEY",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": prompt,
        "max_tokens": 150  # Adjust as needed
    }

    response = requests.post(gpt_api_endpoint, json=payload, headers=headers)
    return response.json()

def send_to_voiceflow(gpt_response):
    # Code to format and send the response back to Voiceflow
    # This depends on how Voiceflow expects to receive the data
    pass  # Replace with actual implementation

if __name__ == '__main__':
    app.run(port=5000)

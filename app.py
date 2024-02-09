from flask import Flask, request
from openai import OpenAI
import os
from config import *

app = Flask(__name__)

@app.route('/to_chatgpt', methods=['POST'])
def to_chatgpt():
    video_topic = request.form['video_topic']
    video_audience = request.form['video_audience']
    # Create custom prompt using video_topic and video_audience
    custom_prompt = f"""
          Write me a short explainer video script for short form social media content that is less than 150 words. make the tone exciting and engaging. 
          Start script with a short hook that highlights who should watch this video and why. 
          Finish script with a very short call to action at the end to like and follow. 
          include latest stats and news if you can. Only provide the script prose. Focus script around the audience and topic delimited by “:”
          Video Audience: {video_audience}
          Video Topic: {video_topic}
        """

    # Send the prompt to GPT API and get response to resend to voiceflow
    gpt_response = send_to_gpt(custom_prompt)

    # Send the GPT response back to Voiceflow
    return {"response" : gpt_response}

def send_to_gpt(prompt):
    
    client = OpenAI(api_key=OPEN_API_KEY)
    
    #create a thread
    thread = client.beta.threads.create()

    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = prompt
    )

    #Create the run, passing in the thread and the assitant
    run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = ASSISTANT_ID
    ) 

    #Periodically retried the run until completed
    while run.status != "completed":
        keep_retrieving_run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        print(f"Run status: {keep_retrieving_run.status}")

        if keep_retrieving_run.status == "completed":
            print("\n")
            break

    assistant_reply = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    response = assistant_reply.data[0].content[0].text.value
    return response

if __name__ == '__main__':
    app.run(port=5000)

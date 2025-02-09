from flask import Flask, request, jsonify
import os
from groq import Groq
from dotenv import load_dotenv
import re
from pydub import AudioSegment
import io
from io import BytesIO
import json

# Load environment variables
load_dotenv()
# Initialize Flask app
app = Flask(__name__)

# Get Groq API Key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

headers = {
    'Authorization': f'Bearer {GROQ_API_KEY}',
    'Content-Type': 'application/json'
}
# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)
@app.route('/subtask', methods=['POST'])
def subtask():
        data = request.json  # Get JSON data from the request
        task = data.get("task")  # Extract location from request
        print(task)
        
        # if not sentence:
        #     return jsonify({'error': 'Sentence is required'}), 400
        #sentence = "I have to complete a run at Columbia  tomorow morniing at five . Give me the date time, location only like Date: , Time: , Location: and the last word should be complete!"
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                   "role": "user",
    "content": f"""Here are some examples of tasks and their subtasks:

    Example 1:
    Task: "I need to go to the gym in the evening."
    Subtask: "Do you want to prepare your gym bag?"

    Example 2:
    Task: "I need to finish my homework."
    Subtask: "Do you want to open your laptop?"

    Example 3:
    Task: "I need to go for a run in the morning"
    Subtask: "Do you want to wear your running shoes?"

    Example 4:
    Task: "Pack your lugguage"
    Subtask: "Do you want to pack your clothes?""
    

    Now, for this task: {task} Just state a subtask with no other words but like a polite question, do you want to ... but mention the main words that define the task?. 
    """
                }
            ],
            temperature=0.7,
            max_completion_tokens=160
            ,
            top_p=0.95,
            stream=True,
            
        )
        subtask = ""
        for chunk in completion:
            subtask += chunk.choices[0].delta.content or ""
        print(subtask)
        # Return the response as JSON
        return jsonify({
            "task": task,
            "subtask": subtask.strip()
        })
      

       

        return jsonify(json_output), 200

if __name__ == '__main__':
    app.run(debug=True)

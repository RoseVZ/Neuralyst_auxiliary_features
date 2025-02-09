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
@app.route('/extract_info', methods=['POST'])
def extract_info():
        data = request.get_json()
        print(request)
        # Get JSON data from the request
        # data = request.get_json()
        data = request.form.to_dict()
    
        sentence = data.get('sentence')
        print(sentence)
        # if not sentence:
        #     return jsonify({'error': 'Sentence is required'}), 400
        #sentence = "I have to complete a run at Columbia  tomorow morniing at five . Give me the date time, location only like Date: , Time: , Location: and the last word should be complete!"
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": f"{sentence}. Give me the date time, location only like Date: , Time: , Location: "
                }
            ],
            temperature=0.1,
            max_completion_tokens=160
            ,
            top_p=0.95,
            stream=True,
            
        )
        response_text = ""
        for chunk in completion:
            response_text += chunk.choices[0].delta.content or ""
        
        date_match = re.search(r"Date:\s*(.*)", response_text)
        time_match = re.search(r"Time:\s*(.*)", response_text)
        location_match = re.search(r"Location:\s*(.*)", response_text)
        print(date_match.group(1))
        print(time_match.group(1))
        print(location_match.group(1))
         # Use regex to extract key-value pairs
        structured_data = {
        "Date": date_match.group(1) if date_match else None,
        "Time": time_match.group(1) if time_match else None,
        "Location": location_match.group(1) if location_match else None,
    }

        

        # Convert to JSON format
        json_output = json.dumps(structured_data, indent=2)

        print(json_output)

        return jsonify(json_output), 200

if __name__ == '__main__':
    app.run(debug=True)

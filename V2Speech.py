# import os
# from groq import Groq
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# # Initialize the Groq client
# client = Groq(api_key=GROQ_API_KEY)

# # Specify the path to the audio file
# filename = os.path.dirname(__file__) + "/Columbia University 2.m4a" # Replace with your audio file!

# # # Open the audio file
# # with open(filename, "rb") as file:
# #     # Create a transcription of the audio file
# #     transcription = client.audio.transcriptions.create(
# #       file=(filename, file.read()), # Required audio file
# #       model="whisper-large-v3-turbo", # Required model to use for transcription
# #       prompt="Specify context or spelling",  # Optional
# #       response_format="json",  # Optional
# #       language="en",  # Optional
# #       temperature=0.0  # Optional
# #     )
# #     # Print the transcription text
# #     print(transcription.text)

from flask import Flask, request, jsonify
import os
from groq import Groq
from dotenv import load_dotenv

from pydub import AudioSegment
import io
from io import BytesIO


# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Get Groq API Key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files["audio"]
    # Check if the file has a filename
    print(audio_file.stream)
    # filename = os.path.dirname(__file__) + audio_file # Replace with your audio file!
    print(audio_file.filename)
    # Assuming 'audio_file' is your Flask FileStorage object
    audio_data = audio_file.read()
    audio_buffer = BytesIO(audio_data)

    # Now you can use audio_buffer as input for your LLM
    file = ("audio.m4a", audio_buffer)

    try:
    
    # Create a transcription of the audio file
        transcription = client.audio.transcriptions.create(
        file=file, # Required audio file
        model="whisper-large-v3-turbo", # Required model to use for transcription
        prompt="Specify context or spelling",  # Optional
        response_format="json",  # Optional
        language="en",  # Optional
        temperature=0.0  # Optional
        )
        # Print the transcription text
        print(transcription.text)

        return jsonify({"transcription": transcription.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

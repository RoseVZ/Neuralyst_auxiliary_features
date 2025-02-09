from geopy.geocoders import Nominatim
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

def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="my_location_finder_123")
    location = geolocator.geocode(location_name)
    if location:
        return {"latitude": location.latitude, "longitude": location.longitude}
    else:
        return None

@app.route("/get_coordinates", methods=["POST"])
def get_location_coordinates():
    data = request.json  # Get JSON data from the request
    location_name = data.get("location")  # Extract location from request
    
    if not location_name:
        return jsonify({"error": "Location name is required"}), 400
    
    coordinates = get_coordinates(location_name)
    
    if coordinates:
        return jsonify({"location": location_name, "coordinates": coordinates})
    else:
        return jsonify({"error": "Location not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)



# import requests
# from geopy.geocoders import Nominatim

# def get_current_location():
#     try:
#         response = requests.get("https://ipinfo.io/json")
#         data = response.json()

#         # Extract latitude and longitude from the 'loc' field
#         if "loc" in data:
#             lat, lon = map(float, data["loc"].split(","))
#             return lat, lon
#         else:
#             return None
#     except Exception as e:
#         print(f"Error: {e}")
#         return None

# # Get coordinates
# coords = get_current_location()
# if coords:
#     print(f"Current Location - Latitude: {coords[0]}, Longitude: {coords[1]}")
# else:
#     print("Could not determine location.")
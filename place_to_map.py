# from geopy.geocoders import Nominatim

# def get_coordinates(location_name):
#     geolocator = Nominatim(user_agent="my_location_finder_123")
#     location = geolocator.geocode(location_name)
#     if location:
#         return {"latitude": location.latitude, "longitude": location.longitude}
#     else:
#         return None

# # Example usage
# location_name = "Columbia University, New York"
# coordinates = get_coordinates(location_name)
# print(coordinates) 
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
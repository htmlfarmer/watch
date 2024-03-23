import requests

def get_geolocation(city_name):
    url = f"https://nominatim.openstreetmap.org/search?format=json&q={city_name}"
    response = requests.get(url)
    data = response.json()
    if data:
        # Extract latitude and longitude
        lat = float(data[0]['lat'])
        lon = float(data[0]['lon'])
        return lat, lon
    else:
        print("Geolocation not found for the city.")
        return None
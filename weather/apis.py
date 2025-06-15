import requests

def get_coordinates(city):
    """ Retrieve the latitude and longitude for a given city name."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": "en", "format": "json"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    if "results" in data and data["results"]:
        lat = data["results"][0]["latitude"]
        lon = data["results"][0]["longitude"]
        return lat, lon
    else:
        raise ValueError(f"City '{city}' not found.")

#     
def get_current_weather(lat, lon):
    """
    Retrieve the current weather for a given latitude and longitude.
    Args:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
    Returns:
        dict: A dictionary containing current weather data for the specified location.
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current_weather": True
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    if "current_weather" in data:
        return data["current_weather"]
    else:
        raise ValueError("Weather data not found.")   

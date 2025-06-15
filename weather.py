#!/usr/bin/env python3
from weather.apis import get_coordinates, get_current_weather
def main():
    city = input("Enter city name to get the current weather details: ").strip()
    if not city:
        print("Error: City name cannot be empty. Please enter a valid city name.")
        return
    try:
        lat, lon = get_coordinates(city)
        weather = get_current_weather(lat, lon)
        print(f"\nCurrent weather in {city}:")
        print("-" * (20 + len(city)))
        print(f"Temperature   : {weather.get('temperature', 'N/A')}°C")
        print(f"Windspeed     : {weather.get('windspeed', 'N/A')} km/h")
        print(f"Wind direction: {weather.get('winddirection', 'N/A')}°")
    except ValueError as ve:
        # Handles non-existing city error from get_coordinates
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()

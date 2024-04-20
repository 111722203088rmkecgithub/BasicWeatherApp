import requests
from datetime import datetime

def get_weather(api_key, location):
    """Fetch current weather data for the specified location."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            weather_info = {
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "weather": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"],
                "visibility": data["visibility"] / 1000,  # Convert to kilometers
                "sunrise": datetime.utcfromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S"),
                "sunset": datetime.utcfromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S"),
                "city": data["name"],
                "country": data["sys"]["country"]
            }
            return weather_info
        elif data["cod"] == "404":
            print("Error: City not found. Please enter a valid city name or ZIP code.")
            return None
        else:
            print(f"Error: Unable to fetch weather data. Response code: {data['cod']}")
            return None
    except requests.exceptions.RequestException as e:
        print("Error: An error occurred while making the request:", e)
        return None
    except KeyError as e:
        print("Error: Unexpected response format from the API:", e)
        return None

def save_to_file(filename, weather_data):
    """Save weather data to a file."""
    with open(filename, 'w') as file:
        for key, value in weather_data.items():
            file.write(f"{key}: {value}\n")
    print(f"Weather data saved to {filename}")

def main():
    print("Welcome to the Command-Line Weather App!")

    # API key for OpenWeatherMap API (replace with your own API key)
    api_key = "29e992a198e2f6eadd42d8382485f482"

    # Prompt user for location
    location = input("Enter a city name or ZIP code: ")

    # Fetch weather data
    weather = get_weather(api_key, location)

    if weather:
        print("\nCurrent Weather:")
        print(f"City: {weather['city']}, {weather['country']}")
        print(f"Temperature: {weather['temperature']}°C")
        print(f"Humidity: {weather['humidity']}%")
        print(f"Weather: {weather['weather']}")
        print(f"Wind Speed: {weather['wind_speed']} m/s")
        print(f"Visibility: {weather['visibility']} km")
        print(f"Sunrise: {weather['sunrise']} UTC")
        print(f"Sunset: {weather['sunset']} UTC")

        # Prompt user to save weather data to a file
        save_file = input("\nDo you want to save the weather data to a file? (y/n): ").lower()
        if save_file == 'y':
            filename = input("Enter the filename to save weather data to (include extension, e.g., weather.txt): ")
            save_to_file(filename, weather)
    else:
        print("Exiting.")

if __name__ == "__main__":
    main()

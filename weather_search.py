import requests


def get_city_coordinates(city):
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "format": "json"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    if "results" not in data or not data["results"]:
        return None

    location = data["results"][0]

    return {
        "name": location["name"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "country": location.get("country", ""),
        "state": location.get("admin1", "")
    }


def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "weather_code,"
            "wind_speed_10m"
        ),
        "timezone": "auto"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json()


def get_weather_description(weather_code):
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        95: "Thunderstorm"
    }

    return weather_codes.get(weather_code, "Unknown")


def display_weather(location, weather):
    current = weather["current"]

    temperature = current["temperature_2m"]
    humidity = current["relative_humidity_2m"]
    weather_code = current["weather_code"]
    wind_speed = current["wind_speed_10m"]

    condition = get_weather_description(weather_code)

    print("\n-----------------------------")
    print(f"Weather for {location['name']}, {location['state']}")
    print(f"Country: {location['country']}")
    print("-----------------------------")
    print(f"Temperature: {temperature} °C")
    print(f"Weather condition: {condition}")
    print(f"Humidity: {humidity}%")
    print(f"Wind speed: {wind_speed} km/h")
    print("-----------------------------\n")


def main():
    print("Weather Search Application")

    while True:
        city = input("Enter a city name (or type 'exit' to quit): ").strip()

        if city.lower() == "exit":
            print("Goodbye!")
            break

        if not city:
            print("Please enter a city name.")
            continue

        try:
            location = get_city_coordinates(city)

            if location is None:
                print("City not found. Please try again.")
                continue

            weather = get_weather(
                location["latitude"],
                location["longitude"]
            )

            display_weather(location, weather)

        except requests.RequestException as error:
            print(f"API request failed: {error}")

        except KeyError:
            print("The API returned unexpected data.")


if __name__ == "__main__":
    main()
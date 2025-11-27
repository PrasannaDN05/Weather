import requests

API_KEY = "2e3690608eaa736e49823f29e40946ec"  # same working key as in test_weather.py
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city_name: str):
    params = {
        "q": city_name,
        "appid": API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=5)
        print("Status code:", response.status_code)  # debug
        print("Raw response (first 200 chars):", repr(response.text[:200]))

        # Try to parse JSON safely
        try:
            data = response.json()
        except ValueError:
            print("❌ Could not parse JSON. Check URL, API key, or internet.")
            return None

        if str(data.get("cod")) != "200":
            print("❌ API error:", data.get("message"))
            return None

        return data

    except requests.exceptions.RequestException as e:
        print("⚠️ Network error:", e)
        return None


def show_weather(data: dict):
    main = data.get("main", {})
    weather_list = data.get("weather", [])
    wind = data.get("wind", {})

    temp = main.get("temp")
    feels_like = main.get("feels_like")
    humidity = main.get("humidity")
    description = weather_list[0].get("description") if weather_list else "N/A"
    wind_speed = wind.get("speed")

    print("\n===== 🌤️ Weather Report 🌤️ =====")
    print(f"City: {data.get('name')}")
    print(f"Temperature: {temp} °C")
    print(f"Feels like: {feels_like} °C")
    print(f"Humidity: {humidity}%")
    print(f"Condition: {description.capitalize()}")
    print(f"Wind speed: {wind_speed} m/s")
    print("=================================")


def main():
    print("=== Simple Weather App ===")
    city = input("Enter city name: ").strip()
    if not city:
        print("❌ City name cannot be empty.")
        return

    weather_data = get_weather(city)
    if weather_data:
        show_weather(weather_data)


if __name__ == "__main__":
    main()

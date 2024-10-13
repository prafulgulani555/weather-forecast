import requests
import os

api_key = os.getenv("weather_api")

def get_data(place, forecast_days=None):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={place}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    filtered_data = data["list"]
    nr_values = 8 * forecast_days
    filtered_data = filtered_data[:nr_values]
    # print(temperatures)
    return filtered_data


if __name__ == "__main__":
    print(get_data(place="Tokyo", forecast_days=3))
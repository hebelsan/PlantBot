import os
import requests

def getCurrentWeatherOnline(city="Emmendingen"):
    api_key = os.getenv('API_KEY')
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "APPID=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] == 200:
        y = x["main"]
        return y
    else:
        return {
            "temp": 0,
            "pressure": 0,
            "humidity": 0,
        }
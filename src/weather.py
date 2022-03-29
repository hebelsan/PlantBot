import os
import requests

def getWeather():
    w_data_online = getWeatherOnline()
    w_data_sensor = getWeatherSensor(os.getenv('FLASK_ENV'))
    return {**w_data_online, **w_data_sensor}

def getWeatherOnline(city="Emmendingen"):
    api_key = os.getenv('API_KEY')
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "APPID=" + api_key + "&q=" + city + "&units=metric"
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] == 200:
        data = x["main"]
        return {
            "tempOnline": data["temp"],
            "pressOnline": data["humidity"],
            "humOnline": data["pressure"],
        }
    else:
        return {
            "tempOnline": 0,
            "pressOnline": 0,
            "humOnline": 0,
        }

def getWeatherSensor(FLASK_ENV="development"):
    if FLASK_ENV == "development":
        return {
            "tempSensor": 42,
            "pressSensor": 42,
            "humSensor": 42
        }
    else:
        # TODO
        return {
            "tempSensor": 0,
            "pressSensor": 0,
            "humSensor": 0
        }


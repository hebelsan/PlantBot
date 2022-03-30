import os
import requests


def initBme280():
    if os.getenv('FLASK_ENV') == "production":
        import board
        from adafruit_bme280 import basic as adafruit_bme280
        i2c = board.I2C()   # uses board.SCL and board.SDA
        bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
        bme280.sea_level_pressure = 1013.25
        return bme280
    else:
        return None



def getWeather(bme280=None):
    w_data_online = getWeatherOnline()
    w_data_sensor = getWeatherSensor(bme280)
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
            "humOnline": data["humidity"],
            "pressOnline": data["pressure"],
        }
    else:
        return {
            "tempOnline": 0,
            "pressOnline": 0,
            "humOnline": 0,
        }

def getWeatherSensor(bme280):
    if bme280 == None:
        return {
            "tempSensor": 42,
            "pressSensor": 42,
            "humSensor": 42
        }
    else:
        return {
            "tempSensor": "{:10.1f}".format(bme280.temperature),
            "humSensor": "{:10.1f}".format(bme280.relative_humidity),
            "pressSensor": "{:10.1f}".format(bme280.pressure)
        }


import datetime
import requests


class Date:
    """Class for returning Date elements"""
    def __init__(self):
        self.today = datetime.datetime.now()
        self.hour1 = self.today.hour

        self.get_date()

    def get_date(self):
        """assing to self.day date in format (YYYY month DD)"""
        months = ["January", "February", "March", "April", "May", "June", "July",
                  "August", "September", "October", "November", "December"]
        self.day = f"{self.today.year} {months[self.today.month - 1]} {self.today.day}"


class Weather:
    """Class for returning weather contitions"""
    def __init__(self, h):
        self.OMW_Endpoint = "https://api.openweathermap.org/data/2.8/onecall"
        self.api_key = "27fddb32ad49da904b460c57943f6d92"
        self.weather_params = {
            "lat": 52.421792,
            "lon": 16.934996,
            "appid": self.api_key,
            "units": "metric",
            "exclude": "minutely,hourly,daily",
        }
        self.degree_sign = u'\N{DEGREE SIGN}'
        self.hour = h

        self.get_weather()
        self.image1()

    def get_weather(self):
        """getting weather. In comment Api version"""
        # response = requests.get(self.OMW_Endpoint, params=self.weather_params)
        # self.info = response.json()["current"]
        self.info = {'dt': 1681561339, 'sunrise': 1681530929, 'sunset': 1681580932, 'temp': 9.88, 'feels_like': 9.47,
                     'pressure': 1007, 'humidity': 92, 'dew_point': 8.64, 'uvi': 0.28, 'clouds': 100,
                     'visibility': 10000, 'wind_speed': 1.54, 'wind_deg': 150,
                     'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}],
                     'rain': {'1h': 1.06}}

        temp, temp_f = self.info["temp"], self.info["feels_like"]
        self.temperature = [f"{round(temp)}{self.degree_sign}", f"{round(temp_f)}{self.degree_sign}"]

    def image1(self):
        """choosing proper image  dependently on the weather"""
        self.type = int(self.info["weather"][0]["id"])

        rise_time = int(datetime.datetime.fromtimestamp(self.info["sunrise"]).strftime("%I"))
        set_time = int(datetime.datetime.fromtimestamp(self.info["sunset"]).strftime("%I")) + 13

        if not rise_time < self.hour < set_time:
            self.image = "images/wi-night-clear.png"
        elif self.type < 300:
            self.image = "images/wi-thunderstorm.png"
        elif self.type < 600:
            self.image = "images/wi-rain.png"
        elif self.type < 700:
            self.image = "images/wi-snow.png"
        elif self.type < 800:
            self.image = "images/wi-dust.png"
        elif self.type == 800:
            self.image = "images/wi-day-sunny.png"
        else:
            self.image = "images/wi-could.png"

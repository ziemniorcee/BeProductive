import datetime
import requests
from customtkinter import *
from actions import *
from settings import *

class Date:
    """Class for returning Date elements"""
    def __init__(self):
        self.date_today = datetime.datetime.now()
        self.now_hour = self.date_today.hour

        self.get_date()

    def get_date(self):
        """assing to self.day date in format (YYYY month DD)"""
        # months = ["January", "February", "March", "April", "May", "June", "July",
        #           "August", "September", "October", "November", "December"]
        # self.day = f"{self.today.year} {months[self.today.month - 1]} {self.today.day}"
        self.formatted_date = self.date_today.date()


class Weather:
    """Class for returning weather contitions"""
    def __init__(self):
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

        self.today = datetime.datetime.now()
        self.hour = self.today.hour

        self.get_weather()
        self.get_image()

    def get_weather(self):
        """getting weather. In comment Api version"""
        response = requests.get(self.OMW_Endpoint, params=self.weather_params)
        self.info = response.json()["current"]
        # self.info = {'dt': 1681561339, 'sunrise': 1681530929, 'sunset': 1681580932, 'temp': 9.88, 'feels_like': 9.47,
        #              'pressure': 1007, 'humidity': 92, 'dew_point': 8.64, 'uvi': 0.28, 'clouds': 100,
        #              'visibility': 10000, 'wind_speed': 1.54, 'wind_deg': 150,
        #              'weather': [{'id': 501, 'main': 'Rain', 'description': 'moderate rain', 'icon': '10d'}],
        #              'rain': {'1h': 1.06}}

        temp, temp_f = self.info["temp"], self.info["feels_like"]
        self.temperature = [f"{round(temp)}{self.degree_sign}", f"{round(temp_f)}{self.degree_sign}"]

    def get_image(self):
        """choosing proper image  dependently on the weather"""
        self.type = int(self.info["weather"][0]["id"])

        rise_time = int(datetime.datetime.fromtimestamp(self.info["sunrise"]).strftime("%I"))
        set_time = int(datetime.datetime.fromtimestamp(self.info["sunset"]).strftime("%I")) + 13

        if not rise_time < self.hour < set_time:
            self.image = "images/weather/wi-night-clear.png"
        elif self.type < 300:
            self.image = "images/weather/wi-thunderstorm.png"
        elif self.type < 600:
            self.image = "images/weather/wi-rain.png"
        elif self.type < 700:
            self.image = "images/weather/wi-snow.png"
        elif self.type < 800:
            self.image = "images/weather/wi-dust.png"
        elif self.type == 800:
            self.image = "images/weather/wi-day-sunny.png"
        else:
            self.image = "images/weather/wi-cloud.png"

class WeatherWidget(CTkFrame):
    def __init__(self, master):
        super().__init__(master,width=500, height=500)
        self.weather_data = Weather()
        self.app = master
        self.settings = Settings()
        res = self.settings.resolution
        self.c_frame = CTkCanvas(self, width=int(500* res[0]), height=int(500* res[1]), bg=self.settings.main_color, highlightthickness=0)
        self.c_frame.grid(row=0, column=0)

        self.c_frame.create_image(250* res[0], 0* res[1], image=create_imagetk(self.weather_data.image, int(500* res[0]), int(500* res[1])), anchor="n")
        self.c_frame.create_text(250* res[0], 200* res[1], text=f" {self.weather_data.temperature[0]}", font=self.settings.font,
                                    fill=self.settings.font_color, anchor="n")
        self.c_frame.create_text(250* res[0], 245* res[1], text=f"Feels like: {self.weather_data.temperature[1]}", font=("Arial", 15),
                                    fill=self.settings.font_color, anchor="n")
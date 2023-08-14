from actions import *
from settings import *
from customtkinter import *
from Data import Date, WeatherWidget, Weather
from habit import HabitsWidget
from goals import GoalsWidget
from timeline import TimelineWidget


class Start_window:
    """
    A class for the main window of the app

    Attributes
    ----------
    settings : Settings
        app info
    app : App
        connection to the app
    today_data : Date
        today's info
    weather_data : Weather
        today's weather

    Methods
    -----------
    create_main_window():
        creates window and essential objects
    b_start_make():
        build start button

    """

    def __init__(self, root):
        """
        Constructs essential attributes

        Parameters
        ----------
        root : App
            connection to the app
        """
        self.settings = Settings()
        self.app = root
        self.res = self.settings.resolution
        self.today_data = Date()
        self.weather_data = Weather()

    def create_main_window(self):
        """
        Build main window

        Returns
        -------
        None
        """
        self.app.page = 0
        self.app.create_c_main()

        habits_widget = HabitsWidget(self.app)
        self.app.c_main.create_window(1830 * self.res[0], 185 * self.res[1], window=habits_widget, anchor="n")

        goals_widget = GoalsWidget(self.app)
        self.app.c_main.create_window(470 * self.res[0], 185 * self.res[1], window=goals_widget, anchor="n")

        timeline_widget = TimelineWidget(self.app)
        self.app.c_main.create_window(1150 * self.res[0], 1090 * self.res[1], window=timeline_widget, anchor="n")

        weather_widget = WeatherWidget(self.app)
        self.app.c_main.create_window(1150 * self.res[0], 0 * self.res[1], window=weather_widget, anchor="n")
        self.b_start_make()

    def b_start_make(self):
        """
        Creates start button

        Return
        ------
        None
        """
        option = 3
        texts = ["Plan your day", "Create goals", "Create blocks", "Configure setup"]

        # if len(self.app.goals.goals_texts) == 0 and self.app.setup2.tl_blocks == 0:
        #     option = 0
        # elif len(self.app.goals.goals_texts) == 0:
        #     option = 1
        # elif len(self.app.setup2.tl_blocks) == 0:
        #     option = 2
        b_start = CTkButton(self.app, text=texts[option], fg_color=self.settings.main_color,
                            font=("Arial", int(50 * self.res[0])), border_width=int(12 * self.res[0]),
                            border_color=self.settings.second_color, text_color=self.settings.font_color,
                            command=self.app.goals.create_window, corner_radius=100,
                            hover_color=self.settings.second_color)
        self.app.c_main.create_window(1150 * self.res[0], 800 * self.res[1], window=b_start, width=400 * self.res[0],
                                      height=150 * self.res[1])

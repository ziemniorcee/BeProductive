from actions import *
from settings import *
from customtkinter import *
from Data import Date, Weather
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

        self.app.c_main.create_image(1080, 250, image=create_imagetk(self.weather_data.image, 500, 500))
        self.app.c_main.create_text(1080, 220, text=f" {self.weather_data.temperature[0]}", font=self.settings.font,
                                    fill=self.settings.font_color)
        self.app.c_main.create_text(1080, 260, text=f"Feels like: {self.weather_data.temperature[1]}",
                                    font=("Arial", 15),
                                    fill=self.settings.font_color)
        self.b_start_make()


        habits_widget = HabitsWidget(self.app)
        self.app.c_main.create_window(1760, 185, window=habits_widget, anchor="n")
        goals_widget = GoalsWidget(self.app)
        self.app.c_main.create_window(400, 185, window=goals_widget, anchor="n")
        timeline_widget = TimelineWidget(self.app)
        self.app.c_main.create_window(1055, 1090, window=timeline_widget, anchor="n")



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
        b_start = CTkButton(self.app, text=texts[option], fg_color=self.settings.main_color, font=("Arial", 50),
                                 border_width=12, border_color=self.settings.second_color,
                                 text_color=self.settings.font_color, command=self.app.goals.create_window,
                                 corner_radius=100, hover_color=self.settings.second_color)
        self.app.c_main.create_window(1080, 800, window=b_start, width=400, height=150)
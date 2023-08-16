from actions import *
from settings import *
from customtkinter import *
from Data import Date, WeatherWidget, Weather



class MainCanvas(CTkCanvas):
    """
     A class for Main canvas

    Attributes
    ----------
    settings : Settings
        contains info about app settings
    res : float
        app's resolution multiplier
    settings_object : SettingsButton
        contains settings object
    settings_window_on : bool
        state of settings window
    """

    def __init__(self, master):
        """
        Constructs necessary attributes

        Parameters
        ----------
        master : App
            connection to the app
        """
        self.settings = Settings()
        self.res = self.settings.resolution
        super().__init__(master, width=2210 * self.res[0], height=1440 * self.res[1], bg=self.settings.main_color,
                         highlightthickness=0)
        self.settings_object = None
        self.settings_window_on = False

        img = CTkImage(light_image=Image.open("images/settings.png"), size=(50 * self.res[0], 50 * self.res[1]))
        b_settings = CTkButton(self, image=img, text="", fg_color=self.settings.main_color,
                               hover_color=self.settings.second_color,
                               command=self.open_settings)
        self.create_window(2170 * self.res[0], 30 * self.res[1], window=b_settings, height=50 * self.res[0],
                           width=70 * self.res[1])

    def open_settings(self):
        """
        opens settings window

        Returns
        -------
        None
        """
        if not self.settings_window_on or not self.settings_object.settings_on:
            self.settings_object = SettingsButton(self)
            self.settings_object.wm_attributes("-topmost", True)
            self.settings_window_on = True
            self.settings_object.protocol("WM_DELETE_WINDOW", self.settings_on_closing)
        else:
            self.settings_object.destroy()
            self.settings_window_on = False

    def settings_on_closing(self):
        """
        destroys settings window

        Returns
        -------
        None
        """
        self.settings_window_on = False
        self.settings_object.destroy()


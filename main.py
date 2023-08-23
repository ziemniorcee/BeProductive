from customtkinter import CTkCanvas, CTkImage, CTkButton, CTk
import customtkinter
from Data import Date, Weather
from actions import *
from settings import Settings, SettingsButton
from start import Start_window
from habit import HabitWindow
from strategy import Strategy
from goals import GoalsWindow
from timeline import TimelineWindow, TimelineWidget
from floatbar import FloatBar


class SidebarCanvas(CTkCanvas):
    """
    A class for Sidebar canvas

    Attributes
    ----------
    settings : Settings
        contains info about app settings
    res : float
        app's resolution multiplier
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
        bg_colors = ["#F7F7F5", "#202020"]
        super().__init__(master, width=350, height=1440 * self.res[1], bg=bg_colors[self.settings.theme],
                         highlightthickness=0)

        b_dayinfo = CTkButton(self, text="Day info", font=("Arial", 30), fg_color=self.settings.second_color,
                              bg_color=self.settings.second_color, hover_color=self.settings.main_color,
                              border_color=self.settings.second_color, text_color=self.settings.font_color,
                              border_width=10, command=self.master.c_start.create_main_window)
        self.create_window(175, 100, window=b_dayinfo, width=250, height=100)

        b_habit_tracker = CTkButton(self, text="Habit Tracker", font=("Arial", 30),
                                    fg_color=self.settings.second_color,
                                    bg_color=self.settings.second_color, hover_color=self.settings.main_color,
                                    border_color=self.settings.second_color, text_color=self.settings.font_color,
                                    border_width=10, command=self.master.c_habit.create_habit_window)
        self.create_window(175, 225, window=b_habit_tracker, width=250, height=100)

        b_strategy = CTkButton(self, text="Life Strategy", font=("Arial", 30), fg_color=self.settings.second_color,
                               bg_color=self.settings.second_color, hover_color=self.settings.main_color,
                               border_color=self.settings.second_color, text_color=self.settings.font_color,
                               border_width=10, command=self.master.c_strategy.build_window)
        self.create_window(175, 350, window=b_strategy, width=250, height=100)

        b_float_bar = CTkButton(self, text="Float bar", font=("Arial", 30), fg_color=self.settings.second_color,
                                bg_color=self.settings.second_color, hover_color=self.settings.main_color,
                                border_color=self.settings.second_color, text_color=self.settings.font_color,
                                border_width=10, command=self.master.c_floatbar.build_floatbar)
        self.create_window(175 , 1150 * self.res[1], window=b_float_bar, width=250, height=100)

        self.create_line(30, 1230 * self.res[1], 320, 1230 * self.res[1], fill=self.settings.second_color, width=5)
        self.create_text(230, 1300 * self.res[1], text=f" {self.master.today_data.formatted_date} ",
                         font=self.settings.font, fill=self.settings.font_color)
        self.create_image(70, 1300 * self.res[1], image=create_imagetk(self.master.weather_data.image, 125, 125))


class App(CTk):
    """
    A class for the app construct

    Methods
    ---------
    create_c_main():
        creates main canvas
    create_c_sidebar():
        creates sidebar canvas
    open_settings():
        opens settings window
    settings_on_closing():
        closes settings window
    """

    def __init__(self):
        """
        Constructs all needed attributes and objects

        """
        super().__init__()
        self.settings = Settings(self)
        self.title("Better Tomorrow")
        self.geometry(f"{self.settings.resolution_w_h[0]}dx{self.settings.resolution_w_h[1]}+0+0")

        if self.winfo_screenwidth() <= self.settings.resolution_w_h[0]:
            self.after(0, lambda: self.state('zoomed'))

        self.today_data = Date()
        self.weather_data = Weather()

        self.strategy = Strategy(self)

        self.page = 0
        self.c_timeline = None
        self.c_timeline = TimelineWindow(self)
        self.c_timeline.grid(row=0, column=1)
        self.c_timeline.grid_remove()

        self.c_goals = GoalsWindow(self)
        self.c_goals.grid(row=0, column=1)
        self.c_goals.grid_remove()

        self.c_start = Start_window(self)
        self.c_start.grid(row=0, column=1)

        self.c_habit = HabitWindow(self)
        self.c_habit.grid(row=0, column=1)
        self.c_habit.grid_remove()

        self.c_strategy = Strategy(self)
        self.c_strategy.grid(row=0, column=1)
        self.c_strategy.grid_remove()

        self.c_floatbar = FloatBar(self)
        self.c_floatbar.grid(row=0, column=0)
        self.c_floatbar.grid_remove()

        self.c_sidebar = SidebarCanvas(self)
        self.c_sidebar.grid(row=0, column=0)
        self.c_start.create_main_window()


if __name__ == "__main__":
    app = App()
    app.mainloop()

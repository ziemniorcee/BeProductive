from customtkinter import CTkCanvas, CTkImage, CTkButton, CTk
from Data import Date, Weather
from actions import *
from settings import Settings, SettingsButton
from start import Start_window
from habit import HabitWindow
from strategy import Strategy
from goals import GoalsWindow
from timeline import TimelineWindow


class SidebarCanvas(CTkCanvas):
    def __init__(self, master):
        self.settings = Settings()
        res = self.settings.resolution
        super().__init__(master, width = 350, height=1440*res[0], bg="#202020", highlightthickness=0)

        b_dayinfo = CTkButton(self, text="Day info", font=("Arial", 30), fg_color=self.settings.second_color,
                              bg_color=self.settings.second_color, hover_color="black",
                              border_color=self.settings.second_color,
                              border_width=10, command=self.master.main.create_main_window)
        self.create_window(175, 100, window=b_dayinfo, width=250, height=100)

        b_habit_tracker = CTkButton(self, text="Habit Tracker", font=("Arial", 30),
                                    fg_color=self.settings.second_color,
                                    bg_color=self.settings.second_color, hover_color="black",
                                    border_color=self.settings.second_color,
                                    border_width=10, command=self.master.habit.create_habit_window)
        self.create_window(175, 225, window=b_habit_tracker, width=250, height=100)

        b_strategy = CTkButton(self, text="Life Strategy", font=("Arial", 30), fg_color=self.settings.second_color,
                               bg_color=self.settings.second_color, hover_color="black",
                               border_color=self.settings.second_color,
                               border_width=10, command=self.master.strategy.create_strategy_window)

        self.create_window(175, 350, window=b_strategy, width=250, height=100)

        self.create_line(30, 1230 * res[1], 320, 1230 * res[1], fill=self.settings.second_color, width=5)
        self.create_text(230, 1300 * res[1], text=f" {self.master.today_data.formatted_date} ", font=self.settings.font,
                                   fill=self.settings.font_color)
        self.create_image(70, 1300 * res[1], image=create_imagetk(self.master.weather_data.image, 125, 125))

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
        self.settings = Settings()
        super().__init__()
        self.title("Better Tomorrow")
        width, height = self.winfo_screenwidth(), self.winfo_screenheight()

        # self.geometry("1920x1080")
        self.geometry(f"{width}dx{height}+0+0")
        self.after(0, lambda: self.state('zoomed'))

        self.today_data = Date()
        self.weather_data = Weather()
        self.c_main = None

        self.main = Start_window(self)
        self.goals = GoalsWindow(self)
        self.timeline = TimelineWindow(self)
        self.habit = HabitWindow(self)
        self.strategy = Strategy(self)

        self.page = 0

        self.c_sidebar = SidebarCanvas(self)
        self.c_sidebar.grid(row=0, column=0)

        # self.create_c_sidebar()
        self.create_c_main()
        self.main.create_main_window()

        self.settings_object = None
        self.settings_window_on = False

    def create_c_main(self):
        """
        creates main canvas

        Returns
        -------
        None
        """
        res = self.settings.resolution
        if self.c_main is not None:
            self.c_main.destroy()
        self.c_main = CTkCanvas(self, width=2210*res[0], height=1440*res[1], bg=self.settings.main_color, highlightthickness=0)
        self.c_main.grid(row=0, column=1)

        img = CTkImage(light_image=Image.open("images/settings.png"), size=(50 * res[0], 50 * res[1]))

        b_settings = CTkButton(self, image=img, text="", fg_color=self.settings.main_color,
                                    hover_color=self.settings.second_color,
                                    command=self.open_settings, )
        self.c_main.create_window(2170 * res[0], 30 * res[1], window=b_settings, height=50 * res[0], width=70 * res[1])


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


if __name__ == "__main__":
    app = App()
    app.mainloop()

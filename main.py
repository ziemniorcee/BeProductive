import customtkinter
from customtkinter import *

from Data import Date, Weather
from actions import *
from settings import *
from setup import Setup1, Setup2
from start import Start_window
from habit import Habit_tracker
from strategy import Strategy


class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Better Tomorrow")
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))
        self.after(0, lambda: self.state('zoomed'))

        self.bind("<Configure>", self.resize)

        self.today_data = Date()
        self.weather_data = Weather()
        self.c_main = None

        self.main = Start_window(self)
        self.setup1 = Setup1(self)
        self.setup2 = Setup2(self)
        self.habit = Habit_tracker(self)
        self.strategy = Strategy(self)
        self.page = 0

        self.create_c_sidebar()
        self.main.create_main_window()

        self.settings_window = None
        self.is_settings_window_on = False

    # create elements
    def create_c_main(self):
        if self.c_main is not None:
            self.c_main.destroy()
        self.c_main = CTkCanvas(self, width=2160, height=1440, bg=COL_1, highlightthickness=0)
        self.c_main.grid(row=0, column=1)

        img = CTkImage(light_image=Image.open("images/settings.png"), size=(50, 50))
        self.settings = CTkButton(self, image=img, text="", fg_color=COL_1, hover_color=COL_2,
                                  command=self.open_settings, )
        self.c_main.create_window(2120, 30, window=self.settings, height=50, width=70)

    def create_c_sidebar(self):
        print("popo ", COL_2)
        self.c_sidebar = CTkCanvas(self, width=400, height=1440,
                                   bg="black", highlightthickness=0)
        self.c_sidebar.grid(row=0, column=0)
        self.b_dayinfo = CTkButton(self, text="Day info", font=("Arial", 40), fg_color=COL_2,
                                   bg_color=COL_2, hover_color="black", border_color=COL_2,
                                   border_width=10, command=self.main.create_main_window)
        self.c_sidebar.create_window(200, 100, window=self.b_dayinfo, width=300, height=100)

        self.b_habit_tracker = CTkButton(self, text="Habit Tracker", font=("Arial", 40), fg_color=COL_2,
                                         bg_color=COL_2, hover_color="black", border_color=COL_2,
                                         border_width=10, command=self.habit.create_habit_window)
        self.c_sidebar.create_window(200, 225, window=self.b_habit_tracker, width=300, height=100)

        self.b_strategy = CTkButton(self, text="Life Stategy", font=("Arial", 40), fg_color=COL_2,
                                    bg_color=COL_2, hover_color="black", border_color=COL_2,
                                    border_width=10, command=self.strategy.create_strategy_window)
        self.c_sidebar.create_window(200, 350, window=self.b_strategy, width=300, height=100)

        self.c_sidebar.create_line(30, 1230, 370, 1230, fill=COL_2, width=5)
        self.c_sidebar.create_text(260, 1300, text=f" {self.today_data.formatted_date} ", font=FONT, fill=COL_FONT)
        self.c_sidebar.create_image(90, 1300, image=create_imagetk(self.weather_data.image, 150, 150))

    def resize(self, e):
        pass

    def open_settings(self):
        if not self.is_settings_window_on or not self.settings_window.is_settings_on:
            self.settings_window = Settings(self)
            self.settings_window.wm_attributes("-topmost", True)
            self.is_settings_window_on = True
            self.settings_window.protocol("WM_DELETE_WINDOW", self.settings_on_closing)
        else:
            self.settings_window.destroy()
            self.is_settings_window_on = False

    def settings_on_closing(self):
        self.is_settings_window_on = False
        self.settings_window.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()

from customtkinter import CTkCanvas, CTkImage, CTkButton, CTk
from Data import Date, Weather
from actions import *
from settings import Settings, SettingsButton
from start import Start_window
from habit import HabitWindow
from strategy import Strategy
from goals import GoalsWindow
from timeline import TimelineWindow


class FloatBar():
    def __init__(self, master):
        self.app = master
        self.settings = Settings()

        self.previous_pos = [2450,400]
        self.app.attributes('-topmost', True)
        self.app.state("normal")
        self.app.overrideredirect(True)
        self.app.c_main.destroy()
        self.app.c_sidebar.destroy()

        self.app.geometry('%dx%d+%d+%d' % (100, 100, 2450, 400))
        self.c_float_bar = CTkCanvas(self.app, width=400, height=400, bg=self.settings.main_color, highlightthickness=0)
        self.c_float_bar.grid(row=0, column=0)

        self.laurels = self.c_float_bar.create_image(0, 0, image=create_imagetk("images/floatbar/laura.png", 100, 100),
                                                     anchor="nw", tag="laurels")

        self.c_float_bar.tag_bind("laurels", "<Button-1>", self.laurels_press)
        self.c_float_bar.tag_bind("laurels", "<B1-Motion>", self.laurels_move)
        self.c_float_bar.tag_bind("laurels", "<ButtonRelease-1>", self.laurels_unpress)


    def laurels_press(self, e):
        self.c_float_bar.itemconfigure(self.laurels, image=create_imagetk("images/floatbar/laura2.png", 100, 100))

    def laurels_move(self, e):
        current_pos = [e.x + self.previous_pos[0]-50, e.y + self.previous_pos[1] - 50]
        self.app.geometry('%dx%d+%d+%d' % (100, 100, current_pos[0], current_pos[1]))
        self.previous_pos = current_pos

    def laurels_unpress(self, e):
        self.c_float_bar.itemconfigure(self.laurels, image=create_imagetk("images/floatbar/laura.png", 100, 100))
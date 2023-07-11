from actions import *
from settings import *
from customtkinter import *
from Data import Date, Weather


class Start_window:
    def __init__(self, root):
        self.app = root

        self.today_data = Date()
        self.weather_data = Weather()

    def create_main_window(self):
        self.app.page = 0
        self.app.setup1.goals_site = 0
        self.app.create_c_main()
        self.app.setup1.widget_goals()
        self.app.c_main.create_text(400, 185, text="Goals for today", font=("Arial", 30), fill=COL_FONT)
        self.app.c_main.create_line(250, 210, 550, 210, fill=COL_2, width=5)

        img = CTkImage(light_image=Image.open("images/goals/up2.png"), size=(50, 50))
        self.arr_up = CTkButton(self.app, image=img, text="",
                                command=lambda: self.app.setup1.widget_goals(0),
                                fg_color=COL_1, hover_color=COL_2)

        self.app.c_main.create_window(575, 190, window=self.arr_up, width=70, height=70)
        img = CTkImage(light_image=Image.open("images/goals/down2.png"), size=(50, 50))
        
        self.arr_down = CTkButton(self.app, image=img, text="",
                                  fg_color=COL_1, hover_color=COL_2,
                                  command=lambda: self.app.setup1.widget_goals(1))
        self.app.c_main.create_window(225, 190, window=self.arr_down, width=70, height=70)

        self.app.c_main.create_image(1080, 250, image=create_imagetk(self.weather_data.image, 500, 500))
        self.app.c_main.create_text(1080, 220, text=f" {self.weather_data.temperature[0]}", font=FONT,
                                    fill=COL_FONT)
        self.app.c_main.create_text(1080, 260, text=f"Feels like: {self.weather_data.temperature[1]}",
                                    font=("Arial", 15),
                                    fill=COL_FONT)
        self.app.setup2.widget_timeline()
        self._b_start_make()
        self.app.c_main.create_window(1080, 800, window=self.b_start, width=400, height=150)
        self.app.c_main.create_line(555, 1330, 1555, 1330, fill=COL_2, width=6)

        self.app.habit.widget_habits()

    def _b_start_make(self):
        option = 3
        texts = ["Plan your day", "Create goals", "Create blocks", "Configure setup"]

        if len(self.app.setup1.goals_texts) == 0 and self.app.setup2.tl_blocks == 0:
            option = 0
        elif len(self.app.setup1.goals_texts) == 0:
            option = 1
        elif len(self.app.setup2.tl_blocks) == 0:
            option = 2

        self.b_start = CTkButton(self.app, text=texts[option], fg_color="transparent", font=("Arial", 50),
                                 border_width=12, border_color=COL_2,
                                 text_color=("gray10", "#DCE4EE"), command=self.app.setup1.create_setup1_window,
                                 corner_radius=100, hover_color=COL_2)

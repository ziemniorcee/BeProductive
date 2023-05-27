from actions import *
from settings import *
from customtkinter import *
from Data import Date, Weather


class start_window:
    def __init__(self, root):
        self.app = root

        self.today_data = Date()
        self.weather_data = Weather()

    def create_c_sidebar(self):
        self.c_sidebar = CTkCanvas(self.app, width=400, height=1440,
                                   bg="black", highlightthickness=0)
        self.c_sidebar.grid(row=0, column=0)
        self.b_dayinfo = CTkButton(self.app, text="Day info", font=("Arial", 40), fg_color=COL_2,
                                   bg_color=COL_2, hover_color="black", border_color=COL_2,
                                   border_width=10, command=self.create_main_window)
        self.c_sidebar.create_window(200, 100, window=self.b_dayinfo, width=300, height=100)
        self.c_sidebar.create_image(200, 1300, image=create_imagetk("images/line.png", 350, 100))
        self.c_sidebar.create_text(260, 1370, text=f" {self.today_data.formatted_date} ", font=FONT, fill=COL_FONT)
        self.c_sidebar.create_image(90, 1370, image=create_imagetk(self.weather_data.image, 150, 150))

    def create_main_window(self):
        self.app.setup1.goals_site = 0
        self.app.create_c_main()
        self.app.setup1.show_goals()
        self.app.c_main.create_text(400, 185, text="Goals for today", font=("Arial", 30), fill=COL_FONT)
        self.app.c_main.create_image(400, 210, image=create_imagetk("images/line.png", 300, 100))

        img = CTkImage(light_image=Image.open("images/goals/up2.png"), size=(50, 50))
        self.arr_up = CTkButton(self.app, image=img, text="",
                                command=lambda: self.app.setup1.show_goals(0),
                                fg_color=COL_1, hover_color=COL_2)

        self.app.c_main.create_window(575, 190, window=self.arr_up, width=70, height=70)
        img = CTkImage(light_image=Image.open("images/goals/down2.png"), size=(50, 50))
        self.arr_down = CTkButton(self.app, image=img, text="",
                                  fg_color=COL_1, hover_color=COL_2,
                                  command=lambda: self.app.setup1.show_goals(1))
        self.app.c_main.create_window(225, 190, window=self.arr_down, width=70, height=70)

        self.app.c_main.create_image(1080, 250, image=create_imagetk(self.weather_data.image, 500, 500))
        self.app.c_main.create_text(1080, 220, text=f" {self.weather_data.temperature[0]}", font=FONT,
                                    fill=COL_FONT)
        self.app.c_main.create_text(1080, 260, text=f"Feels like: {self.weather_data.temperature[1]}",
                                    font=("Arial", 15),
                                    fill=COL_FONT)
        self.b_start = CTkButton(self.app, text="Plan your day", fg_color="transparent", font=("Arial", 50),
                                 border_width=12, border_color=COL_2,
                                 text_color=("gray10", "#DCE4EE"), command=self.app.setup1.create_setup1_window,
                                 corner_radius=100, hover_color=COL_2)
        self.app.c_main.create_window(1080, 800, window=self.b_start, width=400, height=150)

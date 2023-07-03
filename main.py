from customtkinter import *

from Data import Date, Weather
from actions import *
from settings import *
from setup import Setup1, Setup2
from start import start_window


class App(CTk):
    def __init__(self):
        super().__init__()
        self.title("Better Tomorrow")
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (w, h))
        self.after(0, lambda: self.state('zoomed'))

        self.bind("<Configure>", self.resize)
        # data
        self.today_data = Date()
        self.weather_data = Weather()
        self.c_main = None

        self.main = start_window(self)
        self.setup1 = Setup1(self)
        self.setup2 = Setup2(self)
        self.page = 0

        self.create_c_sidebar()
        self.main.create_main_window()

    # create elements
    def create_c_main(self):
        if self.c_main is not None:
            self.c_main.destroy()
        self.c_main = CTkCanvas(self, width=2160, height=1440, bg=COL_1, highlightthickness=0)
        self.c_main.grid(row=0, column=1)

    def create_c_sidebar(self):
        self.c_sidebar = CTkCanvas(self, width=400, height=1440,
                                   bg="black", highlightthickness=0)
        self.c_sidebar.grid(row=0, column=0)
        self.b_dayinfo = CTkButton(self, text="Day info", font=("Arial", 40), fg_color=COL_2,
                                   bg_color=COL_2, hover_color="black", border_color=COL_2,
                                   border_width=10, command=self.main.create_main_window)
        self.c_sidebar.create_window(200, 100, window=self.b_dayinfo, width=300, height=100)
        self.c_sidebar.create_image(200, 1230, image=create_imagetk("images/line.png", 350, 100))
        self.c_sidebar.create_text(260, 1300, text=f" {self.today_data.formatted_date} ", font=FONT, fill=COL_FONT)
        self.c_sidebar.create_image(90, 1300, image=create_imagetk(self.weather_data.image, 150, 150))

    def resize(self, e):
        pass


if __name__ == "__main__":
    app = App()
    app.mainloop()

import customtkinter

from start import start_window
from Data import Date, Weather
from actions import *
from clock import Clock
from settings import *
from setup import Setup1
import os.path


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Better Tomorrow")
        self.attributes("-fullscreen", True)

        # data
        self.today_data = Date()
        self.weather_data = Weather()
        self.c_main = None

        self.clock = Clock()
        self.click = 0

        self.w_main = start_window(self)
        self.setup1 = Setup1(self)
        self.w_main.create_c_sidebar()
        self.w_main.create_main_window()

    def w_setup2(self):
        """setup - creating focus blocks"""
        self.setup1.save_goals_to_file()
        self.create_c_main()

        self.c_main.create_text(1080, 60, text="Create focus blocks", font=FONT, fill=COL_FONT)
        self.c_main.create_image(1080, 100, image=create_imagetk("images/line.png", 450, 150))

        # self.timer = customtkinter.CTkLabel(self, text="00:00:00", font=FONT_TIMER, text_color=COL_FONT, width=500,
        #                                     height=50)
        # self.timer.grid(row=1, column=0)
        # self.c_clock = customtkinter.CTkCanvas(self, width=500, height=500, bg=COL_1, highlightthickness=0)
        # self.c_clock.grid(row=2, column=0)
        # self.c_clock.create_image(250, 250, image=create_imagetk("images/clock/clock.png", 500, 500))
        #
        # self.img = ImageTk.PhotoImage(file="images/clock/hand2.png")
        # self.hand1 = self.c_clock.create_image(250, 250, image=self.img, tags=("meta",))
        #
        # self.c_clock.tag_bind("meta", "<B1-Motion>", self.move)
        # self.c_clock.tag_bind("meta", "<Button-1>", self.press)
        # self.c_clock.tag_bind("meta", "<ButtonRelease-1>", self.unpress)

    # create elements
    def create_c_main(self):
        if self.c_main is not None:
            self.c_main.destroy()
        self.c_main = customtkinter.CTkCanvas(self, width=2160, height=1440, bg=COL_1, highlightthickness=0)
        self.c_main.grid(row=0, column=1)
        self.b_exit = customtkinter.CTkButton(self, text="×", font=("Arial", 60), fg_color="black", bg_color="black",
                                              hover_color="red", command=lambda: self.quit())
        self.c_main.create_window(2135, 125, window=self.b_exit, width=50, height=50)

    # setup2 features
    def move(self, e):
        if self.click:
            self.clock.calculate_angle(e.x, e.y)

            self.img = Image.open("images/hand2_c.png")
            self.img = ImageTk.PhotoImage(self.img.rotate(-self.clock.angle))
            self.hand1 = self.c_clock.create_image(250, 250, image=self.img, tags=("meta",))

            self.timer.configure(text=self.clock.clock_time())
            self.clock.dot_validation()

    def press(self, e):
        x = self.clock.dot_pos[0]
        y = self.clock.dot_pos[1]
        if x + 17 > e.x > x - 17 and y + 17 > e.y > y - 17:
            self.img = Image.open("images/hand2_c.png")
            self.img = ImageTk.PhotoImage(self.img.rotate(-self.clock.angle))
            self.hand1 = self.c_clock.create_image(250, 250, image=self.img, tags=("meta",))
            self.click = 1

    def unpress(self, *_):
        self.click = 0
        self.img = Image.open("images/hand2.png")
        self.img = ImageTk.PhotoImage(self.img.rotate(-self.clock.angle))
        self.hand1 = self.c_clock.create_image(250, 250, image=self.img, tags=("meta",))


if __name__ == "__main__":
    app = App()
    app.mainloop()

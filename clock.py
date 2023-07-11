import math
from customtkinter import *
from settings import *
from actions import *
from CTkColorPicker import *
from CTkMessagebox import *


class Clock(CTkToplevel):
    def __init__(self, root):
        super().__init__()
        self.is_clock_on = True
        self.setup2 = root

        self.last = 0
        self.round1 = 0
        self.hour = 0
        self.minutes = 0
        self.direction = 1
        self.reverse = 0
        self.angle = 0
        self.dot_pos = (250, 163)
        self.click = 0

        self.categories = {"#0000FF": "work", "#FFFF00": "study"}
        self.buttons = []
        self.window = 0
        self.color = None

        self.b_prev = None
        self.b_next = None
        self.create_setup2_clock()

    def create_setup2_clock(self):
        self.hour = 0
        self.minutes = 0

        self.angle = 0
        self.dot_pos = (250, 163)

        if self.window == 1:
            self.b_prev.destroy()
            self.b_next.destroy()
            self.e_category.destroy()
        self.geometry('%dx%d+%d+%d' % (500, 700, 700, 300))
        self.head = CTkCanvas(self, width=500, height=70, bg=COL_1, highlightthickness=0)
        self.header = self.head.create_text(250, 25, text="Select length of focus block", font=FONT, fill=COL_FONT)
        self.head.create_line(50, 55, 450, 55, fill=COL_2, width=5)
        self.head.grid(row=0, column=0, columnspan=2)

        self.l_timer = CTkLabel(self, text="00:00:00", font=FONT_TIMER, text_color=COL_FONT, width=500, height=50)
        self.l_timer.grid(row=1, column=0, columnspan=2)

        self.c_clock = CTkCanvas(self, width=500, height=500, bg=COL_1, highlightthickness=0)
        self.c_clock.grid(row=2, column=0, columnspan=2)
        self.c_clock.create_image(250, 250, image=create_imagetk("images/clock/clock.png", 500, 500))
        self.img = ImageTk.PhotoImage(file="images/clock/hand2.png")
        self.hand1 = self.c_clock.create_image(250, 250, image=self.img, tags=("meta",))

        self.b_prev = CTkButton(self, text="Cancel", font=FONT, fg_color=COL_2, hover_color="red", border_color=COL_2,
                                border_width=5, command=self.quit_clock)
        self.b_prev.grid(row=3, column=0)
        self.b_next = CTkButton(self, text="Next", font=FONT, fg_color=COL_2, hover_color="green", border_color=COL_2,
                                border_width=5, command=self.accept_time)
        self.b_next.grid(row=3, column=1)

        self.c_clock.tag_bind("meta", "<B1-Motion>", self.move)
        self.c_clock.tag_bind("meta", "<Button-1>", self.press)
        self.c_clock.tag_bind("meta", "<ButtonRelease-1>", self.unpress)
        self.window = 0

    def quit_clock(self):
        self.is_clock_on = False
        self.destroy()

    def accept_time(self):
        if self.hour != 0 or self.minutes != 0:
            self.go_next()
        else:
            CTkMessagebox(title="Error", message="Enter length of focus")

    def go_next(self):
        self.c_clock.destroy()
        self.head.itemconfigure(self.header, text="Select category")
        self.l_timer.destroy()
        self.geometry('%dx%d+%d+%d' % (500, 300, 700, 300))
        self.b_prev.grid(row=4, column=0)
        self.b_next.grid(row=4, column=1)
        self.b_next.configure(text="Accept", command=self.accept_settings)
        self.b_prev.configure(text="Previous", command=self.create_setup2_clock)

        self.b_color_picker = CTkButton(self, text="Set Color", fg_color=COL_2, font=("Arial", 30), border_width=5,
                                        border_color=COL_2, command=self.ask_color)
        self.b_color_picker.grid(row=1, column=0, columnspan=2)
        self.l_info = CTkLabel(self, text="Name category:", font=FONT, text_color=COL_FONT)
        self.l_info.grid(row=2, column=0, columnspan=2)
        self.e_category = CTkEntry(self, width=400, font=FONT_TEXT)
        self.e_category.grid(row=3, column=0, columnspan=2, pady=10)
        self.window = 1

        reg = self.register(lambda input1: (FONT_BOX.getbbox(input1)[2] < 350))
        self.e_category.configure(validate="key", validatecommand=(reg, '%P'))

    def ask_color(self):
        pick_color = AskColor()
        self.color = pick_color.get()
        if self.color is not None:
            self.b_color_picker.configure(border_color=self.color)

    def accept_settings(self):
        message = ""
        value = self.e_category.get()
        if value == "" and self.color is None:
            message = "Enter category name and set color!"
        elif value == "":
            message = "Enter category!"
        elif self.color is None:
            message = "Set color!"

        if message != "":
            CTkMessagebox(title="Error", message=message)
        else:
            print("xd2")
            self.setup2.new_block = [self.hour * 60 + self.minutes, self.color, value]
            self.setup2.clock_on_closing()

    def calculate_angle(self, x, y):
        """Return angle based on cursor """
        if y <= 250 and x >= 250:
            a = 250 - y
            b = x - 250
            if a == 0:
                self.angle = 90
            else:
                tangens = b / a
                self.angle = math.degrees(math.atan(tangens))
        elif y >= 250 and x >= 250:
            a = y - 250
            b = x - 250

            if b == 0:
                self.angle = 180
            else:
                tangens = a / b
                self.angle = math.degrees(math.atan(tangens)) + 90
        elif y >= 250 and x <= 250 and self.round1 != 0:
            a = y - 250
            b = 250 - x

            if a == 0:
                self.angle = 270
            else:
                tangens = b / a
                self.angle = math.degrees(math.atan(tangens)) + 180
        elif y <= 250 and x <= 250 and self.round1 != 0:
            a = 250 - y
            b = 250 - x

            if a == 0:
                self.angle = 0
            else:
                tangens = a / b
                self.angle = math.degrees(math.atan(tangens)) + 270

        return int(self.angle)

    def clock_time(self):
        """returns time based on angle"""
        if self.last > self.angle:
            self.direction = 0
            self.round1 = 1
            if self.last - self.angle > 200:
                self.hour += 1
        elif self.last < self.angle:
            self.direction = 1

        if self.direction:
            if self.angle > 90 and self.round1 == 0:
                self.round1 = 1
        else:
            if self.angle > 300 and self.reverse == 0 and self.hour > 0:
                self.reverse = 1
                self.hour -= 1
            elif self.reverse == 1 and self.angle < 180 and self.hour > 0:
                self.reverse = 0
            elif self.hour == 0 and self.angle < 90:
                self.round1 = 0
        self.last = self.angle

        prompt_hour = str(self.hour)
        self.minutes = int(self.angle / 6)
        prompt_minutes = str(self.minutes)
        if self.hour < 10:
            prompt_hour = "0" + prompt_hour
        if self.minutes < 10:
            prompt_minutes = "0" + prompt_minutes
        return f"{prompt_hour}:{prompt_minutes}:00"

    def dot_validation(self):
        y = int(math.cos(math.radians(self.angle)) * 87)
        x = int(math.sin(math.radians(self.angle)) * 87)

        self.dot_pos = (250 + x, 250 - y)

        # setup2 features

    def move(self, e):
        if self.click:
            self.calculate_angle(e.x, e.y)
            self.img = Image.open("images/clock/hand2_c.png")
            self.img = ImageTk.PhotoImage(self.img.rotate(-self.angle))
            self.hand1 = self.c_clock.create_image(250, 250, image=self.img, tags=("meta",))
            self.l_timer.configure(text=self.clock_time())
            self.dot_validation()

    def press(self, e):
        x = self.dot_pos[0]
        y = self.dot_pos[1]
        if x + 17 > e.x > x - 17 and y + 17 > e.y > y - 17:
            self.img = Image.open("images/clock/hand2_c.png")
            self.img = ImageTk.PhotoImage(self.img.rotate(-self.angle))
            self.hand1 = self.c_clock.create_image(250, 250, image=self.img, tags=("meta",))
            self.click = 1

    def unpress(self, *_):
        self.click = 0
        self.img = Image.open("images/clock/hand2.png")
        self.img = ImageTk.PhotoImage(self.img.rotate(-self.angle))
        self.hand1 = self.c_clock.create_image(250, 250, image=self.img, tags=("meta",))

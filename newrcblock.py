import math
from customtkinter import *
from settings import *
from actions import *
from CTkColorPicker import *
from CTkMessagebox import CTkMessagebox


class NewRCBlock(CTkToplevel):
    """
    A class for new block creation
    
    Attributes
    ----------
    settings : Settings
        constains app settings
    window_on : bool
        defines if window is on
    timeline : Timeline
        connection to the timeline
    last : float
        last angle
    round1 : int
        defines current round of the clock
    hour : int
        hour to display
    minutes : int
        minutes to display
    direction : int
        direction of the clock hand
    reverse : int
        reverse state
    angle : int
        current angle of the hand
    dot_pos : list[int]
        current hand's dot position
    click : int
        is dots clicked
    window : int
        currently displayed window
    color : str
        selected color value
    b_prev : int
        id of previous button
    b_next : int
        id of next button

    Methods
    ----------
    create_window():
        builds new block window
    quit_clock():
        after quitting
    accept_time():
        checks if time is not 0
    go_next():
        builds next window
    ask_color():
        color picker
    accept_settings():
        accepting settings
    calculate_angle():
        calculates current angle
    clock_time():
        defines time based on angle
    dot_validation():
        checks if button is clicked
    move():
        move bind for dot
    press():
        press bind for dot
    unpress():
        unpress bind for dot
    """
    def __init__(self, root):
        """
        Constructs essential attributes for class

        Parameters
        ----------
        root : App
            connection to the app
        """
        self.settings = Settings()
        super().__init__(fg_color = self.settings.main_color)
        self.window_on = True
        self.timeline = root

        self.last = 0
        self.round1 = 0
        self.hour = 0
        self.minutes = 0
        self.direction = 1
        self.reverse = 0
        self.angle = 0
        self.dot_pos = (250, 163)
        self.click = 0

        self.window = 0
        self.color = None

        self.b_prev = None
        self.b_next = None
        self.create_window()

    def create_window(self):
        """
        builds new block window

        Returns
        -------
        None
        """
        self.hour = 0
        self.minutes = 0

        self.angle = 0
        self.dot_pos = (250, 163)

        if self.window == 1:
            self.b_prev.destroy()
            self.b_next.destroy()
            self.e_category.destroy()
        self.geometry('%dx%d+%d+%d' % (500, 700, 700, 300))

        self.head = CTkCanvas(self, width=500, height=70, bg=self.settings.main_color, highlightthickness=0)
        self.header = self.head.create_text(250, 25, text="Select length of focus block", font=self.settings.font,
                                            fill=self.settings.font_color)

        self.head.create_line(50, 55, 450, 55, fill=self.settings.second_color, width=5)
        self.head.grid(row=0, column=0, columnspan=2)

        self.l_timer = CTkLabel(self, text="00:00:00", font=("Arial", 50), text_color=self.settings.font_color, width=500,
                                height=50)
        self.l_timer.grid(row=1, column=0, columnspan=2)

        self.c_clock = CTkCanvas(self, width=500, height=500, bg=self.settings.main_color, highlightthickness=0)
        self.c_clock.grid(row=2, column=0, columnspan=2)
        self.c_clock.create_image(250, 250, image=create_imagetk("images/clock/clock.png", 500, 500))
        self.img = ImageTk.PhotoImage(file="images/clock/hand2.png")
        self.hand1 = self.c_clock.create_image(250, 250, image=self.img, tags=("meta",))

        self.b_prev = CTkButton(self, text="Cancel", font=self.settings.font, fg_color=self.settings.second_color, hover_color="red",
                                border_color=self.settings.second_color,
                                border_width=5, command=self.quit_clock)
        self.b_prev.grid(row=3, column=0)
        self.b_next = CTkButton(self, text="Next", font=self.settings.font, fg_color=self.settings.second_color, hover_color="green",
                                border_color=self.settings.second_color,
                                border_width=5, command=self.accept_time)
        self.b_next.grid(row=3, column=1)

        self.c_clock.tag_bind("meta", "<B1-Motion>", self.move)
        self.c_clock.tag_bind("meta", "<Button-1>", self.press)
        self.c_clock.tag_bind("meta", "<ButtonRelease-1>", self.unpress)
        self.window = 0

    def quit_clock(self):
        """
        after quitting

        Returns
        -------
        None
        """
        self.window_on = False
        self.destroy()

    def accept_time(self):
        """
        checks if time is not 0

        Returns
        -------
        None
        """
        if self.hour != 0 or self.minutes != 0:
            self.go_next()
        else:
            CTkMessagebox(title="Error", message="Enter length of focus")

    def go_next(self):
        """
        builds next window

        Returns
        -------
        None
        """
        self.c_clock.destroy()
        self.head.itemconfigure(self.header, text="Select category")
        self.l_timer.destroy()
        self.geometry('%dx%d+%d+%d' % (500, 300, 700, 300))
        self.b_prev.grid(row=4, column=0)
        self.b_next.grid(row=4, column=1)
        self.b_next.configure(text="Accept", command=self.accept_settings)
        self.b_prev.configure(text="Previous", command=self.create_window)

        self.b_color_picker = CTkButton(self, text="Set Color", fg_color=self.settings.second_color, font=("Arial", 30),
                                        border_width=5,
                                        border_color=self.settings.second_color, command=self.ask_color)
        self.b_color_picker.grid(row=1, column=0, columnspan=2)
        self.l_info = CTkLabel(self, text="Name category:", font=self.settings.font, text_color=self.settings.font_color)
        self.l_info.grid(row=2, column=0, columnspan=2)
        self.e_category = CTkEntry(self, width=400, font=("Arial", 20))
        self.e_category.grid(row=3, column=0, columnspan=2, pady=10)
        self.window = 1

        reg = self.register(lambda input1: (ImageFont.truetype("arial.ttf", 20).getbbox(input1)[2] < 350))
        self.e_category.configure(validate="key", validatecommand=(reg, '%P'))

    def ask_color(self):
        """
        color picker

        Returns
        -------
        None
        """
        pick_color = AskColor()
        self.color = pick_color.get()
        if self.color is not None:
            self.b_color_picker.configure(border_color=self.color)

    def accept_settings(self):
        """
        accepting settings

        Returns
        -------
        None
        """
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
            self.timeline.new_block = [self.hour * 60 + self.minutes, self.color, value]
            self.timeline.clock_on_closing()

    def calculate_angle(self, x, y):
        """
        calculates current angle

        Parameters
        ----------
        x : int
            x position
        y : int
            y position

        Returns
        -------
        None
        """
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
        """
        Calculates the time based on the angle.

        Returns
        -------
        str:
        The time in the format of "HH:MM:SS".
        """
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
        """
        checks if button is clicked

        Returns
        -------
        None
        """
        y = int(math.cos(math.radians(self.angle)) * 87)
        x = int(math.sin(math.radians(self.angle)) * 87)

        self.dot_pos = (250 + x, 250 - y)

        # setup2 features

    def move(self, event):
        """
        move bind for dot

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        if self.click:
            self.calculate_angle(event.x, event.y)
            self.img = Image.open("images/clock/hand2_c.png")
            self.img = ImageTk.PhotoImage(self.img.rotate(-self.angle))
            self.hand1 = self.c_clock.create_image(250, 250, image=self.img, tags=("meta",))
            self.l_timer.configure(text=self.clock_time())
            self.dot_validation()

    def press(self, event):
        """
        press bind for dot

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        x = self.dot_pos[0]
        y = self.dot_pos[1]
        if x + 17 > event.x > x - 17 and y + 17 > event.y > y - 17:
            self.img = Image.open("images/clock/hand2_c.png")
            self.img = ImageTk.PhotoImage(self.img.rotate(-self.angle))
            self.hand1 = self.c_clock.create_image(250, 250, image=self.img, tags=("meta",))
            self.click = 1

    def unpress(self, *_):
        """
        unpress bind for dot

        Returns
        -------
        None
        """
        self.click = 0
        self.img = Image.open("images/clock/hand2.png")
        self.img = ImageTk.PhotoImage(self.img.rotate(-self.angle))
        self.hand1 = self.c_clock.create_image(250, 250, image=self.img, tags=("meta",))

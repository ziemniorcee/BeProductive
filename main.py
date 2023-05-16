import customtkinter
from PIL import ImageFont, ImageTk, Image

from Data import Date, Weather
from actions import *
from clock import Clock
from settings import *


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Better Tomorrow")
        self.attributes("-fullscreen", True)

        # goals
        self.positions = []
        self.label_pos = 0
        self.goals = []

        # clock
        self.clock = Clock()
        self.click = 0

    def welcome_window(self):
        today = Date()
        weather_data = Weather()

        self.c_sidebar = customtkinter.CTkCanvas(self, width=400, height=1440,
                                                 bg="black", highlightthickness=0)
        self.c_sidebar.grid(row=0, column=0)
        self.b_dayinfo = customtkinter.CTkButton(self, text="Day start", font=("Arial", 40), fg_color=COL_2,
                                                 bg_color=COL_2, hover_color="black", border_color=COL_2,
                                                 border_width=10)
        self.c_sidebar.create_window(200, 100, window=self.b_dayinfo, width=300, height=100)
        self.c_sidebar.create_image(200, 1300, image=create_imagetk("images/line.png", 350, 100))
        self.c_sidebar.create_text(260, 1370, text=f" {today.day} ", font=FONT, fill=COL_FONT)
        self.c_sidebar.create_image(90, 1370, image=create_imagetk(weather_data.image, 150, 150))

        self.c_main = customtkinter.CTkCanvas(self, width=2160, height=1440, bg=COL_1, highlightthickness=0)
        self.c_main.grid(row=0, column=1)
        self.weather1 = self.c_main.create_image(1080, 250, image=create_imagetk(weather_data.image, 500, 500))
        self.weather2 = self.c_main.create_text(1080, 220, text=f" {weather_data.temperature[0]}", font=FONT,
                                                fill=COL_FONT)
        self.weather3 = self.c_main.create_text(1080, 260, text=f"Feels like: {weather_data.temperature[1]}",
                                                font=("Arial", 15),
                                                fill=COL_FONT)
        self.b_start = customtkinter.CTkButton(self, text="Plan your day", fg_color="transparent", font=("Arial", 50),
                                               border_width=12, border_color=COL_2,
                                               text_color=("gray10", "#DCE4EE"), command=self.second_window,
                                               corner_radius=100)
        self.c_main.create_window(1080, 800, window=self.b_start, width=400, height=150)

        self.b_exit = customtkinter.CTkButton(self, text="×", font=("Arial", 60), fg_color="black", bg_color="black",
                                              hover_color="red", command=lambda: self.quit())
        self.c_main.create_window(2135, 25, window=self.b_exit, width=50, height=50)

    def second_window(self):
        self.c_main.itemconfigure(self.weather1, state='hidden')
        self.c_main.itemconfigure(self.weather2, state='hidden')
        self.c_main.itemconfigure(self.weather3, state='hidden')
        self.b_start.destroy()

        self.head1 = self.c_main.create_text(1080, 60, text="Create goals for today", font=FONT, fill=COL_FONT)
        self.head2 = self.c_main.create_image(1080, 100, image=create_imagetk("images/line.png", 450, 150))
        self.arrow = self.c_main.create_image(75, 750, image=create_imagetk("images/arrow.png", ))
        # noinspection PyArgumentList
        self.arrow2 = self.c_main.create_text(20, 750, text="Importance", font=FONT, fill=COL_FONT, anchor="nw",
                                              angle=90)

        self.e_todo = customtkinter.CTkEntry(self, font=FONT_TEXT)
        self.c_main.create_window(1030, 1365, window=self.e_todo, width=1760, height=50)
        self.b_add = customtkinter.CTkButton(self, text="+", font=FONT_ADD, fg_color=COL_2,
                                             command=self.add_goal, border_width=5, hover_color=COL_1,
                                             border_color=COL_2)
        self.c_main.create_window(75, 1365, window=self.b_add, height=50, width=50)

        self.b_yes = customtkinter.CTkButton(self, text="It's all", font=FONT, fg_color=COL_2,
                                             hover_color=COL_1, border_color=COL_2, border_width=5,
                                             command=self.third_screen)
        self.c_main.create_window(2035, 1365, window=self.b_yes, width=150, height=50)

        self.dots = self.c_main.create_image(125, 210, image=create_imagetk("images/dots.png"), tags=("dots",),
                                             state='hidden')
        self.shadow = self.c_main.create_text(-100, -100, text="", font=FONT_TEXT, fill="grey")
        self.c_main.itemconfigure(self.shadow, state='hidden')
        self.line = self.c_main.create_image(-100, -100 + self.label_pos * 60, image=create_imagetk("images/line2.png"),
                                             state='hidden')

        self.c_main.tag_bind("dots", "<B1-Motion>", self.move_dots)
        self.c_main.tag_bind("dots", "<Button-1>", self.press_dots)
        self.c_main.tag_bind("dots", "<ButtonRelease-1>", self.unpress_dots)
        self.c_main.bind('<Motion>', self.position)
        self.e_todo.bind('<Return>', self.add_goal)

        reg = self.register(self.limit_input)
        self.e_todo.configure(validate="key", validatecommand=(reg, '%P'))

    def third_screen(self):

        self.c_main.itemconfigure(self.arrow, state='hidden')
        self.e_todo.destroy()
        self.b_add.destroy()
        self.b_yes.destroy()

        self.c_main.itemconfigure(self.head1, text="Create focus blocks")
        # self.timer = customtkinter.CTkLabel(self, text="00:00:00", font=FONT_TIMER, text_color=COL_FONT, width=500,
        #                                     height=50)
        # self.timer.grid(row=1, column=0)
        # self.c_clock = customtkinter.CTkCanvas(self, width=500, height=500, bg=COL_1, highlightthickness=0)
        # self.c_clock.grid(row=2, column=0)
        # self.c_clock.create_image(250, 250, image=create_imagetk("images/clock.png", 500, 500))
        #
        # self.img = ImageTk.PhotoImage(file="images/hand2.png")
        # self.hand1 = self.c_clock.create_image(250, 250, image=self.img, tags=("meta",))
        #
        # self.c_clock.tag_bind("meta", "<B1-Motion>", self.move)
        # self.c_clock.tag_bind("meta", "<Button-1>", self.press)
        # self.c_clock.tag_bind("meta", "<ButtonRelease-1>", self.unpress)

    def add_goal(self, *_):

        value = self.e_todo.get()
        if value != "":
            i = len(self.goals) + 1

            goal = self.c_main.create_text(150, 140 + i * 60, text=f"{value}",
                                           font=FONT_TEXT,
                                           fill=COL_FONT, anchor="w", tags=f"todo{i}")
            self.goals.append(goal)
            self.positions.append(140 + i * 60)

            self.c_main.tag_bind(f"todo{i}", '<Enter>', self.strike_on)
            self.c_main.tag_bind(f"todo{i}", '<Leave>', self.strike_off)
            self.c_main.tag_bind(f"todo{i}", '<Button-1>', self.del_goal)

            self.e_todo.delete(0, len(value))

    def limit_input(self, input1):

        font = ImageFont.truetype("arial.ttf", 20)
        box = font.getbbox(input1)

        if box[2] < 1640:
            return True
        else:
            return False

    def strike_on(self, event):
        widget_name = event.widget.find_withtag("current")[0]
        self.text = self.c_main.itemcget(widget_name, 'text')

        self.c_main.itemconfigure(widget_name, font=FONT_TEXT_STRIKE)

    def strike_off(self, event):
        widget_name = event.widget.find_withtag("current")[0]

        self.c_main.itemconfigure(widget_name, font=FONT_TEXT)

    def del_goal(self, event):
        widget_name = event.widget.find_withtag("current")[0]

        index = self.goals.index(widget_name)

        for i in range(index, len(self.goals) - 1):
            next_text = self.c_main.itemcget(self.goals[i + 1], 'text')
            self.c_main.itemconfigure(self.goals[i], text=next_text)

        self.c_main.delete(self.goals[-1])
        self.goals.pop()
        self.positions.pop()
        if len(self.goals) != 0:
            self.c_main.moveto(self.dots, 100, self.positions[-1] - 25)

    def position(self, e):
        flag = 0
        y = 0
        for posy in self.positions:
            if posy - 25 < e.y < posy + 25 and 110 < e.x < 140:
                y = posy
                flag = 1

        if flag == 1 and y - 14 < e.y < y + 14:
            self.c_main.itemconfigure(self.dots, state='normal')
            self.c_main.moveto(self.dots, 100, y - 25)
        else:
            self.c_main.itemconfigure(self.dots, state='hidden')

        self.update()

    def move_dots(self, e):
        self.c_main.itemconfigure(self.shadow, state="normal")

        if e.y < 200:
            self.label_pos = 0
        elif e.y > self.positions[-1]:
            self.label_pos = len(self.positions) - 1
        else:
            self.label_pos = int((e.y - 110) / 60) - 1

        self.c_main.moveto(self.line, 150, 150 + self.label_pos * 60)

        if 200 < e.y < self.positions[-1]:
            self.c_main.moveto(self.dots, 100, e.y - 25)
            self.c_main.moveto(self.shadow, 150, e.y - 20)

    def press_dots(self, e):
        text = ""
        self.goal = 0
        self.c_main.itemconfigure(self.line, state='normal')
        for posy in self.positions:
            if posy - 25 < e.y < posy + 25:
                text = self.c_main.itemcget(self.goals[self.goal], 'text')
            else:
                self.goal += 1
        self.c_main.itemconfigure(self.shadow, text=text)
        self.c_main.unbind("<Motion>")

    def unpress_dots(self, e):
        self.c_main.itemconfigure(self.line, state='hidden')
        self.c_main.bind('<Motion>', self.position)
        self.c_main.itemconfigure(self.shadow, state="hidden")
        self.c_main.moveto(self.line, -100, -100)
        self.c_main.moveto(self.shadow, -100, -100)

        print("!", self.goals)
        # change = self.label_pos, self.c_main.itemcget(self.goals[self.label_pos], 'text')
        new_goals = []

        for i in range(len(self.goals)):
            text = ""
            if i < self.label_pos:
                text = self.c_main.itemcget(self.goals[i], 'text')
            elif i == self.label_pos:
                text = self.c_main.itemcget(self.goals[self.goal], 'text')
            elif i > self.label_pos:
                text = self.c_main.itemcget(self.goals[i - 1], 'text')
            new_goals.append(text)

        for i in range(len(self.goals)):
            self.c_main.itemconfigure(self.goals[i], text=new_goals[i])

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

    def unpress(self, e):
        self.click = 0
        self.img = Image.open("images/hand2.png")
        self.img = ImageTk.PhotoImage(self.img.rotate(-self.clock.angle))
        self.hand1 = self.c_clock.create_image(250, 250, image=self.img, tags=("meta",))


if __name__ == "__main__":
    app = App()
    app.welcome_window()
    app.mainloop()

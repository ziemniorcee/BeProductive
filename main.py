import customtkinter

from Data import Date, Weather
from actions import *
from clock import Clock
from settings import *
import os.path


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.c_main = None
        self.title("Better Tomorrow")
        self.attributes("-fullscreen", True)

        # data
        self.today_data = Date()
        self.weather_data = Weather()

        # main
        self.main_goals_widgets = []
        self.which_goals = [0]
        self.goals_site = 0
        self.is_more_sites = 0

        # setup1
        self.goals_widgets = []
        self.goals_texts = []
        self.shadow_line_position = 0
        self.goal_widgets_yposes = []
        self.is_end = 0
        # setup2
        self.clock = Clock()
        self.click = 0
        self.goals_from_file()

    def w_main(self):
        """Creates sidebar, main and other widgets"""
        self.create_c_main()
        self.show_goals()

        self.c_sidebar = customtkinter.CTkCanvas(self, width=400, height=1440,
                                                 bg="black", highlightthickness=0)
        self.c_sidebar.grid(row=0, column=0)
        self.b_dayinfo = customtkinter.CTkButton(self, text="Day info", font=("Arial", 40), fg_color=COL_2,
                                                 bg_color=COL_2, hover_color="black", border_color=COL_2,
                                                 border_width=10, command=self.w_main)
        self.c_sidebar.create_window(200, 100, window=self.b_dayinfo, width=300, height=100)
        self.c_sidebar.create_image(200, 1300, image=create_imagetk("images/line.png", 350, 100))
        self.c_sidebar.create_text(260, 1370, text=f" {self.today_data.formatted_date} ", font=FONT, fill=COL_FONT)
        self.c_sidebar.create_image(90, 1370, image=create_imagetk(self.weather_data.image, 150, 150))

        # Goals section
        self.c_main.create_text(400, 185, text="Goals for today", font=("Arial", 30), fill=COL_FONT)
        self.c_main.create_image(400, 210, image=create_imagetk("images/line.png", 300, 100))

        img = customtkinter.CTkImage(light_image=Image.open("images/goals/up2.png"), size=(50, 50))
        self.arr_up = customtkinter.CTkButton(self, image=img, text="",
                                              fg_color=COL_1, hover_color=COL_2,
                                              command=lambda: self.show_goals(0) if self.is_more_sites else None)

        self.c_main.create_window(575, 190, window=self.arr_up, width=70, height=70)
        img = customtkinter.CTkImage(light_image=Image.open("images/goals/down2.png"), size=(50, 50))
        self.arr_down = customtkinter.CTkButton(self, image=img, text="",
                                                fg_color=COL_1, hover_color=COL_2,
                                                command=lambda: self.show_goals(1) if self.is_more_sites else None)
        self.c_main.create_window(225, 190, window=self.arr_down, width=70, height=70)

        self.c_main.create_image(1080, 250, image=create_imagetk(self.weather_data.image, 500, 500))
        self.c_main.create_text(1080, 220, text=f" {self.weather_data.temperature[0]}", font=FONT,
                                fill=COL_FONT)
        self.c_main.create_text(1080, 260, text=f"Feels like: {self.weather_data.temperature[1]}",
                                font=("Arial", 15),
                                fill=COL_FONT)
        self.b_start = customtkinter.CTkButton(self, text="Plan your day", fg_color="transparent", font=("Arial", 50),
                                               border_width=12, border_color=COL_2,
                                               text_color=("gray10", "#DCE4EE"), command=self.w_setup1,
                                               corner_radius=100, hover_color=COL_2)
        self.c_main.create_window(1080, 800, window=self.b_start, width=400, height=150)

    def w_setup1(self):
        """setup - creating goals"""

        self.goals_widgets = []
        self.create_c_main()

        if len(self.goals_texts) > 0:
            self.goal_widgets_yposes = []
            for goal in self.goals_texts:
                self.show_entry(goal)

        self.c_main.create_text(1080, 60, text="Create goals for today", font=FONT, fill=COL_FONT)
        self.c_main.create_image(1080, 100, image=create_imagetk("images/line.png", 450, 150))
        self.c_main.create_image(75, 750, image=create_imagetk("images/goals/arrow.png", ))
        # noinspection PyArgumentList
        self.c_main.create_text(20, 750, text="Importance", font=FONT, fill=COL_FONT, anchor="nw",
                                angle=90)

        self.e_todo = customtkinter.CTkEntry(self, font=FONT_TEXT)
        self.e_todo.focus()
        self.c_main.create_window(1030, 1365, window=self.e_todo, width=1760, height=50)
        self.b_add = customtkinter.CTkButton(self, text="+", font=FONT_ADD, fg_color=COL_2,
                                             command=self.add_goal, border_width=5, hover_color=COL_1,
                                             border_color=COL_2)
        self.c_main.create_window(75, 1365, window=self.b_add, height=50, width=50)

        self.b_yes = customtkinter.CTkButton(self, text="Submit", font=FONT, fg_color=COL_2,
                                             hover_color=COL_1, border_color=COL_2, border_width=5,
                                             command=self.w_setup2)
        self.c_main.create_window(2035, 1365, window=self.b_yes, width=150, height=50)

        self.dots = self.c_main.create_image(125, 210, image=create_imagetk("images/goals/dots.png"), tags=("dots",),
                                             state='hidden')
        self.shadow = self.c_main.create_text(-100, -100, text="", font=FONT_TEXT, fill="grey")
        self.c_main.itemconfigure(self.shadow, state='hidden')
        self.line = self.c_main.create_image(-100, -100 + self.shadow_line_position * 60,
                                             image=create_imagetk("images/line2.png"),
                                             state='hidden')

        self.c_main.tag_bind("dots", "<B1-Motion>", self.move_dots)
        self.c_main.tag_bind("dots", "<Button-1>", self.press_dots)
        self.c_main.tag_bind("dots", "<ButtonRelease-1>", self.unpress_dots)
        self.c_main.bind('<Motion>', self.position)
        self.e_todo.bind('<Return>', self.add_goal)

        reg = self.register(lambda input1: (FONT_BOX.getbbox(input1)[2] < 1500))
        self.e_todo.configure(validate="key", validatecommand=(reg, '%P'))

    def w_setup2(self):
        """setup - creating focus blocks"""
        self.savegoals()
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

    # actions
    def goals_from_file(self):
        if os.path.isfile("goals.txt"):
            with open("goals.txt", "r") as f:
                lines = f.readlines()
                if len(lines) != 0:
                    for i in range(len(lines)):
                        lines[i] = lines[i].strip()

                    if str(self.today_data.formatted_date) == lines[0]:
                        self.goals_texts = lines[1:]
            print(self.goals_texts)
        else:
            with open("goals.txt", 'x'):
                pass

    def add_goal(self, *_):
        value = self.e_todo.get()
        if value != "":
            self.show_entry(value)
            self.e_todo.delete(0, len(value))
        self.goals_texts = []
        for i in range(len(self.goals_widgets)):
            self.goals_texts.append(self.c_main.itemcget(self.goals_widgets[i], 'text'))

    def show_entry(self, text):
        i = len(self.goals_widgets) + 1

        goal = self.c_main.create_text(150, 140 + i * 60, text=f"{text}",
                                       font=FONT_TEXT,
                                       fill=COL_FONT, anchor="w", tags=f"todo{i}")
        self.goals_widgets.append(goal)
        self.goal_widgets_yposes.append(140 + i * 60)
        # self.goals_list.append(text)

        self.c_main.tag_bind(f"todo{i}", '<Enter>', self.strike_on)
        self.c_main.tag_bind(f"todo{i}", '<Leave>', self.strike_off)
        self.c_main.tag_bind(f"todo{i}", '<Button-1>', self.del_goal)

    def del_goal(self, event):
        widget_name = event.widget.find_withtag("current")[0]

        index = self.goals_widgets.index(widget_name)

        for i in range(index, len(self.goals_widgets) - 1):
            next_text = self.c_main.itemcget(self.goals_widgets[i + 1], 'text')
            self.c_main.itemconfigure(self.goals_widgets[i], text=next_text)

        self.c_main.delete(self.goals_widgets[-1])
        self.goals_widgets.pop()
        self.goal_widgets_yposes.pop()

        if len(self.goals_widgets) != 0:
            self.c_main.moveto(self.dots, 100, self.goal_widgets_yposes[-1] - 25)

        self.goals_texts = []
        for i in range(len(self.goals_widgets)):
            self.goals_texts.append(self.c_main.itemcget(self.goals_widgets[i], 'text'))

    def savegoals(self):
        if len(self.goals_texts) == 0:
            for i in range(len(self.goals_widgets)):
                self.goals_texts.append(self.c_main.itemcget(self.goals_widgets[i], 'text'))

        with open('goals.txt', 'w+') as file:
            file.write(f"{self.today_data.formatted_date}\n")
            for goals in self.goals_texts:
                file.write('%s\n' % goals)

    def show_goals(self, direction=2):
        if direction == 0 and self.goals_site > 0:
            self.goals_site -= 1
        if direction == 1 and self.is_end == 0:
            self.goals_site += 1

        print(self.goals_site)
        for widget in self.main_goals_widgets:
            self.c_main.delete(widget)

        if len(self.goals_texts) != 0:
            i = self.which_goals[self.goals_site]
            start = 1
            end = 1

            for goal in self.goals_texts[i:]:
                i += 1
                end += 1

                goal_list = goal.split(" ")
                full = ""
                actual = ""
                for word in goal_list:
                    box = FONT_BOX.getbbox(actual + word)
                    if box[2] > 300:
                        full += actual + "\n" + word
                        actual = ""
                        end += 1
                    else:
                        actual += " " + word
                full += actual
                if start < 8:
                    print(200 + start * 35 + (end - start) / 2 * 30, end, start)
                    text = self.c_main.create_text(180, 190 + start * 40 + (end - start) * 20, text=f"{i}. {full}",
                                                   font=FONT_TEXT, width=500,
                                                   fill=COL_FONT, justify="left", anchor="w")
                    self.main_goals_widgets.append(text)
                    self.is_end = 1
                else:
                    self.which_goals.append(i - 1)
                    self.is_end = 0
                    self.is_more_sites = 1
                    break
                start = end

    # setup1 functions

    def strike_on(self, event):
        self.c_main.itemconfigure(event.widget.find_withtag("current")[0], font=FONT_TEXT_STRIKE)

    def strike_off(self, event):
        self.c_main.itemconfigure(event.widget.find_withtag("current")[0], font=FONT_TEXT)

    def position(self, e):
        flag = 0
        y = 0
        for posy in self.goal_widgets_yposes:
            if posy - 25 < e.y < posy + 25 and 110 < e.x < 140:
                y = posy
                flag = 1

        if flag == 1 and y - 14 < e.y < y + 14:
            self.c_main.itemconfigure(self.dots, state='normal')
            self.c_main.moveto(self.dots, 100, y - 25)
        else:
            self.c_main.itemconfigure(self.dots, state='hidden')

    def move_dots(self, e):
        self.c_main.itemconfigure(self.shadow, state="normal")

        if e.y < 200:
            self.shadow_line_position = 0
        elif e.y > self.goal_widgets_yposes[-1]:
            self.shadow_line_position = len(self.goal_widgets_yposes)
        else:
            self.shadow_line_position = int((e.y - 110) / 60) - 1

        self.c_main.moveto(self.line, 150, 150 + self.shadow_line_position * 60)

        if 200 < e.y < self.goal_widgets_yposes[-1]:
            self.c_main.moveto(self.dots, 100, e.y - 25)
            self.c_main.moveto(self.shadow, 150, e.y - 20)

    def press_dots(self, e):
        flag = 0
        text = ""
        self.goal = 0
        self.c_main.itemconfigure(self.line, state='normal')
        for posy in self.goal_widgets_yposes:
            if posy - 25 < e.y < posy + 25:
                text = self.c_main.itemcget(self.goals_widgets[self.goal], 'text')
                flag = 1
            elif flag == 0:
                self.goal += 1
        self.c_main.itemconfigure(self.shadow, text=text)
        self.c_main.unbind("<Motion>")

    def unpress_dots(self, *_):
        self.c_main.itemconfigure(self.line, state='hidden')
        self.c_main.bind('<Motion>', self.position)
        self.c_main.itemconfigure(self.shadow, state="hidden")
        self.c_main.moveto(self.line, -100, -100)
        self.c_main.moveto(self.shadow, -100, -100)

        self.goals_texts = []

        for i in range(len(self.goals_widgets)):
            self.goals_texts.append(self.c_main.itemcget(self.goals_widgets[i], 'text'))

        text = self.c_main.itemcget(self.goals_widgets[self.goal], 'text')

        self.goals_texts.remove(text)
        self.goals_texts.insert(self.shadow_line_position, text)

        for i in range(len(self.goals_widgets)):
            self.c_main.itemconfigure(self.goals_widgets[i], text=self.goals_texts[i])

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
    app.w_main()
    app.mainloop()

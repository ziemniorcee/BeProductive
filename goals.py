from customtkinter import *
from Data import Date
from actions import *
from settings import *


class GoalsManagement:
    def __init__(self):
        self.today_data = Date()

    def goals_from_file(self):
        goals_texts = []
        if os.path.isfile("data/goals.txt"):
            with open("data/goals.txt", "r") as f:
                lines = f.readlines()
                if len(lines) != 0:
                    for i in range(len(lines)):
                        lines[i] = lines[i].strip()

                    if str(self.today_data.formatted_date) == lines[0]:
                        goals_texts = lines[1:]

        else:
            with open("data/goals.txt", 'x'):
                pass

        return goals_texts

    def save_goals_to_file(self, goals_texts):
        if len(goals_texts) == 0:
            for i in range(len(goals_texts)):
                goals_texts.append(self.app.c_main.itemcget(goals_texts[i], 'text'))

        with open('data/goals.txt', 'w+') as file:
            file.write(f"{self.today_data.formatted_date}\n")
            for goals in goals_texts:
                file.write('%s\n' % goals)


class GoalsWidget(CTkFrame):
    def __init__(self, master):
        self.settings = Settings()
        super().__init__(master, width=500, height=500)

        self.management = GoalsManagement()
        goals_texts = self.management.goals_from_file()
        goals_formated = self.format_goals(goals_texts)
        self.display = self.get_display(goals_formated)
        self.current_site = 0
        self.widgets = []

        self.c_frame = CTkCanvas(self, width=500, height=500, bg=self.settings.main_color, highlightthickness=0)
        self.c_frame.grid(row=0, column=0)

        self.c_frame.create_text(250, 25, text="Goals for Today", font=("Arial", 30), fill=self.settings.font_color)
        self.c_frame.create_line(90, 50, 410, 50, fill=self.settings.second_color, width=5)

        img = CTkImage(light_image=Image.open("images/goals/up2.png"), size=(50, 50))
        self.b_arr_up = CTkButton(self, image=img, text="", fg_color=self.settings.main_color,
                                  hover_color=self.settings.second_color, command=lambda: self.show_goals(-1))
        self.c_frame.create_window(425, 30, window=self.b_arr_up, width=70, height=60)

        img = CTkImage(light_image=Image.open("images/goals/down2.png"), size=(50, 50))
        self.b_arr_down = CTkButton(self, image=img, text="", fg_color=self.settings.main_color,
                                    hover_color=self.settings.second_color, command=lambda: self.show_goals(1))
        self.c_frame.create_window(75, 30, window=self.b_arr_down, width=70, height=60)

        self.show_goals()

    def show_goals(self, site=0):
        self.current_site += site
        for widget in self.widgets:
            self.c_frame.delete(widget)

        if self.current_site == 0:
            self.b_arr_up.configure(state="disabled")
        else:
            self.b_arr_up.configure(state="normal")
        if self.current_site == len(self.display) - 1:
            self.b_arr_down.configure(state="disabled")
        else:
            self.b_arr_down.configure(state="normal")

        row = 0
        for line in self.display[self.current_site]:
            text = self.c_frame.create_text(0, 100 + row * 40, text=line, font=("Arial", 20),
                                            fill=self.settings.font_color, justify="left", anchor="w")
            self.widgets.append(text)
            row += 1


    def format_goals(self, texts):
        formated = []
        goal_nr = 1
        for text in texts:
            arr = text.split()
            whole = []
            new = []
            for word in arr:
                if len(new) == 0:
                    new.append(f"{goal_nr}. {word}")
                else:
                    potential = ' '.join(new) + " " + word
                    if ImageFont.truetype("arial.ttf", 20).getbbox(potential)[2] < 420:
                        new.append(word)
                    else:
                        whole.append(' '.join(new))
                        new = [word]

            if len(new) != 0:
                whole.append(' '.join(new))
            formated.append(whole)
            goal_nr += 1

        return formated

    def get_display(self, goals):
        display = []

        new = []
        row = 0

        for goal in goals:
            if len(goal) + row < 9:
                for item in goal:
                    new.append(item)
                    row += 1
            else:
                display.append(new)
                new = goal
                row = len(new)

        if len(new) != 0:
            display.append(new)

        return display

class GoalsWindow:
    def __init__(self, root):
        self.settings = Settings()
        self.management = GoalsManagement()
        self.today_data = Date()

        self.app = root
        self.goals_texts = self.management.goals_from_file()
        self.goals_widgets = []

        self.shadow_line_position = 0
        self.goal_widgets_yposes = []


    def create_setup1_window(self):
        self.app.page = 1
        self.app.create_c_main()

        self.goals_widgets = []
        if len(self.goals_texts) > 0:
            self.goal_widgets_yposes = []
            for goal in self.goals_texts:
                self.show_goal(goal)

        self.app.c_main.create_text(1080, 60, text="Create goals for today", font=self.settings.font, fill=self.settings.font_color)

        self.app.c_main.create_line(870, 100, 1290, 100, fill=self.settings.second_color, width=8)
        self.app.c_main.create_image(75, 750, image=create_imagetk("images/goals/arrow.png", ))
        self.app.c_main.create_text(20, 750, text="Importance", font=self.settings.font, fill=self.settings.font_color, anchor="nw",
                                    angle=90)

        self.e_todo = CTkEntry(self.app, font=("Arial", 20))
        self.e_todo.focus()
        self.app.c_main.create_window(1030, 1295, window=self.e_todo, width=1760, height=50)
        self.b_add = CTkButton(self.app, text="+", font=("Arial", 60), fg_color=self.settings.second_color,
                               command=self.add_goal, border_width=5, hover_color=self.settings.main_color,
                               border_color=self.settings.second_color)
        self.app.c_main.create_window(75, 1295, window=self.b_add, height=50, width=50)

        self.b_submit = CTkButton(self.app, text="Submit", font=self.settings.font, fg_color=self.settings.second_color,
                                  hover_color=self.settings.main_color, border_color=self.settings.second_color,
                                  border_width=5,
                                  command=self.app.setup2.create_setup2_window)
        self.app.c_main.create_window(2035, 1295, window=self.b_submit, width=150, height=50)

        self.dots = self.app.c_main.create_image(125, 210, image=create_imagetk("images/goals/dots.png"),
                                                 tags=("dots",), state='hidden')
        self.shadow = self.app.c_main.create_text(-100, -100, text="", font=("Arial", 20), fill="grey")
        self.app.c_main.itemconfigure(self.shadow, state='hidden')
        self.line = self.app.c_main.create_image(-100, -100 + self.shadow_line_position * 60,
                                                 image=create_imagetk("images/line2.png"), state='hidden')

        self.app.c_main.tag_bind("dots", "<B1-Motion>", self.move_dots)
        self.app.c_main.tag_bind("dots", "<Button-1>", self.press_dots)
        self.app.c_main.tag_bind("dots", "<ButtonRelease-1>", self.unpress_dots)
        self.app.c_main.bind('<Motion>', self.position)
        self.e_todo.bind('<Return>', self.add_goal)

        reg = self.app.register(lambda input1: (ImageFont.truetype("arial.ttf", 20).getbbox(input1)[2] < 1500))
        self.e_todo.configure(validate="key", validatecommand=(reg, '%P'))

    def show_goal(self, text):
        i = len(self.goals_widgets) + 1
        goal = self.app.c_main.create_text(150, 140 + i * 60, text=f"{text}",
                                           font=("Arial", 20),
                                           fill=self.settings.font_color, anchor="w", tags=f"todo{i}")
        self.goals_widgets.append(goal)
        self.goal_widgets_yposes.append(140 + i * 60)

        self.app.c_main.tag_bind(f"todo{i}", '<Enter>', self.strike_on)
        self.app.c_main.tag_bind(f"todo{i}", '<Leave>', self.strike_off)
        self.app.c_main.tag_bind(f"todo{i}", '<Button-1>', self.delete_goal)

    def add_goal(self, *_):
        value = self.e_todo.get()
        if value != "":
            self.show_goal(value)
            self.e_todo.delete(0, len(value))
        self.goals_texts = []
        for i in range(len(self.goals_widgets)):
            self.goals_texts.append(self.app.c_main.itemcget(self.goals_widgets[i], 'text'))
        self.management.save_goals_to_file(self.goals_texts)

    def delete_goal(self, event):
        widget_name = event.widget.find_withtag("current")[0]

        index = self.goals_widgets.index(widget_name)

        for i in range(index, len(self.goals_widgets) - 1):
            next_text = self.app.c_main.itemcget(self.goals_widgets[i + 1], 'text')
            self.app.c_main.itemconfigure(self.goals_widgets[i], text=next_text)

        self.app.c_main.delete(self.goals_widgets[-1])
        self.goals_widgets.pop()
        self.goal_widgets_yposes.pop()

        if len(self.goals_widgets) != 0:
            self.app.c_main.moveto(self.dots, 100, self.goal_widgets_yposes[-1] - 25)

        self.goals_texts = []
        for i in range(len(self.goals_widgets)):
            self.goals_texts.append(self.app.c_main.itemcget(self.goals_widgets[i], 'text'))
        self.management.save_goals_to_file(self.goals_texts)

    # binds for adding goals
    def strike_on(self, event):
        self.app.c_main.itemconfigure(event.widget.find_withtag("current")[0], font=("Arial", 20, "overstrike", "bold"))

    def strike_off(self, event):
        self.app.c_main.itemconfigure(event.widget.find_withtag("current")[0], font=("Arial", 20))

    def position(self, e):
        flag = 0
        y = 0
        for posy in self.goal_widgets_yposes:
            if posy - 25 < e.y < posy + 25 and 110 < e.x < 140:
                y = posy
                flag = 1

        if flag == 1 and y - 14 < e.y < y + 14:
            self.app.c_main.itemconfigure(self.dots, state='normal')
            self.app.c_main.moveto(self.dots, 100, y - 25)
        else:
            self.app.c_main.itemconfigure(self.dots, state='hidden')

    def press_dots(self, e):
        flag = 0
        text = ""
        self.goal = 0
        self.app.c_main.itemconfigure(self.line, state='normal')
        for posy in self.goal_widgets_yposes:
            if posy - 25 < e.y < posy + 25:
                text = self.app.c_main.itemcget(self.goals_widgets[self.goal], 'text')
                flag = 1
            elif flag == 0:
                self.goal += 1
        self.app.c_main.itemconfigure(self.shadow, text=text)
        self.app.c_main.unbind("<Motion>")

    def move_dots(self, e):
        self.app.c_main.itemconfigure(self.shadow, state="normal")

        if e.y < 200:
            self.shadow_line_position = 0
        elif e.y > self.goal_widgets_yposes[-1]:
            self.shadow_line_position = len(self.goal_widgets_yposes)
        else:
            self.shadow_line_position = int((e.y - 110) / 60) - 1

        self.app.c_main.moveto(self.line, 150, 150 + self.shadow_line_position * 60)

        if 200 < e.y < self.goal_widgets_yposes[-1]:
            self.app.c_main.moveto(self.dots, 100, e.y - 25)
            self.app.c_main.moveto(self.shadow, 150, e.y - 20)

    def unpress_dots(self, *_):
        self.app.c_main.itemconfigure(self.line, state='hidden')
        self.app.c_main.bind('<Motion>', self.position)
        self.app.c_main.itemconfigure(self.shadow, state="hidden")
        self.app.c_main.moveto(self.line, -100, -100)
        self.app.c_main.moveto(self.shadow, -100, -100)

        self.goals_texts = []
        for i in range(len(self.goals_widgets)):
            self.goals_texts.append(self.app.c_main.itemcget(self.goals_widgets[i], 'text'))

        text = self.app.c_main.itemcget(self.goals_widgets[self.goal], 'text')
        prev_pos = (self.goals_texts.index(text))

        if prev_pos < self.shadow_line_position:
            self.shadow_line_position -= 1

        self.goals_texts.remove(text)
        self.goals_texts.insert(self.shadow_line_position, text)

        for i in range(len(self.goals_widgets)):
            self.app.c_main.itemconfigure(self.goals_widgets[i], text=self.goals_texts[i])
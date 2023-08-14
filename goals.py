from customtkinter import *
from Data import Date
from actions import *
from settings import *


class GoalsManagement:
    """
    A class for goals classes management

    Methods
    ---------
    goals_from_file():
        gets goals data from file
    save_goals_to_file():
        saves goals data to file
    """

    def __init__(self):
        """
        Constructs today's data attribute
        """
        self.today_data = Date()

    def goals_from_file(self):
        """
        Gets goals from file

        If file doesn't exist, it's created

        Returns
        --------
        List[str]
        """
        goals_texts = []
        if os.path.isfile("data/goals.txt"):
            with open("data/goals.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                if len(lines) != 0:
                    for i in range(len(lines)):
                        lines[i] = lines[i].strip()

                    if str(self.today_data.formatted_date) == lines[0]:
                        goals_texts = lines[1:]

        else:
            with open("data/goals.txt", 'x', encoding="utf-8"):
                pass

        return goals_texts

    def save_goals_to_file(self, goals_texts):
        """
        Saves goals to file

        Parameters
        ----------
        goals_texts : List[str]

        Returns
        --------
        None
        """
        with open('data/goals.txt', 'w+', encoding="utf-8") as file:
            file.write(f"{self.today_data.formatted_date}\n")
            for goals in goals_texts:
                file.write(f"{goals}\n")


class GoalsWidget(CTkFrame):
    """
    A class to create goals widget

    ...
    Attributes
    ----------
    settings : Settings
         app settings
    management : GoalsManagement
        goals management connection
    display : list[list[str]]
        contains list of pages to display
    current_site : int
        currently shown site of goals
    widget : list[int]
        currently displayed widgets
    c_frame : int
        id of the canvas c_frame
    b_arr_up : int
        id of the button b_arr_up
    b_arr_down : int
        id of the button b_arr_down

    Methods
    ---------
    show_goals():
        displays selected goal site
    format_goals():
        breaks goals into lists of limited lines to 420 pixels
    get_display():
        breaks list of lines into list of them
    """

    def __init__(self, master):
        super().__init__(master, width=500, height=400)
        self.settings = Settings()
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
        self.c_frame.create_window(425, 30, window=self.b_arr_up, width=70, height=55)

        img = CTkImage(light_image=Image.open("images/goals/down2.png"), size=(50, 50))
        self.b_arr_down = CTkButton(self, image=img, text="", fg_color=self.settings.main_color,
                                    hover_color=self.settings.second_color, command=lambda: self.show_goals(1))
        self.c_frame.create_window(75, 30, window=self.b_arr_down, width=70, height=55)

        self.show_goals()

    def show_goals(self, direction=0):
        """
        Displays goals

        Parameters
        ----------
        direction : int
            determines which site of display will be shown
        :return:
        """
        self.current_site += direction
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

        if len(self.display) != 0:
            row = 0
            for line in self.display[self.current_site]:
                text = self.c_frame.create_text(0, 100 + row * 40, text=line, font=("Arial", 20),
                                                fill=self.settings.font_color, justify="left", anchor="w")
                self.widgets.append(text)
                row += 1

    def format_goals(self, texts):
        """
        Formats given list of strings

        Parameters
        ----------
        texts : list[str]

        Returns
        --------
        list[list[str]]
        """
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
        """
        Breaks goal lines into display

        Parameters
        ----------
        goals : list[list[str]]
            formatted goals

        Returns
        -------
        list[list[str]]
        """
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
    """
    A class for goals creation window

    ...
    Attirbutes
    ----------
    settings : Settings
         app settings class
    res : float
        app resolution multiplier
    management : GoalsManagement
        goals management class conection
    today_data : Date
        object of Date class
    goals_texts : list[str]
        list of goals
    goals_widgets : list[int]
        list of ids currently displayed
    shadow_line_position : int
        current index of shadow position
    goal_widgets_yposes : list[int]
        list of currently widgets y positions
    e_todo : int
        id of entry for goals
    dots : int
        id of dots widget
    shadow : int
        id of shadow text widget
    line : int
        id of line to show current place
    goal : int
        pressed goal index

    Methods
    ---------
    create_window():
        shows goals window
    show_goal():
        builds and shows goal
    add_goal():
        creates new goal
    delete_goal():
        deletes selected goal
    strike_on():
        strikes font of goal
    strike_off():
        turns off strikes font
    position():
        binds motion
    press_dots():
        binds dots press
    move_dots():
        binds dots movement
    unpress_dots():
        binds dots unpress

    """

    def __init__(self, root):
        """
        Constructs core attributes for class

        Parameters
        ----------
        root : App
            connection to the main app
        """
        self.app = root
        self.settings = Settings()
        self.res = self.settings.resolution
        self.management = GoalsManagement()
        self.today_data = Date()

        self.goals_texts = self.management.goals_from_file()
        self.goals_widgets = []

        self.shadow_line_position = 0
        self.goal_widgets_yposes = []

        self.e_todo = None
        self.dots = None
        self.shadow = None
        self.line = None
        self.goal = 0

    def create_window(self):
        """
        shows goals window

        Returns
        -------
        None
        """
        self.app.page = 1
        self.app.create_c_main()

        self.goals_widgets = []
        if len(self.goals_texts) > 0:
            self.goal_widgets_yposes = []
            for goal in self.goals_texts:
                self.show_goal(goal)

        self.app.c_main.create_text(1080 * self.res[0], 60 * self.res[1], text="Create goals for today", font=self.settings.font,
                                    fill=self.settings.font_color)

        self.app.c_main.create_line(870 * self.res[0], 100 * self.res[1], 1290 * self.res[0], 100 * self.res[1],
                                    fill=self.settings.second_color, width=8)
        self.app.c_main.create_image(75 * self.res[0], 750 * self.res[1],
                                     image=create_imagetk("images/goals/arrow.png", 50, int(1140 * self.res[1])))
        self.app.c_main.create_text(20 * self.res[0], 750 * self.res[1], text="Importance", font=self.settings.font,
                                    fill=self.settings.font_color, anchor="nw", angle=90)

        self.e_todo = CTkEntry(self.app, font=("Arial", 20))
        self.e_todo.focus()
        self.app.c_main.create_window(1030 * self.res[0], 1295 * self.res[1], window=self.e_todo, width=1760 * self.res[0], height=50)
        b_add = CTkButton(self.app, text="+", font=("Arial", 60), fg_color=self.settings.second_color,
                          command=self.add_goal, border_width=5, hover_color=self.settings.main_color,
                          border_color=self.settings.second_color)
        self.app.c_main.create_window(75 * self.res[0], 1295 * self.res[1], window=b_add, height=50, width=50)

        b_submit = CTkButton(self.app, text="Submit", font=("Arial", 30), fg_color=self.settings.second_color,
                             hover_color=self.settings.main_color, border_color=self.settings.second_color,
                             border_width=5,
                             command=self.app.timeline.create_window)
        self.app.c_main.create_window(2035 * self.res[0], 1295 * self.res[1], window=b_submit, width=150, height=50)

        self.dots = self.app.c_main.create_image(125, 210, image=create_imagetk("images/goals/dots.png", 50, 50),
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
        """
        builds and shows goal

        Parameters
        ----------
        text : str
            string to display

        Returns
        ------
        None
        """
        i = len(self.goals_widgets) + 1
        goal = self.app.c_main.create_text(150 * self.res[0], (140 + i * 60) * self.res[1], text=f"{text}",
                                           font=("Arial", 20),
                                           fill=self.settings.font_color, anchor="w", tags=f"todo{i}")
        self.goals_widgets.append(goal)
        self.goal_widgets_yposes.append(140 + i * 60)

        self.app.c_main.tag_bind(f"todo{i}", '<Enter>', self.strike_on)
        self.app.c_main.tag_bind(f"todo{i}", '<Leave>', self.strike_off)
        self.app.c_main.tag_bind(f"todo{i}", '<Button-1>', self.delete_goal)

    def add_goal(self, *_):
        """
        creates new goal

        Returns
        -------
        None
        """
        value = self.e_todo.get()
        if value != "":
            self.show_goal(value)
            self.e_todo.delete(0, len(value))
        self.goals_texts = []
        for i in range(len(self.goals_widgets)):
            self.goals_texts.append(self.app.c_main.itemcget(self.goals_widgets[i], 'text'))
        self.management.save_goals_to_file(self.goals_texts)

    def delete_goal(self, event):
        """
        deletes selected goal

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        widget_name = event.widget.find_withtag("current")[0]

        index = self.goals_widgets.index(widget_name)

        for i in range(index, len(self.goals_widgets) - 1):
            next_text = self.app.c_main.itemcget(self.goals_widgets[i + 1], 'text')
            self.app.c_main.itemconfigure(self.goals_widgets[i], text=next_text)

        self.app.c_main.delete(self.goals_widgets[-1])
        self.goals_widgets.pop()
        self.goal_widgets_yposes.pop()

        if len(self.goals_widgets) != 0:
            self.app.c_main.moveto(self.dots, 100 * self.res[0], (self.goal_widgets_yposes[-1] - 25) * self.res[0])

        self.goals_texts = []
        for i in range(len(self.goals_widgets)):
            self.goals_texts.append(self.app.c_main.itemcget(self.goals_widgets[i], 'text'))
        self.management.save_goals_to_file(self.goals_texts)

    # binds for adding goals
    def strike_on(self, event):
        """
        strikes font of goal

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        self.app.c_main.itemconfigure(event.widget.find_withtag("current")[0], font=("Arial", 20, "overstrike", "bold"))

    def strike_off(self, event):
        """
        turns off strikes font

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        self.app.c_main.itemconfigure(event.widget.find_withtag("current")[0], font=("Arial", 20))

    def position(self, event):
        """
        binds motion

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        flag = 0
        y = 0
        for posy in self.goal_widgets_yposes:
            if (posy - 25) * self.res[1] < event.y < (posy + 25) * self.res[1] and 110 * self.res[0] < event.x < 140 * \
                    self.res[1]:
                y = posy
                flag = 1

        if flag == 1 and (y - 14) * self.res[0] < event.y < (y + 14) * self.res[1]:
            self.app.c_main.itemconfigure(self.dots, state='normal')
            self.app.c_main.moveto(self.dots, 100 * self.res[0], (y - 25) * self.res[0])
        else:
            self.app.c_main.itemconfigure(self.dots, state='hidden')

    def press_dots(self, event):
        """
        binds dots press

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        flag = 0
        text = ""
        self.goal = 0
        self.app.c_main.itemconfigure(self.line, state='normal')
        for posy in self.goal_widgets_yposes:
            if (posy - 25) * self.res[0] < event.y < (posy + 25) * self.res[1]:
                text = self.app.c_main.itemcget(self.goals_widgets[self.goal], 'text')
                flag = 1
            elif flag == 0:
                self.goal += 1
        self.app.c_main.itemconfigure(self.shadow, text=text)
        self.app.c_main.unbind("<Motion>")

    def move_dots(self, event):
        """
        binds dots movement

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        self.app.c_main.itemconfigure(self.shadow, state="normal")

        if event.y < 200 * self.res[1]:
            self.shadow_line_position = 0
        elif event.y > self.goal_widgets_yposes[-1] * self.res[0]:
            self.shadow_line_position = len(self.goal_widgets_yposes)
        else:
            self.shadow_line_position = int((event.y - 110 * self.res[1]) / (60 * self.res[0])) - 1
            print(self.shadow_line_position)

        self.app.c_main.moveto(self.line, 150 * self.res[0], (150 + self.shadow_line_position * 60) * self.res[1])

        if 200 * self.res[1] < event.y < self.goal_widgets_yposes[-1] * self.res[1]:
            self.app.c_main.moveto(self.dots, 100 * self.res[0], (event.y - 25))
            self.app.c_main.moveto(self.shadow, 150 * self.res[0], (event.y - 20))

    def unpress_dots(self, *_):
        """
        binds dots unpress

        Returns
        -------
        None
        """
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

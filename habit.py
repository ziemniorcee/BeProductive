from customtkinter import CTkFrame
from actions import *
from settings import Settings
from customtkinter import *
from Data import Date


class HabitManagement:
    """
    A class to Manage Habit classes

    ...
    Attributes
    ----------
    today_data : Date
         today's date
    new_checks : list[int]
        list of today's checks
    habits : dict{str:str}
        dict with key as a habit name and value of month checks

    Methods
    ---------
    habits_from_file():
        Get habits data from file
    habits_to_file():
        Saves habits data to file
    """

    def __init__(self):
        """
        Constructs attributes used in other habit classes

        Gets data from file
        """
        self.today_data = Date()

        self.new_checks = []
        self.habits = {}

        self.habits_from_file()

    def habits_from_file(self):
        """
        Get habits data from file

        If file doesn't exist, it is created

        Returns
        --------
        None
        """
        if os.path.isfile("data/habits.txt"):
            with open("data/habits.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()

                if len(lines) != 0:
                    data = lines[0].strip()
                    saved = lines[1].strip()
                    new_day = 0
                    if data != str(self.today_data.formatted_date):
                        new_day = 1
                    else:
                        self.new_checks = [int(i) for i in saved]

                    for i in range(2, len(lines), 2):
                        checks = [char for char in lines[i + 1].strip()]
                        if new_day:
                            checks[checks.index('3')] = saved[int(i / 2 - 1)]
                            checks[checks.index('2')] = '3'

                        self.habits[lines[i].strip()] = ''.join(checks)
                    if new_day:
                        self.new_checks = [0 for i in range(len(self.habits))]
                        self.habits_to_file(self.new_checks)
        else:
            with open("data/habits.txt", "x", encoding="utf-8"):
                pass

    def habits_to_file(self, new_checks):
        """
        Saves habits data to file

        Parameters
        ----------
        new_checks : list[int]
            list of today's checks

        Returns
        --------
        None
        """
        with open("data/habits.txt", "w+") as file:
            file.write(f"{self.today_data.formatted_date}\n")
            file.write(''.join(map(str, new_checks)))
            file.write("\n")
            for name, completes in self.habits.items():
                file.write(f'{name}\n')
                file.write(f'{completes}\n')


class HabitsWidget(CTkFrame):
    """
    A class for widget creation

    ...
    Attributes
    -----------
    settings : Settings
         app settings
    management : HabitManagement
        habit management connection
    page : int
        currently open site of goals
    current_widgets = list[int]
        ids of widgets to destroy in future
    new_checks : list[int]
        list of today's checks
    habits : dict{str:str}
        dict with key as a habit name and value of month checks
    c_frame : int
        id of the canvas c_frame
    b_arr_up : int
        id of the button b_arr_up
    b_arr_down : int
        id of the button b_arr_down

    Methods
    ---------
    show_habit():
        displays habits
    change_page():
        changes viewed habits
    change_check():
        changes checkbox value
    """

    def __init__(self, master):
        """
        Constructs attributes for the widget

        Parameters
        ----------
        master : __main__.App
            stores connection to the main app
        """
        self.settings = Settings()
        super().__init__(master, width=500, height=250)

        self.management = HabitManagement()
        self.page = 1
        self.current_widgets = []
        self.new_checks = self.management.new_checks
        self.last_habit = self.management.new_checks
        self.habits = self.management.habits

        self.c_frame = CTkCanvas(self, width=500, height=250, bg=self.settings.main_color, highlightthickness=0)
        self.c_frame.grid(row=0, column=0)

        self.c_frame.create_text(250, 25, text="Habits Tracker", font=("Arial", 30), fill=self.settings.font_color)
        self.c_frame.create_line(90, 50, 410, 50, fill=self.settings.second_color, width=5)

        img = CTkImage(light_image=Image.open("images/goals/up2.png"), size=(50, 50))
        self.b_arr_up = CTkButton(self, image=img, text="", fg_color=self.settings.main_color,
                                  hover_color=self.settings.second_color, command=lambda: self.change_page(-1))
        self.c_frame.create_window(425, 30, window=self.b_arr_up, width=70, height=55)

        img = CTkImage(light_image=Image.open("images/goals/down2.png"), size=(50, 50))
        self.b_arr_down = CTkButton(self, image=img, text="", fg_color=self.settings.main_color,
                                    hover_color=self.settings.second_color, command=lambda: self.change_page(1))
        self.c_frame.create_window(75, 30, window=self.b_arr_down, width=70, height=55)

        self.show_habits()

    def show_habits(self):
        """
        displays habits

        Returns
        --------
        None
        """
        if len(self.new_checks) > self.page * 3:
            self.last_habit = self.page * 3
            self.b_arr_down.configure(state="normal")
        else:
            self.last_habit = len(self.new_checks)
            self.b_arr_down.configure(state="disabled")

        if self.page == 1:
            self.b_arr_up.configure(state="disabled")
        else:
            self.b_arr_up.configure(state="normal")

        for i in range((self.page - 1) * 3, self.last_habit):
            checkbox = CTkCheckBox(self, text="", checkbox_width=38, checkbox_height=38,
                                   command=lambda k=i: self.change_check(k), bg_color=self.settings.main_color,
                                   border_color=self.settings.second_color, width=50, height=50,
                                   variable=IntVar(value=self.new_checks[i]))
            self.c_frame.create_window(40, 100 + (i % 3) * 50, window=checkbox)

            text = self.c_frame.create_text(70, 100 + (i % 3) * 50, text=list(self.habits)[i], font=("Arial", 20),
                                            fill=self.settings.font_color, justify="left", anchor="w")
            self.current_widgets.append([checkbox, text])

    def change_page(self, direction):
        """
        changes displayed page of habits

        Parameters
        ----------
        direction : int
            changes page attribute

        Returns
        --------
        None
        """
        self.page += direction
        for i in self.current_widgets:
            i[0].destroy()
            self.c_frame.delete(i[1])
        self.current_widgets = []
        self.show_habits()

    def change_check(self, i):
        """
        changes checkbox value

        Parameters
        ----------
        i : int
        habits id

        Returns
        --------
        None
        """
        self.new_checks[i] = int(not self.new_checks[i])
        self.management.habits_to_file(self.new_checks)


class HabitWindow:
    """
    A class for full habit tracker window

    ...
    Attributes
    ----------
    app : '__main__.App'
        root of main app
    settings : Settings
         app settings
    management : HabitManagement
        habit management connection
    current_widgets = list[int]
        ids of widgets to destroy in future
    new_checks : list[int]
        list of today's checks
    habits : dict{str:str}
        dict with key as a habit name and value of month checks
    y_pos : int
        current new widget y iteration
    b_configure : int
        id of b_configure

    Methods
    ---------
    create_habit_window():
        creates habit tracker window
    change_check():
        changes checkbox state
    _clear():
        destroys all objects
    new_habit():
        builds adding new habit feature
    configure_habits():
        build removing habits buttons
    delete_habit():
        deletes selected habit
    habit_accept():
        adds new habit to the file

    """

    def __init__(self, root):
        """
        Constructs attributes for habit tracker window

        Parameters
        ----------
        root :  '__main__.App'
            access to main app
        """
        self.app = root
        self.settings = Settings()
        self.res = self.settings.resolution
        self.management = HabitManagement()

        self.new_checks = []
        self.habits = {}
        self.current_widgets = []
        self.y_pos = 0

        self.b_configure = None

    def create_habit_window(self):
        """
        creates habit tracker window

        Returns
        -------
        None
        """
        self.app.create_c_main()
        self.management.habits_from_file()
        self.app.page = 3

        self.y_pos = 0
        self.new_checks = self.management.new_checks
        self.habits = self.management.habits
        self.current_widgets = []

        self.app.c_main.create_text(1080* self.res[0], 60* self.res[1], text="Habit Tracker", font=self.settings.font,
                                    fill=self.settings.font_color)
        self.app.c_main.create_line(870* self.res[0], 100* self.res[1], 1290* self.res[0], 100* self.res[1], fill=self.settings.second_color, width=8)
        b_new = CTkButton(self.app, text="New", font=self.settings.font, fg_color=self.settings.second_color,
                          hover_color=self.settings.main_color, border_color=self.settings.second_color,
                          border_width=5, command=self.new_habit)
        self.app.c_main.create_window(125, 150, window=b_new, width=150, height=50)

        self.b_configure = CTkButton(self.app, text="Configure", font=self.settings.font,
                                     fg_color=self.settings.second_color,
                                     hover_color=self.settings.main_color, border_color=self.settings.second_color,
                                     border_width=5,
                                     command=self.configure_habits)
        self.app.c_main.create_window(300, 150, window=self.b_configure, width=150, height=50)

        self.management.habits_from_file()
        iteration = 0
        for name, completes in self.habits.items():

            self.app.c_main.create_text(50, 200 + self.y_pos * 50, text=name, font=("Arial", 20),
                                        fill=self.settings.font_color,
                                        justify="left", anchor="w")
            self.y_pos += 1

            for i in range(1, 31):
                if completes[i] == '1':
                    self.app.c_main.create_image(400 + i * 50, 150 + self.y_pos * 50,
                                                 image=create_imagetk("images/habits/checked.png"))
                elif completes[i] == '3':
                    checkbox = CTkCheckBox(self.app, text="", checkbox_width=38, checkbox_height=38,
                                           command=lambda k=iteration: self.change_check(k),
                                           border_color="yellow", width=50, height=50,
                                           variable=IntVar(value=self.new_checks[self.y_pos - 1]))
                    self.app.c_main.create_window(405 + i * 50, 150 + self.y_pos * 50, window=checkbox)
                else:
                    self.app.c_main.create_image(400 + i * 50, 150 + self.y_pos * 50,
                                                 image=create_imagetk("images/habits/unchecked.png"))
            iteration += 1

    def change_check(self, i):
        """
        changes checkbutton state

        Returns
        -------
        None
        """
        self.new_checks[i] = int(not self.new_checks[i])
        self.management.habits_to_file(self.new_checks)

    def _clear(self):
        """
        Destroys all widgets

        Returns
        -------
        None
        """
        for i in self.current_widgets:
            i.destroy()
        self.current_widgets = []

    def new_habit(self):
        """
        Creates new habit widget to add new habit

        Returns
        -------
        None
        """
        self._clear()
        e_new = CTkEntry(self.app, font=("Arial", 20))
        self.app.c_main.create_window(212, 200 + self.y_pos * 50, window=e_new, width=325, height=50)
        b_accept = CTkButton(self.app, text="✓", font=("Arial", 50), fg_color=self.settings.second_color,
                             command=self.habit_accept, border_width=5, hover_color="green",
                             border_color=self.settings.second_color)
        self.app.c_main.create_window(425, 200 + self.y_pos * 50, window=b_accept, width=50, height=50)

        b_cancel = CTkButton(self.app, text="✕", font=("Arial", 50), fg_color=self.settings.second_color,
                             command=self._clear, border_width=5, hover_color="red",
                             border_color=self.settings.second_color)
        self.app.c_main.create_window(500, 200 + self.y_pos * 50, window=b_cancel, width=50, height=50)
        self.current_widgets = [e_new, b_accept, b_cancel]

    def configure_habits(self):
        """
        BUilds buttons to delete habits

        Returns
        -------
        None
        """
        self._clear()
        self.b_configure.configure(fg_color="red", text="cancel", command=self.create_habit_window)

        for i in range(self.y_pos):
            b_cancel = CTkButton(self.app, text="✕", font=("Arial", 50), fg_color=self.settings.second_color,
                                 command=lambda k=i: self.delete_habit(k), border_width=5, hover_color="red",
                                 border_color=self.settings.second_color)
            self.app.c_main.create_window(25, 200 + i * 50, window=b_cancel, width=50, height=50)
            self.current_widgets.append(b_cancel)

    def delete_habit(self, habit):
        """
        Deletes selected habit

        habit : int
            id of the widget to delete

        Returns
        -------
        None
        """
        self.habits.pop(list(self.habits)[habit])
        self.new_checks.pop()
        self.management.habits_to_file(self.new_checks)
        self.create_habit_window()

    def habit_accept(self):
        """
        Adds new habit

        Returns
        -------
        None
        """
        self.habits[self.current_widgets[0].get()] = "p" + "3" + "2" * 29
        self.new_checks.append(0)
        self.management.habits_to_file(self.new_checks)
        self.create_habit_window()

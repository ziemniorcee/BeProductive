from actions import *
from settings import *
from customtkinter import *
from Data import Date


class Habit_tracker:
    def __init__(self, root):
        self.app = root

        self.today_data = Date()

        self.new_checks = []
        self.habits = {}

    def create_habit_window(self):
        self.app.page = 3
        self.current_widgets = []
        self.y_pos = 0
        self.app.create_c_main()

        self.app.c_main.create_text(1080, 60, text="Habit Tracker", font=FONT, fill=COL_FONT)
        self.app.c_main.create_line(870, 100, 1290, 100, fill=COL_2, width=8)
        self.b_new = CTkButton(self.app, text="New", font=FONT, fg_color=COL_2,
                               hover_color=COL_1, border_color=COL_2, border_width=5,
                               command=self.new_habit)
        self.app.c_main.create_window(125, 150, window=self.b_new, width=150, height=50)

        self.b_configure = CTkButton(self.app, text="Configure", font=FONT, fg_color=COL_2,
                                     hover_color=COL_1, border_color=COL_2, border_width=5,
                                     command=self.configure_habits)
        self.app.c_main.create_window(300, 150, window=self.b_configure, width=150, height=50)

        self.habits_from_file()
        iteration = 0
        for name, completes in self.habits.items():

            self.app.c_main.create_text(50, 200 + self.y_pos * 50, text=name, font=FONT_TEXT, fill=COL_FONT,
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
        self.new_checks[i] = int(not self.new_checks[i])
        self.habits_to_file()

    def _clear(self):
        for i in self.current_widgets:
            i.destroy()
        self.current_widgets = []

    def new_habit(self):
        self._clear()
        self.e_new = CTkEntry(self.app, font=FONT_TEXT)
        self.app.c_main.create_window(212, 200 + self.y_pos * 50, window=self.e_new, width=325, height=50)
        self.b_accept = CTkButton(self.app, text="✓", font=("Arial", 50), fg_color=COL_2,
                                  command=self.habit_accept, border_width=5, hover_color="green",
                                  border_color=COL_2)
        self.app.c_main.create_window(425, 200 + self.y_pos * 50, window=self.b_accept, width=50, height=50)

        self.b_cancel = CTkButton(self.app, text="✕", font=("Arial", 50), fg_color=COL_2,
                                  command=self._clear, border_width=5, hover_color="red",
                                  border_color=COL_2)
        self.app.c_main.create_window(500, 200 + self.y_pos * 50, window=self.b_cancel, width=50, height=50)
        self.current_widgets = [self.e_new, self.b_accept, self.b_cancel]

    def configure_habits(self):
        self._clear()
        self.b_configure.configure(fg_color="red", text="cancel", command=self.create_habit_window)

        for i in range(self.y_pos):
            b_cancel = CTkButton(self.app, text="✕", font=("Arial", 50), fg_color=COL_2,
                                 command=lambda k=i: self.delete_habit(k), border_width=5, hover_color="red",
                                 border_color=COL_2)
            self.app.c_main.create_window(25, 200 + i * 50, window=b_cancel, width=50, height=50)
            self.current_widgets.append(b_cancel)

    def delete_habit(self, habit):
        self.habits.pop(list(self.habits)[habit])
        self.new_checks.pop()
        self.habits_to_file()
        self.create_habit_window()

    def habit_accept(self):
        self.habits[self.e_new.get()] = "p" + "3" + "2" * 29
        self.new_checks.append(0)
        self.habits_to_file()
        self.create_habit_window()

    def habits_from_file(self):
        if os.path.isfile("data/habits.txt"):
            with open("data/habits.txt", "r") as f:
                lines = f.readlines()

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
                        self.habits_to_file()
        else:
            with open("data/habits.txt", "x"):
                pass

    def habits_to_file(self):
        with open("data/habits.txt", "w+") as file:
            file.write(f"{self.today_data.formatted_date}\n")
            file.write(''.join(map(str, self.new_checks)))
            file.write("\n")
            for name, completes in self.habits.items():
                file.write('%s\n' % name)
                file.write('%s\n' % completes)

    def widget_habits(self):
        self.page = 1
        self.current_widgets = []
        self.last_habit = self.new_checks
        self.app.c_main.create_text(1760, 185, text="Habits Tracker", font=("Arial", 30), fill=COL_FONT)
        self.app.c_main.create_line(1610, 210, 1910, 210, fill=COL_2, width=5)

        img = CTkImage(light_image=Image.open("images/goals/up2.png"), size=(50, 50))
        self.arr_up = CTkButton(self.app, image=img, text="", fg_color=COL_1, hover_color=COL_2,
                                command=lambda: self.change_page(-1))
        self.app.c_main.create_window(1935, 190, window=self.arr_up, width=70, height=70)
        img = CTkImage(light_image=Image.open("images/goals/down2.png"), size=(50, 50))
        self.arr_down = CTkButton(self.app, image=img, text="", fg_color=COL_1, hover_color=COL_2,
                                  command=lambda: self.change_page(1))
        self.app.c_main.create_window(1585, 190, window=self.arr_down, width=70, height=70)
        self.habits_from_file()
        self._show_habits()

    def _show_habits(self):
        if len(self.new_checks) > self.page * 3:
            self.last_habit = self.page * 3
            self.arr_down.configure(state="normal")
        else:
            self.last_habit = len(self.new_checks)
            self.arr_down.configure(state="disabled")

        if self.page == 1:
            self.arr_up.configure(state="disabled")
        else:
            self.arr_up.configure(state="normal")

        for i in range((self.page - 1) * 3, self.last_habit):
            checkbox = CTkCheckBox(self.app, text="", checkbox_width=38, checkbox_height=38,
                                   command=lambda k=i: self.change_check(k),
                                   border_color=COL_2, width=50, height=50,
                                   variable=IntVar(value=self.new_checks[i]))
            self.app.c_main.create_window(1590, 260 + (i % 3) * 50, window=checkbox)

            text = self.app.c_main.create_text(1620, 260 + (i % 3) * 50, text=list(self.habits)[i], font=FONT_TEXT,
                                               fill=COL_FONT, justify="left", anchor="w")
            self.current_widgets.append([checkbox, text])

    def change_page(self, direction):
        self.page += direction
        for i in self.current_widgets:
            i[0].destroy()
            self.app.c_main.delete(i[1])
        self.current_widgets = []
        self._show_habits()

from customtkinter import CTkCanvas, CTkImage, CTkButton, CTk, CTkToplevel
from Data import Date, Weather
from actions import *
from settings import Settings, SettingsButton
from start import Start_window
from habit import HabitWindow, HabitsWidget
from strategy import Strategy
from goals import GoalsWindow, GoalsWidget
from timeline import ShortTimelineWidget
from customtkinter import CTkCanvas


class FloatBar(CTkCanvas):
    def __init__(self, master):
        self.app = master
        self.settings = Settings()
        super().__init__(master, width=100, height=450, bg=self.settings.main_color, highlightthickness=0)

        self.previous_pos = [2450, 450]
        self.bar_height = 100
        self.sidebar = None

        self.laurels = self.create_image(0, 0, image=create_imagetk("images/floatbar/laura.png", 100, 100),
                                         anchor="nw", tag="laurels")
        self.b_goals = GoalsButton(self)
        self.create_window(50, 150, window=self.b_goals, height=100, width=150, anchor="center")

        self.b_timeline = TimelineButton(self)
        self.create_window(50, 250, window=self.b_timeline, height=100, width=150, anchor="center")

        self.b_habit = HabitsButton(self)
        self.create_window(50, 350, window=self.b_habit, height=100, width=150, anchor="center")

        img = CTkImage(light_image=Image.open("images/floatbar/return.png"), size=(47, 47))
        self.b_return = CTkButton(self, image=img, bg_color=self.settings.main_color, text="",
                                  hover_color="#f4ca3e", fg_color=self.settings.main_color, width=100,
                                  border_color="#f4ca3e", border_width=1, command=self.back)
        self.create_window(25, 425, window=self.b_return, width=50, height=50)

        img = CTkImage(light_image=Image.open("images/floatbar/exit.png"), size=(50, 50))
        self.b_exit = CTkButton(self, image=img, bg_color=self.settings.main_color, text="",
                                hover_color="#f4ca3e", fg_color=self.settings.main_color, width=100,
                                border_color="#f4ca3e", border_width=1, command=lambda: self.app.destroy())
        self.create_window(75, 425, window=self.b_exit, width=50, height=50)

        frame_goal = self.create_rectangle(0, 0, 99, 99, outline="#f4ca3e", tags="framegold")

        self.tag_bind("laurels", "<Button-1>", self.laurels_press1)
        self.tag_bind("laurels", "<B1-Motion>", self.laurels_move)
        self.tag_bind("laurels", "<ButtonRelease-1>", self.laurels_unpress)

        self.tag_bind("laurels", "<Button-3>", self.laurels_press2)
        self.tag_bind("laurels", "<ButtonRelease-3>", self.laurels_unpress2)

    def build_floatbar(self):
        self.sidebar = SideBar(self.app)

        self.app.attributes('-topmost', True)
        self.app.state("normal")
        self.app.overrideredirect(True)
        self.app.geometry('%dx%d+%d+%d' % (100, 100, 2450, 450))

        self.app.c_sidebar.grid_remove()
        self.app.c_habit.grid_remove()
        self.app.c_goals.grid_remove()
        self.app.c_timeline.grid_remove()
        self.app.c_strategy.grid_remove()
        self.app.c_start.grid_remove()
        self.app.c_floatbar.grid()

    def laurels_press1(self, e):
        self.itemconfigure(self.laurels, image=create_imagetk("images/floatbar/laura2.png", 100, 100))
        self.middle = [e.x, e.y]
        self.sidebar.middle = [e.x, e.y]

    def laurels_move(self, e):
        current_pos = [e.x + self.previous_pos[0] - self.middle[0], e.y + self.previous_pos[1] - self.middle[1]]
        self.app.geometry('%dx%d+%d+%d' % (100, self.bar_height, current_pos[0], current_pos[1]))
        self.previous_pos = current_pos

        sidebar_pos = [e.x + self.sidebar.previous_pos[0] - self.sidebar.middle[0],
                       e.y + self.sidebar.previous_pos[1] - self.sidebar.middle[1]]
        self.sidebar.geometry('%dx%d+%d+%d' % (
            self.sidebar.current_state[0], self.sidebar.current_state[1], sidebar_pos[0], sidebar_pos[1]))
        self.sidebar.previous_pos = sidebar_pos

    def laurels_unpress(self, e):
        self.itemconfigure(self.laurels, image=create_imagetk("images/floatbar/laura.png", 100, 100))

    def laurels_press2(self, e):
        self.r_start_pos = [e.x, e.y]
        self.itemconfigure(self.laurels, image=create_imagetk("images/floatbar/laura4.png", 100, 100))

    def laurels_unpress2(self, e):
        if e.y < self.r_start_pos[1] - 20 and self.bar_height != 100:
            self.app.geometry('%dx%d+%d+%d' % (100, 100, self.previous_pos[0], self.previous_pos[1]))
            self.bar_height = 100
            if self.b_goals.state:
                self.b_goals.press()
            if self.b_habit.state:
                self.b_habit.press()
            if self.b_timeline.state:
                self.b_timeline.press()
        elif e.y > self.r_start_pos[1] + 20 and self.bar_height != 450:
            self.app.geometry('%dx%d+%d+%d' % (100, 450, self.previous_pos[0], self.previous_pos[1]))
            self.bar_height = 450

        self.itemconfigure(self.laurels, image=create_imagetk("images/floatbar/laura.png", 100, 100))

    def back(self):
        self.app.overrideredirect(False)
        self.app.after(0, lambda: self.app.state('zoomed'))
        self.app.attributes('-topmost', False)
        self.bar_height = 100
        if self.b_goals.state:
            self.b_goals.press()
        if self.b_habit.state:
            self.b_habit.press()
        if self.b_timeline.state:
            self.b_timeline.press()

        self.app.c_habit.grid_remove()
        self.app.c_goals.grid_remove()
        self.app.c_timeline.grid_remove()
        self.app.c_strategy.grid_remove()
        self.app.c_sidebar.grid()
        self.app.c_start.grid()
        self.app.c_floatbar.grid_remove()

class SideBar(CTkToplevel):
    def __init__(self, root):
        super().__init__()
        self.settings = Settings()
        self.app = root
        self.geometry("0x0")
        self.attributes('-topmost', True)
        self.overrideredirect(True)
        self.previous_pos = [1950, 450]
        self.middle = [2200, 600]
        self.current_state = [0, 0]

        self.goal_widget = None
        self.habit_widget = None

    def create_goals(self):
        self.middle = [2200, 600]
        self.current_state = [500, 400]
        self.geometry('%dx%d+%d+%d' % (500, 400, self.previous_pos[0], self.previous_pos[1]))
        self.goal_widget = GoalsWidget(self)
        self.goal_widget.grid(row=0, column=0)
        self.goal_widget.c_frame.create_rectangle(0, 0, 499, 399, outline=self.settings.second_color, width=1)

    def create_habits(self):
        self.middle = [2200, 525]
        self.current_state = [500, 250]
        self.geometry('%dx%d+%d+%d' % (500, 250, self.previous_pos[0], self.previous_pos[1]))
        self.habit_widget = HabitsWidget(self)
        self.habit_widget.grid(row=0, column=0)
        self.habit_widget.c_frame.create_rectangle(0, 0, 499, 249, outline=self.settings.second_color, width=1)

    def create_timeline(self):
        self.middle = [2200, 600]
        self.current_state = [500, 400]
        self.geometry('%dx%d+%d+%d' % (500, 400, self.previous_pos[0], self.previous_pos[1]))
        self.timeline_widget = ShortTimelineWidget(self)
        self.timeline_widget.grid(row=0, column=0)

    def close(self):
        self.current_state = [0, 0]
        self.geometry("0x0")


class GoalsButton(CTkButton):
    def __init__(self, master):
        self.settings = Settings()
        img = CTkImage(light_image=Image.open("images/floatbar/goal0.png"), size=(95, 95))
        super().__init__(master.app, text="", image=img, fg_color=self.settings.second_color, height=110, width=150,
                         border_width=0, border_spacing=0, bg_color=self.settings.second_color,
                         hover_color=self.settings.second_color, border_color="blue", command=self.press)
        self.app = master
        self.state = False

    def press(self):
        self.state = not self.state
        img = CTkImage(light_image=Image.open(f"images/floatbar/goal{int(self.state)}.png"), size=(95, 95))
        self.configure(image=img)
        if self.state:
            if self.app.b_habit.state:
                self.app.b_habit.press()
            if self.app.b_timeline.state:
                self.app.b_timeline.press()
            self.app.sidebar.create_goals()
        else:
            self.app.sidebar.goal_widget.destroy()
            self.app.sidebar.close()


class HabitsButton(CTkButton):
    def __init__(self, master):
        self.settings = Settings()
        img = CTkImage(light_image=Image.open("images/floatbar/habit0.png"), size=(95, 95))
        super().__init__(master.app, text="", image=img, fg_color=self.settings.second_color, height=110, width=150,
                         border_width=0, border_spacing=0, bg_color=self.settings.second_color,
                         hover_color=self.settings.second_color, border_color="blue", command=self.press)
        self.app = master
        self.state = False

    def press(self):
        self.state = not self.state
        img = CTkImage(light_image=Image.open(f"images/floatbar/habit{int(self.state)}.png"), size=(95, 95))
        self.configure(image=img)
        if self.state:
            if self.app.b_goals.state:
                self.app.b_goals.press()
            if self.app.b_timeline.state:
                self.app.b_timeline.press()
            self.app.sidebar.create_habits()
        else:
            self.app.sidebar.habit_widget.destroy()
            self.app.sidebar.close()


class TimelineButton(CTkButton):
    def __init__(self, master):
        self.settings = Settings()
        img = CTkImage(light_image=Image.open("images/floatbar/timeline0.png"), size=(95, 95))
        super().__init__(master.app, text="", image=img, fg_color=self.settings.second_color, height=110, width=150,
                         border_width=0, border_spacing=0, bg_color=self.settings.second_color,
                         hover_color=self.settings.second_color, border_color="blue", command=self.press)
        self.app = master
        self.state = False

    def press(self):
        self.state = not self.state
        img = CTkImage(light_image=Image.open(f"images/floatbar/timeline{int(self.state)}.png"), size=(95, 95))
        self.configure(image=img)
        if self.state:
            if self.app.b_goals.state:
                self.app.b_goals.press()
            if self.app.b_habit.state:
                self.app.b_habit.press()
            self.app.sidebar.create_timeline()
        else:
            self.app.sidebar.timeline_widget.destroy()
            self.app.sidebar.close()

import customtkinter
from Data import Date, Weather
from PIL import Image, ImageTk
from settings import *
import math
from actions import *


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Better Tomorrow")
        self.geometry(f"{500}x{700}")
        self.accept_works = 0
        self.round1 = 0

        self.last = 0

        self.welcome_window()
        # self.second_window()
        # self.accept_goals()
        # self.third_screen()

    def welcome_window(self):
        today = Date()
        weather_data = Weather()

        self.l_date = customtkinter.CTkLabel(self, text=f" {today.day} ", font=FONT, text_color=COL_FONT, width=500,
                                             height=50)
        self.l_date.grid(row=0, column=0)

        self.c_weather = customtkinter.CTkCanvas(self, width=500, height=400, bg=COL_1, highlightthickness=0)
        self.c_weather.grid(row=1, column=0)

        self.c_weather.create_image(250, 150, image=create_imagetk(weather_data.image, 300, 300))

        self.c_weather.create_text(250, 150, text=f"{weather_data.temperature[0]}", font=FONT, fill=COL_FONT)

        self.c_weather.create_text(250, 180, text=f"Feels like: {weather_data.temperature[1]}", font=("Arial", 15),
                                   fill=COL_FONT)

        self.b_start = customtkinter.CTkButton(self, text="Start your day", fg_color="transparent", font=FONT,
                                               border_width=2, border_color=COL_2,
                                               text_color=("gray10", "#DCE4EE"), command=self.second_window)
        self.b_start.grid(row=2, column=0)

    def second_window(self):
        self.c_weather.destroy()
        self.b_start.destroy()
        self.l_date.destroy()

        # 1st block
        self.c_head = customtkinter.CTkCanvas(self, width=500, height=60, bg=COL_1, highlightthickness=0)
        self.c_head.grid(row=0, column=0)
        self.text_head = self.c_head.create_text(250, 25, text="GOALS FOR TODAY", font=FONT, fill=COL_FONT)

        self.c_head.create_image(250, 50, image=create_imagetk("images/line.png", 450, 100))

        # 2nd block
        self.c_todos = customtkinter.CTkCanvas(self, width=500, height=450, bg=COL_1, highlightthickness=0)
        self.c_todos.grid(row=1, column=0)
        self.create_goals()

        self.e_todo = customtkinter.CTkEntry(self, font=("Arial", 20))
        self.e_todo.focus()
        self.c_todos.create_window(220, 400, window=self.e_todo, width=370, height=40)
        self.b_add = customtkinter.CTkButton(self, text="+", font=("Arial", 40), fg_color=COL_2,
                                             command=self.add_goal)

        self.c_todos.create_window(450, 400, window=self.b_add, height=40, width=40)
        self.e_todo.bind('<Return>', self.add_goal)

        reg = self.register(self.limit_input)
        self.e_todo.configure(validate="key", validatecommand=(reg, '%P'))

        for i in range(1, 6):
            self.c_todos.tag_bind(str(i), '<Enter>', self.strike_on)
            self.c_todos.tag_bind(str(i), '<Leave>', self.strike_off)
            self.c_todos.tag_bind(str(i), '<Button-1>', self.del_goal)
        self.flag = 0

    def third_screen(self):
        self.c_todos.destroy()
        self.c_accept.destroy()

        self.c_head.itemconfigure(self.text_head, text="Create focus blocks")
        self.timer = customtkinter.CTkLabel(self, text="00:00", font=FONT_TIMER, text_color=COL_FONT, width=500,
                                            height=50)
        self.timer.grid(row=1, column=0)
        self.c_clock = customtkinter.CTkCanvas(self, width=500, height=500, bg=COL_1, highlightthickness=0)
        # self.c_clock.create_text(100, 10, text="xdxd")
        self.c_clock.grid(row=2, column=0)
        self.c_clock.create_image(250, 250, image=create_imagetk("images/clock.png", 500, 500))
        print(f"img_id {img_id}")


        self.img = ImageTk.PhotoImage(file="images/hand2.png")
        self.hand1 = self.c_clock.create_image(250, 250, image=self.img, tags=("meta",))


        self.c_clock.tag_bind("meta", "<B1-Motion>", self.move)

    def move(self, e):

        angle = 0
        if e.y <= 250 and e.x >= 250:
            a = 250 - e.y
            b = e.x - 250
            if a == 0:
                angle = 90
            else:
                tangens = b / a
                angle = math.degrees(math.atan(tangens))
        elif e.y >= 250 and e.x >= 250:
            a = e.y - 250
            b = e.x - 250

            if b == 0:
                angle = 180
            else:
                tangens = a / b
                angle = math.degrees(math.atan(tangens)) + 90
        elif e.y >= 250 and e.x <= 250 and self.round1 != 0:
            a = e.y - 250
            b = 250 - e.x

            if a == 0:
                angle = 270
            else:
                tangens = b / a
                angle = math.degrees(math.atan(tangens)) + 180
        elif e.y <= 250 and e.x <= 250 and self.round1 != 0:
            a = 250 - e.y
            b = 250 - e.x

            if a == 0:
                angle = 0
            else:
                tangens = a / b
                angle = math.degrees(math.atan(tangens)) + 270

        if angle > self.last:
            self.round1 = 1
        else:
            self.round1 = 0
        if self.last  > 330:
            self.round1 += 1

        self.img = Image.open("images/hand2.png")
        print(angle)
        self.img = ImageTk.PhotoImage(self.img.rotate(-angle))

        self.hand1 = self.c_clock.create_image(250, 250, image=self.img, tags=("meta",))
        self.last = angle

    def create_goals(self):
        self.goals = []
        for i in range(5):
            goal = self.c_todos.create_text(10, 50 + i * 60, text=f"{str(i + 1)}. ", font=("Arial", 20),
                                            fill=COL_FONT, anchor="w", tags=str(i))
            self.goals.append(goal)

    def add_goal(self, *_):
        value = self.e_todo.get()
        for goal in self.goals:
            x = self.c_todos.itemcget(goal, 'text')

            if len(x) < 4:
                y = self.c_todos.itemconfigure(goal)
                print(type(y))
                self.c_todos.itemconfigure(goal, text=f"{x}{value}")
                self.e_todo.delete(0, 100)
                break

        flag = 1
        for i in range(5):
            if len(self.c_todos.itemcget(self.goals[i], 'text')) < 4:
                flag = 0
        if flag == 1:
            self.accept_goals()
            self.e_todo.unbind("<Return>")

    def limit_input(self, input1):
        if len(input1) < 30:
            return True
        else:
            return False

    def strike_on(self, event):
        widget_name = event.widget.find_withtag("current")[0]
        self.text = self.c_todos.itemcget(widget_name, 'text')
        font = ("Arial", 20, "overstrike", "bold")
        if len(self.text) > 3 and self.flag == 0:
            self.c_todos.itemconfigure(widget_name, font=font)
            self.flag = 1

    def strike_off(self, event):
        widget_name = event.widget.find_withtag("current")[0]

        font = ("Arial", 20)
        if self.flag == 1:
            self.c_todos.itemconfigure(widget_name, font=font)
            self.flag = 0

    def del_goal(self, event):
        widget_name = event.widget.find_withtag("current")[0]
        self.text = self.c_todos.itemcget(widget_name, 'text')
        self.c_todos.itemconfigure(widget_name, text=self.text[:3])

        self.hide_accept()
        self.e_todo.bind("<Return>", self.add_goal)

    def accept_goals(self):
        self.accept_works = 1
        self.e_todo.configure(state="disabled")
        self.b_add.configure(state="disabled")
        self.c_accept = customtkinter.CTkCanvas(self, width=500, height=150, bg=COL_1, highlightthickness=0)
        self.c_accept.grid(row=2, column=0)

        self.c_accept.create_text(250, 25, text="These are my goals", font=FONT, fill=COL_FONT)
        self.b_yes = customtkinter.CTkButton(self, text="Yes", font=("Arial", 30), fg_color=COL_2,
                                             command=self.third_screen)
        self.c_accept.create_window(150, 100, window=self.b_yes, height=40, width=150)

        self.b_cancel = customtkinter.CTkButton(self, text="Clear all", font=("Arial", 30), fg_color=COL_1,
                                                border_color=COL_2, border_width=5, command=self.cancel_goals)
        self.c_accept.create_window(350, 100, window=self.b_cancel, height=40, width=150)

    def hide_accept(self):
        self.e_todo.configure(state="normal")
        self.b_add.configure(state="normal")
        if self.accept_works:
            self.c_accept.grid_remove()



    def cancel_goals(self):
        for goal in self.goals:
            x = self.c_todos.itemcget(goal, 'text')
            self.c_todos.itemconfigure(goal, text=x[:3])
        self.hide_accept()


if __name__ == "__main__":
    app = App()
    app.mainloop()

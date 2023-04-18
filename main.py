import customtkinter
from Data import Date, Weather
from PIL import Image, ImageTk

BG_COLOR = "#242424"
FONT_COLOR = "#fcf7ff"
SECOND_COLOR = "#2C0049"

FONT = ("Arial", 30)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Better Tomorrow")
        self.geometry(f"{500}x{700}")

        self.welcome_window()

    def welcome_window(self):
        today = Date()
        date = today.day
        hour = today.hour1
        weather_data = Weather(hour)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=3)

        self.l_date = customtkinter.CTkLabel(self, text=f" {date} ", font=FONT, text_color=FONT_COLOR, )
        self.l_date.grid(row=0, column=1)

        self.c_weather = customtkinter.CTkCanvas(self, width=400, height=300, bg=BG_COLOR, highlightthickness=0)
        self.c_weather.grid(row=1, column=1)

        self.c_weather.create_image(200, 150, image=self.create_image(weather_data.image, 300, 300))
        self.c_weather.create_image(200, 150, image=self.img)
        self.c_weather.create_text(200, 150, text=f"{weather_data.temperature[0]}", font=FONT, fill=FONT_COLOR)
        self.c_weather.create_text(200, 180, text=f"Feels like: {weather_data.temperature[1]}", font=("Arial", 15),
                                   fill=FONT_COLOR)

        self.b_start = customtkinter.CTkButton(self, text="Start your day", fg_color="transparent", font=FONT,
                                               border_width=2, border_color=SECOND_COLOR,
                                               text_color=("gray10", "#DCE4EE"), command=self.second_window)
        self.b_start.grid(row=2, column=0, columnspan=2)

    def second_window(self):
        self.c_weather.destroy()
        self.b_start.destroy()
        self.l_date.destroy()

        # 1st block
        self.c_head = customtkinter.CTkCanvas(self, width=500, height=100, bg=BG_COLOR, highlightthickness=0)
        self.c_head.grid(row=0, column=1)
        self.c_head.create_text(250, 25, text="GOALS FOR TODAY", font=FONT, fill=FONT_COLOR)

        self.c_head.create_image(250, 50, image=self.create_image("images/line.png", 450, 100))

        # 2nd block
        self.c_todos = customtkinter.CTkCanvas(self, width=500, height=450, bg=BG_COLOR, highlightthickness=0)
        self.c_todos.grid(row=1, column=1)
        self.create_goals()

        self.e_todo = customtkinter.CTkEntry(self, font=("Arial", 20))
        self.c_todos.create_window(220, 400, window=self.e_todo, width=370, height=40)
        self.b_add = customtkinter.CTkButton(self, text="+", font=("Arial", 40), fg_color=SECOND_COLOR,
                                             command=self.add_goal)
        self.c_todos.create_window(450, 400, window=self.b_add, height=40, width=40)
        self.e_todo.bind('<Return>', self.add_goal)

        reg = self.register(self.callback)
        self.e_todo.configure(validate="key", validatecommand=(reg, '%P'))

    def create_goals(self):
        self.goals = []
        for i in range(5):
            goal = self.c_todos.create_text(10, 50 + i * 60, text=f"{str(i + 1)}. ", font=("Arial", 20),
                                            fill=FONT_COLOR, anchor="w")
            self.goals.append(goal)

    def add_goal(self, *_):
        value = self.e_todo.get()
        for goal in self.goals:
            x = self.c_todos.itemcget(goal, 'text')

            if len(x) < 4:
                self.c_todos.itemconfigure(goal)
                self.c_todos.itemconfigure(goal, text=f"{x}{value}")
                self.e_todo.delete(0, 100)
                break

        if len(self.c_todos.itemcget(self.goals[4], 'text')) > 3:
            print("xd")
            self.accept_goals()
            self.e_todo.unbind("<Return>")

    def callback(self, input1):
        if len(input1) < 30:
            return True
        else:
            return False

    def accept_goals(self):
        self.e_todo.configure(state="disabled")
        self.b_add.configure(state="disabled")
        self.c_accept = customtkinter.CTkCanvas(self, width=500, height=150, bg=BG_COLOR, highlightthickness=0)
        self.c_accept.grid(row=2, column=1)

        self.c_accept.create_text(250, 25, text="These are my goals", font=FONT, fill=FONT_COLOR)
        self.b_yes = customtkinter.CTkButton(self, text="Yes", font=("Arial", 30), fg_color=SECOND_COLOR)
        self.c_accept.create_window(150, 100, window=self.b_yes, height=40, width=150)

        self.b_no = customtkinter.CTkButton(self, text="No", font=("Arial", 30), fg_color=BG_COLOR,
                                            border_color=SECOND_COLOR, border_width=5)
        self.c_accept.create_window(350, 100, window=self.b_no, height=40, width=150)

    def create_image(self, file, x, y):
        img = Image.open(file)
        img = img.resize((x, y))
        self.img = ImageTk.PhotoImage(img)
        return self.img


if __name__ == "__main__":
    app = App()
    app.mainloop()

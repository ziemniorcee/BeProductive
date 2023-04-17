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
        self.welcome_window()
        # configure window
        self.title("Better Tomorrow")
        self.geometry(f"{500}x{700}")

    def welcome_window(self):
        today = Date()
        date = today.day
        hour = today.hour1

        weather_data = Weather(hour)



        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=3)

        self.label_head = customtkinter.CTkLabel(self, text=f" {date} ", font=FONT, text_color=FONT_COLOR, )
        self.label_head.grid(row=0, column=1)

        self.canvas = customtkinter.CTkCanvas(self, width=400, height=300, bg=BG_COLOR, highlightthickness=0)
        self.canvas.grid(row=1, column=1)

        img = Image.open(weather_data.image)
        img = img.resize((300, 300))
        self.img = ImageTk.PhotoImage(img)

        self.canvas.create_image(200, 150, image=self.img)

        self.canvas.create_text(200, 150, text=f"{weather_data.temperature[0]}", font=FONT, fill=FONT_COLOR)
        self.canvas.create_text(200, 180, text=f"Feels like: {weather_data.temperature[1]}", font=("Arial", 15),
                                fill=FONT_COLOR)

        self.main_button = customtkinter.CTkButton(self, text="Start your day", fg_color="transparent", font=FONT,
                                                   border_width=2, border_color=SECOND_COLOR,
                                                   text_color=("gray10", "#DCE4EE"), command=self.second_window)
        self.main_button.grid(row=2, column=0, columnspan=2)

    def second_window(self):
        self.canvas.destroy()
        self.main_button.destroy()
        self.label_head.destroy()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)

        # 1st block
        self.canvas_head = customtkinter.CTkCanvas(self, width=500, height=100, bg=BG_COLOR, highlightthickness=0)
        self.canvas_head.grid(row=0, column=1)
        self.canvas_head.create_text(250, 25, text="GOALS FOR TODAY", font=FONT, fill=FONT_COLOR)
        img = Image.open("images/line.png")
        img = img.resize((450, 100))
        self.img = ImageTk.PhotoImage(img)
        self.canvas_head.create_image(250, 50, image=self.img)

        # 2nd block
        self.canvas_list = customtkinter.CTkCanvas(self, width=500, height=450, bg=BG_COLOR, highlightthickness=0)
        self.canvas_list.grid(row=1, column=1)
        self.create_goals()

        self.entry_widget = customtkinter.CTkEntry(self, font=("Arial", 20))
        self.canvas_list.create_window(220, 400, window=self.entry_widget, width=370, height=40)
        self.button_widget = customtkinter.CTkButton(self, text="+", font=("Arial", 40), fg_color=SECOND_COLOR,
                                                     command=self.add_goal)
        self.canvas_list.create_window(450, 400, window=self.button_widget, height=40, width=40)
        self.entry_widget.bind('<Return>', self.add_goal)

        reg = self.register(self.callback)
        self.entry_widget.configure(validate="key", validatecommand=(reg, '%P'))

    def create_goals(self):
        self.goals = []
        for i in range(5):
            goal = self.canvas_list.create_text(10, 50 + i * 60, text=f"{str(i + 1)}. ", font=("Arial", 20),
                                                fill=FONT_COLOR, anchor="w")
            self.goals.append(goal)

    def add_goal(self, *_):
        value = self.entry_widget.get()
        for goal in self.goals:
            x = self.canvas_list.itemcget(goal, 'text')

            if len(x) < 4:
                self.canvas_list.itemconfigure(goal)
                self.canvas_list.itemconfigure(goal, text=f"{x}{value}")
                self.entry_widget.delete(0, 100)
                break

        if len(self.canvas_list.itemcget(self.goals[4], 'text')) > 3:
            print("xd")
            self.accept_goals()
            self.entry_widget.unbind("<Return>")

    def callback(self, input1):
        if len(input1) < 30:
            return True
        else:
            return False

    def accept_goals(self):
        self.entry_widget.configure(state="disabled")
        self.button_widget.configure(state="disabled")
        self.accept_canvas = customtkinter.CTkCanvas(self, width=500, height=150, bg=BG_COLOR, highlightthickness=0)
        self.accept_canvas.grid(row=2, column=1)

        self.accept_canvas.create_text(250, 25, text="These are my goals", font=FONT, fill=FONT_COLOR)
        self.yes_button = customtkinter.CTkButton(self, text="+", font=("Arial", 40), fg_color=SECOND_COLOR)
        self.accept_canvas.create_window(150, 100, window=self.yes_button, height=40, width=40)

if __name__ == "__main__":
    app = App()
    app.mainloop()

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
        self.second_window()

    def welcome_window(self):
        today = Date()
        date = today.day
        hour = today.hour1

        weather_data = Weather(hour)

        # configure window
        self.title("Better Tomorrow")
        self.geometry(f"{500}x{700}")

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

        # label_weather = customtkinter.CTkLabel(self, text=text, font=FONT_1)
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

        self.canvas2 = customtkinter.CTkCanvas(self, width=400, height=100, bg=BG_COLOR, highlightthickness=0)
        self.canvas2.grid(row=0, column=1)
        self.canvas2.create_text(200, 25, text="GOALS FOR TODAY", font=FONT, fill=FONT_COLOR)
        img = Image.open("images/line.png")
        self.img = ImageTk.PhotoImage(img)
        self.canvas2.create_image(200, 50, image=self.img)

        self.canvas3 = customtkinter.CTkCanvas(self, width=500, height=600, bg=BG_COLOR, highlightthickness=0)
        self.canvas3.grid(row=1, column=1)
        self.goals = []
        for i in range(5):
            goal = self.canvas3.create_text(50, 50 + i * 60, text=str(i + 1), font=FONT, fill=FONT_COLOR)
            self.goals.append(goal)

        entry_widget = customtkinter.CTkEntry(self, font=("Arial", 20))
        self.canvas3.create_window(220, 400, window=entry_widget, width=370, height=40)
        self.button_widget = customtkinter.CTkButton(self, text="+", font=("Arial", 40), fg_color=SECOND_COLOR)
        self.canvas3.create_window(450, 400, window=self.button_widget, height=40, width=40)




if __name__ == "__main__":
    app = App()
    app.mainloop()

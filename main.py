import customtkinter
from Data import Date, Weather
from PIL import Image, ImageTk

BG_COLOR = "#242424"
FONT_COLOR = "#fcf7ff"
SECOND_COLOR = "#2C0049"

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

FONT = ("Arial", 30)


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

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

        label_date = customtkinter.CTkLabel(self, text=f" {date} ", font=FONT, text_color=FONT_COLOR)
        label_date.grid(row=0, column=1)

        canvas = customtkinter.CTkCanvas(self, width=400, height=300, bg=BG_COLOR, highlightthickness=0)
        canvas.grid(row=1, column=1)

        img = Image.open(weather_data.image)
        img = img.resize((300, 300))
        self.img = ImageTk.PhotoImage(img)

        canvas.create_image(200, 150, image=self.img)

        # label_weather = customtkinter.CTkLabel(self, text=text, font=FONT_1)
        canvas.create_text(200, 150, text=f"{weather_data.temperature[0]}", font=FONT, fill=FONT_COLOR)
        canvas.create_text(200, 180, text=f"Feels like: {weather_data.temperature[1]}", font=("Arial", 15), fill=FONT_COLOR)

        main_button = customtkinter.CTkButton(self, text="Start your day", fg_color="transparent", font=FONT,
                                              border_width=2, border_color=SECOND_COLOR,
                                              text_color=("gray10", "#DCE4EE"))
        main_button.grid(row=2, column=0, columnspan=2)


if __name__ == "__main__":
    app = App()
    app.mainloop()

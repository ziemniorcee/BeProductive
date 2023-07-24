from PIL import ImageFont, Image, ImageColor
from customtkinter import *
from CTkColorPicker import *

images_src = ["/weather/src-wi-cloud.png", "/weather/src-wi-day-sunny.png", "/weather/src-wi-dust.png",
              "/weather/src-wi-night-clear.png", "/weather/src-wi-rain.png", "/weather/src-wi-snow.png",
              "/weather/src-wi-thunderstorm.png", "/habits/src-checked.png", "/habits/src-unchecked.png",
              "/goals/src-arrow.png", "/clock/src-clock.png", "/clock/src-hand2.png"]

images = ["/weather/wi-cloud.png", "/weather/wi-day-sunny.png", "/weather/wi-dust.png",
          "/weather/wi-night-clear.png", "/weather/wi-rain.png", "/weather/wi-snow.png",
          "/weather/wi-thunderstorm.png", "/habits/checked.png", "/habits/unchecked.png", "/goals/arrow.png",
          "/clock/clock.png", "/clock/hand2.png"]


# FONT_TIMER = ("Arial", 50)
# FONT_ADD = ("Arial", 60)
# FONT_BOX = ImageFont.truetype("arial.ttf", 20)
# FONT_BOX2 = ImageFont.truetype("arial.ttf", 30)


class Settings:
    def __init__(self):
        self.main_color = None
        self.second_color = None
        self.font_color = "#D4D4D4"

        self.font = ("Arial", 30)
        self.setup_color()

    def setup_color(self):
        with open("data/settings.txt", "r") as f:
            lines = f.readlines()
            self.main_color = lines[0].strip()
            self.second_color = lines[1].strip()


class SettingsButton(CTkToplevel):
    def __init__(self, root):
        self.settings = Settings()
        super().__init__()
        self.settings_on = True
        self.main = root


        self.create_settings_window()

    def create_settings_window(self):
        self.title("Settings")
        self.resizable(False, False)

        self.geometry('%dx%d+%d+%d' % (300, 600, 2250, 100))
        self.c_settings = CTkCanvas(self, width=300, height=600, bg=self.settings.main_color, highlightthickness=0)
        self.c_settings.grid(row=0, column=0)

        self.b_set_color = CTkButton(self, text="Set leading color", font=self.settings.font, fg_color=self.settings.second_color,
                                     hover_color=self.settings.main_color, border_color=self.settings.second_color,
                                     border_width=5,
                                     command=self.ask_color)
        self.c_settings.create_window(150, 50, window=self.b_set_color, width=250, height=50)

        self.b_save = CTkButton(self, text="Save and restart", font=self.settings.font, fg_color=self.settings.main_color,
                                hover_color=self.settings.second_color, border_color=self.settings.second_color,
                                border_width=5,
                                command=self.save)
        self.c_settings.create_window(150, 550, window=self.b_save, width=250, height=50)

    def ask_color(self):
        pick_color = AskColor()
        self.color = pick_color.get()
        if self.color is not None:
            self.b_set_color.configure(border_color=self.color)

    def save(self):
        self.change_images()
        self.main.destroy()
        os.system("python main.py")

    def change_images(self):
        rgb = ImageColor.getcolor(self.color, "RGB")
        for i in range(len(images_src)):
            img = Image.open(f"images{images_src[i]}")
            img = img.convert("RGBA")
            data = img.getdata()
            new_image = []

            for item in data:
                if item[0] == 44:
                    new_image.append((rgb[0], rgb[1], rgb[2], item[3]))
                elif item[0] != 255:
                    new_image.append(item)
                else:
                    new_image.append((255, 255, 255, 0))

            img.putdata(new_image)
            img.save(f"images{images[i]}")

            with open("data/settings.txt", "w+") as file:
                file.write("#242424\n")
                file.write('%s\n' % self.color)

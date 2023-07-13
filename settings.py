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

with open("data/settings.txt", "r") as f:
    lines = f.readlines()
    COL_2 = lines[1].strip()

COL_1 = "#242424"
COL_FONT = "#fcf7ff"

FONT = ("Arial", 30)
FONT_TIMER = ("Arial", 50)
FONT_ADD = ("Arial", 60)
FONT_BOX = ImageFont.truetype("arial.ttf", 20)

FONT_TEXT = ("Arial", 20)
FONT_TEXT_STRIKE = ("Arial", 20, "overstrike", "bold")


class Settings(CTkToplevel):
    def __init__(self, root):
        super().__init__()
        self.is_settings_on = True
        self.main = root

        self.create_settings_window()

    def create_settings_window(self):
        self.title("Settings")
        self.resizable(False, False)

        self.geometry('%dx%d+%d+%d' % (300, 600, 2250, 100))
        self.c_settings = CTkCanvas(self, width=300, height=600, bg=COL_1, highlightthickness=0)
        self.c_settings.grid(row=0, column=0)

        self.b_set_color = CTkButton(self, text="Set leading color", font=FONT, fg_color=COL_2,
                                     hover_color=COL_1, border_color=COL_2, border_width=5,
                                     command=self.ask_color)
        self.c_settings.create_window(150, 50, window=self.b_set_color, width=250, height=50)

        self.b_save = CTkButton(self, text="Save and restart", font=FONT, fg_color=COL_1,
                                hover_color=COL_2, border_color=COL_2, border_width=5,
                                command=self.save)
        self.c_settings.create_window(150, 550, window=self.b_save, width=250, height=50)

    def ask_color(self):
        pick_color = AskColor()
        self.color = pick_color.get()
        if self.color is not None:
            self.b_set_color.configure(border_color=self.color)
            with open("data/settings.txt", "w") as file:
                file.write('%s\n' % "0")
                file.write('%s\n' % self.color)

    def save(self):
        self.main.destroy()
        os.system("python main.py")


def change_images():
    with open("data/settings.txt", "r") as f:
        lines = f.readlines()

        for i in range(len(lines)):
            lines[i] = lines[i].strip()

    if lines[0] == '0':
        rgb = ImageColor.getcolor(lines[1], "RGB")
        for i in range(len(images_src)):
            img = Image.open(f"images{images_src[i]}")
            img = img.convert("RGBA")
            d = img.getdata()
            new_image = []

            for item in d:
                if item[0] == 44:
                    new_image.append((rgb[0], rgb[1], rgb[2], item[3]))
                elif item[0] != 255:
                    new_image.append(item)
                else:
                    new_image.append((255, 255, 255, 0))

            img.putdata(new_image)

            img.save(f"images{images[i]}")
            lines[0] = '1'

        with open("data/settings.txt", "w+") as file:
            file.write('%s\n' % lines[0])
            file.write('%s\n' % lines[1])


change_images()

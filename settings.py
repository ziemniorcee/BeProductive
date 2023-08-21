from PIL import ImageFont, Image, ImageColor
from customtkinter import *
from CTkColorPicker import *
import customtkinter


class Settings:
    """
    A class for getting settings

    Attributes
    ----------
    main_color : str
        main color used in app
    second_color : str
        secondary color used in app
    font_color : str
        used folor font
    font : tuple(str, int)
        defines mainly used font

    Methods
    -------
    setup_color():
        gets color from file
    """

    def __init__(self, root=None):
        """
        Constructs necessary settings
        """
        self.app = root
        self.themes = ["light", "dark"]
        self.main_color = None
        self.second_color = None
        self.font_color = None
        self.block_font_color = "#D4D4D4"
        self.theme = None
        self.resolution = [1,1]
        self.resolution_w_h = []
        self.get_settings()

        self.font = ("Arial", int(30 * self.resolution[0]))

    def get_settings(self):
        """
        sets up colors for app

        Returns
        -------
        None
        """

        main_colors = ["#FFFFFF", "#242424"]
        font_colors = ["#1B1B1B", "#D4D4D4"]
        with open("data/settings.txt", "r") as file:
            lines = file.readlines()
            self.second_color = lines[0].strip()
            self.theme = int(lines[1].strip())
            self.resolution = [float(lines[2].strip()), float(lines[3].strip())]
            self.first_time = int(lines[4].strip())
        customtkinter.set_appearance_mode(self.themes[self.theme])
        self.main_color = main_colors[self.theme]
        self.font_color = font_colors[self.theme]
        if self.app is not None:
            if self.first_time == 0:
                self.resolution_w_h = [self.app.winfo_screenwidth(), self.app.winfo_screenheight()]
                self.first_time = 1
                if self.resolution_w_h[0] == 1920:
                    self.resolution = [0.7105,0.7375]
                else:
                    self.resolution = [1,1]
                with open("data/settings.txt", "w+") as file:
                    file.write(f"{self.second_color}\n")
                    file.write(f"{self.theme}\n")
                    file.write(f"{self.resolution[0]}\n")
                    file.write(f"{self.resolution[1]}\n")
                    file.write(f"1\n")
            else:
                self.resolution_w_h = [int(self.resolution[0] * 2210 + 350), int(self.resolution[1] * 1370 + 70)]

class SettingsButton(CTkToplevel):
    """
    A class for Settings window

    Attributes
    ----------
    settings : Settings
        contains settings of the app
    settings_on : bool
        is the settings window on
    main : App
        connection to the app

    Methods
    -------
    create_window():
        builds settings window
    ask_color():
        creates color picker
    save():
        saves selected settings and restarts app
    change_images():
        changes images colors
    """

    def __init__(self, root):
        """
        Constructs attributes for class

        Parameters
        ----------
        root : App
            connection to the app
        """
        self.settings = Settings()
        super().__init__()
        self.settings_on = True
        self.main = root
        self.current_resolution = self.settings.resolution
        self.color = self.settings.second_color
        self.create_window()

    def create_window(self):
        """
        builds settings window

        Returns
        -------
        None
        """
        self.title("Settings")
        self.resizable(False, False)

        self.geometry('%dx%d+%d+%d' % (300, 600, 2250, 100))
        self.c_settings = CTkCanvas(self, width=300, height=600, bg=self.settings.main_color, highlightthickness=0)
        self.c_settings.grid(row=0, column=0)

        self.b_set_color = CTkButton(self, text="Set leading color", font=self.settings.font, border_width=5,
                                     fg_color=self.settings.second_color, hover_color=self.settings.main_color,
                                     border_color=self.settings.second_color, command=self.ask_color,
                                     bg_color=self.settings.main_color, text_color=self.settings.font_color)
        self.c_settings.create_window(150, 50, window=self.b_set_color, width=250, height=50)
        self.t_color = self.c_settings.create_text(90, 100, font=("Arial", 20), fill=self.settings.font_color,
                                                   text="#")
        self.e_color = CTkEntry(self, font=("Arial", 20), width=6, bg_color=self.settings.main_color,
                                fg_color=self.settings.main_color, text_color=self.settings.font_color)
        self.e_color.insert(0, self.color[1:])
        self.c_settings.create_window(150, 100, window=self.e_color, width=100, height=30)

        self.b_change_resolution = CTkButton(self, text="Change resolution", font=self.settings.font, border_width=5,
                                             fg_color=self.settings.second_color, hover_color=self.settings.main_color,
                                             border_color=self.settings.second_color, command=self.change_resolution,
                                             bg_color=self.settings.main_color, text_color=self.settings.font_color)
        self.c_settings.create_window(150, 150, window=self.b_change_resolution, width=250, height=50)
        format_res = [int(self.settings.resolution[0] * 2210 + 350), int(self.settings.resolution[1] * 1370 + 70)]
        self.t_resolution = self.c_settings.create_text(150, 200, font=("Arial", 20), fill=self.settings.font_color,
                                                        text=f"Resolution: {format_res[0]}x{format_res[1]}")

        self.b_change_theme = CTkButton(self, text="Change theme", font=self.settings.font, border_width=5,
                                             fg_color=self.settings.second_color, hover_color=self.settings.main_color,
                                             border_color=self.settings.second_color, command=self.change_theme,
                                             bg_color=self.settings.main_color, text_color=self.settings.font_color)
        self.c_settings.create_window(150, 250, window=self.b_change_theme, width=250, height=50)
        self.t_theme = self.c_settings.create_text(150, 300, font=("Arial", 20), fill=self.settings.font_color,
                                                        text=f"{self.settings.themes[self.settings.theme]}", )

        self.b_save = CTkButton(self, text="Save and restart", font=self.settings.font, border_width=5,
                                fg_color=self.settings.main_color, hover_color=self.settings.second_color,
                                border_color=self.settings.second_color, command=self.save,
                                bg_color=self.settings.main_color, text_color=self.settings.font_color)
        self.c_settings.create_window(150, 550, window=self.b_save, width=250, height=50)

    def ask_color(self):
        """
        opens color picker

        Returns
        -------
        None
        """
        pick_color = AskColor()
        self.color = pick_color.get()
        if self.color is not None:
            self.b_set_color.configure(border_color=self.color)
            self.e_color.delete(0, 6)
            self.e_color.insert(0, self.color[1:])

    def save(self):
        """
        saves settings and restarts app

        Returns
        -------
        None
        """
        self.color = "#" + self.e_color.get()
        if self.settings.second_color != self.color:
            self.change_images()
        with open("data/settings.txt", "w+") as file:
            file.write(f"{self.color}\n")
            file.write(f"{self.settings.theme}\n")
            file.write(f"{self.current_resolution[0]}\n")
            file.write(f"{self.current_resolution[1]}\n")
            file.write(f"{self.settings.first_time}\n")

        self.master.destroy()
        os.system("python main.py")

    def change_images(self):
        """
        changes color of the images

        Returns
        -------
        None
        """
        print("xd")
        images = ["/weather/wi-cloud.png", "/weather/wi-day-sunny.png", "/weather/wi-dust.png",
                  "/weather/wi-night-clear.png", "/weather/wi-rain.png", "/weather/wi-snow.png",
                  "/weather/wi-thunderstorm.png", "/habits/checked.png", "/habits/unchecked.png", "/goals/arrow.png",
                  "/clock/clock.png", "/clock/hand2.png", "/floatbar/exit.png", "/floatbar/laura.png",
                  "/floatbar/laura2.png", "/floatbar/next.png", "/floatbar/return.png"]
        rgb = ImageColor.getcolor(self.color, "RGB")
        for image in images:
            last_index = 0
            for j, char in enumerate(image):
                if char == "/":
                    last_index = j

            image_src = image[:last_index + 1] + "src-" + image[last_index + 1:]

            img = Image.open(f"images{image_src}")
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
            img.save(f"images{image}")

    def change_resolution(self):
        resolutions = [[1, 1], [0.7105, 0.7375]]
        resolution_id = resolutions.index(self.current_resolution)
        resolution_id += 1
        if resolution_id + 1 > len(resolutions):
            resolution_id = 0
        self.current_resolution = resolutions[resolution_id]

        print(self.current_resolution)
        format_res = [int(self.current_resolution[0] * 2210 + 350), int(self.current_resolution[1] * 1370 + 70)]
        self.c_settings.itemconfigure(self.t_resolution, text=f"Resolution: {format_res[0]}x{format_res[1]}")

    def change_theme(self):
        self.settings.theme = int(not self.settings.theme)
        self.c_settings.itemconfigure(self.t_theme, text=self.settings.themes[self.settings.theme])
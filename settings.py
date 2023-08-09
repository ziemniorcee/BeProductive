from PIL import ImageFont, Image, ImageColor
from customtkinter import *
from CTkColorPicker import *


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

    def __init__(self):
        """
        Constructs necessary settings
        """
        self.main_color = None
        self.second_color = None
        self.font_color = "#D4D4D4"
        self.resolution = []
        self.get_settings()

        self.font = ("Arial", int(30 * self.resolution[0]))

    def get_settings(self):
        """
        sets up colors for app

        Returns
        -------
        None
        """
        with open("data/settings.txt", "r") as file:
            lines = file.readlines()
            self.main_color = lines[0].strip()
            self.second_color = lines[1].strip()
            self.resolution = [float(lines[2].strip()), float(lines[3].strip())]


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
                                     border_color=self.settings.second_color, command=self.ask_color)
        self.c_settings.create_window(150, 50, window=self.b_set_color, width=250, height=50)
        self.t_color = self.c_settings.create_text(150, 100, font=("Arial", 20), fill=self.settings.second_color,
                                                   text=f"{self.color}")

        self.b_change_resolution = CTkButton(self, text="Change resolution", font=self.settings.font, border_width=5,
                                             fg_color=self.settings.second_color, hover_color=self.settings.main_color,
                                             border_color=self.settings.second_color, command=self.change_resolution)
        self.c_settings.create_window(150, 150, window=self.b_change_resolution, width=250, height=50)
        format_res = [int(self.settings.resolution[0] * 2210 + 350), int(self.settings.resolution[1] * 1370 + 70)]
        self.t_resolution = self.c_settings.create_text(150, 200, font=("Arial", 20), fill=self.settings.font_color,
                                                        text=f"Resolution: {format_res[0]}x{format_res[1]}")

        self.b_save = CTkButton(self, text="Save and restart", font=self.settings.font, border_width=5,
                                fg_color=self.settings.main_color, hover_color=self.settings.second_color,
                                border_color=self.settings.second_color, command=self.save)
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
            self.c_settings.itemconfigure(self.t_color, text=self.color, fill=self.color)
    def save(self):
        """
        saves settings and restarts app

        Returns
        -------
        None
        """
        if self.settings.second_color != self.color:
            self.change_images()
        with open("data/settings.txt", "w+") as file:
            file.write("#242424\n")
            file.write(f"{self.color}\n")
            file.write(f"{self.current_resolution[0]}\n")
            file.write(f"{self.current_resolution[1]}\n")

        self.master.destroy()
        os.system("python main.py")

    def change_images(self):
        """
        changes color of the images

        Returns
        -------
        None
        """
        images = ["/weather/wi-cloud.png", "/weather/wi-day-sunny.png", "/weather/wi-dust.png",
                  "/weather/wi-night-clear.png", "/weather/wi-rain.png", "/weather/wi-snow.png",
                  "/weather/wi-thunderstorm.png", "/habits/checked.png", "/habits/unchecked.png", "/goals/arrow.png",
                  "/clock/clock.png", "/clock/hand2.png"]

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

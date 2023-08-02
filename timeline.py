import os
from dataclasses import dataclass
from customtkinter import CTkCanvas, CTkButton, CTkFrame, CTkImage
from Data import Date
from actions import *
from newrcblock import NewRCBlock
from settings import Settings


class TimelineWidget(CTkFrame):
    """
    A class that creates timeline widget on the main page

    ...
    Attributes
    ----------
    app : App
        connection to the main app
    settings : Settings
        app parameters
    today_data : Date
        today's date parameters
    blocks : list[str]
        contains block's timer, color and category
    c_timeline : CTkCanvas
        timeline canvas
    c_timer : CTkCanvas
        timer canvas

    Methods
    ---------
    create_timeline():
        builds timeline with blocks
    from_file():
        gets timeline blocks parameters
    """
    def __init__(self, master):
        """
        Constructs attributes for the widget

        Builds timeline and player canvases

        Parameters
        ----------
        master : App
            stores connection to the main app

        """
        super().__init__(master, width=2060, height=270)
        self.app = master
        self.settings = Settings()
        self.today_data = Date()
        self.blocks = self.from_file()
        self.c_timeline = CTkCanvas(self, width=2060, height=160, bg=self.settings.main_color, highlightthickness=0)
        self.c_timeline.grid(row=0, column=0)
        self.create_timeline()

        timers = [int(item[0]) for item in self.blocks]
        self.c_player = BlocksPlayer(self, timers)
        self.c_player.grid(row=1, column=0)

    def create_timeline(self):
        """
        builds timeline with blocks

        Returns
        --------
        None
        """
        self.c_timeline.create_line(50, 30, 2060, 30, fill=self.settings.second_color, width=5)
        self.c_timeline.create_line(2010, 60, 2060, 30, fill=self.settings.second_color, width=5)
        self.c_timeline.create_line(2010, 0, 2060, 30, fill=self.settings.second_color, width=5)

        self.c_timeline.create_line(50, 130, 2060, 130, fill=self.settings.second_color, width=5)
        self.c_timeline.create_line(2010, 160, 2060, 130, fill=self.settings.second_color, width=5)
        self.c_timeline.create_line(2010, 100, 2060, 130, fill=self.settings.second_color, width=5)

        for i in range(len(self.blocks)):
            self.c_timeline.create_rectangle(100 + i * 200, 30, 300 + i * 200, 130, fill=self.blocks[i][1],
                                             outline=self.settings.second_color, width=5)
            self.c_timeline.create_text(200 + i * 200, 80, text=format_time(self.blocks[i][0]), font=self.settings.font,
                                        fill=self.settings.font_color)
            self.c_timeline.create_text(200 + i * 200, 110, text=self.blocks[i][2], font=("Arial", 15),
                                        fill=self.settings.font_color)

    def from_file(self):
        """
        gets timeline blocks parameters

        Returns
        --------
        list[str]
        """
        parameters = []
        if os.path.isfile("data/tl_blocks.txt"):
            with open("data/tl_blocks.txt", 'r', encoding="utf-8") as file:
                lines = file.readlines()
                if len(lines) != 0:
                    if str(self.today_data.formatted_date) == lines[0][:-1]:
                        for i in range(1, len(lines), 3):
                            parameters.append([lines[i].strip(), lines[i + 1].strip(), lines[i + 2].strip()])
        else:
            with open("data/tl_blocks.txt", 'x', encoding="utf-8"):
                pass
        return parameters

class BlocksPlayer(CTkCanvas):
    """
    A class for player canvas in timeline widget

    ...
    Attributes
    ----------
    settings : Settings
        contains settings of the app
    master : CTkFrame
        access to the widget
    timer_len : str
        current time of played block
    current_block : int
        number of currently played block
    current_time : int
        time passed in seconds
    pause_on : bool
        is the player paused
    current_timer : str
        current timer state
    end_timer : str
        finish time
    vertical : int
        id of vertical line
    vertical_speed : float
        vertical line speed
    vertical_position : int
        current vertical line x position
    horizontal : int
        id of horizontal line
    horizontal_len : int
        current horizontal line length
    horizontal_speed : float
        horizontal line speed
    play_pause : int
        id of play pause button
    time_current : int
        id of current time item

    Methods
    ----------
    create_timer():
        creates block player element
    start_stop_timer():
        starts or stops player running
    count_down():
        recursion loop of seconds passing
    next_block():
        skips current block to the next one
    prev_block():
        gets back to the previous block
    restart():
        restarts player
    reset():
        resets player current block
    _change_img():
        changes play_pause button image
    _value_reset():
        resets player values

    """
    def __init__(self, master, timers):
        """
        Constructs timer's attributes

        Parameters
        ----------
        master : TimelineWidget
            connection to the window
        timers : list[int]
            stores timers of timeline blocks
        """
        self.settings = Settings()
        super().__init__(master, width=2060, height=110, bg=self.settings.main_color, highlightthickness=0)
        self.master = master
        self.timers = timers
        self.timer_len = None

        self.current_block = 0
        self.current_time = 0
        self.pause_on = False

        self.current_timer = "0:00"
        self.end_timer = None
        self.time_current = None

        self.vertical = None
        self.vertical_speed = None
        self.vertical_position = 100

        self.horizontal = None
        self.horizontal_len = 555
        self.horizontal_speed = None


        self.play_pause = None
        self.create_timer()

    def create_timer(self):
        """
        creates block player element

        Returns
        ---------
        None
        """
        img = CTkImage(light_image=Image.open("images/timeline/play.png"), size=(50, 50))
        self.play_pause = CTkButton(self, image=img, text="", fg_color=self.settings.main_color,
                                    hover_color=self.settings.second_color, command=self.start_stop_timer)
        self.create_window(1055, 30, window=self.play_pause, width=70, height=60)

        img = CTkImage(light_image=Image.open("images/timeline/next.png"), size=(25, 25))
        self.next = CTkButton(self, image=img, text="", fg_color=self.settings.main_color,
                              hover_color=self.settings.second_color, command=self.next_block)
        self.create_window(1155, 30, window=self.next, width=40, height=40)

        img = CTkImage(light_image=Image.open("images/timeline/previous.png"), size=(25, 25))
        self.previous = CTkButton(self, image=img, text="", fg_color=self.settings.main_color,
                                  hover_color=self.settings.second_color, command=self.prev_block)
        self.create_window(955, 30, window=self.previous, width=40, height=40)

        self.time_current = self.create_text(500, 80, text=f"{self.current_timer}", font=("Arial", 20),
                                             fill=self.settings.font_color)
        self.end_timer = self.create_text(1610, 80, text="0:00", font=("Arial", 20),
                                          fill=self.settings.font_color)
        self.vertical = self.master.c_timeline.create_line(100, 0, 100, 160, fill=self.settings.font_color, width=5)
        self.create_line(555, 80, 1555, 80, fill=self.settings.second_color, width=6)
        self.horizontal = self.create_line(555, 80, 555, 80, fill=self.settings.font_color, width=8)

        if len(self.timers) > 0:
            self.timer_len = self.timers[0]
            self.itemconfigure(self.end_timer, text=f"{self.timer_len}:00")
            self.pause_on = False

    def start_stop_timer(self):
        """
        starts or stops player running

        Returns
        ---------
        None
        """
        self.pause_on = not self.pause_on
        self.play_pause.configure(command=None)
        self.master.app.after(500, lambda: self.play_pause.configure(command=self.start_stop_timer))

        if self.pause_on:
            self._change_img("pause")
            self.timer_len = self.timers[self.current_block]
            self.vertical_speed = 200 / (self.timer_len * 60)
            self.horizontal_speed = 1000 / (self.timer_len * 60)

            if self.current_time == 0:
                self.count_down(0)
            else:
                self.count_down(self.current_time)

    def count_down(self, count):
        """
        recursion loop of seconds passing

        Parameters
        ----------
        count : int
            time in seconds

        Returns
        ---------
        None
        """
        if count <= self.timer_len * 60 and self.pause_on:
            self.current_timer = f"{int(count / 60)}:{count % 60 if count % 60 > 9 else f'0{count % 60}'}"
            if self.master.app.page == 0:
                self.itemconfigure(self.time_current, text=self.current_timer)
                self.master.c_timeline.coords(self.vertical, self.vertical_position, 0, self.vertical_position, 160)
                self.coords(self.horizontal, 555, 80, self.horizontal_len, 80)

            self.current_time = count + 1
            self.master.app.after(1000, self.count_down, count + 1)
            self.vertical_position += self.vertical_speed
            self.horizontal_len += self.horizontal_speed
        elif not count < self.timer_len * 60:
            self.next_block()
        else:
            self._change_img("play")

    def next_block(self):
        """
        skips current block to the next one

        Returns
        ---------
        None
        """
        self.play_pause.configure(command=None)
        self.master.app.after(800, lambda: self.play_pause.configure(command=self.start_stop_timer))
        if len(self.timers) - 1 > self.current_block:
            self.current_block += 1
            self.reset()

    def prev_block(self):
        """
        gets back to the previous block

        if player is during block playing than is return to the beginning of the block

        Returns
        ---------
        None
        """
        self.play_pause.configure(command=None)
        self.master.app.after(800, lambda: self.play_pause.configure(command=self.start_stop_timer))
        if self.current_block > 0 and self.current_time == 0:
            self.current_block -= 1
        self.reset()

    def restart(self):
        """
        restarts entire player

        Returns
        ---------
        None
        """
        self.current_block = 0
        self._value_reset()

    def reset(self):
        """
        resets player current block

        Returns
        ---------
        None
        """
        self._value_reset()
        self.itemconfigure(self.end_timer, text=f"{self.timers[self.current_block]}:00")
        self.itemconfigure(self.time_current, text="0:00")
        self.coords(self.horizontal, 555, 1400, 555, 1400)
        self.master.c_timeline.coords(self.vertical, self.vertical_position, 0, self.vertical_position, 160)

    def _change_img(self, file):
        """
        changes play_pause button image

        Parameters
        ----------
        file : str
            file name

        Returns
        ---------
        None
        """
        img = CTkImage(light_image=Image.open(f"images/timeline/{file}.png"), size=(50, 50))
        self.play_pause.configure(image=img)

    def _value_reset(self):
        """
        resets player values

        Returns
        ---------
        None
        """
        self.pause_on = False
        self.vertical_position = 100 + self.current_block * 200
        self._change_img("play")
        self.current_time = 0
        self.horizontal_len = 555


class TimelineWindow:
    """
    A class for timeline window

    Attributes
    ----------
    settings : Settings
        contains settings of the app
    app : App
        connection to the main app
    tl_blocks : TimelineBlocks
        object of the TimelineBlocks class
    rc_blocks : RecentlyBlocks
        object of the RecentlyBlocks class
    saved_blocks : SavedBlocks
        object of the SavedBlocks

    Methods
    ---------
    create_window():
        creates timeline window
    """
    def __init__(self, root):
        """
        Constructs essential attributes

        Parameters
        ----------
        root : App
            access to the main app
        """
        self.settings = Settings()
        self.app = root

        self.tl_blocks = None
        self.rc_blocks = None
        self.saved_blocks = None

    def create_window(self):
        """
        Creates timeline_window

        Returns
        -------
        None
        """
        self.app.page = 2
        self.app.create_c_main()

        self.app.c_main.create_text(1080, 60, text="Create focus timeline", font=self.settings.font,
                                    fill=self.settings.font_color)
        self.app.c_main.create_line(870, 100, 1290, 100, fill=self.settings.second_color, width=8)
        self.app.c_main.create_rectangle(50, 150, 2110, 1000, outline=self.settings.second_color, width=5)
        self.app.c_main.create_line(800, 150, 800, 1000, fill=self.settings.second_color, width=5)

        b_submit = CTkButton(self.app, text="Submit", font=self.settings.font, fg_color=self.settings.second_color,
                                  hover_color=self.settings.main_color, border_color=self.settings.second_color,
                                  border_width=5, command=self.app.main.create_main_window)
        self.app.c_main.create_window(2035, 1295, window=b_submit, width=150, height=50)


        self.pointer = self.app.c_main.create_line(100, 1070, 100, 1270, fill="#155255", width=5, state="hidden")
        self.tl_add_bg = self.app.c_main.create_rectangle(50, 1120, 2060, 1220, fill=self.settings.main_color, width=0)

        self.tl_blocks = TimelineBlocks(self.app)
        self.rc_blocks = RecentlyBlocks(self.app)
        self.saved_blocks = SavedBlocks(self.app)

        self.app.c_main.tag_raise(self.pointer)


@dataclass(frozen=False)
class Block:
    """
    A class to contain blocks parameters

    Attributes
    ----------
    color : str
        color of the block
    timer : str
        formated timer of the block
    text : str
        text of the block
    element_ids : list[int]
        [0] = id of the block rectangle
        [1] = id of the timer text
        [2] = id of the category text
    tag : str
        tag of the Block
    start_pos list[int]
        position [x,y] of the block
    """
    color: str
    timer: str
    text: str
    element_ids: list[int]
    tag: str
    start_pos: list[int] = 0


class Blocks:
    """
    A parent class for recently and saved blocks

    Attributes
    ----------
    app : App
        connection to the main app
    settings : Settings
        app's settings
    timeline : TimelineBlocks
        access to timeline blocks
    blocks : list[BLocks]
        list of objects of Block class
    width : int
        number of how many blocks fit in one row
    startx : int
        x coordinate of max left block
    delete : int
        influence tags
    selected_block : Block
        currently pressed block
    current_pos : int
        defines last block iteration
    change : int
        position of unpressed block on timeline
    pointer : int
        id of pointer widget in timeline
    pos_counter : list[int]
        current position iteration [i, j]
        i = column
        j = row
    params : list[str]
        contains block's timer, color and category
    tl_add_text : int
        id of text widget

    Methods
    ---------
    add_block():
        creates new block based on parameters
    press():
        after press action
    move():
        after move action
    unpress():
        after unpress action
    from_file():
        gets block's params from the file
    to_file():
        saves params to the file

    """
    def __init__(self, root, file_name, startx, width):
        """
        Constructs attributes and creates blocks

        Parameters
        ----------
        root : App
            connection to the app
        file_name : str
            file name for the block params
        startx : int
            max left position for the blocks
        width : int
            how many columns of blocks there are
        """
        self.app = root
        self.settings = Settings()
        self.timeline = self.app.timeline.tl_blocks
        self.blocks = []
        self.width = width
        self.startx = startx
        self.delete = 0
        self.selected_block = None
        self.current_pos = 0
        self.change = 0
        self.pointer = self.app.timeline.pointer
        self.pos_counter = [0, 0]
        self.params = self.from_file(file_name)
        for param in self.params:
            self.add_block(param)

        self.tl_add_text = self.app.c_main.create_text(1055, 1280, font=("Arial", 30), fill=self.settings.font_color,
                                                       state="hidden", text="Add to the timeline")

    def add_block(self, param):
        """
        creates new block based on parameters

        Parameters : list[str]

        Returns
        ---------
        None
        """
        tag_name = f"b{self.width}_{self.pos_counter[1] * 10 + self.pos_counter[0]}_{self.delete}"
        block_id = self.app.c_main.create_rectangle(self.startx + self.pos_counter[0] * 250,
                                                    225 + 150 * self.pos_counter[1],
                                                    self.startx + 200 + self.pos_counter[0] * 250,
                                                    325 + 150 * self.pos_counter[1], fill=param[1], tags=tag_name,
                                                    outline=self.settings.second_color, width=5)
        timer = format_time(param[0])
        timer_id = self.app.c_main.create_text(self.startx + 100 + self.pos_counter[0] * 250,
                                               275 + self.pos_counter[1] * 150, text=timer, font=self.settings.font,
                                               fill=self.settings.font_color, tags=tag_name)
        category_id = self.app.c_main.create_text(self.startx + 100 + self.pos_counter[0] * 250,
                                                  305 + self.pos_counter[1] * 150, text=param[2], tag=tag_name,
                                                  fill=self.settings.font_color, font=("Arial", 15), anchor="center")
        self.blocks.append(Block(param[1], param[0], param[2], [block_id, timer_id, category_id], tag_name,
                                 [self.startx + self.pos_counter[0] * 250, 225 + 150 * self.pos_counter[1]]))
        self.pos_counter[0] += 1
        if self.pos_counter[0] % self.width == 0:
            self.pos_counter[1] += 1
            self.pos_counter[0] = 0

    def press(self, event):
        """
        after press action

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        pressed_id = (event.widget.find_withtag("current")[0])
        for block in self.blocks:
            if pressed_id in block.element_ids:
                self.selected_block = block
                break

        self.app.c_main.itemconfigure(self.app.timeline.tl_add_bg, fill="#313131")
        self.app.c_main.itemconfigure(self.tl_add_text, state="normal")

    def move(self, event):
        """
        after move action, block follows cursor

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        if 1050 < event.y < 1300:

            self.app.c_main.itemconfigure(self.pointer, state='normal')
            self.app.c_main.moveto(self.selected_block.element_ids[0], event.x - 100, 1117)
            self.app.c_main.moveto(self.selected_block.element_ids[1], event.x - 50, 1150)
            self.app.c_main.coords(self.selected_block.element_ids[2], event.x, 1200)

            self.timeline.get_change(event.x)

        else:
            self.app.c_main.moveto(self.selected_block.element_ids[0], event.x - 100, event.y - 50)
            self.app.c_main.moveto(self.selected_block.element_ids[1], event.x - 50, event.y - 20)
            self.app.c_main.coords(self.selected_block.element_ids[2], event.x, event.y + 35)
            if self.pointer is not None:
                self.app.c_main.itemconfigure(self.pointer, state='hidden')

        self.app.c_main.tag_raise(self.selected_block.element_ids[0])
        self.app.c_main.tag_raise(self.selected_block.element_ids[1])
        self.app.c_main.tag_raise(self.selected_block.element_ids[2])

    def unpress(self, event):
        """
        after unpress action

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        if self.pointer is not None:
            self.app.c_main.itemconfigure(self.pointer, state='hidden')

        self.app.c_main.itemconfigure(self.app.timeline.tl_add_bg, fill=self.settings.main_color)
        self.app.c_main.itemconfigure(self.tl_add_text, state="hidden")


        self.app.c_main.moveto(self.selected_block.element_ids[0], self.selected_block.start_pos[0],
                               self.selected_block.start_pos[1])
        self.app.c_main.moveto(self.selected_block.element_ids[1], self.selected_block.start_pos[0] + 50,
                               self.selected_block.start_pos[1] + 30)
        self.app.c_main.coords(self.selected_block.element_ids[2], self.selected_block.start_pos[0] + 100,
                               self.selected_block.start_pos[1] + 85)

        if 1050 < event.y < 1300 and len(self.timeline.blocks) < 9:
            self.timeline.add([self.selected_block.timer, self.selected_block.color, self.selected_block.text])

            element = len(self.timeline.blocks)
            new_pos = 100 + self.timeline.change * 200

            poped = self.timeline.blocks.pop(element - 1)
            self.timeline.blocks.insert(self.timeline.change, poped)

            self.timeline.shift(self.timeline.blocks[self.timeline.change:element + 1], new_pos)
            self.app.timeline.tl_blocks.to_file()

    def from_file(self, file_name):
        """
        gets block's params from the file

        Parameters
        ----------
        file_name : str
            file name

        Returns
        -------
        list[str]
        """
        parameters = []
        if os.path.isfile(f"data/{file_name}"):
            with open(f"data/{file_name}", 'r') as file:
                lines = file.readlines()
                if len(lines) != 0:
                    for i in range(0, len(lines), 3):
                        parameters.append([lines[i].strip(), lines[i + 1].strip(), lines[i + 2].strip()])
        else:
            with open("data/tl_blocks.txt", 'x'):
                pass

        return parameters

    def to_file(self,file_name):
        """
        saves params to the file

        Parameters
        ----------
        file_name : str
            file name

        Returns
        -------
        None
        """
        with open(f"data/{file_name}", "w+") as file:
            for block in self.blocks:
                file.write(f"{block.timer}\n{block.color}\n{block.text}\n")


class RecentlyBlocks(Blocks):
    """
    A class for recently created blocks

    Attributes
    ----------
    app : App
        connection to the app
    todat_data = Date()
        today's date info
    saved_add_bg : int
        id of saved background
    saved_add_text : int
        id of saved text
    clock_window : NewRCBlock
        contains clock window
    is_clock_window_on : bool
        is clock window opened
    new_block : list[str]
        new block parameters

    Methods
    ----------
    bind():
        binds blocks
    rc_press():
        after press bind
    rc_move():
        after move bind
    rc_unpress():
        after unpress bind
    rc_add():
        new recently created block
    clock_on_closing():
        after clock was closed
    """
    def __init__(self, root):
        """
        constructs attributes and builds upon Blocks

        Parameters
        ----------
        root : App
            access to the main app
        """
        super().__init__(root, "rc_blocks.txt", 75, 3)
        self.app = root
        self.today_data = Date()

        self.app.c_main.create_text(425, 175, font=("Arial", 30), fill=self.settings.font_color,
                                    text="Recently created")
        self.saved_add_bg = self.app.c_main.create_rectangle(800, 150, 2110, 1000, fill=self.settings.main_color,
                                                             outline=self.settings.second_color, width=5)
        self.saved_add_text = self.app.c_main.create_text(1455, 975, font=("Arial", 30), fill=self.settings.font_color,
                                                          state="hidden", text="Drop here to save")
        b_rc_create = CTkButton(self.app, text="+", font=("Arial", 70), fg_color=self.settings.main_color,
                                     command=self.rc_add)
        self.app.c_main.create_window(80, 970, window=b_rc_create, height=50, width=50)

        self.clock_window = None
        self.is_clock_window_on = False
        self.new_block = None

        for block in self.blocks:
            self.bind(block.tag)

    def bind(self, tag):
        """
        binds blocks

        Parameters
        ----------
        tag : str
            blocks's tag

        Returns
        -------
        None
        """
        self.app.c_main.tag_bind(tag, "<Button-1>", self.rc_press)
        self.app.c_main.tag_bind(tag, "<B1-Motion>", self.rc_move)
        self.app.c_main.tag_bind(tag, "<ButtonRelease-1>", self.rc_unpress)

    def rc_press(self, event):
        """
        after press bind

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        self.press(event)
        self.app.c_main.itemconfigure(self.saved_add_bg, fill=self.settings.second_color)
        self.app.c_main.itemconfigure(self.saved_add_text, state='normal')

    def rc_move(self, event):
        """
        after move bind

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        self.move(event)
        if 800 < event.x < 2110 and 150 < event.y < 1000:
            self.app.c_main.itemconfigure(self.selected_block.element_ids[0], outline="green")
        else:
            self.app.c_main.itemconfigure(self.selected_block.element_ids[0], outline=self.settings.second_color)

    def rc_unpress(self, event):
        """
        after unpress bind

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        self.unpress(event)
        self.app.c_main.itemconfigure(self.saved_add_bg, fill=self.settings.main_color)
        self.app.c_main.itemconfigure(self.saved_add_text, state='hidden')

        if 800 < event.x < 2110 and 150 < event.y < 1000 and len(self.app.timeline.saved_blocks.blocks) < 25:
            self.app.c_main.itemconfigure(self.saved_add_bg, fill=self.settings.main_color)
            self.app.c_main.itemconfigure(self.saved_add_text, state='hidden')
            self.app.c_main.itemconfigure(self.selected_block.element_ids[0], outline=self.settings.second_color)
            params = [self.selected_block.timer, self.selected_block.color, self.selected_block.text]

            self.app.timeline.saved_blocks.add_block(params)
            self.app.timeline.saved_blocks.bind(self.app.timeline.saved_blocks.blocks[-1].tag)
            self.app.timeline.saved_blocks.to_file("saved_blocks.txt")

    def rc_add(self):
        """
        new recently created block

        Returns
        -------
        None
        """
        if not self.is_clock_window_on or not self.clock_window.window_on:
            self.clock_window = NewRCBlock(self)
            self.clock_window.wm_attributes("-topmost", True)
            self.is_clock_window_on = True
            self.clock_window.protocol("WM_DELETE_WINDOW", self.clock_on_closing)

    def clock_on_closing(self):
        """
        after clock was closed

        Returns
        -------
        None
        """
        start_pos = self.blocks[0].start_pos
        if self.new_block is not None:
            for i in range(len(self.blocks)):
                if i < len(self.blocks) - 1:
                    self.blocks[i].start_pos = self.blocks[i + 1].start_pos
                else:
                    self.blocks[i].start_pos = [self.startx + self.pos_counter[0] * 250,
                                                225 + 150 * self.pos_counter[1]]
                self.app.c_main.moveto(self.blocks[i].element_ids[0], self.blocks[i].start_pos[0],
                                       self.blocks[i].start_pos[1])
                self.app.c_main.moveto(self.blocks[i].element_ids[1], self.blocks[i].start_pos[0] + 50,
                                       self.blocks[i].start_pos[1] + 30)
                self.app.c_main.coords(self.blocks[i].element_ids[2], self.blocks[i].start_pos[0] + 100,
                                       self.blocks[i].start_pos[1] + 85)


            self.delete += 1

            self.add_block(self.new_block)
            self.blocks[-1].start_pos = start_pos
            self.app.c_main.moveto(self.blocks[-1].element_ids[0], start_pos[0], start_pos[1])
            self.app.c_main.moveto(self.blocks[-1].element_ids[1], start_pos[0] + 50, start_pos[1] + 30)
            self.app.c_main.coords(self.blocks[-1].element_ids[2], start_pos[0] + 100, start_pos[1] + 85)
            poped = self.blocks.pop(-1)
            self.blocks.insert(0, poped)
            self.bind(self.blocks[-1].tag)

            if len(self.blocks) > 15:
                self.app.c_main.delete(self.blocks[-1].element_ids[0])
                self.app.c_main.delete(self.blocks[-1].element_ids[1])
                self.app.c_main.delete(self.blocks[-1].element_ids[2])
                self.blocks.pop(-1)
        self.to_file("rc_blocks.txt")
        self.clock_window.destroy()
        self.is_clock_window_on = False


class SavedBlocks(Blocks):
    """
    A class for saved blocks section

    Attributes
    ----------
    app : App
        connection to the app
    saved_trash : int
        id to the trash item

    Methods
    -------
    bind():
        binds blocks
    saved_press():
        after press bind
    saved_move():
        after move bind
    saved_unpress():
        after unpress bind
    """
    def __init__(self, root):
        """
        Constructs attributes for the class

        Parameters
        ----------
        root : App
            connection to the app
        """
        super().__init__(root, "saved_blocks.txt", 825, 5)
        self.app = root
        self.saved_trash = self.app.c_main.create_image(835, 960, image=create_imagetk("images/blocks/trash.png"),
                                                        state="hidden")
        self.app.c_main.create_text(1425, 175, font=("Arial", 30), fill=self.settings.font_color, text="Saved")
        for block in self.blocks:
            self.bind(block.tag)

    def bind(self, tag):
        """
        binds blocks

        Parameters
        ----------
        tag : str
            block's tag
        """
        self.app.c_main.tag_bind(tag, "<Button-1>", self.saved_press)
        self.app.c_main.tag_bind(tag, "<B1-Motion>", self.saved_move)
        self.app.c_main.tag_bind(tag, "<ButtonRelease-1>", self.saved_unpress)

    def saved_press(self, event):
        """
        after press bind

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        self.press(event)
        self.app.c_main.itemconfigure(self.saved_trash, state='normal')

    def saved_move(self, event):
        """
        after move bind

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        self.move(event)
        if 735 < event.x < 935 and 900 < event.y < 1020:
            self.app.c_main.itemconfigure(self.selected_block.element_ids[0], outline="red")
        else:
            self.app.c_main.itemconfigure(self.selected_block.element_ids[0], outline=self.settings.second_color)

    def saved_unpress(self, event):
        """
        after unpress bind

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        self.unpress(event)
        self.app.c_main.itemconfigure(self.saved_trash, state='hidden')
        if 735 < event.x < 935 and 900 < event.y < 1020:
            previous_pos = None

            save_pos = None
            for block in self.blocks[self.blocks.index(self.selected_block):]:
                if previous_pos is not None:
                    self.app.c_main.moveto(block.element_ids[0], previous_pos[0], previous_pos[1])
                    self.app.c_main.moveto(block.element_ids[1], previous_pos[0] + 50, previous_pos[1] + 30)
                    self.app.c_main.coords(block.element_ids[2], previous_pos[0] + 100, previous_pos[1] + 85)
                    save_pos = previous_pos
                previous_pos = block.start_pos
                block.start_pos = save_pos

            if self.pos_counter[0] > 0:
                self.pos_counter[0] -= 1
            else:
                self.pos_counter[1] -= 1
                self.pos_counter[0] = self.width - 1

            self.app.c_main.delete(self.selected_block.element_ids[0])
            self.app.c_main.delete(self.selected_block.element_ids[1])
            self.app.c_main.delete(self.selected_block.element_ids[2])
            self.blocks.remove(self.selected_block)


class TimelineBlocks:
    """
    A class to manage Timeline and blocks

    Attributes
    ----------
    settings : Settings
        contains info about app
    app : App
        connection to the app
    today_data : Date()
        constain today's info
    blocks : list[Block]
        blocks of the timeline
    timeline_positions : list[int]
        existing possible positions
    current_pos : int
        last iteration
    change : int
        next position of the moved block
    selected_block : Block
        pressed block
    pointer : int
        id of pointer item
    tag_id : int
        id for the next block tag
    tl_trash : int
        id of the trash item

    Methods
    ----------
    add():
        builds block
    tl_press():
        after press bind
    tl_move():
        after move bind
    tl_unpress():
        after unpress bind
    shift():
        changes order of blocks
    get_change():
        get selected new position
    from_file():
        gets params from file
    to_file():
        saves params to file
    """
    def __init__(self, root):
        """
        Constructs attributes necessary for class

        Parameters
        ----------
        root : App
            connection to the main app
        """
        self.settings = Settings()
        self.app = root
        self.today_data = Date()

        self.blocks = []
        self.timeline_positions = [100]
        self.current_pos = 0
        self.change = None
        self.selected_block = None

        self.pointer = self.app.timeline.pointer
        self.tag_id = 0
        self.app.c_main.create_line(50, 1120, 2060, 1120, fill=self.settings.second_color, width=5)
        self.app.c_main.create_line(2010, 1090, 2060, 1120, fill=self.settings.second_color, width=5)
        self.app.c_main.create_line(2010, 1150, 2060, 1120, fill=self.settings.second_color, width=5)

        self.app.c_main.create_line(50, 1220, 2060, 1220, fill=self.settings.second_color, width=5)
        self.app.c_main.create_line(2010, 1190, 2060, 1220, fill=self.settings.second_color, width=5)
        self.app.c_main.create_line(2010, 1250, 2060, 1220, fill=self.settings.second_color, width=5)

        self.tl_trash = self.app.c_main.create_image(2100, 1170, image=create_imagetk("images/blocks/trash.png"),
                                                     state="hidden")
        params = self.from_file()
        for param in params:
            self.add(param)

    def add(self, param):
        """
        builds block

        Parameters
        ----------
        param : list[str]
            block data

        Returns
        -------
        None
        """
        tag_name = f"tl{self.tag_id}"
        block_id = self.app.c_main.create_rectangle(self.timeline_positions[self.current_pos], 1120,
                                                    self.timeline_positions[self.current_pos] + 200,
                                                    1220, fill=param[1], outline=self.settings.second_color,
                                                    width=5,
                                                    tags=tag_name)

        timer = format_time(param[0])
        timer_id = self.app.c_main.create_text(self.timeline_positions[self.current_pos] + 100, 1170,
                                               text=timer, font=self.settings.font, fill=self.settings.font_color,
                                               tags=tag_name)
        category_id = self.app.c_main.create_text(self.timeline_positions[self.current_pos] + 100, 1200,
                                                  text=param[2], font=("Arial", 15), fill=self.settings.font_color,
                                                  tags=tag_name)

        self.app.c_main.tag_bind(tag_name, "<B1-Motion>", self.tl_move)
        self.app.c_main.tag_bind(tag_name, "<Button-1>", self.tl_press)
        self.app.c_main.tag_bind(tag_name, "<ButtonRelease-1>", self.tl_unpress)
        self.blocks.append(Block(param[1], param[0], param[2], [block_id, timer_id, category_id], tag_name,
                                 [self.timeline_positions[self.current_pos]]))
        self.timeline_positions.append(self.timeline_positions[self.current_pos] + 200)
        self.current_pos += 1

    def tl_press(self, event):
        """
        after press bind

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        pressed_id = (event.widget.find_withtag("current")[0])
        for block in self.blocks:
            if pressed_id in block.element_ids:
                self.selected_block = block
                break

        self.app.c_main.tag_raise(self.selected_block.element_ids[0])
        self.app.c_main.tag_raise(self.selected_block.element_ids[1])
        self.app.c_main.tag_raise(self.selected_block.element_ids[2])

        self.app.c_main.itemconfigure(self.pointer, state='normal')
        self.app.c_main.itemconfigure(self.tl_trash, state="normal")

    def tl_move(self, event):
        """
        after move bind

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        if 1090 < event.y < 1390:
            self.app.c_main.itemconfigure(self.pointer, state='normal')
            self.app.c_main.moveto(self.selected_block.element_ids[0], event.x - 100, 1117)
            self.app.c_main.moveto(self.selected_block.element_ids[1], event.x - 50, 1150)
            self.app.c_main.coords(self.selected_block.element_ids[2], event.x, 1200)

            self.get_change(event.x)

        if event.x > 2000:
            self.app.c_main.itemconfigure(self.selected_block.element_ids[0], outline="red")
        else:
            self.app.c_main.itemconfigure(self.selected_block.element_ids[0], outline=self.settings.second_color)

    def tl_unpress(self, event):
        """
        after unpress bind

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        self.app.c_main.itemconfigure(self.tl_trash, state="hidden")
        self.app.c_main.itemconfigure(self.pointer, state='hidden')
        self.app.c_main.itemconfigure(self.selected_block.element_ids[0], outline=self.settings.second_color)

        element = int((self.selected_block.start_pos[0] - 100) / 200)
        if element < self.change:
            self.change -= 1

        poped = self.blocks.pop(element)
        self.blocks.insert(self.change, poped)

        if element == self.change:
            self.app.c_main.coords(self.selected_block.element_ids[0], self.selected_block.start_pos[0], 1120,
                                   self.selected_block.start_pos[0] + 200, 1220)
            self.app.c_main.coords(self.selected_block.element_ids[1], self.selected_block.start_pos[0] + 100, 1170)
            self.app.c_main.coords(self.selected_block.element_ids[2], self.selected_block.start_pos[0] + 100, 1200)
        elif self.change > element:
            new_pos = self.selected_block.start_pos[0]
            self.shift(self.blocks[element:self.change + 1], new_pos)
        else:
            new_pos = 100 + self.change * 200
            self.shift(self.blocks[self.change:element + 1], new_pos)

        if event.x > 2000:
            self.current_pos -= 1
            self.timeline_positions.pop(-1)
            self.app.c_main.delete(self.selected_block.element_ids[0])
            self.app.c_main.delete(self.selected_block.element_ids[1])
            self.app.c_main.delete(self.selected_block.element_ids[2])
            self.blocks.pop(-1)

        self.to_file()

    def shift(self, arr, start):
        """
        changes order of blocks

        Parameters
        ----------
        arr : list[BLocks]
            list to change
        start : list[int]
            starting position

        Returns
        -------
        None
        """
        for item in arr:
            item.start_pos[0] = start
            self.app.c_main.coords(item.element_ids[0], start, 1120, start + 200, 1220)
            self.app.c_main.coords(item.element_ids[1], start + 100, 1170)
            self.app.c_main.coords(item.element_ids[2], start + 100, 1200)
            start += 200

    def get_change(self, x):
        """
        get selected new position

        Parameters
        ----------
        x : int
            x position

        Returns
        -------
        None
        """
        i = 0
        for pos in self.timeline_positions:
            if x - 100 <= pos < x + 100:
                self.app.c_main.coords(self.pointer, self.timeline_positions[i], 1070,
                                       self.timeline_positions[i],
                                       1270)
                self.change = i
                break

            i += 1

    def from_file(self):
        """
        gets params from file

        Returns
        -------
        None
        """
        parameters = []
        if os.path.isfile("data/tl_blocks.txt"):
            with open("data/tl_blocks.txt", 'r', encoding="utf-8") as file:
                lines = file.readlines()
                if len(lines) != 0:
                    if str(self.today_data.formatted_date) == lines[0][:-1]:
                        for i in range(1, len(lines), 3):
                            parameters.append([lines[i].strip(), lines[i + 1].strip(), lines[i + 2].strip()])
        else:
            with open("data/tl_blocks.txt", 'x', encoding="utf-8"):
                pass
        return parameters

    def to_file(self):
        """
        saves params to file

        Returns
        -------
        None
        """
        with open("data/tl_blocks.txt", "w+", encoding="utf-8") as file:
            file.write(f"{self.today_data.formatted_date}\n")
            for block in self.blocks:
                file.write(f"{block.timer}\n{block.color}\n{block.text}\n")
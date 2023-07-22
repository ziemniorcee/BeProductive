from CTkMessagebox import CTkMessagebox
from CTkColorPicker import AskColor
from customtkinter import CTkCanvas, CTkButton, CTkFrame, CTkEntry, CTkToplevel, CTkLabel
from settings import *


class Block:
    """A class to represent a block.

    ...
    Attributes
    ----------
    primary_id : int
        block's id
    foreign_ids : list[int]
        ids of blocks connected to the block
    text : str
        text displayed on a block
    color : str
        color of the block
    start_pos : list[int]
        block starting position [x, y]
    end_pos : list[int]
        block position after background move [x, y]
    widget_id : list[int]
        [0] constains block square widget id
        [1] constains block text widget id
    tag : str
        tag of the block
    width :
        calculates width of block square widget based on pixel length of text
    """

    def __init__(self, ids, text, color, start_pos):
        """
        Costructs all the necessary attributes for the block object

        Parameters
        ----------
            ids : str
                chain of intigers, first is id of the block, the rest are other blocks ids for blocks that are connected
            text : str
                text displayed on a block
            color : str
                color of the block
            start_pos : list[int]
                block starting position [x, y]
        """

        self.primary_id = int(ids[0])
        self.foreign_ids = [int(x) for x in ids[1:]]

        self.text = text
        self.color = color
        self.start_pos = start_pos
        self.end_pos = start_pos
        self.widget_id = None
        self.tag = None
        self.width = (FONT_BOX2.getbbox(self.text)[2] * 1.5)


class Strategy:
    """A class to represent a block.

    ...
    Attributes
    ----------
    app : '__main__.App'
        root of main app
    background : Background
        frame of background

    Methods
    ----------
    create_strategy_window():
        Creates life strategy window
    """
    def __init__(self, root):
        """
        Constructs necessary attributes for launching strategy window

        Parameters
        ----------
        root :  '__main__.App'
            access to main app
        """
        self.app = root
        self.background = None

    def create_strategy_window(self):
        """
        Constructs life strategy window in c_main

        Returns
        -------
        None
        """
        self.app.create_c_main()
        self.app.page = 4

        self.app.c_main.create_text(1080, 60, text="Life Strategy", font=FONT, fill=COL_FONT)
        self.app.c_main.create_line(870, 100, 1290, 100, fill=COL_2, width=8)

        self.background = Background(self.app)
        self.background.grid(row=0, column=1)


class Background(CTkFrame):
    """
    A class to build background frame

    ...
    Attributes
    ----------
    move_start : list[int]
        starting position of background [x, y]
    move_diff : list[int]
        background movement vector [x, y]
    c_bg : CTkCanvas
        background canvas

    Methods
    ----------
    bg_press():
        Bind left button press for background tag.
    bg_move():
        Bind left button motion for background tag
    bg_unpress():
        Bind left button unpress for background tag
    """
    def __init__(self, master):
        """
        Constructs all the necessary attributes for the  background

        Parameters
        ----------
        master : __main__.App
            stores connection to the main app
        """
        super().__init__(master, width=2060, height=1170)

        self.grid(row=0, column=1)
        self.move_start = []
        self.move_diff = []


        self.c_bg = CTkCanvas(self, width=2060, height=1170, bg=COL_1)
        self.c_bg.grid(row=0, column=0)
        self.c_bg.create_rectangle(0, 0, 2060, 1170, fill=COL_1, tags="background")
        self.c_bg.tag_bind("background", "<Button-1>", self.bg_press)
        self.c_bg.tag_bind("background", "<B1-Motion>", self.bg_move)
        self.c_bg.tag_bind("background", "<ButtonRelease-1>", self.bg_unpress)

        self.blocks = Blocks(self)

        self.b_new_block = ButtonNewBlock(self)
        self.c_bg.create_window(102, 1142, window=self.b_new_block, height=60, width=200)
        self.b_delete_block = ButtonDeleteBlock(self)
        self.c_bg.create_window(302, 1142, window=self.b_delete_block, height=60, width=200)
        self.b_new_line = ButtonNewLine(self)
        self.c_bg.create_window(502, 1142, window=self.b_new_line, height=60, width=200)
        self.b_delete_line = ButtonDeleteLine(self)
        self.c_bg.create_window(702, 1142, window=self.b_delete_line, height=60, width=200)



    def bg_press(self, event):
        """
        Bind left button press for background tag.

        Saves starting position of background movement
        
        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        self.move_start = [event.x, event.y]

    def bg_move(self, event):
        """
        Bind left button motion for background tag

        Calculates movement difference of background and moves blocks and lines

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        self.move_diff = [event.x - self.move_start[0], event.y - self.move_start[1]]

        for block in self.blocks.blocks:
            block.start_pos = [block.end_pos[0] - self.move_diff[0], block.end_pos[1] - self.move_diff[1]]
            self.c_bg.coords(block.widget_id[0], block.start_pos[0], block.start_pos[1],
                             block.start_pos[0] + block.width, block.start_pos[1] + 70)
            self.c_bg.coords(block.widget_id[1], block.start_pos[0] + int(block.width / 2), block.start_pos[1] + 35)
        self.blocks.create_lines()

    def bg_unpress(self, *_):
        """
        Bind left button unpress for background tag

        Calculates and saves position after background movement

        Returns
        -------
        None
        """
        for block in self.blocks.blocks:
            block.end_pos = [block.end_pos[0] - self.move_diff[0], block.end_pos[1] - self.move_diff[1]]


class Blocks:
    """
    A class for blocks and lines management

    ...
    Attributes
    ----------
    master : CTkFrame
        stores conntection to the background frame
    c_bg : CTkCanvas
        stores connection to the backgorund frame canvas
    blocks : list[Block]
        list of Block objects
    cur_block : Block
        contains selected block
    new_line_id : int
        constains id of the starting block of a new line
    lines : list[int]
        saves widget ids of the lines
    lines_middle : list [list[int]]
         middles of the lines [x, y]
    new_line_start : list [int]
        starting position of new line [x, y]

    Methods
    ---------
    create_blocks():
        creates and displays blocks on the background frame
    create_lines():
        creates and displays lines on the background frame
    block_press():
        Binds left button press to block
    block_move():
        Binds left button motion to block
    block_unpress():
        Binds left button unpress to block
    blocks_from_file():
        Gets blocks info from the file
    blocks_to_file():
        Saves blocks info to the file
    """
    def __init__(self, master):
        """
        Constructs attributes for the blocks and lines management.

        Gets blocks from file and display them with lines

        Parameters
        ----------
        master : CTkFrame
            stores connection to the background frame
        """
        self.master = master
        self.c_bg = master.c_bg

        self.blocks = []
        self.cur_block = None

        self.new_line_id = None
        self.lines = []
        self.lines_middle = []
        self.new_line_start = []

        self.blocks_from_file()
        self.create_blocks()
        self.create_lines()

    def create_blocks(self):
        """
        creates and displays blocks on the background frame

        Adds binds to the blocks

        Returns
        --------
        None
        """
        tag_nr = 0
        for block in self.blocks:
            if block.widget_id is not None:
                self.c_bg.delete(block.widget_id[0])
                self.c_bg.delete(block.widget_id[1])
            block_id = self.c_bg.create_rectangle(block.start_pos[0], block.start_pos[1],
                                                  block.start_pos[0] + block.width,
                                                  block.start_pos[1] + 70, fill=block.color, tags=f"block{tag_nr}",
                                                  outline=COL_2,
                                                  width=3)
            text_id = self.c_bg.create_text(block.start_pos[0] + int(block.width / 2), block.start_pos[1] + 35,
                                            text=block.text, font=FONT, tags=f"block{tag_nr}")
            block.widget_id = [block_id, text_id]
            block.tag = f"block{tag_nr}"
            if tag_nr == 0:
                self.first = int(block_id / 2)
                self.even = text_id % 2
            self.c_bg.tag_bind(f"block{tag_nr}", "<Button-1>", self.block_press)
            self.c_bg.tag_bind(f"block{tag_nr}", "<B1-Motion>", self.block_move)
            self.c_bg.tag_bind(f"block{tag_nr}", "<ButtonRelease-1>", self.block_unpress)
            tag_nr += 1

    def create_lines(self):
        """
        creates and displays lines on the background frame

        Returns
        -------
        None
        """
        for line in self.lines:
            self.c_bg.delete(line[0])
        self.lines = []
        self.lines_middle = []
        for block in self.blocks:

            for key in block.foreign_ids:
                foreign_block = self.blocks[key - 1]
                line = self.c_bg.create_line(block.start_pos[0] + block.width / 2, block.start_pos[1] + 70,
                                             foreign_block.start_pos[0] + foreign_block.width / 2,
                                             foreign_block.start_pos[1],
                                             fill=COL_2, width=3)
                self.lines.append([line, key])
                self.lines_middle.append(
                    [(block.start_pos[0] + block.width / 2 + foreign_block.start_pos[0] + foreign_block.width / 2) / 2,
                     (block.start_pos[1] + 70 + foreign_block.start_pos[1]) / 2])

    def block_press(self, event):
        """
        Binds left button press to block

        If button delete block is on it deletes clicked block
        else if button new line first press choose starting block, second press choose ending block

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        block_id = (event.widget.find_withtag("current")[0])

        if block_id % 2 == self.even:
            block_id -= 1
        block_id = int(block_id / 2 - self.first)
        self.cur_block = self.blocks[block_id]

        print("elif", self.master.b_new_line.new_line_on)
        if self.master.b_delete_block.delete_block_on:
            deleted_id = self.cur_block.primary_id
            self.c_bg.delete(self.cur_block.widget_id[0])
            self.c_bg.delete(self.cur_block.widget_id[1])
            self.blocks.remove(self.cur_block)

            for block in self.blocks:
                if deleted_id in block.foreign_ids:
                    block.foreign_ids.remove(deleted_id)
                if block.primary_id > deleted_id:
                    block.primary_id -= 1

                for i in range(len(block.foreign_ids)):
                    if block.foreign_ids[i] > deleted_id:
                        block.foreign_ids[i] -= 1

            self.blocks_to_file()
            self.create_blocks()
            self.create_lines()

        elif self.master.b_new_line.new_line_on:
            new_line = self.master.b_new_line

            if new_line.new_line_state == 0:
                new_line.new_line_state = 1
                self.new_line_id = self.cur_block.primary_id
                self.new_line_start = [self.cur_block.start_pos[0] + self.cur_block.width / 2,
                                       self.cur_block.start_pos[1] + 70]
                self.c_bg.tag_bind("background", "<Motion>", new_line.update_new_line)
                new_line.new_line = self.c_bg.create_line(self.new_line_start[0], self.new_line_start[1], event.x,
                                                          event.y,
                                                          fill=COL_2, width=3)
            elif new_line.new_line_state == 1:
                if self.new_line_id != self.cur_block.primary_id and self.cur_block.primary_id not in self.blocks[
                    self.new_line_id - 1].foreign_ids:
                    self.c_bg.delete(new_line.new_line)
                    self.blocks[self.new_line_id - 1].foreign_ids.append(self.cur_block.primary_id)
                    self.blocks_to_file()
                    self.create_blocks()
                    new_line.new_line_on = False
                    new_line.configure(fg_color=COL_2, text="New line")
                    self.c_bg.tag_unbind("background", "<Motion>")
                    new_line.new_line_state = 0
                    for block in self.blocks:
                        self.c_bg.tag_bind(block.tag, "<B1-Motion>", self.block_move)
                    self.create_lines()

    def block_move(self, event):
        """
        Binds left button movement to block.

        Updates position of block and lines

        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        self.c_bg.coords(self.cur_block.widget_id[0], event.x - self.cur_block.width / 2, event.y - 35,
                         event.x + self.cur_block.width / 2, event.y + 35)
        self.c_bg.coords(self.cur_block.widget_id[1], event.x, event.y)

        self.cur_block.start_pos = [int(event.x - self.cur_block.width / 2), event.y - 35]
        self.cur_block.end_pos = [int(event.x - self.cur_block.width / 2), event.y - 35]

        self.create_lines()

    def block_unpress(self, *_):
        """
        Binds left button unpress to block

        Saves final block position to file

        Returns
        -------
        None
        """
        self.blocks_to_file()

    def blocks_from_file(self):
        """
        Gets blocks params from the file

        Returns
        -------
        None
        """
        if os.path.isfile("data/strategy.txt"):
            with open("data/strategy.txt", "r", encoding="utf-8") as f:
                lines = f.readlines()
                if len(lines) != 0:
                    for i in range(0, len(lines), 5):
                        if lines[i] != "":
                            block = Block(lines[i].strip(), lines[i + 1].strip(), lines[i + 2].strip(),
                                          [int(lines[i + 3].strip()), int(lines[i + 4].strip())])
                            self.blocks.append(block)

    def blocks_to_file(self):
        """
        Saves blocks params to the file

        Returns
        -------
        None
        """
        with open("data/strategy.txt", "w", encoding="utf-8") as file:
            for block in self.blocks:
                keys = str(block.primary_id) + ''.join([str(elem) for elem in block.foreign_ids])
                file.write(f"{keys}\n")
                file.write(f"{block.text}\n")
                file.write(f"{block.color}\n")
                file.write(f"{block.start_pos[0]}\n")
                file.write(f"{block.start_pos[1]}\n")


class ButtonNewBlock(CTkButton):
    """
    A class for New block button

    ...
    Attributes
    ----------
    master : CTkFrame
        connection to the background frame
    new_block_window_on : bool
        is the window on
    new_block_object : NewBlock
        object of NewBlock class

    Methods
    -------
    create_new_block():
        button command creates new block object if there is not and destroys if there is
    new_block_on_closing():
        on closing
    """
    def __init__(self, master):
        """
        Constructs button and necessary attributes

        Parameters
        ----------
        master : CTkFrame
            stores connection to the background frame
        """
        super().__init__(master, text="New block", fg_color=COL_2, font=("Arial", 30), command=self.create_new_block,
                         border_color="white", border_width=1)
        self.master = master

        self.new_block_window_on = False

        self.new_block_object = None

    def create_new_block(self):
        """
        button command creates new block object if there is not and destroys if there is

        Returns
        --------
        None
        """
        print(not self.new_block_window_on)
        if not self.new_block_window_on:
            self.new_block_object = NewBlock(self.master)
            self.new_block_object.wm_attributes("-topmost", True)
            self.new_block_window_on = True
            self.new_block_object.protocol("WM_DELETE_WINDOW", self.new_block_on_closing)
        else:
            self.new_block_window_on = False
            self.new_block_object.destroy()

    def new_block_on_closing(self):
        """
        launching on new_block_object closing

        Returns
        --------
        None
        """
        self.new_block_window_on = False
        self.new_block_object.destroy()


class ButtonDeleteBlock(CTkButton):
    """
    A class for Delete block button

    ...
    Attributes
    ----------
    delete_block_on : bool
        is the button selected
    c_bg : CTkCanvas
        background canvas
    blocks : Blocks
        access to blocks

    Methods
    -------
    change_delete_block():
        click or unclick delete block button

    """
    def __init__(self, master):
        """
        Constructs button and necessary attributes

        Parameters
        ----------
        master : CTkFrame
            stores connection to the background frame
        """
        super().__init__(master, text="Delete block", font=("Arial", 30), fg_color=COL_2,
                         border_color="white",
                         command=self.change_delete_block, border_width=1)
        self.delete_block_on = False
        self.c_bg = master.c_bg
        self.blocks = master.blocks

    def change_delete_block(self):
        """
        click or unclick delete block button

        Returns
        --------
        None
        """
        self.delete_block_on = not self.delete_block_on
        if self.delete_block_on:

            self.configure(fg_color="red", text="cancel")
            for block in self.blocks.blocks:
                self.c_bg.tag_unbind(block.tag, "<B1-Motion>")
        else:
            self.configure(fg_color=COL_2, text="Delete")
            for block in self.blocks.blocks:
                self.c_bg.tag_bind(block.tag, "<B1-Motion>", self.blocks.block_move)


class ButtonNewLine(CTkButton):
    """
    A class for new line button

    ...
    Attributes
    ----------
    new_line_on : bool
        is the button selected
    c_bg : CTkCanvas
        background canvas
    blocks : strategy.Blocks
        access to blocks
    new_line_state : int
        defines current state of new line
        0 = nothing clicked
        1 = starting point clicked
    new_line : int
        widget of new line

    Methods
    -------
    change_new_line():


    """
    def __init__(self, master):
        """
        Constructs button and necessary attributes

        Parameters
        ----------
        master : CTkFrame
             stores connection to the background frame
        """
        super().__init__(master, text="New line", font=("Arial", 30), fg_color=COL_2,
                         border_color="white", command=self.change_new_line, border_width=1)
        self.new_line_on = False
        self.new_line_state = 0
        self.c_bg = master.c_bg
        self.blocks = master.blocks
        self.new_line = None

    def change_new_line(self):
        """
        click or unclick delete block button

        If new_line_state = 1 destroy new line
        Returns
        --------
        None
        """
        if self.new_line_state == 1:
            self.c_bg.delete(self.new_line)

        self.new_line_on = not self.new_line_on

        if self.new_line_on:
            self.configure(fg_color="red", text="cancel")
            for block in self.blocks.blocks:
                self.c_bg.tag_unbind(block.tag, "<B1-Motion>")
        else:
            self.configure(fg_color=COL_2, text="New line")
            self.c_bg.tag_unbind("background", "<Motion>")

            for block in self.blocks.blocks:
                self.c_bg.tag_bind(block.tag, "<B1-Motion>", self.blocks.block_move)

    def update_new_line(self, event):
        """
        binds cursor motion to the new line
        Parameters
        ----------
        event : tkinter.Event, default
            event handler param

        Returns
        -------
        None
        """
        if self.new_line_state == 1:
            self.c_bg.coords(self.new_line, self.blocks.new_line_start[0], self.blocks.new_line_start[1],
                             event.x, event.y)


class ButtonDeleteLine(CTkButton):
    """
    A class for delete line button

    ...
    Attributes
    ----------
    master : CTkFrame
        connection to the background frame
    delete_line_on : bool
        is the button clicked
    c_bg : CTkCanvas
        background canvas
    blocks : Blocks
        access to blocks

    Methods
    -------
    change_delete_block():
        click or unclick delete line button
    delete_line(line):
        delete given line
    """
    def __init__(self, master):
        """
        Constructs button and necessary attributes

        Parameters
        ----------
        master : CTkFrame
            stores connection to the background frame
        """
        super().__init__(master, text="Delete line", font=("Arial", 30), fg_color=COL_2, border_color="white",
                         command=self.change_delete_line, border_width=1)
        self.master = master
        self.delete_line_on = False
        self.c_bg = master.c_bg
        self.blocks = master.blocks


    def change_delete_line(self):
        """
        click or unclick delete block button

        Creates X buttons in the middle of the lines

        Returns
        --------
        None
        """
        self.delete_line_on = not self.delete_line_on
        if self.delete_line_on:
            self.delete_buttons = []
            self.configure(fg_color="red", text="cancel")

            for i in range(len(self.blocks.lines_middle)):
                b_delete = CTkButton(self.master, text="×", font=("Arial", 90), fg_color=COL_2,
                                     command=lambda x=i: self.delete_line(self.blocks.lines[x]))
                self.c_bg.create_window(int(self.blocks.lines_middle[i][0]), int(self.blocks.lines_middle[i][1]),
                                        window=b_delete,
                                        height=50, width=50)
                self.delete_buttons.append(b_delete)
        else:
            self.configure(fg_color=COL_2, text="Delete line")
            for b_delete in self.delete_buttons:
                b_delete.destroy()
                self.blocks.create_blocks()

    def delete_line(self, line):
        """
        deletes given line and destroys buttons

        Parameters
        ----------
        line : int (widget_id)
            constains line to delete
        Returns
        --------
        None
        """
        self.c_bg.delete(line[0])
        for block in self.blocks.blocks:
            for key in block.foreign_ids:
                if key == line[1]:
                    block.foreign_ids.remove(key)
                    self.blocks.blocks_to_file()
        for b_delete in self.delete_buttons:
            b_delete.destroy()
            self.blocks.create_blocks()
        self.configure(fg_color=COL_2, text="Delete line")
        self.delete_line_on = False


class NewBlock(CTkToplevel):
    """
    A class to build new block creator

    ...
    Attributes
    ----------
    root : CTkFrame
        access to the background frame
    blocks : Blocks
        access to blocks object
    color : str
        hex color from color picker

    Methods
    -------
    create_new_block_window()
        displays new block creator
    ask_color()
        new color button command
    quit_window()
        command for cancel button
    accept()
        command for accept button
    """
    def __init__(self, root):
        """
        Constructs attributes for NewBlock object

        parameters
        ----------
        root : CTkFrame
            access to the background frame
        """
        super().__init__()
        self.root = root
        self.blocks = root.blocks
        self.color = None

        self.create_new_block_window()

    def create_new_block_window(self):
        """
        Creates new block creator

        Returns
        -------
        None
        """
        self.resizable(False, False)
        self.geometry('%dx%d+%d+%d' % (500, 300, 450, 930))

        self.title("New block")

        head = CTkCanvas(self, width=500, height=70, bg=COL_1, highlightthickness=0)
        head.create_text(250, 25, text="Create new block", font=FONT, fill=COL_FONT)
        head.create_line(50, 55, 450, 55, fill=COL_2, width=5)
        head.grid(row=0, column=0, columnspan=2)

        self.b_color_picker = CTkButton(self, text="Set Color", fg_color=COL_2, font=("Arial", 30), border_width=5,
                                        border_color=COL_2, command=self.ask_color)
        self.b_color_picker.grid(row=1, column=0, columnspan=2)

        l_info = CTkLabel(self, text="Name category:", font=FONT, text_color=COL_FONT)
        l_info.grid(row=2, column=0, columnspan=2)
        self.e_name = CTkEntry(self, width=400, font=FONT_TEXT)
        self.e_name.grid(row=3, column=0, columnspan=2, pady=10)
        b_cancel = CTkButton(self, text="Cancel", font=FONT, fg_color=COL_2, hover_color="red", border_color=COL_2,
                                  border_width=5, command=self.quit_window)
        b_cancel.grid(row=4, column=0)
        b_accept = CTkButton(self, text="Next", font=FONT, fg_color=COL_2, hover_color="green", border_color=COL_2,
                                  border_width=5, command=self.accept)
        b_accept.grid(row=4, column=1)

    def ask_color(self):
        """
        choose color of the block

        Returns
        -------
        None
        """
        pick_color = AskColor()
        self.color = pick_color.get()
        if self.color is not None:
            self.b_color_picker.configure(border_color=self.color)

    def quit_window(self):
        """
        quits creator

        Returns
        -------
        None
        """
        self.root.b_new_block.new_block_window_on = False
        self.destroy()

    def accept(self):
        """
        accepts input

        If something is not entered by user, there is popup
        Returns
        -------
        None
        """
        message = ""
        value = self.e_name.get()
        if value == "" and self.color is None:
            message = "Enter name and set color!"
        elif value == "":
            message = "Enter category!"
        elif self.color is None:
            message = "Set color!"

        if message != "":
            CTkMessagebox(title="Error", message=message)
        else:
            if len(self.blocks.blocks) == 0:
                new_block = Block(str(1), value, self.color, [1030, 780])
            else:
                new_block = Block(str(self.blocks.blocks[-1].primary_id + 1), value, self.color, [1030, 780])
            self.blocks.blocks.append(new_block)
            self.blocks.blocks_to_file()
            self.blocks.create_blocks()
            self.root.b_new_block.new_block_on_closing()

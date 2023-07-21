from CTkMessagebox import CTkMessagebox
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
        self.widget_id = []
        self.tag = None
        self.width = (FONT_BOX2.getbbox(self.text)[2] * 1.5)


class Strategy:
    def __init__(self, root):
        self.app = root
        self.new_line_state = 0

        # bg
        self.move_diff = None
        self.delete_block_on = False
        self.new_line_on = False
        self.delete_line_on = False

        #blocks
        self.blocks = []
        self.new_block_object = None
        self.new_block_window_on = False

        #lines
        self.lines = []

        # both
        self.first = 0
        self.even = 0

    def create_strategy_window(self):
        self.blocks_from_file()
        self.app.create_c_main()

        self.app.page = 4
        self.new_line_state = 0

        self.new_block_window_on = False
        self.delete_block_on = False
        self.new_line_on = False
        self.delete_line_on = False

        self.app.c_main.create_text(1080, 60, text="Life Strategy", font=FONT, fill=COL_FONT)
        self.app.c_main.create_line(870, 100, 1290, 100, fill=COL_2, width=8)
        self.frame = CTkFrame(master=self.app, width=2060, height=1170)
        self.frame.grid(row=0, column=1)

        self.c_bg = CTkCanvas(self.frame, width=2060, height=1170, bg=COL_1)
        self.c_bg.grid(row=0, column=0)
        self.c_bg.create_rectangle(0, 0, 2060, 1170, fill=COL_1, tags="background")

        self.b_new_block = CTkButton(self.frame, text="New block", font=("Arial", 30), fg_color=COL_2,
                                     command=self.new_block,
                                     border_color="white", border_width=1)
        self.c_bg.create_window(102, 1142, window=self.b_new_block, height=60, width=200)
        self.b_delete_block = CTkButton(self.frame, text="Delete block", font=("Arial", 30), fg_color=COL_2,
                                        border_color="white",
                                        command=self.change_delete_block, border_width=1)
        self.c_bg.create_window(302, 1142, window=self.b_delete_block, height=60, width=200)

        self.b_new_line = CTkButton(self.frame, text="New line", font=("Arial", 30), fg_color=COL_2,
                                    border_color="white",
                                    command=self.change_new_line, border_width=1)
        self.c_bg.create_window(502, 1142, window=self.b_new_line, height=60, width=200)
        self.b_delete_line = CTkButton(self.frame, text="Delete line", font=("Arial", 30), fg_color=COL_2,
                                       border_color="white",
                                       command=self.change_delete_line, border_width=1)
        self.c_bg.create_window(702, 1142, window=self.b_delete_line, height=60, width=200)

        self.c_bg.tag_bind("background", "<Button-1>", self.bg_press)
        self.c_bg.tag_bind("background", "<B1-Motion>", self.bg_move)
        self.c_bg.tag_bind("background", "<ButtonRelease-1>", self.bg_unpress)

        tag_nr = 0
        for block in self.blocks:
            block_id = self.c_bg.create_rectangle(block.start_pos[0], block.start_pos[1],
                                                  block.start_pos[0] + block.width,
                                                  block.start_pos[1] + 70, fill=block.color, tags=f"block{tag_nr}",
                                                  outline=COL_2,
                                                  width=3)
            text_id = self.c_bg.create_text(block.start_pos[0] + int(block.width / 2), block.start_pos[1] + 35,
                                            text=block.text, font=FONT, tags=f"block{tag_nr}")
            print("block id type", type(block_id))
            block.widget_id = [block_id, text_id]
            block.tag = f"block{tag_nr}"


            if tag_nr == 0:
                self.first = int(block_id / 2)
                self.even = text_id % 2

            self.c_bg.tag_bind(f"block{tag_nr}", "<Button-1>", self.block_press)
            self.c_bg.tag_bind(f"block{tag_nr}", "<B1-Motion>", self.block_move)
            self.c_bg.tag_bind(f"block{tag_nr}", "<ButtonRelease-1>", self.block_unpress)
            tag_nr += 1

        self._create_lines()

    def _create_lines(self):
        for line in self.lines:
            self.c_bg.delete(line[0])
        self.lines = []
        self.line_positions = []
        for block in self.blocks:

            for key in block.foreign_ids:
                foreign_block = self.blocks[key - 1]
                line = self.c_bg.create_line(block.start_pos[0] + block.width / 2, block.start_pos[1] + 70,
                                             foreign_block.start_pos[0] + foreign_block.width / 2,
                                             foreign_block.start_pos[1],
                                             fill=COL_2, width=3)
                self.lines.append([line, key])
                self.line_positions.append(
                    [(block.start_pos[0] + block.width / 2 + foreign_block.start_pos[0] + foreign_block.width / 2) / 2,
                     (block.start_pos[1] + 70 + foreign_block.start_pos[1]) / 2])

    def new_block(self):
        if not self.new_block_window_on or not self.new_block_object.new_block_on:
            self.new_block_object = New_block(self)
            self.new_block_object.wm_attributes("-topmost", True)
            self.new_block_window_on = True
            self.new_block_object.protocol("WM_DELETE_WINDOW", self.new_block_on_closing)
        else:
            self.new_block_window_on = False
            self.new_block_object.destroy()

    def new_block_on_closing(self):
        self.new_block_window_on = False
        self.new_block_object.destroy()

    def change_delete_block(self):
        self.delete_block_on = not self.delete_block_on
        if self.delete_block_on:

            self.b_delete_block.configure(fg_color="red", text="cancel")
            for block in self.blocks:
                self.c_bg.tag_unbind(block.tag, "<B1-Motion>")
        else:
            self.b_delete_block.configure(fg_color=COL_2, text="Delete")
            for block in self.blocks:
                self.c_bg.tag_bind(block.tag, "<B1-Motion>", self.block_move)

    def change_new_line(self):
        if self.new_line_state == 1:
            self.c_bg.delete(self.dynamic_line)

        self.new_line_on = not self.new_line_on

        if self.new_line_on:
            self.b_new_line.configure(fg_color="red", text="cancel")
            for block in self.blocks:
                self.c_bg.tag_unbind(block.tag, "<B1-Motion>")
        else:
            self.b_new_line.configure(fg_color=COL_2, text="New line")
            self.c_bg.tag_unbind("background", "<Motion>")

            for block in self.blocks:
                self.c_bg.tag_bind(block.tag, "<B1-Motion>", self.block_move)

    def change_delete_line(self):
        self.delete_line_on = not self.delete_line_on
        if self.delete_line_on:
            self.delete_buttons = []
            self.b_delete_line.configure(fg_color="red", text="cancel")

            for i in range(len(self.line_positions)):
                b_delete = CTkButton(self.frame, text="×", font=("Arial", 90), fg_color=COL_2,
                                     command=lambda x=i: self.delete_line(self.lines[x]))
                self.c_bg.create_window(int(self.line_positions[i][0]), int(self.line_positions[i][1]), window=b_delete,
                                        height=50, width=50)
                self.delete_buttons.append(b_delete)
        else:
            self.b_delete_line.configure(fg_color=COL_2, text="Delete line")
            for b_delete in self.delete_buttons:
                b_delete.destroy()
                self._create_lines()

    def delete_line(self, line):
        print(line)
        self.c_bg.delete(line[0])
        for block in self.blocks:
            print(block.foreign_ids)
            for key in block.foreign_ids:
                if key == line[1]:
                    block.foreign_ids.remove(key)
                    self.blocks_to_file()
        for b_delete in self.delete_buttons:
            b_delete.destroy()
            self._create_lines()
        self.b_delete_line.configure(fg_color=COL_2, text="Delete line")
        self.delete_line_on = False

    def bg_press(self, e):
        self.move_start = [e.x, e.y]

    def bg_move(self, e):
        self.move_diff = [e.x - self.move_start[0], e.y - self.move_start[1]]

        for block in self.blocks:
            block.start_pos = [block.end_pos[0] - self.move_diff[0], block.end_pos[1] - self.move_diff[1]]
            self.c_bg.coords(block.widget_id[0], block.start_pos[0], block.start_pos[1],
                             block.start_pos[0] + block.width, block.start_pos[1] + 70)
            self.c_bg.coords(block.widget_id[1], block.start_pos[0] + int(block.width / 2), block.start_pos[1] + 35)
        self._create_lines()

    def bg_unpress(self, e):
        for block in self.blocks:
            block.end_pos = [block.end_pos[0] - self.move_diff[0], block.end_pos[1] - self.move_diff[1]]

    def block_press(self, e):
        block_id = (e.widget.find_withtag("current")[0])

        if block_id % 2 == self.even:
            block_id -= 1
        block_id = int(block_id / 2 - self.first)
        self.cur_block = self.blocks[block_id]

        if self.delete_block_on:
            deleted_id = self.cur_block.primary_id
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
            self.create_strategy_window()

        elif self.new_line_on:
            if self.new_line_state == 0:
                self.new_line_state = 1
                self.new_line_id = self.cur_block.primary_id
                self.new_line_start = [self.cur_block.start_pos[0] + self.cur_block.width / 2,
                                       self.cur_block.start_pos[1] + 70]
                self.c_bg.tag_bind("background", "<Motion>", self.update_dynamic_line)
                self.dynamic_line = self.c_bg.create_line(self.new_line_start[0], self.new_line_start[1], e.x, e.y,
                                                          fill=COL_2, width=3)
            elif self.new_line_state == 1:
                if self.new_line_id != self.cur_block.primary_id and self.cur_block.primary_id not in self.blocks[
                    self.new_line_id - 1].foreign_ids:
                    self.c_bg.delete(self.dynamic_line)
                    self.blocks[self.new_line_id - 1].foreign_ids.append(self.cur_block.primary_id)
                    self.blocks_to_file()
                    self._create_lines()
                    self.new_line_on = False
                    self.b_new_line.configure(fg_color=COL_2, text="New line")
                    self.c_bg.tag_unbind("background", "<Motion>")
                    self.new_line_state = 0
                    for block in self.blocks:
                        self.c_bg.tag_bind(block.tag, "<B1-Motion>", self.block_move)

    def update_dynamic_line(self, e):
        if self.new_line_state == 1:
            self.c_bg.coords(self.dynamic_line, self.new_line_start[0], self.new_line_start[1], e.x, e.y)

    def block_move(self, e):
        self.c_bg.coords(self.cur_block.widget_id[0], e.x - self.cur_block.width / 2, e.y - 35,
                         e.x + self.cur_block.width / 2, e.y + 35)
        self.c_bg.coords(self.cur_block.widget_id[1], e.x, e.y)

        self.cur_block.start_pos = [int(e.x - self.cur_block.width / 2), e.y - 35]
        self.cur_block.end_pos = [int(e.x - self.cur_block.width / 2), e.y - 35]

        self._create_lines()

    def block_unpress(self, e):
        self.blocks_to_file()

    def blocks_from_file(self):
        if os.path.isfile("data/strategy.txt"):
            with open("data/strategy.txt", "r") as f:
                lines = f.readlines()
                if len(lines) != 0:
                    for i in range(0, len(lines), 5):
                        if lines[i] != "":
                            block = Block(lines[i].strip(), lines[i + 1].strip(), lines[i + 2].strip(),
                                          [int(lines[i + 3].strip()), int(lines[i + 4].strip())])
                            self.blocks.append(block)

    def blocks_to_file(self):
        with open("data/strategy.txt", "w") as file:
            for block in self.blocks:
                keys = str(block.primary_id) + ''.join([str(elem) for elem in block.foreign_ids])
                file.write('%s\n' % keys)
                file.write('%s\n' % block.text)
                file.write('%s\n' % block.color)
                file.write('%s\n' % block.start_pos[0])
                file.write('%s\n' % block.start_pos[1])


class New_block(CTkToplevel):
    def __init__(self, root):
        super().__init__()
        self.new_block_on = True
        self.main = root

        self.create_new_block_window()

    def create_new_block_window(self):
        self.resizable(False, False)
        self.geometry('%dx%d+%d+%d' % (500, 300, 450, 930))
        self.title("New block")

        self.color = None

        self.head = CTkCanvas(self, width=500, height=70, bg=COL_1, highlightthickness=0)
        self.header = self.head.create_text(250, 25, text="Create new block", font=FONT, fill=COL_FONT)
        self.head.create_line(50, 55, 450, 55, fill=COL_2, width=5)
        self.head.grid(row=0, column=0, columnspan=2)

        self.b_color_picker = CTkButton(self, text="Set Color", fg_color=COL_2, font=("Arial", 30), border_width=5,
                                        border_color=COL_2, command=self.ask_color)
        self.b_color_picker.grid(row=1, column=0, columnspan=2)

        self.l_info = CTkLabel(self, text="Name category:", font=FONT, text_color=COL_FONT)
        self.l_info.grid(row=2, column=0, columnspan=2)
        self.e_name = CTkEntry(self, width=400, font=FONT_TEXT)
        self.e_name.grid(row=3, column=0, columnspan=2, pady=10)
        self.b_cancel = CTkButton(self, text="Cancel", font=FONT, fg_color=COL_2, hover_color="red", border_color=COL_2,
                                  border_width=5, command=self.quit_clock)
        self.b_cancel.grid(row=4, column=0)
        self.b_accept = CTkButton(self, text="Next", font=FONT, fg_color=COL_2, hover_color="green", border_color=COL_2,
                                  border_width=5, command=self.accept)
        self.b_accept.grid(row=4, column=1)

    def ask_color(self):
        pick_color = AskColor()
        self.color = pick_color.get()
        if self.color is not None:
            self.b_color_picker.configure(border_color=self.color)

    def quit_clock(self):
        self.is_clock_on = False
        self.destroy()

    def accept(self):
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
            if len(self.main.blocks) == 0:
                new_block = Block(str(1), value, self.color, [1030, 780])
            else:
                new_block = Block(str(self.main.blocks[-1].primary_id + 1), value, self.color, [1030, 780])
            self.main.blocks.append(new_block)
            self.main.blocks_to_file()
            self.main.create_strategy_window()
            self.main.new_block_on_closing()

from customtkinter import *
from Data import Date
from actions import *
from clock import Clock
from settings import *
from settings import Settings


class Setup2:
    """Creating timeline setup
    rc = recently created
    tl = timeline"""

    def __init__(self, root):
        self.settings = Settings()
        self.app = root
        self.today_data = Date()
        self.tag_id = 0

        self.clock_window = None
        self.is_clock_window_on = False
        self.new_block = None

        self.startx = [75, 825]
        self.width = [3, 5]
        self.blocks = [[], []]
        self.binds = [[self.rc_move, self.rc_press, self.rc_unpress],
                      [self.saved_move, self.saved_press, self.saved_unpress]]
        self.blocks_files = ["blocks.txt", "saved_blocks.txt"]
        self.file_length = [45, 225]

        self.change = 0
        self.current_position = 100
        self.create_mode = 0

        self.tl_blocks = None

    def create_setup2_window(self):
        self.app.page = 2

        self.app.create_c_main()
        self.app.c_main.create_text(1080, 60, text="Create focus timeline", font=self.settings.font, fill=self.settings.font_color)

        self.app.c_main.create_line(870, 100, 1290, 100, fill=self.settings.second_color, width=8)
        self.app.c_main.create_rectangle(50, 150, 2110, 1000, outline=self.settings.second_color, width=5)
        self.app.c_main.create_line(800, 150, 800, 1000, fill=self.settings.second_color, width=5)
        self.b_submit = CTkButton(self.app, text="Submit", font=self.settings.font, fg_color=self.settings.second_color,
                                  hover_color=self.settings.main_color, border_color=self.settings.second_color,
                                  border_width=5,
                                  command=self.app.main.create_main_window)
        self.app.c_main.create_window(2035, 1295, window=self.b_submit, width=150, height=50)

        # Recently created panel
        self.app.c_main.create_text(425, 175, font=("Arial", 30), fill=self.settings.font_color,
                                    text="Recently created")
        self.b_rc_create = CTkButton(self.app, text="+", font=("Arial", 70), fg_color=self.settings.main_color,
                                     command=self.rc_add)
        self.app.c_main.create_window(80, 970, window=self.b_rc_create, height=50, width=50)
        self.rc_show()
        # saved panel
        self.saved_add_bg = self.app.c_main.create_rectangle(800, 150, 2110, 1000, fill=self.settings.main_color,
                                                             outline=self.settings.second_color, width=5)
        self.app.c_main.create_text(1455, 175, font=("Arial", 30), fill=self.settings.font_color, text="Saved")
        self.saved_add_text = self.app.c_main.create_text(1455, 975, font=("Arial", 30), fill=self.settings.font_color,
                                                          state="hidden",
                                                          text="Drop here to save")
        self.saved_trash = self.app.c_main.create_image(835, 960, image=create_imagetk("images/blocks/trash.png"),
                                                        state="hidden")
        self.saved_show()
        # Timeline panel
        self.tl_add_bg = self.app.c_main.create_rectangle(50, 1120, 2060, 1220, fill=self.settings.main_color, width=0)
        self.tl_add_text = self.app.c_main.create_text(1055, 1280, font=("Arial", 30), fill=self.settings.font_color,
                                                       state="hidden",
                                                       text="Add to the timeline")
        self._tl_bg_create()
        self.tl_show()
        self.tl_trash = self.app.c_main.create_image(2100, 1170, image=create_imagetk("images/blocks/trash.png"),
                                                     state="hidden")

    def rc_show(self):
        self.rc_params = []

        self.rc_from_file()
        self._blocks_create(self.rc_params)

    def rc_add(self):
        if not self.is_clock_window_on or not self.clock_window.is_clock_on:
            self.clock_window = Clock(self)
            self.clock_window.wm_attributes("-topmost", True)
            self.is_clock_window_on = True
            self.clock_window.protocol("WM_DELETE_WINDOW", self.clock_on_closing)

    def saved_show(self):
        self.saved_params = []

        self.saved_from_file()
        self._blocks_create(self.saved_params)

    def tl_show(self):
        self.tl_blocks = []
        self.tl_params = []
        self.current_pos = 0

        self.pointer = self.app.c_main.create_line(self.timeline_positions[self.current_pos], 1070,
                                                   self.timeline_positions[self.current_pos],
                                                   1270, fill="#155255", width=5, state="hidden")
        self.tl_from_file()
        for item in self.tl_params:
            self.tl_add_block(item[0], item[1], item[2])

    def tl_add_block(self, timer, col, text, is_move=1):
        timer = format_time(timer)
        tag = f"tl{self.tag_id}"
        self.tag_id += 1
        block = self.app.c_main.create_rectangle(self.timeline_positions[self.current_pos], 1120,
                                                 self.timeline_positions[self.current_pos] + 200,
                                                 1220, fill=col, outline=self.settings.second_color, width=5, tags=tag)

        block_time = self.app.c_main.create_text(self.timeline_positions[self.current_pos] + 100, 1170,
                                                 text=timer, font=self.settings.font, fill=self.settings.font_color, tags=tag)
        block_text = self.app.c_main.create_text(self.timeline_positions[self.current_pos] + 100, 1200,
                                                 text=text, font=("Arial", 15), fill=self.settings.font_color, tags=tag)

        if is_move:
            self.app.c_main.tag_bind(tag, "<B1-Motion>", self.tl_move)
            self.app.c_main.tag_bind(tag, "<Button-1>", self.tl_press)
            self.app.c_main.tag_bind(tag, "<ButtonRelease-1>", self.tl_unpress)

        self.tl_blocks.append([block, block_time, block_text])

        self.timeline_positions.append(self.timeline_positions[self.current_pos] + 200)
        self.current_pos += 1

    def _tl_bg_create(self):
        self.app.c_main.create_line(50, 1120, 2060, 1120, fill=self.settings.second_color, width=5)
        self.app.c_main.create_line(2010, 1090, 2060, 1120, fill=self.settings.second_color, width=5)
        self.app.c_main.create_line(2010, 1150, 2060, 1120, fill=self.settings.second_color, width=5)

        self.app.c_main.create_line(50, 1220, 2060, 1220, fill=self.settings.second_color, width=5)
        self.app.c_main.create_line(2010, 1190, 2060, 1220, fill=self.settings.second_color, width=5)
        self.app.c_main.create_line(2010, 1250, 2060, 1220, fill=self.settings.second_color, width=5)

    def _blocks_create(self, arr):
        self.blocks[self.create_mode] = []
        startx = self.startx[self.create_mode]
        starty = 225
        i = 0
        j = 0

        for block in arr:
            tag_block = f"block{self.tag_id}"
            self.tag_id += 1

            block_id = self.app.c_main.create_rectangle(startx + i * 250, starty + 150 * j, startx + 200 + i * 250,
                                                        starty + 100 + 150 * j, fill=block[1], tags=tag_block,
                                                        outline=self.settings.second_color,
                                                        width=5)

            timer = format_time(block[0])
            category = self.app.c_main.create_text(startx + 100 + i * 250, 275 + j * 150,
                                                   text=timer, font=self.settings.font, fill=self.settings.font_color, tags=tag_block)
            time = self.app.c_main.create_text(startx + 100 + i * 250, 305 + j * 150, text=block[2],
                                               fill=self.settings.font_color,
                                               font=("Arial", 15),
                                               tag=tag_block, anchor="center")
            i += 1
            if i % self.width[self.create_mode] == 0:
                j += 1
                i = 0

            self.app.c_main.tag_bind(tag_block, "<B1-Motion>", self.binds[self.create_mode][0])
            self.app.c_main.tag_bind(tag_block, "<Button-1>", self.binds[self.create_mode][1])
            self.app.c_main.tag_bind(tag_block, "<ButtonRelease-1>", self.binds[self.create_mode][2])

            self.blocks[self.create_mode].append([block_id, category, time])

        self.create_mode = not self.create_mode

    # binds

    # recent blocks binds
    def rc_press(self, e):
        self._press(e)
        self.app.c_main.itemconfigure(self.saved_add_bg, fill=self.settings.second_color)
        self.app.c_main.itemconfigure(self.saved_add_text, state='normal')

    def rc_move(self, e):
        self._move(e)
        if 800 < e.x < 2110 and 150 < e.y < 1000:
            self.app.c_main.itemconfigure(self.blocks[self.category][self.element][0], outline="green")
        else:
            self.app.c_main.itemconfigure(self.blocks[self.category][self.element][0],
                                          outline=self.settings.second_color)

    def rc_unpress(self, e):
        self._unpress(e)
        self.app.c_main.itemconfigure(self.saved_add_bg, fill=self.settings.main_color)
        self.app.c_main.itemconfigure(self.saved_add_text, state='hidden')
        if 800 < e.x < 2110 and 150 < e.y < 1000:
            self.app.c_main.itemconfigure(self.saved_add_bg, fill=self.settings.main_color)
            self.app.c_main.itemconfigure(self.saved_add_text, state='hidden')

            timer = self.app.c_main.itemcget(self.blocks[self.category][self.element][1], 'text')
            col = self.app.c_main.itemcget(self.blocks[self.category][self.element][0], 'fill')
            text = self.app.c_main.itemcget(self.blocks[self.category][self.element][2], 'text')

            timer = deformat_time(timer)

            self.new_block = [timer, col, text]

            self.category = 1
            self.to_file()
            self.create_setup2_window()
            self.new_block = None

    def saved_press(self, e):
        self._press(e)
        self.app.c_main.itemconfigure(self.saved_trash, state='normal')

    def saved_move(self, e):
        self._move(e)
        if 735 < e.x < 935 and 900 < e.y < 1020:
            self.app.c_main.itemconfigure(self.blocks[1][self.element][0], outline="red")
        else:
            self.app.c_main.itemconfigure(self.blocks[1][self.element][0], outline=self.settings.second_color)

    def saved_unpress(self, e):
        self._unpress(e)
        self.app.c_main.itemconfigure(self.saved_trash, state='hidden')
        if 735 < e.x < 935 and 900 < e.y < 1020:
            self._delete_saved()

    def tl_press(self, e):
        block = (e.widget.find_withtag("current")[0])
        self.element = calculate_element(block, self.tl_blocks)

        self.app.c_main.itemconfigure(self.pointer, state='normal')
        self.app.c_main.itemconfigure(self.tl_trash, state="normal")

    def tl_move(self, e):
        if 1090 < e.y < 1390:
            self._track(self.tl_blocks, e)
        if e.x > 2000:
            self.app.c_main.itemconfigure(self.tl_blocks[self.element][0], outline="red")
        else:
            self.app.c_main.itemconfigure(self.tl_blocks[self.element][0], outline=self.settings.second_color)

    def tl_unpress(self, e):
        self.app.c_main.itemconfigure(self.tl_trash, state="hidden")
        self.app.c_main.itemconfigure(self.pointer, state='hidden')
        self.app.c_main.itemconfigure(self.tl_blocks[self.element][0], outline=self.settings.second_color)

        self.app.c_main.coords(self.tl_blocks[self.element][0], self.timeline_positions[self.element], 1120,
                               self.timeline_positions[self.element] + 200, 1220)
        self.app.c_main.coords(self.tl_blocks[self.element][1], self.timeline_positions[self.element] + 100, 1170)
        self.app.c_main.coords(self.tl_blocks[self.element][2], self.timeline_positions[self.element] + 100, 1200)

        if self.element < self.change:
            self.change -= 1
        new_tl = self.tl_blocks[:]
        poped = new_tl.pop(self.element)
        new_tl.insert(self.change, poped)

        if self.element != self.change:
            self.restart()
        self._tl_shift(new_tl)

        if e.x > 2000:
            self.current_pos -= 1
            self.timeline_positions.pop(-1)
            self.app.c_main.delete(self.tl_blocks[-1][0])
            self.app.c_main.delete(self.tl_blocks[-1][1])
            self.app.c_main.delete(self.tl_blocks[-1][2])
            self.tl_blocks.pop(-1)
            new_tl.pop(-1)

        self.tl_to_file()

    # supportive functions for all binds
    def _press(self, e):
        block = (e.widget.find_withtag("current")[0])
        self.category, self.element = calculate_category(block, self.blocks)
        i = int(self.element % self.width[self.category])
        j = int(self.element // self.width[self.category])
        self.start_pos = [self.startx[self.category] + i * 250, 225 + 150 * j]

        self.app.c_main.itemconfigure(self.tl_add_bg, fill="#313131")
        self.app.c_main.itemconfigure(self.tl_add_text, state="normal")

    def _move(self, e):

        if 1090 < e.y < 1390:
            self._track(self.blocks[self.category], e)

        else:
            self.app.c_main.moveto(self.blocks[self.category][self.element][0], e.x - 100, e.y - 50)
            self.app.c_main.moveto(self.blocks[self.category][self.element][1], e.x - 50, e.y - 20)
            self.app.c_main.coords(self.blocks[self.category][self.element][2], e.x, e.y + 35)
            if self.pointer is not None:
                self.app.c_main.itemconfigure(self.pointer, state='hidden')

        self.app.c_main.tag_raise(self.blocks[self.category][self.element][0])
        self.app.c_main.tag_raise(self.blocks[self.category][self.element][1])
        self.app.c_main.tag_raise(self.blocks[self.category][self.element][2])

    def _unpress(self, e):

        if self.pointer is not None:
            self.app.c_main.itemconfigure(self.pointer, state='hidden')

        self.app.c_main.moveto(self.blocks[self.category][self.element][0], self.start_pos[0], self.start_pos[1])
        self.app.c_main.moveto(self.blocks[self.category][self.element][1], self.start_pos[0] + 50,
                               self.start_pos[1] + 30)
        self.app.c_main.coords(self.blocks[self.category][self.element][2], self.start_pos[0] + 100,
                               self.start_pos[1] + 85)

        if 1090 < e.y < 1390 and len(self.tl_blocks) < 9:
            col = self.app.c_main.itemcget(self.blocks[self.category][self.element][0], 'fill')
            timer = self.app.c_main.itemcget(self.blocks[self.category][self.element][1], 'text')
            text = self.app.c_main.itemcget(self.blocks[self.category][self.element][2], 'text')

            timer = deformat_time(timer)
            self.tl_add_block(timer, col, text)

            self.element = len(self.tl_blocks)

            new_tl = self.tl_blocks[:]
            poped = new_tl.pop(self.element - 1)
            new_tl.insert(self.change, poped)
            self._tl_shift(new_tl)

        if self.element != self.change:
            self.restart()
            self.tl_to_file()

        self.app.c_main.itemconfigure(self.tl_add_bg, fill=self.settings.main_color)
        self.app.c_main.itemconfigure(self.tl_add_text, state="hidden")

    def _delete_saved(self):
        self.saved_params.remove(self.saved_params[self.element])

        with open("data/saved_blocks.txt", "w") as file:
            for block in self.saved_params:
                for item in block:
                    file.write('%s\n' % item)
        self.create_setup2_window()

    def _tl_shift(self, arr):
        """changes order of blocks in timeline"""
        blocks = []

        for i in range(len(arr)):
            col = self.app.c_main.itemcget(arr[i][0], 'fill')
            text = self.app.c_main.itemcget(arr[i][1], 'text')
            time = self.app.c_main.itemcget(arr[i][2], 'text')

            blocks.append([col, text, time])

        for i in range(self.current_pos):
            self.app.c_main.itemconfigure(self.tl_blocks[i][0], fill=blocks[i][0])
            self.app.c_main.itemconfigure(self.tl_blocks[i][1], text=blocks[i][1])
            self.app.c_main.itemconfigure(self.tl_blocks[i][2], text=blocks[i][2])

    def _track(self, arr, e):
        self.app.c_main.itemconfigure(self.pointer, state='normal')
        self.app.c_main.moveto(arr[self.element][0], e.x - 100, 1117)
        self.app.c_main.moveto(arr[self.element][1], e.x - 50, 1150)
        self.app.c_main.coords(arr[self.element][2], e.x, 1200)

        self.get_change(e.x)

    # functions for files

    def rc_from_file(self):
        if os.path.isfile("data/blocks.txt"):
            with open("data/blocks.txt", "r") as file:
                lines = file.readlines()

                for i in range(0, len(lines), 3):
                    self.rc_params.append([lines[i].strip(), lines[i + 1].strip(), lines[i + 2].strip()])
        else:
            with open("data/blocks.txt", 'x'):
                pass

    def to_file(self):
        with open(f"data/{self.blocks_files[self.category]}", "r+") as file:
            lines = file.readlines()
        if len(self.new_block) == 3:
            if len(lines) < self.file_length[self.category]:
                for item in lines[:len(lines)]:
                    self.new_block.append(item.strip())
            else:
                for item in lines[:self.file_length[self.category] - 3]:
                    self.new_block.append(item.strip())

            with open(f"data/{self.blocks_files[self.category]}", 'w+') as file:
                for element in self.new_block:
                    file.write('%s\n' % element)

    # saved
    def saved_from_file(self):
        if os.path.isfile("data/saved_blocks.txt"):
            with open("data/saved_blocks.txt", "r") as file:
                lines = file.readlines()
                for i in range(0, len(lines), 3):
                    self.saved_params.append([lines[i].strip(), lines[i + 1].strip(), lines[i + 2].strip()])

        else:
            with open("data/saved_blocks.txt", 'x'):
                pass

    # timeline
    def tl_from_file(self):
        if os.path.isfile("data/tl_blocks.txt"):
            with open("data/tl_blocks.txt", 'r') as file:
                lines = file.readlines()

                if len(lines) != 0:

                    if str(self.today_data.formatted_date) == lines[0][:-1]:

                        for i in range(1, len(lines), 3):
                            self.tl_params.append([lines[i].strip(), lines[i + 1].strip(), lines[i + 2].strip()])
        else:
            with open("data/tl_blocks.txt", 'x'):
                pass

    def tl_to_file(self):
        with open("data/tl_blocks.txt", "w") as file:
            file.write(f"{self.today_data.formatted_date}\n")
            for i in range(self.current_pos):
                file.write('%s\n' % deformat_time(self.app.c_main.itemcget(self.tl_blocks[i][1], 'text')))
                file.write('%s\n' % self.app.c_main.itemcget(self.tl_blocks[i][0], 'fill'))
                file.write('%s\n' % self.app.c_main.itemcget(self.tl_blocks[i][2], 'text'))

    # other
    def get_change(self, x):
        i = 0
        for pos in self.timeline_positions:
            if x - 100 <= pos < x + 100:
                self.app.c_main.coords(self.pointer, self.timeline_positions[i], 1070,
                                       self.timeline_positions[i],
                                       1270)
                self.change = i
                break

            i += 1

    def clock_on_closing(self):
        self.category = 0
        if self.new_block is not None:
            self.to_file()
            self.create_setup2_window()
        self.clock_window.destroy()
        self.is_clock_window_on = False

    # methods for main window

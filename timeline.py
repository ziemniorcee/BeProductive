from customtkinter import *
from Data import Date
from actions import *
from clock import Clock
from settings import *
from settings import Settings
from dataclasses import dataclass


class TimelineWidget(CTkFrame):
    def __init__(self, master):
        self.settings = Settings()
        super().__init__(master, width=2060, height=270)
        self.app = master
        self.today_data = Date()
        self.blocks = self.from_file()

        self.c_timeline = CTkCanvas(self, width=2060, height=160, bg=self.settings.main_color, highlightthickness=0)
        self.c_timeline.grid(row=0, column=0)
        self.create_timeline()

        timers = [int(item[0]) for item in self.blocks]
        self.c_timer = Timer(self, timers)
        self.c_timer.grid(row=1, column=0)

    def create_timeline(self):
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
        parameters = []
        if os.path.isfile("data/tl_blocks.txt"):
            with open("data/tl_blocks.txt", 'r') as file:
                lines = file.readlines()
                if len(lines) != 0:
                    if str(self.today_data.formatted_date) == lines[0][:-1]:
                        for i in range(1, len(lines), 3):
                            parameters.append([lines[i].strip(), lines[i + 1].strip(), lines[i + 2].strip()])
        else:
            with open("data/tl_blocks.txt", 'x'):
                pass
        return parameters

class Timer(CTkCanvas):
    def __init__(self, master, timers):
        self.settings = Settings()
        super().__init__(master, width=2060, height=110, bg=self.settings.main_color, highlightthickness=0)

        self.timers = timers
        self.master = master
        self.timer = "0:00"
        self.current_position = 100
        self.current_pos = 0
        self.current = None
        self.current_line_len = 555
        self.current_time = 0

        self.current_speed = None
        self.line_speed = None
        self.current_block = 0

        self.pause_on = False
        self.time = None

        self.create_timer()

    def create_timer(self):
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

        self.time_current = self.create_text(500, 80, text=f"{self.timer}", font=("Arial", 20),
                                             fill=self.settings.font_color)
        self.block_len = self.create_text(1610, 80, text="0:00", font=("Arial", 20),
                                          fill=self.settings.font_color)

        self.current = self.master.c_timeline.create_line(100, 0, 100, 160, fill=self.settings.font_color, width=5)

        self.create_line(555, 80, 1555, 80, fill=self.settings.second_color, width=6)
        self.line_length = self.create_line(555, 80, 555, 80, fill=self.settings.font_color, width=8)

        if len(self.timers) > 0:
            self.time = self.timers[0]
            self.itemconfigure(self.block_len, text=f"{self.time}:00")
            self.pause_on = False

    def start_stop_timer(self):
        self.pause_on = not self.pause_on
        self.play_pause.configure(command=None)
        self.master.app.after(500, lambda: self.play_pause.configure(command=self.start_stop_timer))

        if self.pause_on:
            self._change_img("pause")
            self.time = self.timers[self.current_block]
            self.current_speed = 200 / (self.time * 60)
            self.line_speed = 1000 / (self.time * 60)

            if self.current_time == 0:
                self.count_down(0)
            else:
                self.count_down(self.current_time)

    def count_down(self, count):
        if count <= self.time * 60 and self.pause_on:
            self.timer = f"{int(count / 60)}:{count % 60 if count % 60 > 9 else f'0{count % 60}'}"
            if self.master.app.page == 0:
                self.itemconfigure(self.time_current, text=self.timer)
                self.master.c_timeline.coords(self.current, self.current_position, 0, self.current_position, 160)
                self.coords(self.line_length, 555, 80, self.current_line_len, 80)

            self.current_time = count + 1
            self.master.app.after(1000, self.count_down, count + 1)
            self.current_position += self.current_speed
            self.current_line_len += self.line_speed
        elif not count < self.time * 60:
            self.next_block()
        else:
            self._change_img("play")

    def next_block(self):
        self.play_pause.configure(command=None)
        self.master.app.after(500, lambda: self.play_pause.configure(command=self.start_stop_timer))
        if len(self.timers) - 1 > self.current_block:
            self.current_block += 1
            self.reset()

    def prev_block(self):
        self.play_pause.configure(command=None)
        self.master.app.after(500, lambda: self.play_pause.configure(command=self.start_stop_timer))
        if self.current_block > 0 and self.current_time == 0:
            self.current_block -= 1
        self.reset()

    def restart(self):
        self.current_block = 0
        self._value_reset()

    def reset(self):
        self._value_reset()
        self.itemconfigure(self.block_len, text=f"{self.timers[self.current_block]}:00")
        self.itemconfigure(self.time_current, text=f"0:00")
        self.coords(self.line_length, 555, 1400, 555, 1400)
        self.master.c_timeline.coords(self.current, self.current_position, 0, self.current_position, 160)

    def _change_img(self, file):
        img = CTkImage(light_image=Image.open(f"images/timeline/{file}.png"), size=(50, 50))
        self.play_pause.configure(image=img)

    def _value_reset(self):
        self.pause_on = False
        self.current_position = 100 + self.current_block * 200
        self._change_img("play")
        self.current_time = 0
        self.current_line_len = 555


class TimelineWindow:
    def __init__(self, root):
        self.settings = Settings()
        self.app = root

        self.tl_blocks = None

    def create_window(self):
        self.app.page = 2
        self.app.create_c_main()

        self.app.c_main.create_text(1080, 60, text="Create focus timeline", font=self.settings.font,
                                    fill=self.settings.font_color)
        self.app.c_main.create_line(870, 100, 1290, 100, fill=self.settings.second_color, width=8)
        self.app.c_main.create_rectangle(50, 150, 2110, 1000, outline=self.settings.second_color, width=5)
        self.app.c_main.create_line(800, 150, 800, 1000, fill=self.settings.second_color, width=5)

        self.b_submit = CTkButton(self.app, text="Submit", font=self.settings.font, fg_color=self.settings.second_color,
                                  hover_color=self.settings.main_color, border_color=self.settings.second_color,
                                  border_width=5, command=self.app.main.create_main_window)
        self.app.c_main.create_window(2035, 1295, window=self.b_submit, width=150, height=50)


        self.pointer = self.app.c_main.create_line(100, 1070, 100, 1270, fill="#155255", width=5, state="hidden")
        self.tl_add_bg = self.app.c_main.create_rectangle(50, 1120, 2060, 1220, fill=self.settings.main_color, width=0)

        self.tl_blocks = TimelineBlocks(self.app)
        self.rc_blocks = RecentlyBlocks(self.app)
        self.saved_blocks = SavedBlocks(self.app)

        self.app.c_main.tag_raise(self.pointer)


@dataclass(frozen=False)
class Block:
    color: str
    timer: str
    text: str
    element_ids: list[int]
    tag: str
    start_pos: list[int] = 0


class Blocks:
    def __init__(self, root, file_name, startx, width):
        self.app = root
        self.settings = Settings()
        self.params = self.from_file(file_name)
        self.timeline = self.app.timeline.tl_blocks
        self.blocks = []
        self.width = width
        self.startx = startx
        self.delete = 0


        self.selected_block = None
        self.timeline_positions = self.timeline.timeline_positions
        self.current_pos = 0
        self.change = 0


        self.tl_add_text = self.app.c_main.create_text(1055, 1280, font=("Arial", 30), fill=self.settings.font_color,
                                                       state="hidden", text="Add to the timeline")
        self.pointer = self.app.timeline.pointer
        self.pos_counter = [0, 0]

        for param in self.params:
            self.add_block(param)

    def add_block(self, param):
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

    def press(self, e):
        pressed_id = (e.widget.find_withtag("current")[0])
        for block in self.blocks:
            if pressed_id in block.element_ids:
                self.selected_block = block
                break

        self.app.c_main.itemconfigure(self.app.timeline.tl_add_bg, fill="#313131")
        self.app.c_main.itemconfigure(self.tl_add_text, state="normal")

    def move(self, e):
        if 1050 < e.y < 1300:

            self.app.c_main.itemconfigure(self.pointer, state='normal')
            self.app.c_main.moveto(self.selected_block.element_ids[0], e.x - 100, 1117)
            self.app.c_main.moveto(self.selected_block.element_ids[1], e.x - 50, 1150)
            self.app.c_main.coords(self.selected_block.element_ids[2], e.x, 1200)

            self.timeline.get_change(e.x)

        else:
            self.app.c_main.moveto(self.selected_block.element_ids[0], e.x - 100, e.y - 50)
            self.app.c_main.moveto(self.selected_block.element_ids[1], e.x - 50, e.y - 20)
            self.app.c_main.coords(self.selected_block.element_ids[2], e.x, e.y + 35)
            if self.pointer is not None:
                self.app.c_main.itemconfigure(self.pointer, state='hidden')

        self.app.c_main.tag_raise(self.selected_block.element_ids[0])
        self.app.c_main.tag_raise(self.selected_block.element_ids[1])
        self.app.c_main.tag_raise(self.selected_block.element_ids[2])

    def unpress(self, e):
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

        if 1050 < e.y < 1300 and len(self.timeline.blocks) < 9:
            self.timeline.add([self.selected_block.timer, self.selected_block.color, self.selected_block.text])

            element = len(self.timeline.blocks)
            new_pos = 100 + self.timeline.change * 200

            poped = self.timeline.blocks.pop(element - 1)
            self.timeline.blocks.insert(self.timeline.change, poped)

            self.timeline.shift(self.timeline.blocks[self.timeline.change:element + 1], new_pos)
            self.app.timeline.tl_blocks.to_file()

    def from_file(self, file_name):
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
        with open(f"data/{file_name}", "w+") as file:
            for block in self.blocks:
                file.write(f"{block.timer}\n{block.color}\n{block.text}\n")


class RecentlyBlocks(Blocks):
    def __init__(self, root):
        super().__init__(root, "rc_blocks.txt", 75, 3)
        self.app = root
        self.today_data = Date()

        self.app.c_main.create_text(425, 175, font=("Arial", 30), fill=self.settings.font_color,
                                    text="Recently created")
        self.saved_add_bg = self.app.c_main.create_rectangle(800, 150, 2110, 1000, fill=self.settings.main_color,
                                                             outline=self.settings.second_color, width=5)
        self.saved_add_text = self.app.c_main.create_text(1455, 975, font=("Arial", 30), fill=self.settings.font_color,
                                                          state="hidden", text="Drop here to save")
        self.b_rc_create = CTkButton(self.app, text="+", font=("Arial", 70), fg_color=self.settings.main_color,
                                     command=self.rc_add)
        self.app.c_main.create_window(80, 970, window=self.b_rc_create, height=50, width=50)

        self.clock_window = None
        self.is_clock_window_on = False
        self.new_block = None

        for block in self.blocks:
            self.bind(block.tag)

    def bind(self, tag):
        self.app.c_main.tag_bind(tag, "<Button-1>", self.rc_press)
        self.app.c_main.tag_bind(tag, "<B1-Motion>", self.rc_move)
        self.app.c_main.tag_bind(tag, "<ButtonRelease-1>", self.rc_unpress)

    def rc_press(self, e):
        self.press(e)
        self.app.c_main.itemconfigure(self.saved_add_bg, fill=self.settings.second_color)
        self.app.c_main.itemconfigure(self.saved_add_text, state='normal')

    def rc_move(self, e):
        self.move(e)
        if 800 < e.x < 2110 and 150 < e.y < 1000:
            self.app.c_main.itemconfigure(self.selected_block.element_ids[0], outline="green")
        else:
            self.app.c_main.itemconfigure(self.selected_block.element_ids[0], outline=self.settings.second_color)

    def rc_unpress(self, e):
        self.unpress(e)
        self.app.c_main.itemconfigure(self.saved_add_bg, fill=self.settings.main_color)
        self.app.c_main.itemconfigure(self.saved_add_text, state='hidden')

        if 800 < e.x < 2110 and 150 < e.y < 1000 and len(self.app.timeline.saved_blocks.blocks) < 25:
            self.app.c_main.itemconfigure(self.saved_add_bg, fill=self.settings.main_color)
            self.app.c_main.itemconfigure(self.saved_add_text, state='hidden')
            self.app.c_main.itemconfigure(self.selected_block.element_ids[0], outline=self.settings.second_color)
            params = [self.selected_block.timer, self.selected_block.color, self.selected_block.text]

            self.app.timeline.saved_blocks.add_block(params)
            self.app.timeline.saved_blocks.bind(self.app.timeline.saved_blocks.blocks[-1].tag)
            self.app.timeline.saved_blocks.to_file("saved_blocks.txt")

    def rc_add(self):
        if not self.is_clock_window_on or not self.clock_window.is_clock_on:
            self.clock_window = Clock(self)
            self.clock_window.wm_attributes("-topmost", True)
            self.is_clock_window_on = True
            self.clock_window.protocol("WM_DELETE_WINDOW", self.clock_on_closing)

    def clock_on_closing(self):
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
    def __init__(self, root):
        super().__init__(root, "saved_blocks.txt", 825, 5)
        self.app = root
        self.saved_trash = self.app.c_main.create_image(835, 960, image=create_imagetk("images/blocks/trash.png"),
                                                        state="hidden")
        self.app.c_main.create_text(1425, 175, font=("Arial", 30), fill=self.settings.font_color, text="Saved")
        for block in self.blocks:
            self.bind(block.tag)

    def bind(self, tag):
        self.app.c_main.tag_bind(tag, "<Button-1>", self.saved_press)
        self.app.c_main.tag_bind(tag, "<B1-Motion>", self.saved_move)
        self.app.c_main.tag_bind(tag, "<ButtonRelease-1>", self.saved_unpress)

    def saved_press(self, e):
        self.press(e)
        self.app.c_main.itemconfigure(self.saved_trash, state='normal')

    def saved_move(self, e):
        self.move(e)
        if 735 < e.x < 935 and 900 < e.y < 1020:
            self.app.c_main.itemconfigure(self.selected_block.element_ids[0], outline="red")
        else:
            self.app.c_main.itemconfigure(self.selected_block.element_ids[0], outline=self.settings.second_color)

    def saved_unpress(self, e):
        self.unpress(e)
        self.app.c_main.itemconfigure(self.saved_trash, state='hidden')
        if 735 < e.x < 935 and 900 < e.y < 1020:
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
    def __init__(self, root):
        self.settings = Settings()
        self.app = root
        self.today_data = Date()

        self.blocks = []
        self.timeline_positions = [100]
        self.current_pos = 0
        self.change = None
        self.selected_block = None

        self.pointer = self.app.timeline.pointer
        self.tag_ig = 0
        self.app.c_main.create_line(50, 1120, 2060, 1120, fill=self.settings.second_color, width=5)
        self.app.c_main.create_line(2010, 1090, 2060, 1120, fill=self.settings.second_color, width=5)
        self.app.c_main.create_line(2010, 1150, 2060, 1120, fill=self.settings.second_color, width=5)

        self.app.c_main.create_line(50, 1220, 2060, 1220, fill=self.settings.second_color, width=5)
        self.app.c_main.create_line(2010, 1190, 2060, 1220, fill=self.settings.second_color, width=5)
        self.app.c_main.create_line(2010, 1250, 2060, 1220, fill=self.settings.second_color, width=5)

        self.tl_trash = self.app.c_main.create_image(2100, 1170, image=create_imagetk("images/blocks/trash.png"),
                                                     state="hidden")
        self.params = self.from_file()
        for param in self.params:
            self.add(param)

    def add(self, param):
        tag_name = f"tl{self.tag_ig}"
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

    def tl_press(self, e):
        pressed_id = (e.widget.find_withtag("current")[0])
        for block in self.blocks:
            if pressed_id in block.element_ids:
                self.selected_block = block
                break

        self.app.c_main.tag_raise(self.selected_block.element_ids[0])
        self.app.c_main.tag_raise(self.selected_block.element_ids[1])
        self.app.c_main.tag_raise(self.selected_block.element_ids[2])

        self.app.c_main.itemconfigure(self.pointer, state='normal')
        self.app.c_main.itemconfigure(self.tl_trash, state="normal")

    def tl_move(self, e):
        if 1090 < e.y < 1390:
            self.app.c_main.itemconfigure(self.pointer, state='normal')
            self.app.c_main.moveto(self.selected_block.element_ids[0], e.x - 100, 1117)
            self.app.c_main.moveto(self.selected_block.element_ids[1], e.x - 50, 1150)
            self.app.c_main.coords(self.selected_block.element_ids[2], e.x, 1200)

            self.get_change(e.x)

        if e.x > 2000:
            self.app.c_main.itemconfigure(self.selected_block.element_ids[0], outline="red")
        else:
            self.app.c_main.itemconfigure(self.selected_block.element_ids[0], outline=self.settings.second_color)

    def tl_unpress(self, e):
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

        if e.x > 2000:
            self.current_pos -= 1
            self.timeline_positions.pop(-1)
            self.app.c_main.delete(self.selected_block.element_ids[0])
            self.app.c_main.delete(self.selected_block.element_ids[1])
            self.app.c_main.delete(self.selected_block.element_ids[2])
            self.blocks.pop(-1)

        self.to_file()

    def shift(self, arr, start):
        for item in arr:
            item.start_pos[0] = start
            self.app.c_main.coords(item.element_ids[0], start, 1120, start + 200, 1220)
            self.app.c_main.coords(item.element_ids[1], start + 100, 1170)
            self.app.c_main.coords(item.element_ids[2], start + 100, 1200)
            start += 200

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

    def from_file(self):
        parameters = []
        if os.path.isfile("data/tl_blocks.txt"):
            with open("data/tl_blocks.txt", 'r') as file:
                lines = file.readlines()
                if len(lines) != 0:
                    if str(self.today_data.formatted_date) == lines[0][:-1]:
                        for i in range(1, len(lines), 3):
                            parameters.append([lines[i].strip(), lines[i + 1].strip(), lines[i + 2].strip()])
        else:
            with open("data/tl_blocks.txt", 'x'):
                pass
        return parameters

    def to_file(self):
        with open("data/tl_blocks.txt", "w+") as file:
            file.write(f"{self.today_data.formatted_date}\n")
            for block in self.blocks:
                file.write(f"{block.timer}\n{block.color}\n{block.text}\n")
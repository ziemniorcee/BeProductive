from customtkinter import *
from Data import Date
from actions import *
from clock import Clock
from settings import *
from settings import Settings
from dataclasses import dataclass


class TimelineManagement:
    def __init__(self):
        self.today_data = Date()

    def from_file(self, file_name):
        parameters = []
        if os.path.isfile(f"data/{file_name}"):
            with open(f"data/{file_name}", 'r') as file:
                lines = file.readlines()
                if len(lines) != 0:

                    if file_name == "tl_blocks.txt":
                        if str(self.today_data.formatted_date) == lines[0][:-1]:
                            for i in range(1, len(lines), 3):
                                parameters.append([lines[i].strip(), lines[i + 1].strip(), lines[i + 2].strip()])
                    else:
                        for i in range(0, len(lines), 3):
                            parameters.append([lines[i].strip(), lines[i + 1].strip(), lines[i + 2].strip()])
        else:
            with open("data/tl_blocks.txt", 'x'):
                pass
        return parameters

    # def to_file(self, file_name, length):
    #     with open(f"data/{file_name}", "r+") as file:
    #         lines = file.readlines()
    #     if len(self.new_block) == 3:
    #         if len(lines) < length:
    #             for item in lines[:len(lines)]:
    #                 self.new_block.append(item.strip())
    #         else:
    #             for item in lines[:self.file_length[self.category] - 3]:
    #                 self.new_block.append(item.strip())
    #
    #         with open(f"data/{self.blocks_files[self.category]}", 'w+') as file:
    #             for element in self.new_block:
    #                 file.write('%s\n' % element)


class TimelineWidget(CTkFrame):
    def __init__(self, master):
        self.settings = Settings()
        super().__init__(master, width=2060, height=270)
        self.app = master

        self.management = TimelineManagement()
        self.blocks = self.management.from_file("tl_blocks.txt")

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

    def create_window(self):
        self.app.page = 2
        self.app.create_c_main()

        self.app.c_main.create_text(1080, 60, text="Create focus timeline", font=self.settings.font,
                                    fill=self.settings.font_color)
        self.app.c_main.create_line(870, 100, 1290, 100, fill=self.settings.second_color, width=8)
        self.app.c_main.create_rectangle(50, 150, 2110, 1000, outline=self.settings.second_color, width=5)
        self.app.c_main.create_line(800, 150, 800, 1000, fill=self.settings.second_color, width=5)

        self.pointer = self.app.c_main.create_line(100, 1070, 100, 1270, fill="#155255", width=5, state="hidden")

        self.rc_blocks = RecentlyBlocks(self.app)
        self.saved_blocks = SavedBlocks(self.app)
        self.tl_blocks = TimelineBlocks(self.app)

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
    def __init__(self, root, file_name):
        self.app = root
        self.settings = Settings()
        self.management = TimelineManagement()
        self.params = self.management.from_file(file_name)
        self.blocks = []

        self.selected_block = None
        self.timeline_positions = [100]
        self.current_pos = 0

        self.tl_add_bg = self.app.c_main.create_rectangle(50, 1120, 2060, 1220, fill=self.settings.main_color, width=0)
        self.tl_add_text = self.app.c_main.create_text(1055, 1280, font=("Arial", 30), fill=self.settings.font_color,
                                                       state="hidden", text="Add to the timeline")

        self.pointer = self.app.timeline.pointer

    def create(self, startx, width, length):
        i = 0
        j = 0
        for param in self.params:
            tag_name = f"b{width}_{j * 10 + i}"
            block_id = self.app.c_main.create_rectangle(startx + i * 250, 225 + 150 * j, startx + 200 + i * 250,
                                                        325 + 150 * j, fill=param[1], tags=tag_name,
                                                        outline=self.settings.second_color, width=5)

            timer = format_time(param[0])
            timer_id = self.app.c_main.create_text(startx + 100 + i * 250, 275 + j * 150,
                                                   text=timer, font=self.settings.font,
                                                   fill=self.settings.font_color, tags=tag_name)
            category_id = self.app.c_main.create_text(startx + 100 + i * 250, 305 + j * 150, text=param[2],
                                                      tag=tag_name, fill=self.settings.font_color, font=("Arial", 15),
                                                      anchor="center")
            self.blocks.append(Block(param[1], param[0], param[2], [block_id, timer_id, category_id], tag_name,
                                     [startx + i * 250, 225 + 150 * j]))
            i += 1
            if i % width == 0:
                j += 1
                i = 0

    def press(self, e):
        pressed_id = (e.widget.find_withtag("current")[0])
        for block in self.blocks:
            if pressed_id in block.element_ids:
                self.selected_block = block
                break
        self.app.c_main.itemconfigure(self.tl_add_bg, fill="#313131")
        self.app.c_main.itemconfigure(self.tl_add_text, state="normal")

    def move(self, e):
        if 1050 < e.y < 1300:

            self.app.c_main.itemconfigure(self.pointer, state='normal')
            self.app.c_main.moveto(self.selected_block.element_ids[0], e.x - 100, 1117)
            self.app.c_main.moveto(self.selected_block.element_ids[1], e.x - 50, 1150)
            self.app.c_main.coords(self.selected_block.element_ids[2], e.x, 1200)

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

        self.app.c_main.itemconfigure(self.tl_add_bg, fill=self.settings.main_color)
        self.app.c_main.itemconfigure(self.tl_add_text, state="hidden")

        self.app.c_main.moveto(self.selected_block.element_ids[0], self.selected_block.start_pos[0],
                               self.selected_block.start_pos[1])
        self.app.c_main.moveto(self.selected_block.element_ids[1], self.selected_block.start_pos[0] + 50,
                               self.selected_block.start_pos[1] + 30)
        self.app.c_main.coords(self.selected_block.element_ids[2], self.selected_block.start_pos[0] + 100,
                               self.selected_block.start_pos[1] + 85)

        # if 1090 < e.y < 1390 and len(self.tl_blocks) < 9:
        #     col = self.app.c_main.itemcget(self.blocks[self.category][self.element][0], 'fill')
        #     timer = self.app.c_main.itemcget(self.blocks[self.category][self.element][1], 'text')
        #     text = self.app.c_main.itemcget(self.blocks[self.category][self.element][2], 'text')
        #
        #     timer = deformat_time(timer)
        #     self.tl_add_block(timer, col, text)
        #
        #     self.element = len(self.tl_blocks)
        #
        #     new_tl = self.tl_blocks[:]
        #     poped = new_tl.pop(self.element - 1)
        #     new_tl.insert(self.change, poped)
        #     self._tl_shift(new_tl)
        #
        # if self.element != self.change:
        #     self.restart()
        #     self.tl_to_file()
        #


class RecentlyBlocks(Blocks):
    def __init__(self, root):
        super().__init__(root, "blocks.txt")
        self.app = root
        self.saved_add_bg = self.app.c_main.create_rectangle(800, 150, 2110, 1000, fill=self.settings.main_color,
                                                             outline=self.settings.second_color, width=5)
        self.saved_add_text = self.app.c_main.create_text(1455, 975, font=("Arial", 30), fill=self.settings.font_color,
                                                          state="hidden", text="Drop here to save")
        self.create(75, 3, 45)
        for block in self.blocks:
            self.app.c_main.tag_bind(block.tag, "<Button-1>", self.rc_press)
            self.app.c_main.tag_bind(block.tag, "<B1-Motion>", self.rc_move)
            self.app.c_main.tag_bind(block.tag, "<ButtonRelease-1>", self.rc_unpress)

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


class SavedBlocks(Blocks):
    def __init__(self, root):
        super().__init__(root, "saved_blocks.txt")
        self.app = root
        self.saved_trash = self.app.c_main.create_image(835, 960, image=create_imagetk("images/blocks/trash.png"),
                                                        state="hidden")

        self.create(startx=825, width=5, length=225)

        for block in self.blocks:
            self.app.c_main.tag_bind(block.tag, "<Button-1>", self.saved_press)
            self.app.c_main.tag_bind(block.tag, "<B1-Motion>", self.saved_move)
            self.app.c_main.tag_bind(block.tag, "<ButtonRelease-1>", self.saved_unpress)

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
        # if 735 < e.x < 935 and 900 < e.y < 1020:
        #     self._delete_saved()


class TimelineBlocks:
    def __init__(self, root):
        self.settings = Settings()
        self.app = root
        self.management = TimelineManagement()
        self.params = self.management.from_file("tl_blocks.txt")
        self.blocks = []
        self.timeline_positions = [100]
        self.current_pos = 0
        self.selected_block = None

        self.pointer = self.app.timeline.pointer

        self.app.c_main.create_line(50, 1120, 2060, 1120, fill=self.settings.second_color, width=5)
        self.app.c_main.create_line(2010, 1090, 2060, 1120, fill=self.settings.second_color, width=5)
        self.app.c_main.create_line(2010, 1150, 2060, 1120, fill=self.settings.second_color, width=5)

        self.app.c_main.create_line(50, 1220, 2060, 1220, fill=self.settings.second_color, width=5)
        self.app.c_main.create_line(2010, 1190, 2060, 1220, fill=self.settings.second_color, width=5)
        self.app.c_main.create_line(2010, 1250, 2060, 1220, fill=self.settings.second_color, width=5)

        self.tl_trash = self.app.c_main.create_image(2100, 1170, image=create_imagetk("images/blocks/trash.png"),
                                                     state="hidden")

        self.create()

    def create(self):
        tag_id = 0
        for param in self.params:
            tag_name = f"tl{tag_id}"
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
            tag_id += 1

    def tl_press(self, e):
        pressed_id = (e.widget.find_withtag("current")[0])
        print("pressedid", pressed_id)
        for block in self.blocks:
            if pressed_id in block.element_ids:
                self.selected_block = block
                break

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


        element = int((self.selected_block.start_pos[0]-100)/200)
        print(element)
        if element < self.change:
            self.change -= 1

        print(self.change)

        poped = self.blocks.pop(element)
        self.blocks.insert(self.change, poped)

        print(self.selected_block.start_pos[0])
        if element == self.change:
            print("xd")
            self.app.c_main.coords(self.selected_block.element_ids[0], self.selected_block.start_pos[0], 1120,
                                   self.selected_block.start_pos[0] + 200, 1220)
            self.app.c_main.coords(self.selected_block.element_ids[1], self.selected_block.start_pos[0] + 100, 1170)
            self.app.c_main.coords(self.selected_block.element_ids[2], self.selected_block.start_pos[0] + 100, 1200)

        elif self.change > element:
            new_pos = self.selected_block.start_pos[0]
            print("ster", element, " ", self.change)
            for item in self.blocks[element:self.change+1]:
                if item.start_pos[0] > self.selected_block.start_pos[0]:
                    item.start_pos[0] = new_pos
                elif item.start_pos[0] == self.selected_block.start_pos[0]:

                    item.start_pos[0] = new_pos
                else:
                    break
                self.app.c_main.coords(item.element_ids[0], new_pos, 1120, new_pos + 200, 1220)
                self.app.c_main.coords(item.element_ids[1], new_pos + 100, 1170)
                self.app.c_main.coords(item.element_ids[2], new_pos + 100, 1200)
                new_pos += 200
        else:
            new_pos = 100 + self.change * 200
            for item in self.blocks[self.change:element+1]:
                if item.start_pos[0] > self.selected_block.start_pos[0]:
                    item.start_pos[0] = new_pos
                elif item.start_pos[0] == self.selected_block.start_pos[0]:
                    item.start_pos[0] = new_pos
                else:
                    break
                self.app.c_main.coords(item.element_ids[0], new_pos, 1120, new_pos + 200, 1220)
                self.app.c_main.coords(item.element_ids[1], new_pos + 100, 1170)
                self.app.c_main.coords(item.element_ids[2], new_pos + 100, 1200)
                new_pos += 200

        # else:




        # for item in self.blocks:
        #     self.app.c_main.itemconfigure(self.tl_blocks[i][0], fill=blocks[i][0])
        #     self.app.c_main.itemconfigure(self.tl_blocks[i][1], text=blocks[i][1])
        #     self.app.c_main.itemconfigure(self.tl_blocks[i][2], text=blocks[i][2])
        # if self.element != self.change:
        #     self.restart()
        # self._tl_shift(new_tl)

        # if e.x > 2000:
        #     self.current_pos -= 1
        #     self.timeline_positions.pop(-1)
        #     self.app.c_main.delete(self.tl_blocks[-1][0])
        #     self.app.c_main.delete(self.tl_blocks[-1][1])
        #     self.app.c_main.delete(self.tl_blocks[-1][2])
        #     self.tl_blocks.pop(-1)
        #     new_tl.pop(-1)
        #
        # self.tl_to_file()

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

from customtkinter import *

from Data import Date
from actions import *
from clock import Clock
from settings import *


class Setup1:
    """Creating goals setup"""

    def __init__(self, root):
        self.app = root
        self.c_main = None

        self.today_data = Date()

        self.goals_texts = []
        self.shadow_line_position = 0
        self.goal_widgets_yposes = []
        self.is_end = 0

        self.goals_widgets = []
        self.which_goals = [0]
        self.goals_site = 0

        self.goals_from_file()

    def create_setup1_window(self):
        self.app.page = 1
        self.app.create_c_main()

        self.goals_widgets = []
        if len(self.goals_texts) > 0:
            self.goal_widgets_yposes = []
            for goal in self.goals_texts:
                self.show_goal(goal)

        self.app.c_main.create_text(1080, 60, text="Create goals for today", font=FONT, fill=COL_FONT)
        self.app.c_main.create_image(1080, 100, image=create_imagetk("images/line.png", 450, 150))
        self.app.c_main.create_image(75, 750, image=create_imagetk("images/goals/arrow.png", ))
        self.app.c_main.create_text(20, 750, text="Importance", font=FONT, fill=COL_FONT, anchor="nw",
                                    angle=90)

        self.e_todo = CTkEntry(self.app, font=FONT_TEXT)
        self.e_todo.focus()
        self.app.c_main.create_window(1030, 1295, window=self.e_todo, width=1760, height=50)
        self.b_add = CTkButton(self.app, text="+", font=FONT_ADD, fg_color=COL_2,
                               command=self.add_goal, border_width=5, hover_color=COL_1,
                               border_color=COL_2)
        self.app.c_main.create_window(75, 1295, window=self.b_add, height=50, width=50)

        self.b_submit = CTkButton(self.app, text="Submit", font=FONT, fg_color=COL_2,
                                  hover_color=COL_1, border_color=COL_2, border_width=5,
                                  command=self.app.setup2.create_setup2_window)
        self.app.c_main.create_window(2035, 1295, window=self.b_submit, width=150, height=50)

        self.dots = self.app.c_main.create_image(125, 210, image=create_imagetk("images/goals/dots.png"),
                                                 tags=("dots",),
                                                 state='hidden')
        self.shadow = self.app.c_main.create_text(-100, -100, text="", font=FONT_TEXT, fill="grey")
        self.app.c_main.itemconfigure(self.shadow, state='hidden')
        self.line = self.app.c_main.create_image(-100, -100 + self.shadow_line_position * 60,
                                                 image=create_imagetk("images/line2.png"),
                                                 state='hidden')

        self.app.c_main.tag_bind("dots", "<B1-Motion>", self.move_dots)
        self.app.c_main.tag_bind("dots", "<Button-1>", self.press_dots)
        self.app.c_main.tag_bind("dots", "<ButtonRelease-1>", self.unpress_dots)
        self.app.c_main.bind('<Motion>', self.position)
        self.e_todo.bind('<Return>', self.add_goal)

        reg = self.app.register(lambda input1: (FONT_BOX.getbbox(input1)[2] < 1500))
        self.e_todo.configure(validate="key", validatecommand=(reg, '%P'))

    def show_goal(self, text):
        print("xd")
        i = len(self.goals_widgets) + 1
        goal = self.app.c_main.create_text(150, 140 + i * 60, text=f"{text}",
                                           font=FONT_TEXT,
                                           fill=COL_FONT, anchor="w", tags=f"todo{i}")
        self.goals_widgets.append(goal)
        self.goal_widgets_yposes.append(140 + i * 60)

        self.app.c_main.tag_bind(f"todo{i}", '<Enter>', self.strike_on)
        self.app.c_main.tag_bind(f"todo{i}", '<Leave>', self.strike_off)
        self.app.c_main.tag_bind(f"todo{i}", '<Button-1>', self.delete_goal)

    def add_goal(self, *_):
        value = self.e_todo.get()
        if value != "":
            self.show_goal(value)
            self.e_todo.delete(0, len(value))
        self.goals_texts = []
        for i in range(len(self.goals_widgets)):
            self.goals_texts.append(self.app.c_main.itemcget(self.goals_widgets[i], 'text'))
        self.save_goals_to_file()

    def delete_goal(self, event):
        widget_name = event.widget.find_withtag("current")[0]

        index = self.goals_widgets.index(widget_name)

        for i in range(index, len(self.goals_widgets) - 1):
            next_text = self.app.c_main.itemcget(self.goals_widgets[i + 1], 'text')
            self.app.c_main.itemconfigure(self.goals_widgets[i], text=next_text)

        self.app.c_main.delete(self.goals_widgets[-1])
        self.goals_widgets.pop()
        self.goal_widgets_yposes.pop()

        if len(self.goals_widgets) != 0:
            self.app.c_main.moveto(self.dots, 100, self.goal_widgets_yposes[-1] - 25)

        self.app.setup1.goals_texts = []
        for i in range(len(self.goals_widgets)):
            self.app.setup1.goals_texts.append(self.app.c_main.itemcget(self.goals_widgets[i], 'text'))
        self.save_goals_to_file()

    # binds for adding goals
    def strike_on(self, event):
        self.app.c_main.itemconfigure(event.widget.find_withtag("current")[0], font=FONT_TEXT_STRIKE)

    def strike_off(self, event):
        self.app.c_main.itemconfigure(event.widget.find_withtag("current")[0], font=FONT_TEXT)

    def position(self, e):
        flag = 0
        y = 0
        for posy in self.goal_widgets_yposes:
            if posy - 25 < e.y < posy + 25 and 110 < e.x < 140:
                y = posy
                flag = 1

        if flag == 1 and y - 14 < e.y < y + 14:
            self.app.c_main.itemconfigure(self.dots, state='normal')
            self.app.c_main.moveto(self.dots, 100, y - 25)
        else:
            self.app.c_main.itemconfigure(self.dots, state='hidden')

    def press_dots(self, e):
        flag = 0
        text = ""
        self.goal = 0
        self.app.c_main.itemconfigure(self.line, state='normal')
        for posy in self.goal_widgets_yposes:
            if posy - 25 < e.y < posy + 25:
                text = self.app.c_main.itemcget(self.goals_widgets[self.goal], 'text')
                flag = 1
            elif flag == 0:
                self.goal += 1
        self.app.c_main.itemconfigure(self.shadow, text=text)
        self.app.c_main.unbind("<Motion>")

    def move_dots(self, e):
        self.app.c_main.itemconfigure(self.shadow, state="normal")

        if e.y < 200:
            self.shadow_line_position = 0
        elif e.y > self.goal_widgets_yposes[-1]:
            self.shadow_line_position = len(self.goal_widgets_yposes)
        else:
            self.shadow_line_position = int((e.y - 110) / 60) - 1

        self.app.c_main.moveto(self.line, 150, 150 + self.shadow_line_position * 60)

        if 200 < e.y < self.goal_widgets_yposes[-1]:
            self.app.c_main.moveto(self.dots, 100, e.y - 25)
            self.app.c_main.moveto(self.shadow, 150, e.y - 20)

    def unpress_dots(self, *_):
        self.app.c_main.itemconfigure(self.line, state='hidden')
        self.app.c_main.bind('<Motion>', self.position)
        self.app.c_main.itemconfigure(self.shadow, state="hidden")
        self.app.c_main.moveto(self.line, -100, -100)
        self.app.c_main.moveto(self.shadow, -100, -100)

        self.goals_texts = []
        for i in range(len(self.goals_widgets)):
            self.goals_texts.append(self.app.c_main.itemcget(self.goals_widgets[i], 'text'))

        text = self.app.c_main.itemcget(self.goals_widgets[self.goal], 'text')
        prev_pos = (self.goals_texts.index(text))
        if prev_pos - 1 == self.shadow_line_position:
            pass
        elif self.shadow_line_position != 0:
            self.shadow_line_position -= 1
        self.goals_texts.remove(text)
        self.goals_texts.insert(self.shadow_line_position, text)
        print(self.shadow_line_position)

        for i in range(len(self.goals_widgets)):
            self.app.c_main.itemconfigure(self.goals_widgets[i], text=self.goals_texts[i])

    # method for getting/saving goals
    def goals_from_file(self):
        if os.path.isfile("data/goals.txt"):
            with open("data/goals.txt", "r") as f:
                lines = f.readlines()
                if len(lines) != 0:
                    for i in range(len(lines)):
                        lines[i] = lines[i].strip()

                    if str(self.today_data.formatted_date) == lines[0]:
                        self.goals_texts = lines[1:]

        else:
            with open("data/goals.txt", 'x'):
                pass

    def save_goals_to_file(self):
        if len(self.goals_texts) == 0:
            for i in range(len(self.goals_widgets)):
                self.goals_texts.append(self.app.c_main.itemcget(self.goals_widgets[i], 'text'))

        with open('data/goals.txt', 'w+') as file:
            file.write(f"{self.today_data.formatted_date}\n")
            for goals in self.goals_texts:
                file.write('%s\n' % goals)

    # methods for main window
    def widget_goals(self, direction=2):
        for widget in self.goals_widgets:
            self.app.c_main.delete(widget)
        if direction == 0 and self.goals_site > 0:
            self.goals_site -= 1
        if direction == 1 and self.is_end == 0:
            self.goals_site += 1
        if len(self.goals_texts) != 0:
            i = self.which_goals[self.goals_site]
            start = 1
            end = 1
            self.goals_widgets = []
            for goal in self.goals_texts[i:]:
                i += 1
                end += 1
                goal_list = goal.split(" ")
                full = ""
                actual = ""
                for word in goal_list:
                    box = FONT_BOX.getbbox(actual + word)
                    if box[2] > 300:
                        full += actual + "\n" + word
                        actual = ""
                        end += 1
                    else:
                        actual += " " + word
                full += actual
                if start < 8:
                    text = self.app.c_main.create_text(180, 190 + start * 40 + (end - start) * 20,
                                                       text=f"{i}. {full}",
                                                       font=FONT_TEXT, width=500,
                                                       fill=COL_FONT, justify="left", anchor="w")
                    self.goals_widgets.append(text)
                    self.is_end = 1
                else:
                    self.which_goals.append(i - 1)
                    self.is_end = 0

                    break
                start = end


class Setup2:
    """Creating timeline setup
    rc = recently created
    tl = timeline"""

    def __init__(self, root):
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

    def create_setup2_window(self):
        self.app.page = 2

        self.app.create_c_main()
        self.app.c_main.create_text(1080, 60, text="Create focus timeline", font=("Arial", 40), fill=COL_FONT)
        self.app.c_main.create_image(1080, 100, image=create_imagetk("images/line.png", 450, 150))
        self.app.c_main.create_rectangle(50, 150, 2110, 1000, outline=COL_2, width=5)
        self.app.c_main.create_line(800, 150, 800, 1000, fill=COL_2, width=5)
        self.b_submit = CTkButton(self.app, text="Submit", font=FONT, fg_color=COL_2,
                                  hover_color=COL_1, border_color=COL_2, border_width=5,
                                  command=self.app.main.create_main_window)
        self.app.c_main.create_window(2035, 1295, window=self.b_submit, width=150, height=50)

        # Recently created panel
        self.app.c_main.create_text(425, 175, font=("Arial", 30), fill=COL_FONT, text="Recently created")
        self.b_rc_create = CTkButton(self.app, text="+", font=("Arial", 70), fg_color=COL_1,
                                     command=self.rc_add)
        self.app.c_main.create_window(80, 970, window=self.b_rc_create, height=50, width=50)
        self.rc_show()
        # saved panel
        self.saved_add_bg = self.app.c_main.create_rectangle(800, 150, 2110, 1000, fill=COL_1, outline=COL_2, width=5)
        self.app.c_main.create_text(1455, 175, font=("Arial", 30), fill=COL_FONT, text="Saved")
        self.saved_add_text = self.app.c_main.create_text(1455, 975, font=("Arial", 30), fill=COL_FONT, state="hidden",
                                                          text="Drop here to save")
        self.saved_trash = self.app.c_main.create_image(835, 960, image=create_imagetk("images/blocks/trash.png"),
                                                        state="hidden")
        self.saved_show()
        # Timeline panel
        self.tl_add_bg = self.app.c_main.create_rectangle(50, 1120, 2060, 1220, fill=COL_1, width=0)
        self.tl_add_text = self.app.c_main.create_text(1055, 1280, font=("Arial", 30), fill=COL_FONT, state="hidden",
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
                                                 1220, fill=col, outline=COL_2, width=5, tags=tag)

        block_time = self.app.c_main.create_text(self.timeline_positions[self.current_pos] + 100, 1170,
                                                 text=timer, font=FONT, fill=COL_FONT, tags=tag)
        block_text = self.app.c_main.create_text(self.timeline_positions[self.current_pos] + 100, 1200,
                                                 text=text, font=("Arial", 15), fill=COL_FONT, tags=tag)

        if is_move:
            self.app.c_main.tag_bind(tag, "<B1-Motion>", self.tl_move)

            self.app.c_main.tag_bind(tag, "<Button-1>", self.tl_press)
            self.app.c_main.tag_bind(tag, "<ButtonRelease-1>", self.tl_unpress)

        self.tl_blocks.append([block, block_time, block_text])

        self.timeline_positions.append(self.timeline_positions[self.current_pos] + 200)
        self.current_pos += 1

    def _tl_bg_create(self):
        self.app.c_main.create_line(50, 1120, 2060, 1120, fill=COL_2, width=5)
        self.app.c_main.create_line(2010, 1090, 2060, 1120, fill=COL_2, width=5)
        self.app.c_main.create_line(2010, 1150, 2060, 1120, fill=COL_2, width=5)

        self.app.c_main.create_line(50, 1220, 2060, 1220, fill=COL_2, width=5)
        self.app.c_main.create_line(2010, 1190, 2060, 1220, fill=COL_2, width=5)
        self.app.c_main.create_line(2010, 1250, 2060, 1220, fill=COL_2, width=5)

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
                                                        outline=COL_2,
                                                        width=5)

            timer = format_time(block[0])
            category = self.app.c_main.create_text(startx + 100 + i * 250, 275 + j * 150,
                                                   text=timer, font=FONT, fill=COL_FONT, tags=tag_block)
            time = self.app.c_main.create_text(startx + 100 + i * 250, 305 + j * 150, text=block[2], fill=COL_FONT,
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
        self.app.c_main.itemconfigure(self.saved_add_bg, fill=COL_2)
        self.app.c_main.itemconfigure(self.saved_add_text, state='normal')

    def rc_move(self, e):
        self._move(e)
        if 800 < e.x < 2110 and 150 < e.y < 1000:
            self.app.c_main.itemconfigure(self.blocks[self.category][self.element][0], outline="green")
        else:
            self.app.c_main.itemconfigure(self.blocks[self.category][self.element][0], outline=COL_2)

    def rc_unpress(self, e):
        self._unpress(e)
        self.app.c_main.itemconfigure(self.saved_add_bg, fill=COL_1)
        self.app.c_main.itemconfigure(self.saved_add_text, state='hidden')
        if 800 < e.x < 2110 and 150 < e.y < 1000:
            self.app.c_main.itemconfigure(self.saved_add_bg, fill=COL_1)
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
            self.app.c_main.itemconfigure(self.blocks[1][self.element][0], outline=COL_2)

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
            self.app.c_main.itemconfigure(self.tl_blocks[self.element][0], outline=COL_2)

    def tl_unpress(self, e):
        self.app.c_main.itemconfigure(self.tl_trash, state="hidden")
        self.app.c_main.itemconfigure(self.pointer, state='hidden')
        self.app.c_main.itemconfigure(self.tl_blocks[self.element][0], outline=COL_2)

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

        if 1090 < e.y < 1390:
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

        self.app.c_main.itemconfigure(self.tl_add_bg, fill=COL_1)
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
            print(self.current_pos)
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

    def widget_timeline(self):
        self.current_pos = 0
        self.timeline_positions = [100]
        self.tl_blocks = []
        self.tl_params = []
        self.current_block = 0
        self.timer = "0:00"
        self.current_line_len = 555
        self.current_time = 0

        self._tl_bg_create()
        self.tl_from_file()
        for item in self.tl_params:
            self.tl_add_block(item[0], item[1], item[2], 0)

        img = CTkImage(light_image=Image.open("images/timeline/play.png"), size=(50, 50))
        self.play_pause = CTkButton(self.app, image=img, text="", fg_color=COL_1, hover_color=COL_2,
                                    command=self.start_stop_timer)
        self.app.c_main.create_window(1055, 1280, window=self.play_pause, width=70, height=70)

        img = CTkImage(light_image=Image.open("images/timeline/next.png"), size=(25, 25))
        self.next = CTkButton(self.app, image=img, text="", fg_color=COL_1, hover_color=COL_2, command=self.next_block)
        self.app.c_main.create_window(1155, 1280, window=self.next, width=40, height=40)

        img = CTkImage(light_image=Image.open("images/timeline/previous.png"), size=(25, 25))
        self.previous = CTkButton(self.app, image=img, text="", fg_color=COL_1, hover_color=COL_2,
                                  command=self.prev_block)
        self.app.c_main.create_window(955, 1280, window=self.previous, width=40, height=40)

        self.time_current = self.app.c_main.create_text(500, 1330, text=f"{self.timer}", font=("Arial", 20),
                                                        fill=COL_FONT)
        self.block_len = self.app.c_main.create_text(1610, 1330, text="0:00", font=("Arial", 20), fill=COL_FONT)
        self.current = self.app.c_main.create_line(self.current_position, 1090, self.current_position, 1250,
                                                   fill=COL_FONT, width=5)
        self.line_length = self.app.c_main.create_line(555, 1330, 555, 1330, fill=COL_FONT, width=8)

        if len(self.tl_params) > 0:
            self.time = int(self.tl_params[self.current_block][0])
            self.app.c_main.itemconfigure(self.block_len, text=f"{self.time}:00")
            self.pause_on = False
        if self.current_pos == 0:
            self.play_pause.configure(state="disabled")

    def start_stop_timer(self):
        self.pause_on = not self.pause_on
        self.play_pause.configure(command=None)
        self.app.after(500, lambda: self.play_pause.configure(command=self.start_stop_timer))

        if self.pause_on:
            self._change_img("pause")
            self.time = int(self.tl_params[self.current_block][0])
            self.current_speed = 200 / (self.time * 60)
            self.line_speed = 1000 / (self.time * 60)

            if self.current_time == 0:
                self.count_down(0)
            else:
                self.count_down(self.current_time)

    def count_down(self, count):
        if count <= self.time * 60 and self.pause_on:
            self.timer = f"{int(count / 60)}:{count % 60 if count % 60 > 9 else f'0{count % 60}'}"
            if self.app.page == 0:
                self.app.c_main.itemconfigure(self.time_current, text=self.timer)
                self.app.c_main.coords(self.current, self.current_position, 1090, self.current_position, 1250)
                self.app.c_main.coords(self.line_length, 555, 1330, self.current_line_len, 1330)

            self.current_time = count + 1
            self.app.after(1000, self.count_down, count + 1)
            self.current_position += self.current_speed
            self.current_line_len += self.line_speed
        elif not count < self.time * 60:
            self.next_block()
        else:
            self._change_img("play")

    def next_block(self):
        self.play_pause.configure(command=None)
        self.app.after(500, lambda: self.play_pause.configure(command=self.start_stop_timer))
        if len(self.tl_params) - 1 > self.current_block:
            self.current_block += 1
            self.reset()

    def prev_block(self):
        self.play_pause.configure(command=None)
        self.app.after(500, lambda: self.play_pause.configure(command=self.start_stop_timer))
        if self.current_block > 0 and self.current_time == 0:
            self.current_block -= 1
        self.reset()

    def restart(self):
        self.current_block = 0
        self._value_reset()

    def reset(self):
        self._value_reset()
        self.app.c_main.itemconfigure(self.block_len, text=f"{self.tl_params[self.current_block][0]}:00")
        self.app.c_main.itemconfigure(self.time_current, text=f"0:00")
        self.app.c_main.coords(self.line_length, 555, 1400, 555, 1400)
        self.app.c_main.coords(self.current, self.current_position, 1090, self.current_position, 1250)

    def _change_img(self, file):
        img = CTkImage(light_image=Image.open(f"images/timeline/{file}.png"), size=(50, 50))
        self.play_pause.configure(image=img)

    def _value_reset(self):
        self.pause_on = False
        self.current_position = 100 + self.current_block * 200
        self._change_img("play")
        self.current_time = 0
        self.current_line_len = 555

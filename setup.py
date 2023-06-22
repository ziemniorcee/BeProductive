from Data import Date
from settings import *
from customtkinter import *
from actions import *
from clock import Clock


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
        self.app.create_c_main()

        self.goals_widgets = []
        if len(self.goals_texts) > 0:
            self.goal_widgets_yposes = []
            for goal in self.goals_texts:
                self.show_entry(goal)

        self.app.c_main.create_text(1080, 60, text="Create goals for today", font=FONT, fill=COL_FONT)
        self.app.c_main.create_image(1080, 100, image=create_imagetk("images/line.png", 450, 150))
        self.app.c_main.create_image(75, 750, image=create_imagetk("images/goals/arrow.png", ))
        self.app.c_main.create_text(20, 750, text="Importance", font=FONT, fill=COL_FONT, anchor="nw",
                                    angle=90)

        self.e_todo = CTkEntry(self.app, font=FONT_TEXT)
        self.e_todo.focus()
        self.app.c_main.create_window(1030, 1365, window=self.e_todo, width=1760, height=50)
        self.b_add = CTkButton(self.app, text="+", font=FONT_ADD, fg_color=COL_2,
                               command=self.add_goal, border_width=5, hover_color=COL_1,
                               border_color=COL_2)
        self.app.c_main.create_window(75, 1365, window=self.b_add, height=50, width=50)

        self.b_yes = CTkButton(self.app, text="Submit", font=FONT, fg_color=COL_2,
                               hover_color=COL_1, border_color=COL_2, border_width=5,
                               command=self.app.setup2.create_setup2_window)
        self.app.c_main.create_window(2035, 1365, window=self.b_yes, width=150, height=50)

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

    def show_entry(self, text):
        i = len(self.goals_widgets) + 1

        goal = self.app.c_main.create_text(150, 140 + i * 60, text=f"{text}",
                                           font=FONT_TEXT,
                                           fill=COL_FONT, anchor="w", tags=f"todo{i}")
        self.goals_widgets.append(goal)
        self.goal_widgets_yposes.append(140 + i * 60)

        self.app.c_main.tag_bind(f"todo{i}", '<Enter>', self.strike_on)
        self.app.c_main.tag_bind(f"todo{i}", '<Leave>', self.strike_off)
        self.app.c_main.tag_bind(f"todo{i}", '<Button-1>', self.del_goal)

    # methods for adding goals
    def add_goal(self, *_):
        value = self.e_todo.get()
        if value != "":
            self.show_entry(value)
            self.e_todo.delete(0, len(value))
        self.goals_texts = []
        for i in range(len(self.goals_widgets)):
            self.goals_texts.append(self.app.c_main.itemcget(self.goals_widgets[i], 'text'))

    def del_goal(self, event):
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

        self.goals_texts.remove(text)
        self.goals_texts.insert(self.shadow_line_position, text)

        for i in range(len(self.goals_widgets)):
            self.app.c_main.itemconfigure(self.goals_widgets[i], text=self.goals_texts[i])

    # methods for main window
    def show_goals(self, direction=2):
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


class Setup2:
    def __init__(self, root):
        self.app = root
        self.clock_window = None
        self.is_clock_window_on = False

    def create_setup2_window(self):
        self.tag_id = 0

        self.app.create_c_main()
        self.app.c_main.create_text(1080, 60, text="Create focus timeline", font=("Arial", 40), fill=COL_FONT)
        self.app.c_main.create_image(1080, 100, image=create_imagetk("images/line.png", 450, 150))
        self.app.c_main.create_rectangle(50, 150, 2110, 1000, outline=COL_2, width=5)
        self.app.c_main.create_line(800, 150, 800, 1000, fill=COL_2, width=5)
        # Recently created panel
        self.app.c_main.create_text(425, 175, font=("Arial", 30), fill=COL_FONT, text="Recently created")
        self.b_create_block = CTkButton(self.app, text="+", font=("Arial", 70), fg_color=COL_1,
                                        command=self.rc_add)
        self.app.c_main.create_window(80, 970, window=self.b_create_block, height=50, width=50)
        self.rc_create()

        # saved panel
        self.app.c_main.create_text(1455, 175, font=("Arial", 30), fill=COL_FONT, text="Saved")

        # Timeline panel
        self.app.c_main.create_line(50, 1190, 2060, 1190, fill=COL_2, width=5)
        self.app.c_main.create_line(2010, 1160, 2060, 1190, fill=COL_2, width=5)
        self.app.c_main.create_line(2010, 1220, 2060, 1190, fill=COL_2, width=5)

        self.app.c_main.create_line(50, 1290, 2060, 1290, fill=COL_2, width=5)
        self.app.c_main.create_line(2010, 1260, 2060, 1290, fill=COL_2, width=5)
        self.app.c_main.create_line(2010, 1320, 2060, 1290, fill=COL_2, width=5)

        self.trash = self.app.c_main.create_image(2100, 1240, image=create_imagetk("images/blocks/trash.png"),
                                                  state="hidden")

        self.tl_create()

    def rc_create(self):
        self.rc_params = []
        self.rc_blocks = []
        startx = 75
        starty = 225
        i = 0
        j = 0

        self.rc_from_file()

        for block in self.rc_blocks:

            tag_block = f"r_block{10 + i + j * 10}"
            block_id = self.app.c_main.create_rectangle(startx + i * 250, starty + 150 * j, startx + 200 + i * 250,
                                                        starty + 100 + 150 * j, fill=block[1], tags=tag_block,
                                                        outline=COL_2,
                                                        width=5)
            hour = int(block[0]) // 60
            minutes = int(block[0]) % 60
            timer = f"{hour if hour > 9 else '0' + str(hour)}:{minutes if minutes > 9 else '0' + str(minutes)}"
            category = self.app.c_main.create_text(175 + i * 250, 275 + j * 150,
                                                   text=timer, font=FONT, fill=COL_FONT, tags=tag_block)
            time = self.app.c_main.create_text(175 + i * 250, 305 + j * 150, text=block[2], fill=COL_FONT,
                                               font=("Arial", 15),
                                               tag=tag_block, anchor="center")
            i += 1
            if i % 3 == 0:
                j += 1
                i = 0

            self.app.c_main.tag_bind(tag_block, "<B1-Motion>", self.rc_move)
            self.app.c_main.tag_bind(tag_block, "<Button-1>", self.rc_press)
            self.app.c_main.tag_bind(tag_block, "<ButtonRelease-1>", self.rc_unpress)
            self.rc_params.append([block_id, category, time])


    def rc_add(self):
        if not self.is_clock_window_on or not self.clock_window.is_clock_on:
            self.clock_window = Clock(self)
            self.clock_window.wm_attributes("-topmost", True)
            self.is_clock_window_on = True
            self.clock_window.protocol("WM_DELETE_WINDOW", self.clock_on_closing)

    def saved_create(self):
        self.saved_blocks = []
        self.saved_from_file()

    def tl_create(self):
        self.tl_blocks = []
        self.current_pos = []
        self.tl_params = []
        self.current_pos = 0
        self.timeline_positions = [100]
        self.pointer = self.app.c_main.create_line(self.timeline_positions[self.current_pos], 1140,
                                                   self.timeline_positions[self.current_pos],
                                                   1340, fill="#155255", width=5, state="hidden")
        self.tl_from_file()
        for item in self.tl_params:
            self.tl_add_block(item[0], item[1], item[2])

    def tl_add_block(self, col, timer, text):
        tag = f"tl{self.tag_id}"
        self.tag_id += 1
        block = self.app.c_main.create_rectangle(self.timeline_positions[self.current_pos], 1190,
                                                 self.timeline_positions[self.current_pos] + 200,
                                                 1290, fill=col, outline=COL_2, width=5, tags=tag)

        block_time = self.app.c_main.create_text(self.timeline_positions[self.current_pos] + 100, 1240,
                                                 text=timer, font=FONT, fill=COL_FONT, tags=tag)
        block_text = self.app.c_main.create_text(self.timeline_positions[self.current_pos] + 100, 1270,
                                                 text=text, font=("Arial", 15), fill=COL_FONT, tags=tag)

        self.app.c_main.tag_bind(tag, "<B1-Motion>", self.tl_move)

        self.app.c_main.tag_bind(tag, "<Button-1>", self.tl_press)
        self.app.c_main.tag_bind(tag, "<ButtonRelease-1>", self.tl_unpress)

        self.tl_blocks.append([block, block_time, block_text])

        self.timeline_positions.append(self.timeline_positions[self.current_pos] + 200)
        self.current_pos += 1

    def get_change(self, x):
        i = 0
        for pos in self.timeline_positions:
            if x - 100 <= pos < x + 100:
                self.app.c_main.coords(self.pointer, self.timeline_positions[i], 1140,
                                       self.timeline_positions[i],
                                       1340)
                self.change = i
                break

            i += 1

    # from other classes
    def clock_on_closing(self):

        self.is_clock_window_on = False
        self.rc_to_file()
        self.clock_window.destroy()
        self.create_setup2_window()

    # binds

    # recent blocks binds
    def rc_press(self, e):
        block = (e.widget.find_withtag("current")[0])
        self.element = calculate_element(block, self.rc_params)
        i = int(self.element % 3)
        j = int(self.element // 3)
        self.start_pos = [75 + i * 250, 225 + 150 * j]

    def rc_move(self, e):

        if 1090 < e.y < 1390:
            self._move(self.rc_params, e)

        else:
            self.app.c_main.moveto(self.rc_params[self.element][0], e.x - 100, e.y - 50)
            self.app.c_main.moveto(self.rc_params[self.element][1], e.x - 50, e.y - 20)
            self.app.c_main.coords(self.rc_params[self.element][2], e.x, e.y + 35)
            if self.pointer is not None:
                self.app.c_main.itemconfigure(self.pointer, state='hidden')

        self.app.c_main.tag_raise(self.rc_params[self.element][0])
        self.app.c_main.tag_raise(self.rc_params[self.element][1])
        self.app.c_main.tag_raise(self.rc_params[self.element][2])

    def rc_unpress(self, e):
        if self.pointer is not None:
            self.app.c_main.itemconfigure(self.pointer, state='hidden')

        self.app.c_main.moveto(self.rc_params[self.element][0], self.start_pos[0], self.start_pos[1])
        self.app.c_main.moveto(self.rc_params[self.element][1], self.start_pos[0] + 50, self.start_pos[1] + 30)
        self.app.c_main.coords(self.rc_params[self.element][2], self.start_pos[0] + 100, self.start_pos[1] + 85)

        if 1090 < e.y < 1390:

            col = self.app.c_main.itemcget(self.rc_params[self.element][0], 'fill')
            timer = self.app.c_main.itemcget(self.rc_params[self.element][1], 'text')
            text = self.app.c_main.itemcget(self.rc_params[self.element][2], 'text')

            self.tl_add_block(col, timer, text)

            self.element = len(self.tl_blocks)

            new_tl = self.tl_blocks[:self.change]
            new_tl.append(self.tl_blocks[self.element - 1])
            for item in self.tl_blocks[self.change:self.element - 1]:
                new_tl.append(item)
            for item in self.tl_blocks[self.element + 1:]:
                new_tl.append(item)
            self._tl_shift(new_tl)
            self.tl_to_file()

    # Timeline binds
    def tl_press(self, e):
        block = (e.widget.find_withtag("current")[0])
        self.element = calculate_element(block, self.tl_blocks)

        self.app.c_main.itemconfigure(self.pointer, state='normal')
        self.app.c_main.itemconfigure(self.trash, state="normal")

    def tl_move(self, e):
        if 1090 < e.y < 1390:
            self._move(self.tl_blocks, e)
        if e.x > 2000:
            self.app.c_main.itemconfigure(self.tl_blocks[self.element][0], outline="red")
        else:
            self.app.c_main.itemconfigure(self.tl_blocks[self.element][0], outline=COL_2)

    def tl_unpress(self, e):
        self.app.c_main.itemconfigure(self.trash, state="hidden")
        self.app.c_main.itemconfigure(self.pointer, state='hidden')
        self.app.c_main.itemconfigure(self.tl_blocks[self.element][0], outline=COL_2)

        self.app.c_main.coords(self.tl_blocks[self.element][0], self.timeline_positions[self.element], 1190,
                               self.timeline_positions[self.element] + 200, 1290)
        self.app.c_main.coords(self.tl_blocks[self.element][1], self.timeline_positions[self.element] + 100, 1240)
        self.app.c_main.coords(self.tl_blocks[self.element][2], self.timeline_positions[self.element] + 100, 1270)

        if self.element != self.change:
            if self.element > self.change:
                print(self.tl_blocks)
                new_tl = self.tl_blocks[:self.change]
                new_tl.append(self.tl_blocks[self.element])
                for item in self.tl_blocks[self.change:self.element]:
                    new_tl.append(item)
                for item in self.tl_blocks[self.element + 1:]:
                    new_tl.append(item)
                self._tl_shift(new_tl)
                print(new_tl)
                print(self.tl_blocks)
            else:
                new_tl = self.tl_blocks[:self.element]
                for item in self.tl_blocks[self.element + 1:self.change]:
                    new_tl.append(item)
                new_tl.append(self.tl_blocks[self.element])
                for item in self.tl_blocks[self.change:]:
                    new_tl.append(item)
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
    def _tl_shift(self, arr):
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

    def _move(self, arr, e):
        self.app.c_main.itemconfigure(self.pointer, state='normal')
        self.app.c_main.moveto(arr[self.element][0], e.x - 100, 1187)
        self.app.c_main.moveto(arr[self.element][1], e.x - 50, 1220)
        self.app.c_main.coords(arr[self.element][2], e.x, 1270)

        self.get_change(e.x)

    # functions for files

    # recent blocks
    def rc_from_file(self):
        self.rc_blocks = []
        if os.path.isfile("data/blocks.txt"):
            with open("data/blocks.txt", "r") as file:
                xd = file.readlines()
                for i in range(0, len(xd), 3):
                    self.rc_blocks.append([xd[i].strip(), xd[i + 1].strip(), xd[i + 2].strip()])
        else:
            with open("data/blocks.txt", 'x'):
                pass

    def rc_to_file(self):

        with open("data/blocks.txt", "r+") as file:
            lines = file.readlines()

        if len(self.new_block) == 3:
            if len(lines) < 45:
                for item in lines[:len(lines)]:
                    self.new_block.append(item.strip())
            else:
                for item in lines[:42]:
                    self.new_block.append(item.strip())

            with open('data/blocks.txt', 'w+') as file:
                for element in self.new_block:
                    file.write('%s\n' % element)

    # saved
    def saved_from_file(self):
        self.rc_blocks = []
        if os.path.isfile("data/blocks.txt"):
            with open("data/blocks.txt", "r") as file:
                xd = file.readlines()
                for i in range(0, len(xd), 3):
                    self.rc_blocks.append([xd[i].strip(), xd[i + 1].strip(), xd[i + 2].strip()])
        else:
            with open("data/blocks.txt", 'x'):
                pass

    # timeline
    def tl_from_file(self):
        if os.path.isfile("data/tl_blocks.txt"):
            with open("data/tl_blocks.txt", 'r') as file:
                arr = file.readlines()
            for i in range(0, len(arr), 3):
                self.tl_params.append([arr[i].strip(), arr[i + 1].strip(), arr[i + 2].strip()])

    def tl_to_file(self):
        with open("data/tl_blocks.txt", "w") as file:
            for i in range(self.current_pos):
                file.write('%s\n' % self.app.c_main.itemcget(self.tl_blocks[i][0], 'fill'))
                file.write('%s\n' % self.app.c_main.itemcget(self.tl_blocks[i][1], 'text'))
                file.write('%s\n' % self.app.c_main.itemcget(self.tl_blocks[i][2], 'text'))

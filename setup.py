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
        self.clock_window = None
        self.app = root
        self.is_clock_window_on = False
        self.recent_blocks = []

        self.new_block = []
        self.start_pos = []
        self.first_block_id = None

        self.timeline_positions = [100]
        self.current_pos = 0
        self.timeline_blocks = []

        self.pointer = None

        self.blocks_tl = []
        self.tag_nr = 0
        self.change = 0

    def create_setup2_window(self):
        self.recent_blocks = []
        self.app.create_c_main()
        self.app.c_main.create_text(1080, 60, text="Create focus blocks", font=("Arial", 40), fill=COL_FONT)
        self.app.c_main.create_image(1080, 100, image=create_imagetk("images/line.png", 450, 150))
        self.app.c_main.create_rectangle(50, 150, 2110, 1000, outline=COL_2, width=5)
        self.app.c_main.create_line(800, 150, 800, 1000, fill=COL_2, width=5)
        # Left block
        self.app.c_main.create_text(425, 175, font=("Arial", 30), fill=COL_FONT, text="Recently created")
        self.b_create_block = CTkButton(self.app, text="+", font=("Arial", 70), fg_color=COL_1,
                                        command=self.create_block)
        self.app.c_main.create_window(80, 970, window=self.b_create_block, height=50, width=50)

        # Right block
        self.app.c_main.create_text(1455, 175, font=("Arial", 30), fill=COL_FONT, text="Saved")

        self.blocks_from_file()
        startx = 75
        starty = 225
        i = 0
        j = 0
        for block in self.recent_blocks:
            tag_block = f"r_block{10 + i + j * 10}"
            block_id = self.app.c_main.create_rectangle(startx + i * 250, starty + 150 * j, startx + 200 + i * 250,
                                                        starty + 100 + 150 * j, fill=block[1], tags=tag_block,
                                                        outline=COL_2,
                                                        width=5)
            if self.first_block_id is None:
                self.first_block_id = block_id

            hour = int(block[0]) // 60
            minutes = int(block[0]) % 60
            timer = f"{hour if hour > 9 else '0' + str(hour)}:{minutes if minutes > 9 else '0' + str(minutes)}"
            self.app.c_main.create_text(175 + i * 250, 275 + j * 150,
                                        text=timer, font=FONT, fill=COL_FONT, tags=tag_block)
            self.app.c_main.create_text(175 + i * 250, 305 + j * 150, text=block[2], fill=COL_FONT, font=("Arial", 15),
                                        tag=tag_block, anchor="center")
            i += 1
            if i % 3 == 0:
                j += 1
                i = 0

            self.app.c_main.tag_bind(tag_block, "<B1-Motion>", self.move_block)
            self.app.c_main.tag_bind(tag_block, "<Button-1>", self.press_block)
            self.app.c_main.tag_bind(tag_block, "<ButtonRelease-1>", self.unpress_block)

        # Timeline
        self.app.c_main.create_line(50, 1190, 2060, 1190, fill=COL_2, width=5)
        self.app.c_main.create_line(2010, 1160, 2060, 1190, fill=COL_2, width=5)
        self.app.c_main.create_line(2010, 1220, 2060, 1190, fill=COL_2, width=5)

        self.app.c_main.create_line(50, 1290, 2060, 1290, fill=COL_2, width=5)
        self.app.c_main.create_line(2010, 1260, 2060, 1290, fill=COL_2, width=5)
        self.app.c_main.create_line(2010, 1320, 2060, 1290, fill=COL_2, width=5)

        self.trash = self.app.c_main.create_image(2100, 1240, image=create_imagetk("images/blocks/trash.png"),
                                                  state="hidden")

    def create_block(self):
        print(self.is_clock_window_on)
        if not self.is_clock_window_on or not self.clock_window.is_clock_on:
            self.clock_window = Clock(self)
            self.clock_window.wm_attributes("-topmost", True)
            self.is_clock_window_on = True
            self.clock_window.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):

        self.is_clock_window_on = False
        self.save_blocks_to_file()
        self.clock_window.destroy()
        self.create_setup2_window()

    def blocks_from_file(self):
        self.recent_blocks = []
        if os.path.isfile("data/blocks.txt"):
            with open("data/blocks.txt", "r") as file:
                xd = file.readlines()
                for i in range(0, len(xd), 3):
                    self.recent_blocks.append([xd[i].strip(), xd[i + 1].strip(), xd[i + 2].strip()])
        else:
            with open("data/blocks.txt", 'x'):
                pass

    def save_blocks_to_file(self):

        with open("data/blocks.txt", "r+") as file:
            lines = file.readlines()
            print(len(lines))

        new_arr = self.new_block

        if len(new_arr) == 3:
            if len(lines) < 45:
                for item in lines[:len(lines)]:
                    new_arr.append(item.strip())
            else:
                for item in lines[:42]:
                    new_arr.append(item.strip())

            with open('data/blocks.txt', 'w+') as file:
                for element in new_arr:
                    file.write('%s\n' % element)

    def move_block(self, e):
        self.change = self.current_pos
        block = (e.widget.find_withtag("current")[0])

        element = (block - self.first_block_id) % 3
        if 1090 < e.y < 1390:
            self.app.c_main.itemconfigure(self.pointer, state='normal')
            self.app.c_main.moveto(block - element, e.x - 100, 1187)
            self.app.c_main.moveto(block - element + 1, e.x - 50, 1220)
            self.app.c_main.coords(block - element + 2, e.x, 1270)
            i = 0
            for pos in self.timeline_positions:
                if e.x - 100 <= pos < e.x + 100:
                    self.app.c_main.coords(self.pointer, self.timeline_positions[i], 1140,
                                           self.timeline_positions[i],
                                           1340)
                    self.change = i

                i += 1
        else:
            self.app.c_main.moveto(block - element, e.x - 100, e.y - 50)
            self.app.c_main.moveto(block - element + 1, e.x - 50, e.y - 20)
            self.app.c_main.coords(block - element + 2, e.x, e.y + 35)
            if self.pointer is not None:
                self.app.c_main.itemconfigure(self.pointer, state='hidden')
        self.app.c_main.tag_raise(block - element)
        self.app.c_main.tag_raise(block - element + 1)
        self.app.c_main.tag_raise(block - element + 2)

    def press_block(self, e):

        self.pointer = self.app.c_main.create_line(self.timeline_positions[self.current_pos], 1140,
                                                   self.timeline_positions[self.current_pos],
                                                   1340, fill="#155255", width=5, state="hidden")

        block = ((e.widget.find_withtag("current")[0]) - self.first_block_id) / 3
        i = int(block % 3)
        j = int(block // 3)
        self.start_pos = [75 + i * 250, 225 + 150 * j]

    def unpress_block(self, e):

        if self.pointer is not None:
            self.app.c_main.itemconfigure(self.pointer, state='hidden')

        block = (e.widget.find_withtag("current")[0])

        element = (block - self.first_block_id) % 3

        self.app.c_main.moveto(block - element, self.start_pos[0], self.start_pos[1])
        self.app.c_main.moveto(block + 1 - element, self.start_pos[0] + 50, self.start_pos[1] + 30)
        self.app.c_main.coords(block + 2 - element, self.start_pos[0] + 100, self.start_pos[1] + 85)

        if 1090 < e.y < 1390:
            tag = f"tl{self.tag_nr}"
            self.tag_nr += 1

            col = self.app.c_main.itemcget(block - element, 'fill')
            timer = self.app.c_main.itemcget(block + 1 - element, 'text')
            text = self.app.c_main.itemcget(block + 2 - element, 'text')

            block = self.app.c_main.create_rectangle(self.timeline_positions[self.current_pos], 1190,
                                                     self.timeline_positions[self.current_pos] + 200,
                                                     1290, fill=col, outline=COL_2, width=5, tags=tag)

            block_time = self.app.c_main.create_text(self.timeline_positions[self.current_pos] + 100, 1240,
                                                     text=timer, font=FONT, fill=COL_FONT, tags=tag)
            block_text = self.app.c_main.create_text(self.timeline_positions[self.current_pos] + 100, 1270,
                                                     text=text, font=("Arial", 15), fill=COL_FONT, tags=tag)

            self.app.c_main.tag_bind(tag, "<B1-Motion>", self.tl_move_block)

            self.app.c_main.tag_bind(tag, "<Button-1>", self.tl_press_block)
            self.app.c_main.tag_bind(tag, "<ButtonRelease-1>", self.tl_unpress_block)

            self.blocks_tl.append([block, block_time, block_text])

            self.timeline_positions.append(self.timeline_positions[self.current_pos] + 200)
            self.current_pos += 1

            self.element = len(self.blocks_tl)

            if self.element > 0:
                new_tl = self.blocks_tl[:self.change]
                new_tl.append(self.blocks_tl[self.element - 1])
                for item in self.blocks_tl[self.change:self.element-1]:
                    new_tl.append(item)
                for item in self.blocks_tl[self.element + 1:]:
                    new_tl.append(item)

                self.tl_shift(new_tl)

    def tl_move_block(self, e):
        self.element = 0
        block = (e.widget.find_withtag("current")[0])
        for i in range(len(self.blocks_tl)):
            for j in range(3):
                if self.blocks_tl[i][j] == block:
                    self.element = i
                    break

        if 1090 < e.y < 1390:
            self.app.c_main.itemconfigure(self.pointer, state='normal')
            self.app.c_main.moveto(self.blocks_tl[self.element][0], e.x - 100, 1187)
            self.app.c_main.moveto(self.blocks_tl[self.element][1], e.x - 50, 1220)
            self.app.c_main.coords(self.blocks_tl[self.element][2], e.x, 1270)

            i = 0
            for pos in self.timeline_positions:
                if e.x - 100 <= pos < e.x + 100:
                    self.app.c_main.coords(self.pointer, self.timeline_positions[i], 1140,
                                           self.timeline_positions[i],
                                           1340)

                    self.change = i
                i += 1
        if e.x > 2000:
            self.app.c_main.itemconfigure(self.blocks_tl[self.element][0], outline="red")
        else:
            self.app.c_main.itemconfigure(self.blocks_tl[self.element][0], outline=COL_2)

    def tl_press_block(self, e):
        self.app.c_main.itemconfigure(self.pointer, state='normal')
        self.element = 0
        block = (e.widget.find_withtag("current")[0])
        for i in range(len(self.blocks_tl)):
            for j in range(3):
                if self.blocks_tl[i][j] == block:
                    self.element = i
                    break

        self.app.c_main.itemconfigure(self.trash, state="normal")

    def tl_unpress_block(self, e):
        self.app.c_main.itemconfigure(self.trash, state="hidden")
        self.app.c_main.itemconfigure(self.pointer, state='hidden')
        self.app.c_main.itemconfigure(self.blocks_tl[self.element][0], outline=COL_2)

        colors = []
        texts = []
        times = []
        new_tl = []

        self.app.c_main.coords(self.blocks_tl[self.element][0], self.timeline_positions[self.element], 1190,
                               self.timeline_positions[self.element] + 200, 1290)
        self.app.c_main.coords(self.blocks_tl[self.element][1], self.timeline_positions[self.element] + 100, 1240)
        self.app.c_main.coords(self.blocks_tl[self.element][2], self.timeline_positions[self.element] + 100, 1270)

        if e.x > 2000:

            self.change = len(self.blocks_tl)
            new_tl = self.blocks_tl[:self.element]
            for item in self.blocks_tl[self.element + 1:self.change]:
                new_tl.append(item)
            new_tl.append(self.blocks_tl[self.element])
            for item in self.blocks_tl[self.change:]:
                new_tl.append(item)

            for i in range(len(new_tl)):
                block_col = self.app.c_main.itemcget(new_tl[i][0], 'fill')
                colors.append(block_col)
                block_text = self.app.c_main.itemcget(new_tl[i][1], 'text')
                texts.append(block_text)
                block_time = self.app.c_main.itemcget(new_tl[i][2], 'text')
                times.append(block_time)
            self.current_pos -= 1
            self.timeline_positions.pop(-1)

            for i in range(len(new_tl)):
                self.app.c_main.itemconfigure(self.blocks_tl[i][0], fill=colors[i])
                self.app.c_main.itemconfigure(self.blocks_tl[i][1], text=texts[i])
                self.app.c_main.itemconfigure(self.blocks_tl[i][2], text=times[i])

            self.app.c_main.delete(self.blocks_tl[-1][0])
            self.app.c_main.delete(self.blocks_tl[-1][1])
            self.app.c_main.delete(self.blocks_tl[-1][2])
            self.blocks_tl.pop(-1)

        elif self.element != self.change:
            if self.element > self.change:
                new_tl = self.blocks_tl[:self.change]
                new_tl.append(self.blocks_tl[self.element])
                for item in self.blocks_tl[self.change:self.element]:
                    new_tl.append(item)
                for item in self.blocks_tl[self.element + 1:]:
                    new_tl.append(item)
            else:
                new_tl = self.blocks_tl[:self.element]
                for item in self.blocks_tl[self.element + 1:self.change]:
                    new_tl.append(item)
                new_tl.append(self.blocks_tl[self.element])
                for item in self.blocks_tl[self.change:]:
                    new_tl.append(item)

            self.tl_shift(new_tl)

    def tl_shift(self, arr):
        print(arr)
        colors = []
        texts = []
        times = []

        for i in range(len(arr)):
            print("xd")
            block_col = self.app.c_main.itemcget(arr[i][0], 'fill')
            colors.append(block_col)
            block_text = self.app.c_main.itemcget(arr[i][1], 'text')
            texts.append(block_text)
            block_time = self.app.c_main.itemcget(arr[i][2], 'text')
            times.append(block_time)

        for i in range(len(arr)):
            self.app.c_main.itemconfigure(self.blocks_tl[i][0], fill=colors[i])
            self.app.c_main.itemconfigure(self.blocks_tl[i][1], text=texts[i])
            self.app.c_main.itemconfigure(self.blocks_tl[i][2], text=times[i])

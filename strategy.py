from actions import *
from settings import *
from customtkinter import *


class Strategy:
    def __init__(self, root):
        self.app = root

        self.move_diff = [0, 0]
        self.position = [1030, 700]
        self.end = [1030, 700]

        self.blocks = []
        self.blocks_from_file()

    def create_strategy_window(self):
        self.app.page = 4
        self.app.create_c_main()

        self.app.c_main.create_text(1080, 60, text="Life Strategy", font=FONT, fill=COL_FONT)
        self.app.c_main.create_line(870, 100, 1290, 100, fill=COL_2, width=8)
        self.frame = CTkFrame(master = self.app, width = 2060, height=1170)
        self.frame.grid(row = 0, column = 1)

        self.c_bg = CTkCanvas(self.frame, width = 2060, height=1170, bg="#2B2B2B", highlightthickness=0)
        self.c_bg.grid(row=0, column= 0)
        self.c_bg.bind("<B1-Motion>", self.bg_move)
        self.c_bg.bind("<Button-1>", self.bg_press)
        self.c_bg.bind("<ButtonRelease-1>", self.bg_unpress)


        for block in self.blocks:
            widget_id = self.c_bg.create_rectangle(block.start_pos[0], block.start_pos[1], block.start_pos[0] + 100,
                                                   block.start_pos[1] + 70, fill=block.color)
            block.widget_id = widget_id




    def blocks_from_file(self):
        if os.path.isfile("data/strategy.txt"):
            with open("data/strategy.txt", "r") as f:
                lines = f.readlines()
                print(lines)
                if len(lines) != 0:
                    for i in range(0, len(lines), 4):
                        if lines[i] != "":
                            block = Block(lines[i].strip(), lines[i+1].strip(), [int(lines[i+2].strip()), int(lines[i+3].strip())])
                            self.blocks.append(block)



    def bg_press(self, e):
        self.move_start = [e.x, e.y]


    def bg_move(self, e):
        self.move_diff = [e.x - self.move_start[0], e.y - self.move_start[1]]

        for block in self.blocks:
            block.start_pos = [block.end_pos[0] - self.move_diff[0], block.end_pos[1] - self.move_diff[1]]
            self.c_bg.coords(block.widget_id, block.start_pos[0], block.start_pos[1],  block.start_pos[0]+100, block.start_pos[1] + 70)
        # self.position = [self.end[0] - self.move_diff[0], self.end[1] - self.move_diff[1]]
        # self.c_bg.coords(self.test, self.position[0], self.position[1], self.position[0] + 100, self.position[1] + 70)
    def bg_unpress(self, e):
        for block in self.blocks:
            block.end_pos = [block.end_pos[0] - self.move_diff[0], block.end_pos[1] - self.move_diff[1]]
        # self.end = [self.end[0] - self.move_diff[0], self.end[1] - self.move_diff[1]]
        pass

class Block:
    def __init__(self, text, color, start):
        self.text = text
        self.color = color
        self.start_pos = start
        self.end_pos = start
        self.widget_id = []
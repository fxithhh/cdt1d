import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont

from timeit import default_timer as timer
from tkinter.constants import CURRENT

import gameclasses as gc
import check_value as cv


class MainApp(gc.GameRoot):
    """Main app class.

    Inherits:
        gc.GameRoot
        
    Members:
        difficulty [int]: Currently selected difficulty level of the game. [0, 1, 2] Easy -> Hard.
    """

    difficulty: int = 1

    def __init__(self, width, height, animation_fps, frames_list, *args, **kwargs):
        super().__init__(width, height, animation_fps, frames_list, *args, **kwargs)
        
        self.content_font = tkFont.Font(family='Comic Sans Ms', size=18, weight="bold")
        
        self.load_frames()
        
        self.show_frame(MainMenuFrame)

class MainMenuFrame(gc.GameFrame):
    """Main menu page.

    Inherits:
        gc.GameFrame
    """
   
    def __init__(self, parent, root):
        super().__init__(parent, root)
        
        
        self.background_image = tk.PhotoImage(file="./assets/home_bg.png")
        self.canvas.create_image(400, 300, anchor=tk.CENTER, image=self.background_image)

        # self.canvas.pack()
        # label = tk.Label(self, text="This is the start page", font=root.title_font)
        # label.pack(side="top", fill="x", pady=10)
        style = ttk.Style()
        style.configure("C.TButton", font=root.content_font, background = '#ff7733', foreground = '#cc0000')
        style.map("C.TButton",
                  foreground=[('active', '#006622')],
                  background=[('active', '#00cc44')])
        
        # create button
        startBtn = ttk.Button(self, text="Start", style="C.TButton",
                              command=lambda: root.show_frame(DifficultyFrame))
        startBtn.grid(row=0, column=0, rowspan= 5, pady=(80, 0))


class DifficultyFrame(gc.GameFrame):
    """Difficulty selection page.

    Inherits:
        gc.GameFrame
    """

    def __init__(self, parent, root):
        super().__init__(parent, root)

        # Title for difficulty level
        label = tk.Label(self, text="Choose a Difficulty Level!",
                         font=root.title_font, foreground="yellow", background="black")
        label.grid(row=0, column=0, pady=(25, 25))

        # style easy medium hard buttons
        style = ttk.Style()
        style.configure("TButton", font=root.content_font)
        style.map("TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'white')])

        def all_fn(val):
            root.show_frame(GameFrame)
            root.difficulty = val
            print(val)

        # easy medium hard level buttons
        buttonEasy = ttk.Button(self, text="Easy", style="TButton",
                                command=lambda: all_fn(1))

        buttonMed = ttk.Button(self, text="Medium", style="TButton",
                               command=lambda: all_fn(2))

        buttonHard = ttk.Button(self, text="Hard", style="TButton",
                                command=lambda: all_fn(3))

        buttonEasy.grid(row=1, column=0, pady=(25,25))
        buttonMed.grid(row=2, column=0, pady=(25,25))
        buttonHard.grid(row=3, column=0, pady=(25,25))


class GameFrame(gc.GameFrame):
    """Main game page.

    Inherits:
        gc.GameFrame
    """
    
    start_time: float = 0
    scroll_speed: int = 200
    
    cat_sequence: list = [
        r'assets/Cat_frame01.png',
        r'assets/Cat_frame02.png',
        r'assets/Cat_frame03.png',
        r'assets/Cat_frame04.png',
        r'assets/Cat_frame05.png',
        r'assets/Cat_frame06.png',
        r'assets/Cat_frame07.png',
        r'assets/Cat_frame08.png',
    ]
    mouse_sequence = [
        r'assets/Mouse_frame01.png',
        r'assets/Mouse_frame02.png',
        r'assets/Mouse_frame03.png',
        r'assets/Mouse_frame04.png',
        r'assets/Mouse_frame05.png',
        r'assets/Mouse_frame06.png',
        r'assets/Mouse_frame07.png',
        r'assets/Mouse_frame08.png',
    ]

    def __init__(self, parent, root):
        super().__init__(parent, root)
        self.root = root
        
        # Title Label
        self.label = tk.Label(self, text="Unscramble the WORD", font=root.content_font)
        self.label.place(x=400, y=200, anchor='s')
        
        self.ans_canvas = tk.Canvas(self)
        self.ans_canvas.place(x=400, y=220, width=800, height=44, anchor='n')
        
        self.background1 = gc.Sprite(0, 0, self.canvas, r'assets/Background_Long.png', anchor=tk.NW)
        self.background2 = gc.Sprite(1600, 0, self.canvas, r'assets/Background_Long.png', anchor=tk.NW)
        
        self.animated_cat = gc.AnimatedSprite(root, 200, 500, self.canvas, self.cat_sequence, subsample=2)
        self.animated_mouse = gc.AnimatedSprite(root, 500, 550, self.canvas, self.mouse_sequence, subsample=4)
        
        # Debug button (goes to end screen)
        button = tk.Button(self, text="End Game", command=lambda: root.show_frame(EndWinFrame))
        button.grid(row=2, column=2, sticky='se')
        
        self.enabled = False

        self.root.update_event.append(self.update)
    
    def on_enable(self) -> None:
        print(cv.set_current_list(self.root.difficulty))
        self.start_time = timer()
        
    def update(self):
        if not self.enabled: return
    
        c_time = timer() - self.start_time
        
        self.canvas.coords(self.background1.sprite, int(-((c_time*self.scroll_speed + 1600) % 3200) + 1600), 0)
        self.canvas.coords(self.background2.sprite, int(-((c_time*self.scroll_speed) % 3200) + 1600), 0)

class EndWinFrame(gc.GameFrame):
    """Ending page on win.

    Inherits:
        gc.GameFrame
    """

    def __init__(self, parent, root):
        super().__init__(parent, root)
        self.background_image2 = tk.PhotoImage(file="./assets/8x6.png")
        label = tk.Label(self, text="You Win!",
                         font=root.title_font,
                         image=self.background_image2,
                         compound = "center")
        label.grid(row=0, column=0, sticky="nsew")
        
        # styling buttons
        style = ttk.Style()
        style.configure("TButton", font=root.content_font)
        style.map("TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'white')])
        button = ttk.Button(self, text="Play Again",
                           command=lambda: root.show_frame(MainMenuFrame))
        button.grid(row=0, column=0, pady=(100,0))

class EndLoseFrame(gc.GameFrame):
    """Ending page on lose.

    Inherits:
        gc.GameFrame
    """

    def __init__(self, parent, root):
        super().__init__(parent, root)
        self.background_image3 = tk.PhotoImage(file="./assets/house.png")
        label = tk.Label(self, text="You ded lol",
                         font=root.title_font,
                         image = self.background_image3,
                         compound = "center")
        label.grid(row=0, column=0, sticky="nsew")

        # styling buttons
        style = ttk.Style()
        style.configure("TButton", font=root.content_font)
        style.map("TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'white')])
        button = ttk.Button(self, text="Try Again!", command=lambda: root.show_frame(MainMenuFrame))
        button.grid(row=1, column=0)

if __name__ == '__main__':
    width, height = 800, 600
    animation_fps = 30
    frame_list = [MainMenuFrame, DifficultyFrame, GameFrame, EndWinFrame, EndLoseFrame]
    
    app = MainApp(width, height, animation_fps, frame_list)
    app.resizable(False, False)
    app.mainloop()

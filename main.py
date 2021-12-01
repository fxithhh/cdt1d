import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont

from timeit import default_timer as timer

import gameclasses as gc
import GameScrambled as game


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
        self.background = gc.Sprite(0, 0, self.canvas, r'assets/Difficulty_page.png', anchor=tk.NW)
        label = tk.Label(self, text="Choose a Difficulty Level!",
                         font=root.title_font, foreground="Black", background = "#c3eeff", height=2)
        label.grid(row=0, column=0, pady=(40, 0))

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

        buttonEasy.grid(row=1, column=0, pady=(60,25))
        buttonMed.grid(row=2, column=0, pady=(25,25))
        buttonHard.grid(row=3, column=0, pady=(25,25))


class GameFrame(gc.GameFrame):
    """Main game page.

    Inherits:
        gc.GameFrame
    """
    
    start_time: float = 0
    scroll_speed: int = 500
    
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
    
    begin_anim_playing: bool = False
    begin_anim_start: float = 0
    end_anim_playing: bool = False
    end_anim_start: float = 0
    
    game_instance = None

    def __init__(self, parent, root):
        super().__init__(parent, root)
        self.root = root
        
        # Title Label
        self.label = tk.Label(self, text="Unscramble the WORD", font=root.content_font)
        self.label.place(x=400, y=200, anchor='s')
        
        self.ans_canvas = tk.Canvas(self)
        self.ans_canvas.place(x=400, y=220, width=800, height=88, anchor='n')
        
        self.background1 = gc.Sprite(0, 0, self.canvas, r'assets/Background_Long.png', anchor=tk.NW)
        self.background2 = gc.Sprite(1600, 0, self.canvas, r'assets/Background_Long.png', anchor=tk.NW)
        
        self.animated_cat = gc.AnimatedSprite(root, 200, 500, self.canvas, self.cat_sequence, subsample=2)
        self.animated_mouse = gc.AnimatedSprite(root, 500, 550, self.canvas, self.mouse_sequence, subsample=4)
        
        self.tree = gc.Sprite(100, 590, self.canvas, r'assets/tree.png', anchor=tk.S)
        self.house = gc.Sprite(1200, 590, self.canvas, r'assets/house.png', anchor=tk.S)
        
        # Score display
        self.score_label = tk.Label(self, text="Score: 0", font=root.content_font, background='#C3EEFF')
        self.score_label.grid(row=0, column=0, sticky='nw', padx=12, pady=12)
        
        # Debug button (goes to end screen)
        button = tk.Button(self, text="End Game", command=lambda: root.show_frame(EndWinFrame), foreground = "red", background="#C3EEFF", font="Papyrus")
        button.grid(row=0, column=2, sticky='se')
        
        self.enabled = False

        self.root.update_event.append(self.update)
    
    def on_enable(self) -> None:
        self.start_time = timer()
        self.begin_starting_animation()
        self.game_instance = game.GameScrambled(self.root.difficulty)
        self.game_instance.initiate_game()
        
    def begin_starting_animation(self) -> None:
        self.begin_anim_playing = True
        self.canvas.coords(self.tree.sprite, 200, 590)
        self.begin_anim_start = timer()
        
    def begin_ending_animation(self) -> None:
        self.end_anim_playing = True
        self.canvas.coords(self.house.sprite, 1200, 590)
        self.end_anim_start = timer()
        
    def update(self):
        if not self.enabled: return
    
        c_time = self.get_time()
        
        self.canvas.coords(self.background1.sprite, int(-((c_time*self.scroll_speed + 1600) % 3200) + 1600), 0)
        self.canvas.coords(self.background2.sprite, int(-((c_time*self.scroll_speed) % 3200) + 1600), 0)
        
        if self.begin_anim_playing:
            c_begin_time = timer() - self.begin_anim_start
            new_x = 200 - c_begin_time*self.scroll_speed
            self.canvas.coords(self.tree.sprite, new_x, 590)
            self.begin_anim_playing = new_x > -300
        
        if self.end_anim_playing:
            c_end_time = timer() - self.begin_anim_start
            new_x = 1200 - c_end_time*self.scroll_speed
            self.canvas.coords(self.house.sprite, new_x, 590)
            self.end_anim_playing = new_x > 420
        
    def get_time(self) -> float:
        return timer() - self.start_time

class EndWinFrame(gc.GameFrame):
    """Ending page on win.

    Inherits:
        gc.GameFrame
    """

    def __init__(self, parent, root):
        super().__init__(parent, root)
        self.background_image2 = tk.PhotoImage(file="./assets/You Win.png")
        label = tk.Label(self, image=self.background_image2,
                         compound = "center")
        label.grid(row=0, column=0)
        
        # styling buttons
        style = ttk.Style()
        style.configure("TButton", font=root.content_font)
        style.map("TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'white')])
        button = ttk.Button(self, text="Play Again",
                           command=lambda: root.show_frame(MainMenuFrame))
        button.grid(row=0, column=0)

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
    animation_fps = 60
    frame_list = [MainMenuFrame, DifficultyFrame, GameFrame, EndWinFrame, EndLoseFrame]
    
    app = MainApp(width, height, animation_fps, frame_list)
    app.resizable(False, False)
    app.mainloop()

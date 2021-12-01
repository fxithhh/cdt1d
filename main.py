import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont

import gameclasses as GC

# Import word list
import wordlist


class MainApp(GC.GameRoot):
    """Main app class.

    Inherits:
        GC.GameRoot
        
    Members:
        difficulty [int]: Currently selected difficulty level of the game. [0, 1, 2] Easy -> Hard.
    """

    difficulty: int = 1

    def __init__(self, width, height, frame_delay, frames_list, *args, **kwargs):
        super().__init__(width, height, frame_delay, frames_list, *args, **kwargs)

        self.title_font = tkFont.Font(
            family='Papyrus', size=18, weight="bold", slant="italic")
        
        self.show_frame(MainMenuFrame)

class MainMenuFrame(GC.GameFrame):
    """Main menu page.

    Inherits:
        GC.GameFrame
    """
   
    def __init__(self, parent, root):
        super().__init__(parent, root)
        
        
        self.background_image = tk.PhotoImage(file="giphy.gif")
        self.canvas.create_image(400, 300, anchor=tk.CENTER, image=self.background_image)
        
        button1 = tk.Button(self, text="Start",
                            command=lambda: root.show_frame(DifficultyFrame))

        # self.canvas.pack()
        # label = tk.Label(self, text="This is the start page", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)
        style = ttk.Style()
        style.configure("C.TButton", font=controller.content_font)
        style.map("C.TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'white')])
        
        # create button
        startBtn = ttk.Button(self, text="Start", style="C.TButton",
                              command=lambda: root.show_frame(DifficultyFrame))
        startBtn.grid(row=0, column=0)


class DifficultyFrame(GC.GameFrame):
    """Difficulty selection page.

    Inherits:
        GC.GameFrame
    """

    def __init__(self, parent, root):
        super().__init__(parent, root)

        # Title for difficulty level
        label = tk.Label(self, text="Choose a Difficulty Level!",
                         font=root.title_font, foreground="yellow", background="black")
        label.grid(row=0, column=0, sticky="nsew")

        # style easy medium hard buttons
        style = ttk.Style()
        style.configure("TButton", font=controller.content_font)
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

        buttonEasy.grid(row=0, column=0)
        buttonMed.grid(row=0, column=0)
        buttonHard.grid(row=0, column=0)


class GameFrame(GC.GameFrame):
    """Main game page.

    Inherits:
        GC.GameFrame
    """

    def __init__(self, parent, root):
        super().__init__(parent, root)
        
        label = tk.Label(self, text="Unscramble the words",
                         font=root.title_font)
        label.grid(row=0, column=0, sticky="nsew")
        button = tk.Button(self, text="End Game",
                           command=lambda: root.show_frame(EndWinFrame))
        button.grid(row=0, column=0)
        


class EndWinFrame(GC.GameFrame):
    """Ending page on win.

    Inherits:
        GC.GameFrame
    """

    def __init__(self, parent, root):
        super().__init__(parent, root)
        
        label = tk.Label(self, text="You Win!",
                         font=root.title_font)
        label.grid(row=0, column=0, sticky="nsew")
        button = tk.Button(self, text="Play Again",
                           command=lambda: root.show_frame(MainMenuFrame))
        button.grid(row=0, column=0)


class EndLoseFrame(GC.GameFrame):
    """Ending page on lose.

    Inherits:
        GC.GameFrame
    """

    def __init__(self, parent, root):
        super().__init__(parent, root)
        
        label = tk.Label(self, text="You ded lol",
                         font=root.title_font)
        label.grid(row=0, column=0, sticky="nsew")
        button = tk.Button(self, text="Try Again!",
                           command=lambda: root.show_frame(MainMenuFrame))
        button.grid(row=0, column=0)

if __name__ == '__main__':
    width, height = 800, 600
    frame_delay = 1000//60
    frame_list = [MainMenuFrame, DifficultyFrame, GameFrame, EndWinFrame, EndLoseFrame]
    
    app = MainApp(width, height, frame_delay, frame_list)
    app.mainloop()

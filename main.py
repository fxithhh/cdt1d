import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
# import list of words
from wordlist import *



class MainApp(tk.Tk):
    """Main app class.

    Inherits:
        tk.Tk
    """

    difficulty = 0

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(
            family='Papyrus', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainMenuFrame, DifficultyFrame, GameFrame, EndWinFrame, EndLoseFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainMenuFrame")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class MainMenuFrame(tk.Frame):
    """Main menu page.

    Inherits:
        tk.Frame
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Button styling
        style = ttk.Style()
        style.map("C.TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'white')]
                  )
        # create button
        startBtn = ttk.Button(self, text="Start", style="C.TButton",
                              command=lambda: controller.show_frame(
                                  "DifficultyFrame")
                              )
        startBtn.pack()


class DifficultyFrame(tk.Frame):
    """Difficulty selection page.

    Inherits:
        tk.Frame
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Title for difficulty level
        label = tk.Label(self, text="Choose a Difficulty Level!",
                         font=controller.title_font, foreground="yellow", background="black")
        label.pack(side="top", fill="x", pady=10)

        # style easy medium hard buttons
        style = ttk.Style()
        style.map("TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'white')]
                  )

        
        def all_fn(val):
            controller.show_frame("GameFrame")
            controller.difficulty = val
            print(val)
           
        # easy medium hard level buttons
        buttonEasy = ttk.Button(self, text="Easy", style="TButton",
                                command=lambda: all_fn(1))

        buttonMed = ttk.Button(self, text="Medium", style="TButton",
                               command=lambda: all_fn(2))

        buttonHard = ttk.Button(self, text="Hard", style="TButton",
                                command=lambda: all_fn(3))

        buttonEasy.pack()
        buttonMed.pack()
        buttonHard.pack()


class GameFrame(DifficultyFrame, tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Unscramble the words",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="End Game",
                           command=lambda: controller.show_frame("EndWinFrame"))
        button.pack()
        


class EndWinFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="You Win!",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Play Again",
                           command=lambda: controller.show_frame("MainMenuFrame"))
        button.pack()


class EndLoseFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="You ded lol",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Try Again!",
                           command=lambda: controller.show_frame("MainMenuFrame"))
        button.pack()


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()

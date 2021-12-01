import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from PIL import ImageTk


class MainApp(tk.Tk):
    """Main app class.

    Inherits:
        tk.Tk
    """
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(
            family='Segoe UI', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (MainMenuFrame, DifficultyFrame, GameFrame):
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
        # waiting for png files
        C = tk.Canvas(self, bg='blue', height=500, width=500)
        background_image = ImageTk.PhotoImage(file='./assets/home-bg.jpg')
        background_label = tk.Label(self, image=background_image)
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        button1 = tk.Button(self, text="Start",
                            command=lambda: controller.show_frame("DifficultyFrame"))
        # button2 = tk.Button(self, text="Go to Page Two",
        #                     command=lambda: controller.show_frame("GameFrame"))
        C.pack()
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        style = ttk.Style()
        style.map("C.TButton",
        foreground=[('pressed', 'red'), ('active', 'blue')],
        background=[('pressed', '!disabled', 'black'), ('active', 'white')]
        )
        button1 = ttk.Button(self, text="Go to Page One", style="C.TButton",
                            command=lambda: controller.show_frame("DifficultyFrame")
                            )
        # button2 = ttk.Button(self, text="Go to Page Two", style="C.TButton",    
        #                     command=lambda: controller.show_frame("GameFrame"))
                            
        button1.pack()
        # button2.pack()


class DifficultyFrame(tk.Frame):
    """Difficulty selection page.

    Inherits:
        tk.Frame
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Choose a Difficulty Level!", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        # easy medium hard level buttons
        buttonEasy = tk.Button(self, text="Easy",
                           command=lambda: controller.show_frame("GameFrame"))
        
        buttonMed = tk.Button(self, text="Medium",
                           command=lambda: controller.show_frame("GameFrame"))
        
        buttonHard = tk.Button(self, text="Hard",
                           command=lambda: controller.show_frame("GameFrame"))

        buttonEasy.pack()
        buttonMed.pack()
        buttonHard.pack()


class GameFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("MainMenuFrame"))
        button.pack()


class EndWinFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("MainMenuFrame"))
        button.pack()


class EndLoseFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is page 2",
                         font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("MainMenuFrame"))
        button.pack()


if __name__ == '__main__':
    app = MainApp()
    app.mainloop()

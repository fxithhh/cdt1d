import tkinter as tk
from tkinter import font as tkfont


class AnimationTest(tk.Frame):
    """Main menu page.

    Inherits:
        tk.Frame
    """
    
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        
        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        canvas = tk.Canvas(self, width=300, height=200, background='white')
        canvas.grid(row=0, column=0, sticky="nsew")
        self.show_image(canvas)
    
    def show_image(self, canvas):
        self.cat_img = tk.PhotoImage(file=r'assets/Cat_frame01.png')
        self.cat_img = self.cat_img.subsample(2, 2)
        canvas.create_image(150, 100, image=self.cat_img, anchor=tk.CENTER)

class MainApp(tk.Tk):
    """Main app class.
    
    Inherits:
        tk.Tk
    """
    
    # Frame list
    F_LIST: tuple = (AnimationTest,)
    
    # Window sizes
    width: int = 800
    height: int = 600

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Segoe UI', size=18, weight="bold")
        
        # Window size
        self.geometry(f'{self.width}x{self.height}')

        # The container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Put all of the pages in the same location;
        # the one on the top of the stacking order
        # will be the one that is visible.
        self.frames = {}
        for F in self.F_LIST:
            page_name = F.__name__
            frame = F(parent=container, root=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Show the default frame
        self.show_frame(AnimationTest)

    def show_frame(self, page_class: tk.Tk):
        '''Show a frame for the given page class.'''
        if page_class.__name__ in self.frames:
            frame = self.frames[page_class.__name__]
            frame.tkraise()

if __name__ == '__main__':
    app = MainApp()
    app.mainloop()
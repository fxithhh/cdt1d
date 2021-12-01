import tkinter as tk
from tkinter import font as tkfont


class AnimationFrame(tk.Frame):
    """Main menu page.

    Inherits:
        tk.Frame
    """
    
    delay: int = 1000//30
    image_sequence: str = [
        r'assets/Cat_frame01.png',
        r'assets/Cat_frame02.png',
        r'assets/Cat_frame03.png',
        r'assets/Cat_frame04.png',
        r'assets/Cat_frame05.png',
        r'assets/Cat_frame06.png',
        r'assets/Cat_frame07.png',
        r'assets/Cat_frame08.png',
    ]
    current_seq_index: int = 0
    paused: bool = False
    
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        
        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.canvas = tk.Canvas(self, background='white')
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        self.update()
    
    def show_image(self, x: int, y: int, image_file: str):
        self.cat_img = tk.PhotoImage(file=image_file)
        self.cat_img = self.cat_img.subsample(2, 2)
        self.canvas.create_image(x, y, image=self.cat_img, anchor=tk.CENTER)
    
    def update(self):
        if self.paused:
            return

        # Rollover animation index if reached the end
        if self.current_seq_index == len(self.image_sequence): self.current_seq_index = 0
        
        # Update image
        self.show_image(100, 500, self.image_sequence[self.current_seq_index])
        
        # Update animation index
        self.current_seq_index += 1
        
        self.canvas.after(self.delay, self.update)

class GameRoot(tk.Tk):
    """Main app class.
    
    Inherits:
        tk.Tk
    """
    
    # Frame list
    F_LIST: tuple = (AnimationFrame,)
    
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
        self.show_frame(AnimationFrame)

    def show_frame(self, page_class: tk.Tk):
        '''Show a frame for the given page class.'''
        if page_class.__name__ in self.frames:
            frame = self.frames[page_class.__name__]
            frame.tkraise()

if __name__ == '__main__':
    app = GameRoot()
    app.mainloop()
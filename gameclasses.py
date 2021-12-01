import tkinter as tk
from tkinter import font as tkfont


class GameObject:
    """Base game object interface.
    
    Members:
        name [str]: Name of this object.
        enabled [bool]: Whether this GameObject is enabled. Affects the children.
        game_children [list]: List of all children to this GameObject. If a child is a subclass of GameObject, the update() function will be called on the child.
    """
    
    name: str = ""
    enabled: bool = True
    game_children: list = []
    
    def __init__(self, name):
        self.name = name
        
    def on_enable(self) -> None:
        """Called when the GameObject is enabled.
        """
        pass
    
    def on_disable(self) -> None:
        """Called when the GameObject is disabled.
        """
        pass
        
    def update(self) -> None:
        """Update function. Called every frame.
        """
        if not self.enabled: return
        for child in self.game_children:
            # Check if child object is a subclass of GameObject (and thus contains the update() function).
            if not issubclass(type(child), GameObject):
                return
            # Calls the update function on the child.
            child.update()

class AnimationFrame(GameObject, tk.Frame):
    """Main menu page.

    Inherits:
        GameObject, tk.Frame
    """
    image_sequence: list = [
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
    
    
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        
        self.root = root

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.canvas = tk.Canvas(self, background='white')
        self.canvas.grid(row=0, column=0, sticky="nsew")
        
        self.update()
    
    def update_sprite(self, x: int, y: int, image_file: str):
        """Update sprite image.

        Args:
            x (int): x position of the sprite.
            y (int): y position of the sprite.
            image_file (str): File path the image asset.
        """
        self.sprite = tk.PhotoImage(file=image_file)
        self.sprite = self.sprite.subsample(2, 2)
        self.canvas.create_image(x, y, image=self.sprite, anchor=tk.CENTER)
    
    def update(self):
        super().update()
        
        # Rollover animation index if reached the end
        if self.current_seq_index == len(self.image_sequence): self.current_seq_index = 0
        
        # Update image
        self.update_sprite(100, 500, self.image_sequence[self.current_seq_index])
        
        # Update animation index
        self.current_seq_index += 1

class GameFrame(GameObject, tk.Frame):
    """Game frame class with helpful event callbacks.

    Inherits:
        GameObject, tk.Frame
    """
    
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
            
        self.root = root

        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
            
        self.canvas = tk.Canvas(self, background='red')
        self.canvas.grid(row=0, column=0, rowspan= 5, sticky="nsew")
        
    def update(self):
        super().update()
        

class GameRoot(GameObject, tk.Tk):
    """Root game class. Calls update functions on all layouts it can.
    
    Inherits:
        GameObject, tk.Tk
    
    Members:
        f_list [list]: List of frames that represent different game screens.
        current_frame [tk.Frame]: Currently active frame.
        container [tk.Frame]: Base container to contain all the game frames.
        
        width [int]: Window width.
        height [int]: Window height.
        frame_delay [int]: Delay between update frames in ms.
    """
    
    # Frame list
    f_list: list = []
    current_frame: tk.Frame = None
    
    # Window sizes
    width: int = 800
    height: int = 600

    # Game loop settings
    frame_delay: int = 1000//30

    def __init__(self, width, height, frame_delay, frames_list, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # fonts used
        self.title_font = tkfont.Font(family='Papyrus', size=18, weight="bold")
        self.content_font = tkfont.Font(
            family='Cosmic San Ms', size=16, weight = "bold", slant="italic")

        self.width, self.height = width, height
        self.frame_delay = frame_delay
        self.f_list = frames_list
        
        # Window size
        self.geometry(f'{self.width}x{self.height}')

        # The container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Run update function
        self.update()

    def show_frame(self, page_class: tk.Tk):
        """Show a frame for the given page class.

        Args:
            page_class (tk.Tk): Page class.
        """
        if page_class.__name__ in self.frames:
            # Disable previous frame (if any)
            if self.current_frame and issubclass(type(self.current_frame), GameObject):
                self.current_frame.enabled = False
                self.current_frame.on_disable()
            
            widget = self.frames[page_class.__name__]
            widget.tkraise()
            self.current_frame = widget
            
            # Enable current frame
            if issubclass(type(self.current_frame), GameObject):
                self.current_frame.enabled = True
                self.current_frame.on_enable()
    
    def load_frames(self):
        # Put all of the pages in the same location;
        # the one on the top of the stacking order
        # will be the one that is visible.
        self.frames = {}
        self.game_children = []
        for widget_class in self.f_list:
            page_name = widget_class.__name__
            widget = widget_class(parent=self.container, root=self)
            self.frames[page_name] = widget
                
            # Add the frames to the GameObject index
            self.game_children.append(widget)
            widget.grid(row=0, column=0, sticky="nsew")
            
    def update(self):
        super().update()
        
        self.after(self.frame_delay, self.update)

if __name__ == '__main__':
    width, height = 800, 600
    frame_delay = 1000//60
    frame_list = [AnimationFrame,]
    
    app = GameRoot(width, height, frame_delay, frame_list)
    app.load_frames()
    app.show_frame(AnimationFrame)
    app.mainloop()
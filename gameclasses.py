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

class Sprite(GameObject):
    """Sprite class.

    Inherits:
        GameObject, tk.Frame
    """ 
        
    def __init__(self, x, y, canvas, sprite_image=None, anchor=tk.CENTER):
        self.x, self.y = x, y
        self.anchor = anchor
            
        self.canvas = canvas
        
        if sprite_image:
            self.update_sprite(self.x, self.y, sprite_image)
        
    def update_sprite(self, x: int, y: int, image_file: str):
        """Update sprite image.

        Args:
            x (int): x position of the sprite.
            y (int): y position of the sprite.
            image_file (str): File path the image asset.
        """
        self.sprite = tk.PhotoImage(file=image_file)
        self.sprite = self.sprite.subsample(2, 2)
        self.canvas.create_image(x, y, image=self.sprite, anchor=self.anchor)

class AnimatedSprite(Sprite):
    """Animated sprite class.

    Inherits:
        Sprite
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
    
    
    def __init__(self, root, x, y, canvas, image_sequence=image_sequence, anchor=tk.CENTER):
        super().__init__(x, y, canvas, anchor=anchor)
        self.root = root
        
        self.image_sequence = image_sequence
        self.root.update_event.append(self.update)
    
    def update(self):
        # Rollover animation index if reached the end
        if self.current_seq_index == len(self.image_sequence): self.current_seq_index = 0
        
        # Update image
        self.update_sprite(self.x, self.y, self.image_sequence[self.current_seq_index])
        
        # Update animation index
        self.current_seq_index += 1

class GameFrame(GameObject, tk.Frame):
    """Game frame class with helpful event callbacks.

    Inherits:
        GameObject, tk.Frame
    """
    
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
            
        self.canvas = tk.Canvas(self, background='red')
        self.canvas.grid(row=0, column=0, rowspan= 5, sticky="nsew")
        
        # Make sure that the canvas covers everything
        self.canvas.grid(row=0, column=0, sticky="nsew", columnspan=100, rowspan=100)
        
class DemoFrame(GameFrame):
    def __init__(self, parent, root):
        super().__init__(parent, root)
        
        mouse_sequence = [r'assets/Mouse_frame01.png',
                        r'assets/Mouse_frame02.png',
                        r'assets/Mouse_frame03.png',
                        r'assets/Mouse_frame04.png',
                        r'assets/Mouse_frame05.png',
                        r'assets/Mouse_frame06.png',
                        r'assets/Mouse_frame07.png',
                        r'assets/Mouse_frame08.png',]
                
        self.animated_cat = AnimatedSprite(root, 500, 500, self.canvas)
        self.animated_mouse = AnimatedSprite(root, 200, 500, self.canvas, mouse_sequence)
                
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
    
    update_event: list = []

    def __init__(self, width, height, animation_fps, frames_list, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Fonts used
        self.title_font = tkfont.Font(family='Papyrus', size=18, weight="bold")

        self.width, self.height = width, height
        self.animation_fps = animation_fps
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
        
        # Begin the update loop
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
    
    def get_animation_frame_delay(self) -> int:
        return 1000//self.animation_fps
    
    def update(self):
        for func in self.update_event:
            func()
        
        self.after(self.get_animation_frame_delay(), self.update)

if __name__ == '__main__':
    width, height = 800, 600
    animation_fps = 30
    frame_list = [DemoFrame,]
    
    app = GameRoot(width, height, animation_fps, frame_list)
    app.load_frames()
    app.show_frame(DemoFrame)
    app.mainloop()
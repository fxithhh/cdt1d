import tkinter as tk
from typing import *

class GameObject:
    """Base game object interface.

    Members:
        name [str]: Name of this object.
        enabled [bool]: Whether this GameObject is enabled. Affects the children.
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

    def __init__(self, x, y, canvas, sprite_image=None, subsample = None, anchor=tk.CENTER):
        self.x, self.y = x, y # x and y coordinates
        self.anchor = anchor # Sprite anchor point
        self.subsample = subsample # Shrink image by picking every Xth and Yth pixel of the image

        self.canvas = canvas # Get canvas reference this sprite will be placed on

        if sprite_image:
            self.update_sprite(self.x, self.y, sprite_image)

    def update_sprite(self, x: int, y: int, image_file: str):
        """Update sprite image.

        Args:
            x (int): x position of the sprite.
            y (int): y position of the sprite.
            image_file (str): File path the image asset.
        """

        self.sprite_image = tk.PhotoImage(file=image_file) # Set sprite image
        if self.subsample:
            self.sprite_image = self.sprite_image.subsample(self.subsample, self.subsample) # Shrink the image

        # Create animation sprite by canvas with the image in the x, y position with specified anchor point
        self.sprite = self.canvas.create_image(x, y, image=self.sprite_image, anchor=self.anchor)

class AnimatedSprite(Sprite):
    """Animated sprite class.

    Inherits:
        Sprite
    """

    # List of cat frames for the animation
    image_sequence: list = []

    # Store the index of the current frame in image_sequence, thus starting from the first frame
    current_seq_index: int = 0

    def __init__(self, root, x, y, canvas, image_sequence=image_sequence, subsample = None, anchor=tk.CENTER):
        super().__init__(x, y, canvas, subsample=subsample, anchor=anchor)
        self.root = root
        self.image_sequence = image_sequence
        self.root.update_event_handler.append(self.update)

    def update(self):
        if not self.enabled: return

        # Rollover animation index if reached the end
        self.current_seq_index += 1
        if self.current_seq_index == len(self.image_sequence): self.current_seq_index = 0

        # Update image
        self.update_sprite(self.x, self.y, self.image_sequence[self.current_seq_index])


class GameFrame(GameObject, tk.Frame):
    """Game frame class with helpful event callbacks.

    Inherits:
        GameObject, tk.Frame
    """

    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.canvas = tk.Canvas(self, background='#dddddd') #create a canvas that will host all the sprites for the cat animation
        self.canvas.grid(row=0, column=0, columnspan=5, rowspan=5, sticky="nsew") # Make sure that the canvas covers everything

class DemoFrame(GameFrame): # For testing purposes only, to make sure the animation sprite works well
    def __init__(self, parent, root):
        super().__init__(parent, root)

        # Create the mouse animation sequence
        mouse_sequence =[r'assets/Mouse_frame01.png',
                        r'assets/Mouse_frame02.png',
                        r'assets/Mouse_frame03.png',
                        r'assets/Mouse_frame04.png',
                        r'assets/Mouse_frame05.png',
                        r'assets/Mouse_frame06.png',
                        r'assets/Mouse_frame07.png',
                        r'assets/Mouse_frame08.png',]

        #create cat animation (default animation is cat)
        self.animated_cat = AnimatedSprite(root, 500, 500, self.canvas)

        #create mouse animation (substitute default image sequence with mouse image sequence)
        self.animated_mouse = AnimatedSprite(root, 200, 500, self.canvas, mouse_sequence)

class GameRoot(GameObject, tk.Tk):
    """Root game class. Calls update functions on all layouts it can.

    Inherits:
        GameObject, tk.Tk

    Members:
        f_list (list): List of frames that represent different game screens.
        current_frame (tk.Frame): Currently active frame.
        container (tk.Frame): Base container to contain all the game frames.

        width (int): Window width.
        height (int): Window height.
        frame_delay (int): Delay between update frames in ms.
        update_event_handler (List[Callable[[], None]]): All functions in this list are invoked every update frame.
    """

    # Frame list
    f_list: List[GameFrame] = []
    current_frame: tk.Frame = None

    # Window dimension
    width: int = 800
    height: int = 600

    update_event_handler: List[Callable[[], None]] = []

    def __init__(self, width, height, animation_fps, frames_list, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.width, self.height = width, height #fix the window dimensions
        self.animation_fps = animation_fps
        self.f_list = frames_list

        # Window size
        self.geometry(f'{self.width}x{self.height}')

        # We'll stack all the frames on top of each other in the container and the current frame will be raised above the others
        self.container = tk.Frame(self) #create container

        #configure the container to be at the top of the window and fill the entire space horizontally and vertically
        self.container.pack(side="top", fill="both", expand=True)

        #configure the rows and columns inside the container itself with the same width as other columns
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Begin the update loop
        self.update()

    def show_frame(self, page_class: tk.Tk) -> None:
        """Show a frame for the given page class.

        Args:
            page_class (tk.Tk): Page class.
        """

        if page_class.__name__ in self.frames:
            # Disable previous frame (if any)
            if self.current_frame and isinstance(self.current_frame, GameObject):
                self.current_frame.enabled = False
                self.current_frame.on_disable() #call back the disable frame function in the beginning

            # Create the frame widgets for each game screen
            widget = self.frames[page_class.__name__]

            # Raise the frame and bring it to the most front (in the frame stack)
            widget.tkraise()
            self.current_frame = widget

            # Enable current frame
            if isinstance(self.current_frame, GameObject):
                self.current_frame.enabled = True
                self.current_frame.on_enable()

    def load_frames(self) -> None:
        """Put all of the pages in the same location and the one on the top of the stacking order will be visible
        """

        self.frames = {}
        self.game_children = []
        for widget_class in self.f_list:
            page_name = widget_class.__name__
            widget = widget_class(parent=self.container, root=self)
            self.frames[page_name] = widget #append to the frames dictionary

            # Add the frames to the GameObject index
            self.game_children.append(widget)
            widget.grid(row=0, column=0, sticky="nsew")

    def get_animation_frame_delay(self) -> int: #the timing between the swap of each animation frame
        return 1000//self.animation_fps

    def update(self) -> None:
        # Call all subscribed update_event_handler to run the core game loop
        for func in self.update_event_handler:
            func()

        # self.after is provided by tinker where after the delay, update(self) will run again
        # which creates an update loop to run the game
        self.after(self.get_animation_frame_delay(), self.update)

if __name__ == '__main__':
    width, height = 800, 600
    animation_fps = 30
    frame_list = [DemoFrame,]

    app = GameRoot(width, height, animation_fps, frame_list)
    app.load_frames()
    app.show_frame(DemoFrame)
    app.mainloop()
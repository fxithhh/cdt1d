import tkinter as tk
from tkinter import ttk

def main() -> None:
    """Main function. Runs TKinter window and everything else.
    """
    
    window = tk.Tk()
    initialize_window(window, "Dont touch me", icon='./icon.ico')
    
    # Place a label on the root window
    for _ in range(100):
        ttk.Label(window, text="Peepeepoopoo!").pack()
    
    # Keep the window open until it is closed
    window.mainloop()

def initialize_window(window: tk.Tk, title: str, window_width: int = 300, window_height: int = 200, icon: str = None) -> None:
    """Initializes the program window.

    Args:
        window (tk.Tk): Window instance.
        title (str): Window title.
        window_width (int, optional): Window width. Defaults to 300.
        window_height (int, optional): Window height. Defaults to 200.
        icon (str, optional): Icon path. Defaults to None.
    """
    
    window.title(title)

    # Get the screen dimension
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Find the center point
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
        
    window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    
    if icon:
        window.iconbitmap(icon)

if __name__ == '__main__':
    main()
    
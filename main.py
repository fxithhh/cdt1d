import tkinter as tk


def initialize_window(window: tk.Tk, title: str, window_width: int = 300, window_height: int = 200, icon: str = None):
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

def show_typing(window: tk.Tk, label: tk.Label, text: str) -> None:
    label.config(text=text)
    label.pack()

def main() -> None:
    """Main function. Runs TKinter window and everything else.
    """

    window = tk.Tk()
    initialize_window(window, "Dont touch me", icon='./icon.ico')

    # Place a label on the root window
    message = tk.Label(window, text="Peepeepoopoo!")
    message.pack()

    # Place button
    button = tk.Button(
        text="Click me!",
        width=5,
        height=3,
        bg="blue",
        fg="yellow",
    )
    button.pack()

    # Place input
    label = tk.Label(text="Name")
    entry = tk.Entry(fg="yellow", bg="blue", width=10)
    label.pack()
    entry.pack()
    label2 = tk.Label(window)

    entry.bind('<Key>', lambda event: show_typing(window, label2, entry.get()))
  
    # Keep the window open until it is closed
    window.mainloop()

if __name__ == '__main__':
    main()

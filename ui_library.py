import tkinter as tk
import ui_library as ui

class BorderedBox(tk.Frame):
    
    def __init__(self, parent: tk.Canvas, image_file, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        
        self.parent = parent
        
        self.sprite = tk.PhotoImage(file=image_file)
        self.parent.create_image(0, 0, image=self.sprite, anchor=tk.NW)
        

if __name__ == '__main__':
    root = tk.Tk()
    
    width, height = 800, 600
                
    # Window size
    root.geometry(f'{width}x{height}')

    # The container is where we'll stack a bunch of frames
    # on top of each other, then the one we want visible
    # will be raised above the others
    
    container = tk.Frame(root)
    container.pack(side="top", fill="both", expand=True)
    canvas = tk.Canvas(container)
    canvas.grid(row=0, column=0, sticky="nsew")
    
    bbox = BorderedBox(canvas, r'assets/AnswerBox.png')
    bbox.grid(row=0, column=0)
    
    root.mainloop()
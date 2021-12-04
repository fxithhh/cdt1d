import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

from timeit import default_timer as current_time

import gameclasses as gc
import game_scrambled as game


#Create a function to check if any value is a float, returns either True or False
def is_float(element: any) -> bool:
    try:
        float(element)
        return True
    except ValueError: 
        return False



class MainApp(gc.GameRoot):
    """Main app class
    Inherits:
        gc.GameRoot
        
    Members:
        difficulty [int]: Currently selected difficulty level of the game. {Easy:1, Medium:2, Hard: 3}
    """

    #Setting variables with temporary placeholders
    difficulty: int = 1
    last_score: int = 0
    last_name: str = ""

    def __init__(self, width, height, animation_fps, frames_list, *args, **kwargs):
        super().__init__(width, height, animation_fps, frames_list, *args, **kwargs)
        
        # Loading fonts
        self.title_font = tkfont.Font(family='Comic Sans Ms', size=24, weight="bold")
        self.button_font = tkfont.Font(family='Comic Sans Ms', size=14, weight="bold")
        self.header_font = tkfont.Font(family='Comic Sans Ms', size=18, weight="bold")
        self.meme_font = tkfont.Font(family='Papyrus', size=16, weight="bold")
        self.big_meme_font = tkfont.Font(family='Papyrus', size=20, weight="bold")
        self.content_font = tkfont.Font(family='Comic Sans Ms', size=14, weight="bold")
        
        self.load_frames()
        
        self.show_frame(MainMenuFrame)


"""
--------------------------------------------------------------------------------------------------------------------------------------------------------
MAIN FRAME
--------------------------------------------------------------------------------------------------------------------------------------------------------
"""

class MainMenuFrame(gc.GameFrame):
    """Main menu page.

    Inherits:
        gc.GameFrame
    """
   
    def __init__(self, parent, root):
        super().__init__(parent, root)
        
        #Configure row 0 to be 3 times the size of row 1
        #Layout is used to arrange the start and credits button
        self.grid_rowconfigure(0, weight=3) 
        self.grid_rowconfigure(3, weight=1)

        # Setting Background
        self.background = gc.Sprite(0, 0, self.canvas, r'assets/home_bg.png', anchor=tk.NW)
        
        # Define button style
        style = ttk.Style()
        style.configure("C.TButton", font=root.button_font, background = '#ff7733', foreground='#cc0000')
        style.map("C.TButton",
                  foreground=[('active', '#006622')],
                  background=[('active', '#00cc44')])
        
        # Create start and credit buttons
        startBtn = ttk.Button(self, text="Start", style="C.TButton",
                              command=lambda: root.show_frame(DifficultyFrame)) #Redirect to difficulty page

        creditBtn = ttk.Button(self, text="Credits", style="C.TButton",
                              command=lambda: root.show_frame(CreditsFrame)) #Redirect to credits page

        instructionBtn = ttk.Button(self, text="How To Play", style="C.TButton",
                              command=lambda: root.show_frame(InstructionFrame)) #Redirect to instruction page
        
        #Layout of buttons
        startBtn.grid(row=1, column=0, pady=(15, 10), sticky='s')
        creditBtn.grid(row=2, column=0, pady=(10, 10))
        instructionBtn.grid(row=3, column=0, pady=(10,15), sticky="n")


"""
--------------------------------------------------------------------------------------------------------------------------------------------------------
CREDITS FRAME
--------------------------------------------------------------------------------------------------------------------------------------------------------
"""

class CreditsFrame(gc.GameFrame):
    """Game credit page.

    Inherits:
        gc.GameFrame
    """
    
    def __init__(self, parent, root):
        super().__init__(parent, root)
    
        # Setting Background
        self.background = gc.Sprite(0, 0, self.canvas, r'assets/home_bg.png', anchor=tk.NW)
        
        style = ttk.Style()
        style.configure("C.TButton", font=root.button_font, background='#ff7733', foreground='#cc0000')
        style.map("C.TButton",
                foreground=[('active', '#006622')],
                background=[('active', '#00cc44')])

        # Create button
        startBtn = ttk.Button(self, text="Back", style="C.TButton",
                            command=lambda: root.show_frame(MainMenuFrame)) #Return to main menu
        startBtn.grid(row=0, column=0, sticky='nw', padx=(20, 20), pady=(25, 25))
        
        # Create frame for credits
        textFrame = tk.Frame(self, background='white')
        textFrame.grid(row=0, column=0, ipady=10)
        
        # Title
        c_title_label = tk.Label(textFrame, text='Credits', font=root.title_font, background='#FFB600')
        c_title_label.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=(20, 20), pady=(15, 20))
        
        # Team title
        c_team_label = tk.Label(textFrame, text='21F01 - Team 1J', font=root.header_font, background='white')
        c_team_label.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky='w')
        
        # Everyone and their roles
        c_people = [('Seah Ying Xiang', 'Lead Developer'),
                    ('Cheng Wei Xuan', 'Gameplay Developer, Lead Artist'),
                    ('Ang Yue Sheng', 'Gameplay Developer, Artist'),
                    ('Lim Tiang Sui, Faith', 'GUI Developer, Lead UI/UX'),
                    ('Jeriah Yeo Ruei', 'GUI Developer, Content Lead')]
        
        # Create labels from c_people
        c_people_labels = [(tk.Label(textFrame, text=name, font=root.content_font, background='white'), 
                            tk.Label(textFrame, text=role, font=root.content_font, background='white')) for name, role in c_people]
        
        # Grid those labels!
        for i, person_labels in enumerate(c_people_labels):
            name_label, role_label = person_labels
            name_label.grid(row=i+2, column=0, padx=(20, 20), pady= (10, 10), sticky='w') #Add spacing between the name and the role
            role_label.grid(row=i+2, column=1, padx=(20, 20), pady= (10, 10), sticky='e')


"""
--------------------------------------------------------------------------------------------------------------------------------------------------------
INSTRUCTIONS FRAME
--------------------------------------------------------------------------------------------------------------------------------------------------------
"""

class InstructionFrame(gc.GameFrame):
    """Instruction page.

    Inherits:
        gc.GameFrame
    """
    
    def __init__(self, parent, root):
        super().__init__(parent, root)
    
        # Setting Background
        self.background = gc.Sprite(0, 0, self.canvas, r'assets/home_bg.png', anchor=tk.NW)
        
        style = ttk.Style()
        style.configure("C.TButton", font=root.button_font, background='#ff7733', foreground='#cc0000')
        style.map("C.TButton",
                foreground=[('active', '#006622')],
                background=[('active', '#00cc44')])

        # Create button
        startBtn = ttk.Button(self, text="Back", style="C.TButton",
                            command=lambda: root.show_frame(MainMenuFrame)) #Return to main menu
        startBtn.grid(row=0, column=0, sticky='nw', padx=(20, 20), pady=(30, 30))
        
        # Create frame for credits
        textFrame = tk.Frame(self, background='white')
        textFrame.grid(row=0, column=0, ipady=10)
        
        # Title
        c_title_label = tk.Label(textFrame, text='How To Play?', font=root.title_font, background='#FFB600')
        c_title_label.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=(20, 20), pady=(15, 20))
        
        # Instructions

        instruction_label1 = tk.Label(textFrame, 
                                text='~ The theme of Cat me if you can is Animals!',
                                font=root.content_font, background='white')

        instruction_label2 = tk.Label(textFrame, 
                                text='~ Unscramble the words as fast as you can to help get mousey home!',
                                font=root.content_font, background='white')

        instruction_label3 = tk.Label(textFrame, 
                                text='~ The faster you answer the questions correctly, the faster mousey will run!', 
                                font=root.content_font, background='white')

        instruction_label4 = tk.Label(textFrame, 
                                text='~ But watch out! Every wrong answer will cause mousey to run slower', 
                                font=root.content_font, background='white')

        instruction_label5 = tk.Label(textFrame, 
                                text="~ To submit your answer, press enter (Don't worry about capitalization!)",
                                font=root.content_font, background='white')

        instruction_label6 = tk.Label(textFrame, 
                                text='~ However, pressing enter without typing anything will lead to a skip!)',
                                font=root.content_font, background='white')

        #Layout of text
        instruction_label1.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky='w')
        instruction_label2.grid(row=3, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky='w')
        instruction_label3.grid(row=5, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky='w')
        instruction_label4.grid(row=7, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky='w')
        instruction_label5.grid(row=9, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky='w')
        instruction_label6.grid(row=11, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky='w')
                               

"""
--------------------------------------------------------------------------------------------------------------------------------------------------------
DIFFICULTY FRAME
--------------------------------------------------------------------------------------------------------------------------------------------------------
"""

class DifficultyFrame(gc.GameFrame):
    """Difficulty selection page.

    Inherits:
        gc.GameFrame
    """

    def __init__(self, parent, root):
        super().__init__(parent, root)

        # Creating layout for the buttons, row 0 and 3 will expand and take up remaining space based on the ratio of the weight
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(3, weight=3)
        
        # Setting Background
        self.background = gc.Sprite(0, 0, self.canvas, r'assets/Difficulty_page.png', anchor=tk.NW)

        # Title for difficulty level
        label = tk.Label(self, text="Choose a Difficulty Level!",
                         font=root.title_font, foreground="Black", background = "#c3eeff", height=2)
        label.grid(row=0, column=0, sticky='s', pady=(40, 0))

        # style easy medium hard buttons
        style = ttk.Style()
        style.configure("TButton", font=root.button_font)
        style.map("TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'white')])

        #Set value to difficulty button
        def all_fn(val):
            root.difficulty = val
            root.show_frame(GameFrame)
            print(val)

        # Setting up buttons
        buttonEasy = ttk.Button(self, text="Easy", style="TButton",
                                command=lambda: all_fn(1)) #root.difficulty = 1

        buttonMed = ttk.Button(self, text="Medium", style="TButton",
                               command=lambda: all_fn(2)) #root.difficulty = 2

        buttonHard = ttk.Button(self, text="Hard", style="TButton",
                                command=lambda: all_fn(3)) #root.difficulty = 3
       
        buttonBack = ttk.Button(self, text="Back", style = "TButton",
                                command=lambda: root.show_frame(MainMenuFrame)) #Return to main page

        buttonEasy.grid(row=1, column=0, pady=(15, 15))
        buttonMed.grid(row=2, column=0, pady=(15, 15))
        buttonHard.grid(row=3, column=0, pady=(15, 15), sticky='n')
        buttonBack.grid(row=0, column=0, padx=(15, 15), pady=(30,30), sticky='nw')


"""
--------------------------------------------------------------------------------------------------------------------------------------------------------
GAME FRAME
--------------------------------------------------------------------------------------------------------------------------------------------------------
"""
class GameFrame(gc.GameFrame):
    """Main game page.

    Inherits:
        gc.GameFrame
    """
    
    #Setting variables with some placeholder for start_time and game_end_time
    start_time: float = 0
    game_end_time: float = 0
    scroll_speed: int = 500
    
    #Container of Cat Animation Frames
    cat_sequence: list = [
        r'assets/Cat_frame01.png',
        r'assets/Cat_frame02.png',
        r'assets/Cat_frame03.png',
        r'assets/Cat_frame04.png',
        r'assets/Cat_frame05.png',
        r'assets/Cat_frame06.png',
        r'assets/Cat_frame07.png',
        r'assets/Cat_frame08.png',
    ]

    #Container of Mouse Animation Frames
    mouse_sequence = [
        r'assets/Mouse_frame01.png',
        r'assets/Mouse_frame02.png',
        r'assets/Mouse_frame03.png',
        r'assets/Mouse_frame04.png',
        r'assets/Mouse_frame05.png',
        r'assets/Mouse_frame06.png',
        r'assets/Mouse_frame07.png',
        r'assets/Mouse_frame08.png',
    ]
    
    #Set the starting x,y coordinates of the Cat and Mouse Frames
    mouse_start_x: int = 600
    mouse_start_y: int = 550
    cat_start_x: int = 200
    cat_start_y: int = 500
    
    cool_text_duration: float = 2
    cool_text_start: float = 0
    
    
    last_score: int = 0
    
    begin_anim_playing: bool = False
    begin_anim_start: float = 0

    end_anim_playing: bool = False
    end_anim_start: float = 0

    end_anim_cat_end_position: int = 0
    end_anim_catescape_duration: float = 2
    end_anim_house_duration: float = 1.8
    end_anim_mouseescape_duration: float = 3
    
    game_instance = None

    """
    -------------------------------------------------------------------------------------------------------------------------------------------------
    GUI PORTION
    -------------------------------------------------------------------------------------------------------------------------------------------------
    """

    def __init__(self, parent, root):
        super().__init__(parent, root)
        self.root = root
        
        # Question label
        self.qn_label = tk.Label(self, text='', background='white', font=root.title_font)
        self.qn_label.place(x=400, y=200, anchor='s')
        
        # Question frame
        self.ans_frame = tk.Frame(self, background='white')
        self.ans_frame.grid_rowconfigure(0, weight=1)
        self.ans_frame.grid_columnconfigure(0, weight=1)
        self.ans_frame.place(x=400, y=220, width=800, height=88, anchor='n')
        
        # Coolness Label
        self.cool_label = tk.Label(self.ans_frame, text='', font=root.meme_font, background='white')
        self.cool_label.place(x=650, y=44, anchor='center')

        # Question entry
        self.answer_input = tk.StringVar()
        
        # Only allow letters to be inputed
        def validate_input(inserted_text):
            return inserted_text.isalpha()
        
        validate_cmd = (self.register(validate_input), '%S')
        self.entry = ttk.Entry(self.ans_frame, width=20, font=16, textvariable=self.answer_input, validate='key', validatecommand=validate_cmd)
        self.entry.grid(row=0, column=0)

        # Backgrounds
        self.background1 = gc.Sprite(0, 0, self.canvas, r'assets/Background_Long.png', anchor=tk.NW)
        self.background2 = gc.Sprite(1600, 0, self.canvas, r'assets/Background_Long.png', anchor=tk.NW) #loop the background again 
        
        #Set the cat, resized to be 1/2 the size of the original image
        self.animated_cat = gc.AnimatedSprite(root, self.cat_start_x, self.cat_start_y, self.canvas, self.cat_sequence, subsample=2)
        
        #Set the mouse, resized to be 1/4 of the size of the original image
        self.animated_mouse = gc.AnimatedSprite(root, self.mouse_start_x, self.mouse_start_y, self.canvas, self.mouse_sequence, subsample=4)
        
        #Tree is the starting point, located at the front of the background
        self.tree = gc.Sprite(100, 590, self.canvas, r'assets/tree.png', anchor=tk.S) 
        
        #House is the ending point, located at the end of the background
        self.house = gc.Sprite(1200, 590, self.canvas, r'assets/house.png', anchor=tk.S) 
        
        # Theme title display
        self.theme_label = tk.Label(self, text='Theme: Animals', font=root.header_font, background='#C3EEFF')
        self.theme_label.grid(row=0, column=0, sticky='nw', padx=12, pady=12)
        
        # Time/Score display
        self.time_label = tk.Label(self, text='Time: 0', font=root.header_font, background='#C3EEFF')
        self.time_label.grid(row=0, column=2, sticky='ne', padx=12, pady=12)
            
        # End game button (goes to lose screen)
        def on_end_game_pressed():
            root.show_frame(EndLoseFrame) #Switch to Lose frame
            self.entry.delete(0,'end') #Clear all contents in entry (input box)
        
        #Creating button 
        end_game_button = tk.Button(self, text="End Game", 
                                    command=lambda: on_end_game_pressed(), 
                                    foreground = "red", background="#C3EEFF", font="Papyrus")
        end_game_button.grid(row=0, column=2, sticky='se', pady=(15,0))
        
    
        self.game_instance = game.GameScrambled()
        self.game_instance.on_win_callback = self.on_win
        self.game_instance.on_question_callback = self.on_question
        
        self.enabled = False

        self.root.update_events.append(self.update)

    """
    -----------------------------------------------------------------------------------------------------------------------------------------------
    GAME CODE
    -----------------------------------------------------------------------------------------------------------------------------------------------
    """
    
    def on_enable(self) -> None:
        self.start_time = current_time() #Note: current_time() only gives back the current system time
        self.end_anim_playing = False #Do not play end animation
        self.begin_starting_animation() #Start animation
        print(self.root.difficulty)
        
        self.animated_cat.enabled = True
        self.animated_mouse.enabled = True
        
        #From game_scrambled initiate_game take in arguments difficulty and cat_initial points
        self.game_instance.initiate_game(self.root.difficulty, -10) #Set the cat_initial points to be -10
        self.game_instance.get_current_scrambled_word() #Get the scrambled words
        
        #Set the location of the house (ending of the game) outside of the window screen for now
        self.canvas.coords(self.house.sprite, 1200, 590) 
        self.animated_mouse.x = self.mouse_start_x #set the initial coordinate for the mouse
        self.qn_label.place(x=400, y=200, anchor='s')
        self.ans_frame.place(x=400, y=220, width=800, height=88, anchor='n')


        def lowercasify(event): #Lower case the input so that it will be the same as the answer
            self.answer_input.set(self.answer_input.get().lower())
        

        def check_ans(event):
            value = self.entry.get() #Get the input from input box

            #From game_scrambled.py, check_answer(answer, skip:bool=False) 
            #If user does not put it any input, skip: bool = True which will result in -3 points, else check answer 
            self.last_score = self.game_instance.check_answer(answer=value, skip=value=="")
            
            self.cool_text_start = current_time() #Get the time answer was checked

            self.entry.delete(0,'end') #Clear data in input box
        
        #Bind pressing laptop keys to triggering certain function
        self.entry.bind("<Return>", check_ans) #When enter is pressed, trigger check_ans() function
        self.entry.bind("<KeyPress>", lowercasify) #When any other letter is pressed, trigger lowercasify() function
        
        self.entry.delete(0,'end') #Clear data in input box
        self.entry.focus() #Focus on the input box, any keypress will immediately be put into the input box
    
    def on_disable(self) -> None:
        #Unbind laptop keys
        self.entry.unbind("<Return>")
        self.entry.unbind("<KeyPress>")

        
    def begin_starting_animation(self) -> None: #Function to start the animation
        self.begin_anim_playing = True

        #Set the tree as the tree is the starting animation 
        self.canvas.coords(self.tree.sprite, 200, 590)
        self.begin_anim_start = current_time() #Get the current time the begin animation starts
        

    def begin_ending_animation(self) -> None:
        self.end_anim_playing = True
        self.end_anim_start = current_time() #Get the current time the end animation starts

        #setting the position between the cat and mouse where the game ends (Cat should be very near the mouse)
        self.end_anim_cat_end_position = int(self.mouse_start_x - ((self.mouse_start_x - 200)/self.game_instance.fast_win_points)*self.game_instance.get_cat_dist_from_mouse() - 200)
        
    def on_question(self, scrambled_word: str) -> None:
        self.qn_label.config(text=f'{scrambled_word}') #Show the scrambled word on the screen 
        
    def on_win(self, win_type: game.GameScrambled.WinType) -> None:
        print(f'Win type: {win_type}')
        
        self.game_end_time = current_time()
        
        if win_type == game.GameScrambled.WinType.LOSE:
            #Lose
            #Stop all the animation, stop taking inputs 
            self.enabled = False
            self.animated_cat.enabled = False
            self.animated_mouse.enabled = False
            self.root.show_frame(EndLoseFrame) #Redirect to lose frame
        
        else:
            #Win!!
            self.qn_label.place_forget() #Hide question frames
            self.ans_frame.place_forget() #Hide input box widget
            self.begin_ending_animation()
            self.game_end_time = current_time() #Get the current time the game ends
            self.root.last_score = self.get_gameplay_duration( )
    
    def move_background(self, c_time: float):
        #Make animation move based on the c_time
        self.canvas.coords(self.background1.sprite, int(-((c_time*self.scroll_speed + 1600) % 3200) + 1600), 0)
        self.canvas.coords(self.background2.sprite, int(-((c_time*self.scroll_speed) % 3200) + 1600), 0)
    
    def update(self):
        if not self.enabled: return #Game not running
        c_time = self.get_time() #get current time
        
        if not self.end_anim_playing:#Game is still running, ending animation not yet
            self.game_instance.check_cat_position()
            
            self.move_background(c_time)
            
            #Constantly update the x coordinate of the car base on the points earn(get_cat_dist_from_mouse())
            #Gives the impression that the cat is moving closer to the mouse when the difference in points between cat and mouse decreases
            self.animated_cat.x = int(self.mouse_start_x - ((self.mouse_start_x - 200)/self.game_instance.fast_win_points)*self.game_instance.get_cat_dist_from_mouse() - 200)
            
            #Update time/score
            self.time_label.config(text=f'Time: {round(self.get_time(), 1)}')
            
            #Update cool text
            cool_time = current_time() - self.cool_text_start #Get the current time - time the question was checked
            
            #Checks that the check_ans() function just ran
            if cool_time < self.cool_text_duration: 
                cool_text = ''
                
                #Show comments based on the points
                if self.last_score == -3:
                    cool_text = 'Skipped'
                elif self.last_score == -1:
                    cool_text = 'Wrong answer'
                elif self.last_score == 1:
                    cool_text = 'not bad...try to be quicker!'
                elif self.last_score == 2:
                    cool_text = 'Getting the hang of it?'
                elif self.last_score == 3:
                    cool_text = 'Noice.'
                elif self.last_score == 4:
                    cool_text = 'WOW!'
                elif self.last_score == 5:
                    cool_text = 'AWESOME!!'
                
                self.cool_label.configure(text=cool_text)
            
            else: #Haven't check answer, show an empty string
                self.cool_label.configure(text='')

            
        else: #Game ending
            c_end_time = current_time() - self.end_anim_start 
            #Current time - time the end animation start to get when end animation should end
            #End animation ends when current time = end_animation_start time, c_end_time = 0
            
            cat_anim_time = c_end_time 
            house_anim_time = c_end_time - self.end_anim_catescape_duration
            mouse_anim_time = c_end_time - self.end_anim_catescape_duration - self.end_anim_house_duration
            
            # Animation flow will be: Cat will disappear -> House appears -> Mouse runs forward into house
            
            """<END ANIMATION RUNNING>"""
            
            if mouse_anim_time < 0: #End animation hasn't ened, background still moves
                self.move_background(c_time)
            
            if cat_anim_time < self.end_anim_catescape_duration: 
                #X coordinate is now towards 0 as the cat slowly leaves the screen
                new_cat_x = int(self.end_anim_cat_end_position - ((300 + self.end_anim_cat_end_position)* cat_anim_time/self.end_anim_catescape_duration))
                self.animated_cat.x = new_cat_x
                
            elif house_anim_time < self.end_anim_house_duration: 
                #House appears onto the screen at the end to signify the ending
                house_x = 1200 - house_anim_time * self.scroll_speed
                self.canvas.coords(self.house.sprite, house_x, 590)
                
            elif mouse_anim_time < self.end_anim_mouseescape_duration:
                #Mouse starts to move forward towards house
                new_mouse_x = int(self.mouse_start_x + self.scroll_speed * mouse_anim_time)
                self.animated_mouse.x = new_mouse_x
                
            else: 
                #c_end_time = 0, end animation ends, all animation has played, conclude
                self.end_anim_playing = False

                #Stop animations
                self.enabled = False
                self.animated_cat.enabled = False
                self.animated_mouse.enabled = False
                
                #Change to winning screen
                self.root.show_frame(EndWinFrame)

        if self.begin_anim_playing: #If the game just started
            c_begin_time = current_time() - self.begin_anim_start 
            new_x = 200 - c_begin_time*self.scroll_speed

            #Set the tree location as tree is in beginning animation
            self.canvas.coords(self.tree.sprite, new_x, 590) 
            self.begin_anim_playing = new_x > -300
        
        
    def get_time(self) -> float: #Function to get time
        return current_time() - self.start_time
     
    def get_gameplay_duration(self) -> float: #Function to get total time
        return round(self.game_end_time - self.start_time, 1)



"""
--------------------------------------------------------------------------------------------------------------------------------------------------------
WIN FRAME
--------------------------------------------------------------------------------------------------------------------------------------------------------
"""
class EndWinFrame(gc.GameFrame):
    """Ending page on win.

    Inherits:
        gc.GameFrame
    """

    def __init__(self, parent, root):
        super().__init__(parent, root)
        
        self.root = root
        
        #Setting background
        self.background_image2 = tk.PhotoImage(file="./assets/You Win.png")
        label = tk.Label(self, image=self.background_image2, compound = "center")
        label.grid(row=0, column=0)
        
        #Highscore recording
        #Creating input widget to get user name
        self.name_enter_frame = tk.Frame(self, background='white')
        self.name_enter_frame.grid(row=0, column=0, sticky='s')
        
        name_enter_label = tk.Label(self.name_enter_frame, text='Enter your name, champion!', font=root.header_font, background='#FFB600')
        name_enter_label.grid(row=0, column=0, sticky='nsew', padx=(20, 20), pady=(10, 5))
        
        name_input = tk.StringVar

        #Check if the name is valid
        def validate_name_input(inserted_text: str):
            return inserted_text.isalnum()

        validate_cmd = (self.register(validate_name_input), '%S') #Check for any special characters

        self.name_entry = ttk.Entry(self.name_enter_frame, width=20, font=12, textvariable=name_input, validate='key', validatecommand=validate_cmd)
        self.name_entry.grid(row=1, column=0, padx=(20, 20), pady=(5, 5))
        
        help_label = tk.Label(self.name_enter_frame, text='Press enter to continue', font=root.content_font, background='white')
        help_label.grid(row=2, column=0, padx=(20, 20), pady=(5, 10))
        
        # Highscore frame
        self.hs_frame = tk.Frame(self, background='#FFB600')
        
        #Creating hall of frame
        hs_title = tk.Label(self.hs_frame, text='Hall of Fame', font=root.big_meme_font, background='#FFB600')
        hs_title.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(20, 10))
        
        # Styling buttons
        style = ttk.Style()
        style.configure("TButton", font=root.button_font)
        style.map("TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'white')])
        self.play_again_button = ttk.Button(self, text="Play Again",
                           command=lambda: root.show_frame(MainMenuFrame)) #Redirect back to main screen
        
    def on_enable(self):

        #Disable play again button
        self.play_again_button.grid_forget() 
        self.hs_frame.grid_forget()
        self.name_enter_frame.grid(row=0, column=0, sticky='s')
        self.name_entry.focus() #Focus on input box widget
        
        def on_enter_name(event):
            self.root.last_name = self.name_entry.get() #Get the input from input_box
            
            # Save highscore in a txt file
            if self.root.last_name != '':
                with open(f'highscores{self.root.difficulty}.txt', 'a+') as f:
                    f.write(f'{self.root.last_name},{self.root.last_score}\n') #append to txt file name, score
            
            self.show_highscores()
        self.name_entry.bind("<Return>", on_enter_name) #Bind enter key to trigger on_enter_name() function
    

    def show_highscores(self):
        self.name_entry.unbind("<Return>") #Unbind key
        
        self.name_enter_frame.grid_forget() #Remove input box
        self.hs_frame.grid(row=0, column=0, ipady=10)
        self.play_again_button.grid(row=0, column=0, pady=(20, 20), sticky='s') #Enable play again button
        
        #Read from highscore file
        scores: list = []
        with open(f'highscores{self.root.difficulty}.txt','a+') as f:
            f.seek(0)
            while True:
                line = f.readline()
                if not line:
                    break
                split_line = line.strip().split(',') #Get the name, score
                if len(split_line) == 2 and is_float(split_line[1]): #Comfirm only name and score is in the list
                    split_line[1] = float(split_line[1]) #Get the score
                    scores.append(tuple(split_line)) 
                
        #Sort highscores
        scores.sort(key=lambda tup: float(tup[1]))
                
        #Create labels (only first 10)
        score_labels = [(tk.Label(self.hs_frame, text=name, font=self.root.content_font, background='#FFB600'), 
                        tk.Label(self.hs_frame, text=f'{time}s', font=self.root.content_font, background='#FFB600')) 
                        for name, time in scores[:10]]
        
        #Grid those labels!
        for i, player_label in enumerate(score_labels):
            name_label, time_label = player_label
            name_label.grid(row=i+1, column=0, padx=(20, 20), pady= (2, 2), sticky='w') #Create space between name and score
            time_label.grid(row=i+1, column=1, padx=(20, 20), pady= (2, 2), sticky='e')



"""
--------------------------------------------------------------------------------------------------------------------------------------------------------
LOSE FRAME
--------------------------------------------------------------------------------------------------------------------------------------------------------
"""
class EndLoseFrame(gc.GameFrame):
    """Ending page on lose.

    Inherits:
        gc.GameFrame
    """

    def __init__(self, parent, root):
        super().__init__(parent, root)

        #Create background
        self.background_image3 = tk.PhotoImage(file="./assets/You_Lose.png")

        #Create labels
        label = tk.Label(self, text="You ded lol",
                         font=root.title_font,
                         image = self.background_image3,
                         compound = "center")
        label.grid(row=0, column=0, sticky="nsew")

        #Styling buttons
        style = ttk.Style()
        style.configure("TButton", font=root.button_font)
        style.map("TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'white')])
        
        #Setting buttons 
        button = ttk.Button(self, text="Play Again",
                           command=lambda: root.show_frame(MainMenuFrame)) #Redirect back to main screen
        button.place(x=400,y=535, anchor = "n")



if __name__ == '__main__':
    width, height = 800, 600 #Fixed window screen
    animation_fps = 60
    #Container of all the frames
    frame_list = [MainMenuFrame, CreditsFrame, InstructionFrame,  DifficultyFrame, GameFrame, EndWinFrame, EndLoseFrame]
    
    app = MainApp(width, height, animation_fps, frame_list)
    app.resizable(False, False)
    app.title('Cat me if you can! by 21F01 - Team 1J')
    app.iconbitmap('icon.ico')
    app.mainloop()

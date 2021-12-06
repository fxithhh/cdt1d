# GUI library
import tkinter as tk
from tkinter import ttk, font as tkfont

# For animation timing
from timeit import default_timer as current_time

# Better type hinting
from typing import *

# Core game classes
import gameclasses as gc
import game_scrambled as game


def is_float(element: any) -> bool:
    """Check whether a value is convertable to float.

    Args:
        element (any): Input variable.

    Returns:
        bool: Whether the input variable can be converted to float.
    """
    try:
        float(element)
        return True
    except ValueError:
        return False


"""
--------------------------------------------------------------------------------------------------------------------------------------------------------
CORE GAME CLASS
--------------------------------------------------------------------------------------------------------------------------------------------------------
"""
class MainApp(gc.GameRoot):
    """Main app class. Handles the display of the different game screens and switching.

    Inherits:
        gc.GameRoot

    Members:
        difficulty (int): Currently selected difficulty level of the game. {Easy:1, Medium:2, Hard: 3}
        last_score (int): The last highscore in the current game session.
        last_name (str): The name of the last player who got a score.
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
MAIN MENU SCREEN
--------------------------------------------------------------------------------------------------------------------------------------------------------
"""
class MainMenuFrame(gc.GameFrame):
    """Main menu screen. Shows the play and credits button.

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
        btn_start = ttk.Button(self, text="Start", style="C.TButton",
                              command=lambda: root.show_frame(DifficultyFrame)) #Redirect to difficulty page

        btn_credits = ttk.Button(self, text="Credits", style="C.TButton",
                              command=lambda: root.show_frame(CreditsFrame)) #Redirect to credits page

        btn_instr = ttk.Button(self, text="How To Play", style="C.TButton",
                              command=lambda: root.show_frame(InstructionFrame)) #Redirect to instruction page

        #Layout of buttons
        btn_start.grid(row=1, column=0, pady=(15, 10), sticky='s')
        btn_credits.grid(row=2, column=0, pady=(10, 10))
        btn_instr.grid(row=3, column=0, pady=(10,15), sticky="n")



"""
--------------------------------------------------------------------------------------------------------------------------------------------------------
CREDITS SCREEN
--------------------------------------------------------------------------------------------------------------------------------------------------------
"""
class CreditsFrame(gc.GameFrame):
    """Game credit screen. Shows the glorious people who built this masterpiece.

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
        btn_back = ttk.Button(self, text="Back", style="C.TButton",
                            command=lambda: root.show_frame(MainMenuFrame)) # Return to main menu
        btn_back.grid(row=0, column=0, sticky='se', padx=(20, 20), pady=(25, 25))

        # Create frame for credits
        frame_text = tk.Frame(self, background='white')
        frame_text.grid(row=0, column=0, ipady=10)

        # Title
        c_title_label = tk.Label(frame_text, text='Credits', font=root.title_font, background='#FFB600')
        c_title_label.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=(20, 20), pady=(15, 20))

        # Team title
        c_team_label = tk.Label(frame_text, text='21F01 - Team 1J', font=root.header_font, background='white')
        c_team_label.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky='w')

        # Everyone and their roles
        c_people = [('Cheng Wei Xuan', 'Gameplay Developer, Lead Artist'),
                    ('Ang Yue Sheng', 'Gameplay Developer, Artist'),
                    ('Lim Tiang Sui, Faith', 'GUI Developer, Lead UI/UX'),
                    ('Jeriah Yeo Ruei', 'GUI Developer, Content Lead'),
                    ('Seah Ying Xiang', 'Noob Developer')]

        # Create labels from c_people
        c_people_labels = [(tk.Label(frame_text, text=name, font=root.content_font, background='white'),
                            tk.Label(frame_text, text=role, font=root.content_font, background='white')) for name, role in c_people]

        # Grid those labels!
        for i, person_labels in enumerate(c_people_labels):
            name_label, role_label = person_labels
            name_label.grid(row=i+2, column=0, padx=(20, 20), pady= (10, 10), sticky='w') #Add spacing between the name and the role
            role_label.grid(row=i+2, column=1, padx=(20, 20), pady= (10, 10), sticky='e')



"""
--------------------------------------------------------------------------------------------------------------------------------------------------------
INSTRUCTIONS SCREEN
--------------------------------------------------------------------------------------------------------------------------------------------------------
"""
class InstructionFrame(gc.GameFrame):
    """Instruction screen. Shows players how to play the game.

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
        btn_back = ttk.Button(self, text="Back", style="C.TButton",
                            command=lambda: root.show_frame(MainMenuFrame)) # Return to main menu
        btn_back.grid(row=0, column=0, sticky='se', padx=(20, 20), pady=(25, 25))

        # Create frame for credits
        frame_text = tk.Frame(self, background='white')
        frame_text.grid(row=0, column=0, ipady=10)

        # Title
        c_title_label = tk.Label(frame_text, text='How To Play?', font=root.title_font, background='#FFB600')
        c_title_label.grid(row=0, column=0, columnspan=2, sticky='nsew', padx=(20, 20), pady=(15, 20))

        # Instructions
        label_instr1 = tk.Label(frame_text,
                                text='~ The theme of the game is Animals.',
                                font=root.content_font, background='white')

        label_instr2 = tk.Label(frame_text,
                                text='~ Unscramble the words as fast as you can to help get mousey home.',
                                font=root.content_font, background='white')

        label_instr3 = tk.Label(frame_text,
                                text='~ The faster you answer the questions correctly, the faster mousey will run!',
                                font=root.content_font, background='white')

        label_instr4 = tk.Label(frame_text,
                                text='~ To submit your answer, press enter.',
                                font=root.content_font, background='white')

        label_instr5 = tk.Label(frame_text,
                                text="~ Pressing enter without typing anything will skip the question.",
                                font=root.content_font, background='white')

        label_instr6 = tk.Label(frame_text,
                                text='~ But watch out! Every wrong answer will cause mousey to run slower!',
                                font=root.content_font, background='white')

        label_instr7 = tk.Label(frame_text,
                                text='~ And skipped questions will cause mousey to run even slower!',
                                font=root.content_font, background='white')

        # Layout the labels
        label_instr1.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky='w')
        label_instr2.grid(row=2, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky='w')
        label_instr3.grid(row=3, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky='w')
        label_instr4.grid(row=4, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky='w')
        label_instr5.grid(row=5, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky='w')
        label_instr6.grid(row=6, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky='w')
        label_instr7.grid(row=7, column=0, columnspan=2, padx=(20, 20), pady=(10, 10), sticky='w')



"""
--------------------------------------------------------------------------------------------------------------------------------------------------------
DIFFICULTY SCREEN
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
        label_title = tk.Label(self, text="Choose a Difficulty Level!",
                         font=root.title_font, foreground="Black", background = "#c3eeff", height=2)
        label_title.grid(row=0, column=0, sticky='s', pady=(40, 0))

        # Style easy medium hard buttons
        style = ttk.Style()
        style.configure("TButton", font=root.button_font)
        style.map("TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'white')])

        # Set value to difficulty button
        def all_fn(val):
            root.difficulty = val
            root.show_frame(GameFrame)
            print(val)

        # Setting up buttons
        btn_easy = ttk.Button(self, text="Easy", style="TButton",
                                command=lambda: all_fn(1)) # root.difficulty = 1

        btn_medium = ttk.Button(self, text="Medium", style="TButton",
                               command=lambda: all_fn(2)) # root.difficulty = 2

        btn_hard = ttk.Button(self, text="Hard", style="TButton",
                                command=lambda: all_fn(3)) # root.difficulty = 3

        btn_back = ttk.Button(self, text="Back", style = "TButton",
                                command=lambda: root.show_frame(MainMenuFrame)) # Return to main page

        btn_easy.grid(row=1, column=0, pady=(15, 15))
        btn_medium.grid(row=2, column=0, pady=(15, 15))
        btn_hard.grid(row=3, column=0, pady=(15, 15), sticky='n')

        btn_back.grid(row=3, column=0, padx=(15, 15), pady=(25, 25), sticky='se')



"""
--------------------------------------------------------------------------------------------------------------------------------------------------------
MAIN GAME SCREEN
--------------------------------------------------------------------------------------------------------------------------------------------------------
"""
class GameFrame(gc.GameFrame):
    """Main game screen. This is where all the action are!

    Inherits:
        gc.GameFrame
    """

    # Initialize variables with some placeholder for start_time and game_end_time
    start_time: float = 0
    game_end_time: float = 0
    scroll_speed: int = 500

    # Cat Animation Frames
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

    # Mouse Animation Frames
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

    # Set the starting x,y coordinates of the Cat and Mouse sprites
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

    def __init__(self, parent, root):
        super().__init__(parent, root)
        self.root = root

        # Question label
        self.label_qn = tk.Label(self, text='', background='white', font=root.title_font)
        self.label_qn.place(x=400, y=200, anchor='s')

        # Question frame
        self.frame_ans = tk.Frame(self, background='white')
        self.frame_ans.grid_rowconfigure(0, weight=1)
        self.frame_ans.grid_columnconfigure(0, weight=1)
        self.frame_ans.place(x=400, y=220, width=800, height=88, anchor='n')

        # Coolness Label
        self.label_cool = tk.Label(self.frame_ans, text='', font=root.meme_font, background='white')
        self.label_cool.place(x=650, y=44, anchor='center')

        # Question entry
        self.answer_input = tk.StringVar()

        # Only allow letters to be inputted
        def validate_input(inserted_text):
            return inserted_text.isalpha()

        validate_cmd = (self.register(validate_input), '%S')
        self.entry = ttk.Entry(self.frame_ans, width=20, font=16, textvariable=self.answer_input, validate='key', validatecommand=validate_cmd)
        self.entry.grid(row=0, column=0)

        # Backgrounds
        self.spr_bg1 = gc.Sprite(0, 0, self.canvas, r'assets/Background_Long.png', anchor=tk.NW)
        self.spr_bg2 = gc.Sprite(1600, 0, self.canvas, r'assets/Background_Long.png', anchor=tk.NW)
        # loop the background again

        # Set the cat, resized to be 1/2 the size of the original image
        self.animspr_cat = gc.AnimatedSprite(root, self.cat_start_x, self.cat_start_y, self.canvas, self.cat_sequence, subsample=2)

        # Set the mouse, resized to be 1/4 of the size of the original image
        self.animspr_mouse = gc.AnimatedSprite(root, self.mouse_start_x, self.mouse_start_y, self.canvas, self.mouse_sequence, subsample=4)

        # Tree is the starting point, located at the front of the background
        self.spr_tree = gc.Sprite(100, 590, self.canvas, r'assets/tree.png', anchor=tk.S)

        # House is the ending point, located at the end of the background
        self.spr_house = gc.Sprite(1200, 590, self.canvas, r'assets/house.png', anchor=tk.S)

        # Theme title display
        self.label_theme = tk.Label(self, text='Theme: Animals', font=root.header_font, background='#C3EEFF')
        self.label_theme.grid(row=0, column=0, sticky='nw', padx=12, pady=12)

        # Time/Score display
        self.label_time = tk.Label(self, text='Time: 0', font=root.header_font, background='#C3EEFF')
        self.label_time.grid(row=0, column=2, sticky='ne', padx=12, pady=12)

        # End game button (goes to lose screen)
        def on_end_game_pressed():
            root.show_frame(EndLoseFrame) # Switch to Lose frame
            self.entry.delete(0,'end') # Clear all contents in entry (input box)

        # Creating button
        btn_end_game = tk.Button(self, text="End Game",
                                    command=lambda: on_end_game_pressed(),
                                    foreground = "red", background="#C3EEFF", font="Papyrus")
        btn_end_game.grid(row=0, column=2, sticky='se', pady=(15,0))


        self.game_instance = game.GameScrambled()
        self.game_instance.on_win_callback = self.on_win
        self.game_instance.on_question_callback = self.on_question

        self.enabled = False

        self.root.update_event_handler.append(self.update)

    # Super function overrides
    def on_enable(self) -> None:
        self.start_time = current_time() # Note: current_time() only gives back the current system time
        self.end_anim_playing = False # Do not play end animation
        self.begin_starting_animation() # Start animation
        print(self.root.difficulty)

        self.animspr_cat.enabled = True
        self.animspr_mouse.enabled = True

        # From game_scrambled initiate_game take in arguments difficulty and cat_initial points
        self.game_instance.initiate_game(self.root.difficulty, -10) # Set the cat_initial points to be -10
        self.game_instance.get_current_scrambled_word() # Get the scrambled words

        # Set the location of the house (ending of the game) outside of the window screen for now
        self.canvas.coords(self.spr_house.sprite, 1200, 590)
        self.animspr_mouse.x = self.mouse_start_x # Set the initial coordinate for the mouse
        self.label_qn.place(x=400, y=200, anchor='s')
        self.frame_ans.place(x=400, y=220, width=800, height=88, anchor='n')

        def lowercasify(event): # Make the input lowercase to let the user know capitalization does not matter
            self.answer_input.set(self.answer_input.get().lower())

        def check_ans(event):
            value = self.entry.get() # Get the input from input box

            # From game_scrambled.py, check_answer(answer, skip:bool=False)
            # If user does not put it any input, skip: bool = True which will result in -3 points, else check answer
            self.last_score = self.game_instance.check_answer(answer=value, skip=value=="")

            self.cool_text_start = current_time() # Get the time answer was checked

            self.entry.delete(0,'end') # Clear data in input box

        # Bind pressing keys to triggering certain function
        self.entry.bind("<Return>", check_ans) # When enter is pressed, trigger check_ans() function
        self.entry.bind("<KeyPress>", lowercasify) # When any other letter is pressed, trigger lowercasify() function

        self.entry.delete(0,'end') # Clear data in input box
        self.entry.focus() # Focus on the input box, any keypress will immediately be put into the input box

    def on_disable(self) -> None:
        # Unbind keys
        self.entry.unbind("<Return>")
        self.entry.unbind("<KeyPress>")

    # Animation initializers
    def begin_starting_animation(self) -> None: # Function to start the animation
        self.begin_anim_playing = True

        # Set the tree as the tree is the starting animation
        self.canvas.coords(self.spr_tree.sprite, 200, 590)
        self.begin_anim_start = current_time() # Get the current time the begin animation starts

    def begin_ending_animation(self) -> None:
        self.end_anim_playing = True
        self.end_anim_start = current_time() # Get the current time the end animation starts

        # Setting the position between the cat and mouse where the game ends
        self.end_anim_cat_end_position = int(self.mouse_start_x - ((self.mouse_start_x - 200)/self.game_instance.fast_win_points)*self.game_instance.get_cat_dist_from_mouse() - 200)

    # Callbacks
    def on_question(self, scrambled_word: str) -> None:
        """Callback function that is invoked when a new question starts.

        Args:
            scrambled_word (str): Scrambled word for the new question.
        """
        self.label_qn.config(text=f'{scrambled_word}') # Show the scrambled word on the screen

    def on_win(self, win_type: game.GameScrambled.WinType) -> None:
        """Callback function that is invoked on a winning condition.

        Args:
            win_type (game.GameScrambled.WinType): Type of game ending condition.
        """
        print(f'Win type: {win_type}')

        self.game_end_time = current_time()

        if win_type == game.GameScrambled.WinType.LOSE:
            # Lose
            # Stop all the animation, stop taking inputs
            self.enabled = False
            self.animspr_cat.enabled = False
            self.animspr_mouse.enabled = False
            self.root.show_frame(EndLoseFrame) # Redirect to lose frame

        else:
            # Win!!
            self.label_qn.place_forget() # Hide question frames
            self.frame_ans.place_forget() # Hide input box widget
            self.begin_ending_animation()
            self.game_end_time = current_time() # Get the current time the game ends
            self.root.last_score = self.get_gameplay_duration( )

    # Helper functions
    def move_background(self, c_time: float):
        # Make animation move based on the c_time
        self.canvas.coords(self.spr_bg1.sprite, int(-((c_time*self.scroll_speed + 1600) % 3200) + 1600), 0)
        self.canvas.coords(self.spr_bg2.sprite, int(-((c_time*self.scroll_speed) % 3200) + 1600), 0)

    def get_time(self) -> float:
        """Get the time elapsed from the start of the round, regardless of whether the round has ended.

        Returns:
            float: Current time elapsed from start of round.
        """
        return current_time() - self.start_time

    def get_gameplay_duration(self) -> float:
        """Get the time elapsed for the game round. The timer stops after the round has ended.

        Returns:
            float: Total time elapsed for the game round, rounded to 1 d.p.
        """
        return round(self.game_end_time - self.start_time, 1)

    # Update loop
    def update(self):
        if not self.enabled: return # Game not running
        c_time = self.get_time() # get current time

        if not self.end_anim_playing:# Game is still running, ending animation not yet
            self.game_instance.check_cat_position()

            self.move_background(c_time)

            # Constantly update the x coordinate of the car base on the points earn(get_cat_dist_from_mouse())
            # Gives the impression that the cat is moving closer to the mouse when the difference in points between cat and mouse decreases
            self.animspr_cat.x = int(self.mouse_start_x - ((self.mouse_start_x - 200)/self.game_instance.fast_win_points)*self.game_instance.get_cat_dist_from_mouse() - 200)

            # Update time/score
            self.label_time.config(text=f'Time: {round(self.get_time(), 1)}')

            # Update cool text
            cool_time = current_time() - self.cool_text_start # Get the current time - time the question was checked

            # Checks that the check_ans() function just ran
            if cool_time < self.cool_text_duration:
                cool_text = ''

                # Show comments based on the points
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

                self.label_cool.configure(text=cool_text)

            else: # Don't show anything on downtime
                self.label_cool.configure(text='')


        else: # Game ending
            c_end_time = current_time() - self.end_anim_start
            # Current time - time the end animation start to get when end animation should end
            # End animation ends when current time = end_animation_start time, c_end_time = 0

            cat_anim_time = c_end_time
            house_anim_time = c_end_time - self.end_anim_catescape_duration
            mouse_anim_time = c_end_time - self.end_anim_catescape_duration - self.end_anim_house_duration

            # Animation flow will be: Cat will disappear -> House appears -> Mouse runs forward into house

            """<END ANIMATION RUNNING>"""

            if mouse_anim_time < 0: # End animation hasn't ended, background still moves
                self.move_background(c_time)

            if cat_anim_time < self.end_anim_catescape_duration:
                # X coordinate is now towards 0 as the cat slowly leaves the screen
                new_cat_x = int(self.end_anim_cat_end_position - ((300 + self.end_anim_cat_end_position)* cat_anim_time/self.end_anim_catescape_duration))
                self.animspr_cat.x = new_cat_x

            elif house_anim_time < self.end_anim_house_duration:
                # House appears onto the screen at the end to signify the ending
                house_x = 1200 - house_anim_time * self.scroll_speed
                self.canvas.coords(self.spr_house.sprite, house_x, 590)

            elif mouse_anim_time < self.end_anim_mouseescape_duration:
                # Mouse starts to move forward towards house
                new_mouse_x = int(self.mouse_start_x + self.scroll_speed * mouse_anim_time)
                self.animspr_mouse.x = new_mouse_x

            else:
                # c_end_time = 0, end animation ends, all animation has played, conclude
                self.end_anim_playing = False

                # Stop animations
                self.enabled = False
                self.animspr_cat.enabled = False
                self.animspr_mouse.enabled = False

                # Change to winning screen
                self.root.show_frame(EndWinFrame)

        if self.begin_anim_playing: # If the game just started
            c_begin_time = current_time() - self.begin_anim_start
            new_x = 200 - c_begin_time*self.scroll_speed

            # Set the tree location as tree is in beginning animation
            self.canvas.coords(self.spr_tree.sprite, new_x, 590)
            self.begin_anim_playing = new_x > -300



"""
--------------------------------------------------------------------------------------------------------------------------------------------------------
WINNING SCREEN
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

        # Setting background
        self.background_image2 = tk.PhotoImage(file="./assets/You Win.png")
        label = tk.Label(self, image=self.background_image2, compound = "center")
        label.grid(row=0, column=0)

        # Highscore recording
        # Creating input widget to get user name
        self.frame_name_enter = tk.Frame(self, background='white')
        self.frame_name_enter.grid(row=0, column=0, sticky='s')

        name_enter_label = tk.Label(self.frame_name_enter, text='Enter your name, champion!', font=root.header_font, background='#FFB600')
        name_enter_label.grid(row=0, column=0, sticky='nsew', padx=(20, 20), pady=(10, 5))

        name_input = tk.StringVar

        # Check if the name is valid
        def validate_name_input(inserted_text: str):
            return inserted_text.isalnum()

        validate_cmd = (self.register(validate_name_input), '%S') #Check for any special characters

        self.entry_name = ttk.Entry(self.frame_name_enter, width=20, font=12, textvariable=name_input, validate='key', validatecommand=validate_cmd)
        self.entry_name.grid(row=1, column=0, padx=(20, 20), pady=(5, 5))

        label_help = tk.Label(self.frame_name_enter, text='Press enter to continue', font=root.content_font, background='white')
        label_help.grid(row=2, column=0, padx=(20, 20), pady=(5, 10))

        # Highscore frame
        self.frame_hs = tk.Frame(self, background='#FFB600')

        # Creating hall of frame
        label_hs_title = tk.Label(self.frame_hs, text='Hall of Fame', font=root.big_meme_font, background='#FFB600')
        label_hs_title.grid(row=0, column=0, columnspan=2, padx=(20, 20), pady=(20, 10))

        # Styling buttons
        style = ttk.Style()
        style.configure("TButton", font=root.button_font)
        style.map("TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'white')])
        self.btn_play_again = ttk.Button(self, text="Play Again",
                           command=lambda: root.show_frame(MainMenuFrame)) # Redirect back to main screen

    def on_enable(self):
        # Disable play again button
        self.btn_play_again.grid_forget()
        self.frame_hs.grid_forget()
        self.frame_name_enter.grid(row=0, column=0, sticky='s')
        self.entry_name.focus() # Focus on input box widget

        def on_enter_name(event):
            self.root.last_name = self.entry_name.get() # Get the input from input_box

            # Save highscore in a txt file
            if self.root.last_name != '':
                with open(f'highscores{self.root.difficulty}.txt', 'a+') as f:
                    f.write(f'{self.root.last_name},{self.root.last_score}\n') # append to txt file name, score

            self.show_highscores()
        self.entry_name.bind("<Return>", on_enter_name) # Bind enter key to trigger on_enter_name() function

    def on_disable(self) -> None:
        # Ungrid dem labels!
        for player_label in self.labels_score:
            name_label, time_label = player_label
            name_label.grid_forget()
            time_label.grid_forget()

        # Forget everything!
        self.labels_score.clear()

    def show_highscores(self):
        self.entry_name.unbind("<Return>") # Unbind key

        self.frame_name_enter.grid_forget() # Remove input box
        self.frame_hs.grid(row=0, column=0, ipady=10)
        self.btn_play_again.grid(row=0, column=0, pady=(20, 20), sticky='s') # Enable play again button

        # Read from highscore file
        scores: list = []
        with open(f'highscores{self.root.difficulty}.txt','a+') as f:
            f.seek(0)
            while True:
                line = f.readline()
                if not line:
                    break
                split_line = line.strip().split(',') # Get the name, score
                if len(split_line) == 2 and is_float(split_line[1]): # Confirm only name and score is in the list
                    split_line[1] = float(split_line[1]) # Get the score
                    scores.append(tuple(split_line))

        # Sort highscores
        scores.sort(key=lambda tup: float(tup[1]))

        # Create name and score label sets (only first 10)
        self.labels_score = [(tk.Label(self.frame_hs, text=name, font=self.root.content_font, background='#FFB600'),
                        tk.Label(self.frame_hs, text=f'{time}s', font=self.root.content_font, background='#FFB600'))
                        for name, time in scores[:10]]

        # Grid those labels!
        for i, player_label in enumerate(self.labels_score):
            name_label, time_label = player_label
            name_label.grid(row=i+1, column=0, padx=(20, 20), pady= (2, 2), sticky='w') # Create space between name and score
            time_label.grid(row=i+1, column=1, padx=(20, 20), pady= (2, 2), sticky='e')



"""
--------------------------------------------------------------------------------------------------------------------------------------------------------
LOSING SCREEN
--------------------------------------------------------------------------------------------------------------------------------------------------------
"""
class EndLoseFrame(gc.GameFrame):
    """Ending page on lose.

    Inherits:
        gc.GameFrame
    """

    def __init__(self, parent, root):
        super().__init__(parent, root)

        # Create background
        self.background_image3 = tk.PhotoImage(file="./assets/You_Lose.png")

        # Create labels
        label = tk.Label(self, text="You ded lol",
                         font=root.title_font,
                         image = self.background_image3,
                         compound = "center")
        label.grid(row=0, column=0, sticky="nsew")

        # Styling buttons
        style = ttk.Style()
        style.configure("TButton", font=root.button_font)
        style.map("TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'white')])

        # Setting buttons
        btn_play_again = ttk.Button(self, text="Play Again",
                           command=lambda: root.show_frame(MainMenuFrame)) #Redirect back to main screen
        btn_play_again.place(x=400,y=535, anchor = "n")



if __name__ == '__main__':
    width, height = 800, 600 # Fixed window screen
    target_fps = 60
    # Container of all the frames
    frame_list = [MainMenuFrame, CreditsFrame, InstructionFrame, DifficultyFrame, GameFrame, EndWinFrame, EndLoseFrame]

    app = MainApp(width, height, target_fps, frame_list)
    app.resizable(False, False)
    app.title('Cat me if you can! by 21F01 - Team 1J')
    app.iconbitmap('icon.ico')
    app.mainloop()

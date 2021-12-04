import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

from timeit import default_timer as timer

import gameclasses as gc
import game_scrambled as game

def is_float(element: any) -> bool:
    try:
        float(element)
        return True
    except ValueError:
        return False

class MainApp(gc.GameRoot):
    """Main app class.

    Inherits:
        gc.GameRoot
        
    Members:
        difficulty [int]: Currently selected difficulty level of the game. [0, 1, 2] Easy -> Hard.
    """

    difficulty: int = 1
    last_score: int = 0
    last_name: str = ""

    def __init__(self, width, height, animation_fps, frames_list, *args, **kwargs):
        super().__init__(width, height, animation_fps, frames_list, *args, **kwargs)
        
        # Load fonts
        self.title_font = tkfont.Font(family='Comic Sans Ms', size=24, weight="bold")
        self.button_font = tkfont.Font(family='Comic Sans Ms', size=14, weight="bold")
        self.header_font = tkfont.Font(family='Comic Sans Ms', size=18, weight="bold")
        self.meme_font = tkfont.Font(family='Papyrus', size=16, weight="bold")
        self.big_meme_font = tkfont.Font(family='Papyrus', size=20, weight="bold")
        self.content_font = tkfont.Font(family='Comic Sans Ms', size=14, weight="bold")
        
        self.load_frames()
        
        self.show_frame(MainMenuFrame)

class MainMenuFrame(gc.GameFrame):
    """Main menu page.

    Inherits:
        gc.GameFrame
    """
   
    def __init__(self, parent, root):
        super().__init__(parent, root)
        
        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(1, weight=1)

        # Background
        self.background = gc.Sprite(0, 0, self.canvas, r'assets/home_bg.png', anchor=tk.NW)
        
        # Define button style
        style = ttk.Style()
        style.configure("C.TButton", font=root.button_font, background = '#ff7733', foreground='#cc0000')
        style.map("C.TButton",
                  foreground=[('active', '#006622')],
                  background=[('active', '#00cc44')])
        
        # Create start and credit buttons
        startBtn = ttk.Button(self, text="Start", style="C.TButton",
                              command=lambda: root.show_frame(DifficultyFrame))
        creditBtn = ttk.Button(self, text="Credits", style="C.TButton",
                              command=lambda: root.show_frame(CreditsFrame))
        startBtn.grid(row=0, column=0, pady=(15, 15), sticky='s')
        creditBtn.grid(row=1, column=0, pady=(15, 15), sticky='n')

class CreditsFrame(gc.GameFrame):
    """Game credit page.

    Inherits:
        gc.GameFrame
    """
    
    def __init__(self, parent, root):
        super().__init__(parent, root)
    
        # Background
        self.background = gc.Sprite(0, 0, self.canvas, r'assets/home_bg.png', anchor=tk.NW)
        
        style = ttk.Style()
        style.configure("C.TButton", font=root.button_font, background='#ff7733', foreground='#cc0000')
        style.map("C.TButton",
                foreground=[('active', '#006622')],
                background=[('active', '#00cc44')])

        # Create button
        startBtn = ttk.Button(self, text="Back", style="C.TButton",
                            command=lambda: root.show_frame(MainMenuFrame))
        startBtn.grid(row=0, column=0, sticky='se', padx=(20, 20), pady=(10, 10))
        
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
        c_people_labels = [(tk.Label(textFrame, text=name, font=root.content_font, background='white'), tk.Label(textFrame, text=role, font=root.content_font, background='white')) for name, role in c_people]
        # Grid those labels!
        for i, person_labels in enumerate(c_people_labels):
            name_label, role_label = person_labels
            name_label.grid(row=i+2, column=0, padx=(20, 20), pady= (10, 10), sticky='w')
            role_label.grid(row=i+2, column=1, padx=(20, 20), pady= (10, 10), sticky='e')

class DifficultyFrame(gc.GameFrame):
    """Difficulty selection page.

    Inherits:
        gc.GameFrame
    """

    def __init__(self, parent, root):
        super().__init__(parent, root)

        self.grid_rowconfigure(0, weight=2)
        self.grid_rowconfigure(3, weight=3)
        
        # Background
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

        def all_fn(val):
            root.difficulty = val
            root.show_frame(GameFrame)
            print(val)

        # easy medium hard level buttons
        buttonEasy = ttk.Button(self, text="Easy", style="TButton",
                                command=lambda: all_fn(1))

        buttonMed = ttk.Button(self, text="Medium", style="TButton",
                               command=lambda: all_fn(2))

        buttonHard = ttk.Button(self, text="Hard", style="TButton",
                                command=lambda: all_fn(3))

        buttonEasy.grid(row=1, column=0, pady=(15, 15))
        buttonMed.grid(row=2, column=0, pady=(15, 15))
        buttonHard.grid(row=3, column=0, pady=(15, 15), sticky='n')

class GameFrame(gc.GameFrame):
    """Main game page.

    Inherits:
        gc.GameFrame
    """
    
    start_time: float = 0
    # Time when the game has concluded (excludes ending animations)
    game_end_time: float = 0
    scroll_speed: int = 500
    
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
        def validate_input(inserted_text):
            return inserted_text.isalpha()
        validate_cmd = (self.register(validate_input), '%S')
        self.entry = ttk.Entry(self.ans_frame, width=20, font=16, textvariable=self.answer_input, validate='key', validatecommand=validate_cmd)
        self.entry.grid(row=0, column=0)

        # Backgrounds
        self.background1 = gc.Sprite(0, 0, self.canvas, r'assets/Background_Long.png', anchor=tk.NW)
        self.background2 = gc.Sprite(1600, 0, self.canvas, r'assets/Background_Long.png', anchor=tk.NW)
        
        self.animated_cat = gc.AnimatedSprite(root, self.cat_start_x, self.cat_start_y, self.canvas, self.cat_sequence, subsample=2)
        self.animated_mouse = gc.AnimatedSprite(root, self.mouse_start_x, self.mouse_start_y, self.canvas, self.mouse_sequence, subsample=4)
        
        self.tree = gc.Sprite(100, 590, self.canvas, r'assets/tree.png', anchor=tk.S)
        self.house = gc.Sprite(1200, 590, self.canvas, r'assets/house.png', anchor=tk.S)
        
        # Theme title display
        self.theme_label = tk.Label(self, text='Theme: Animals and Insects', font=root.header_font, background='#C3EEFF')
        self.theme_label.grid(row=0, column=0, sticky='nw', padx=12, pady=12)
        
        # Time/Score display
        self.time_label = tk.Label(self, text='Time: 0', font=root.header_font, background='#C3EEFF')
        self.time_label.grid(row=0, column=2, sticky='ne', padx=12, pady=12)
            
        # End game button (goes to lose screen)
        def on_end_game_pressed():
            root.show_frame(EndLoseFrame)
            self.entry.delete(0,'end')
        
        end_game_button = tk.Button(self, text="End Game", command=lambda: on_end_game_pressed(), foreground = "red", background="#C3EEFF", font="Papyrus")
        end_game_button.grid(row=0, column=2, sticky='se')
        
        self.game_instance = game.GameScrambled()
        self.game_instance.on_win_callback = self.on_win
        self.game_instance.on_question_callback = self.on_question
        
        self.enabled = False

        self.root.update_events.append(self.update)
    
    def on_enable(self) -> None:
        self.start_time = timer()
        self.end_anim_playing = False
        self.begin_starting_animation()
        print(self.root.difficulty)
        
        self.animated_cat.enabled = True
        self.animated_mouse.enabled = True
        
        self.game_instance.initiate_game(self.root.difficulty, -10)
        self.game_instance.get_current_scrambled_word()
        
        self.canvas.coords(self.house.sprite, 1200, 590)
        self.animated_mouse.x = self.mouse_start_x
        self.qn_label.place(x=400, y=200, anchor='s')
        self.ans_frame.place(x=400, y=220, width=800, height=88, anchor='n')

        def lowercasify(event):
            self.answer_input.set(self.answer_input.get().lower())
        def check_ans(event):
            value = self.entry.get() 
            self.last_score = self.game_instance.check_answer(answer=value, skip=value=="")
            self.cool_text_start = timer()
            self.entry.delete(0,'end')
        self.entry.bind("<Return>", check_ans)
        self.entry.bind("<KeyPress>", lowercasify)
        self.entry.delete(0,'end')
        self.entry.focus()
    
    def on_disable(self) -> None:
        self.entry.unbind("<Return>")
        self.entry.unbind("<KeyPress>")
        
    def begin_starting_animation(self) -> None:
        self.begin_anim_playing = True
        self.canvas.coords(self.tree.sprite, 200, 590)
        self.begin_anim_start = timer()
        
    def begin_ending_animation(self) -> None:
        self.end_anim_playing = True
        self.end_anim_start = timer()
        self.end_anim_cat_end_position = int(self.mouse_start_x - ((self.mouse_start_x - 200)/self.game_instance.fast_win_points)*self.game_instance.get_cat_dist_from_mouse() - 200)
        
    def on_question(self, scrambled_word: str) -> None:
        self.qn_label.config(text=f'{scrambled_word}')
        
    def on_win(self, win_type: game.GameScrambled.WinType) -> None:
        print(f'Win type: {win_type}')
        
        self.game_end_time = timer()
        
        if win_type == game.GameScrambled.WinType.LOSE:
            # Lose
            self.enabled = False
            self.animated_cat.enabled = False
            self.animated_mouse.enabled = False
            self.root.show_frame(EndLoseFrame)
        else:
            # Win!!
            self.qn_label.place_forget()
            self.ans_frame.place_forget()
            self.begin_ending_animation()
            self.game_end_time = timer()
            self.root.last_score = self.get_gameplay_duration()
    
    def move_background(self, c_time: float):
        self.canvas.coords(self.background1.sprite, int(-((c_time*self.scroll_speed + 1600) % 3200) + 1600), 0)
        self.canvas.coords(self.background2.sprite, int(-((c_time*self.scroll_speed) % 3200) + 1600), 0)
    
    def update(self):
        if not self.enabled: return

        c_time = self.get_time()
        
        if not self.end_anim_playing:
            self.game_instance.check_cat_position()
            
            self.move_background(c_time)
            
            self.animated_cat.x = int(self.mouse_start_x - ((self.mouse_start_x - 200)/self.game_instance.fast_win_points)*self.game_instance.get_cat_dist_from_mouse() - 200)
            
            # Update time/score
            self.time_label.config(text=f'Time: {round(self.get_time(), 1)}')
            
            # Update cool text
            cool_time = timer() - self.cool_text_start
            if cool_time < self.cool_text_duration:
                cool_text = ''
                
                if self.last_score == -3:
                    cool_text = 'skipped'
                elif self.last_score == -1:
                    cool_text = 'wrong answer'
                elif self.last_score == 1:
                    cool_text = 'good'
                elif self.last_score == 2:
                    cool_text = 'noice.'
                elif self.last_score == 3:
                    cool_text = 'not bad...'
                elif self.last_score == 4:
                    cool_text = 'WOW!'
                elif self.last_score == 5:
                    cool_text = 'AWESOME!'
                
                self.cool_label.configure(text=cool_text)
            else:
                self.cool_label.configure(text='')
            
        else:
            c_end_time = timer() - self.end_anim_start
            cat_anim_time = c_end_time
            house_anim_time = c_end_time - self.end_anim_catescape_duration
            mouse_anim_time = c_end_time - self.end_anim_catescape_duration - self.end_anim_house_duration
            
            # Cat animation -> House animation -> Mouse animation
            # |<--Background animation playing-->|
            
            if mouse_anim_time < 0:
                self.move_background(c_time)
            
            if cat_anim_time < self.end_anim_catescape_duration:
                # Cat animation
                new_cat_x = int(self.end_anim_cat_end_position - ((300 + self.end_anim_cat_end_position)* cat_anim_time/self.end_anim_catescape_duration))
                self.animated_cat.x = new_cat_x
                
            elif house_anim_time < self.end_anim_house_duration:
                # House animation
                house_x = 1200 - house_anim_time * self.scroll_speed
                self.canvas.coords(self.house.sprite, house_x, 590)
                
            elif mouse_anim_time < self.end_anim_mouseescape_duration:
                # Mouse animation
                new_mouse_x = int(self.mouse_start_x + self.scroll_speed * mouse_anim_time)
                self.animated_mouse.x = new_mouse_x
                
            else:
                # All animation has played, conclude
                self.end_anim_playing = False

                # Stop animations
                self.enabled = False
                self.animated_cat.enabled = False
                self.animated_mouse.enabled = False
                
                # Change to winning screen
                self.root.show_frame(EndWinFrame)
        
        if self.begin_anim_playing:
            c_begin_time = timer() - self.begin_anim_start
            new_x = 200 - c_begin_time*self.scroll_speed
            self.canvas.coords(self.tree.sprite, new_x, 590)
            self.begin_anim_playing = new_x > -300
        
    def get_time(self) -> float:
        return timer() - self.start_time
    
    def get_gameplay_duration(self) -> float:
        return round(self.game_end_time - self.start_time, 1)

class EndWinFrame(gc.GameFrame):
    """Ending page on win.

    Inherits:
        gc.GameFrame
    """

    def __init__(self, parent, root):
        super().__init__(parent, root)
        
        self.root = root
        
        self.background_image2 = tk.PhotoImage(file="./assets/You Win.png")
        label = tk.Label(self, image=self.background_image2, compound = "center")
        label.grid(row=0, column=0)
        
        # Highscore recording
        self.name_enter_frame = tk.Frame(self, background='white')
        self.name_enter_frame.grid(row=0, column=0, sticky='s')
        
        name_enter_label = tk.Label(self.name_enter_frame, text='Enter your name, champion!', font=root.header_font, background='#FFB600')
        name_enter_label.grid(row=0, column=0, sticky='nsew', padx=(20, 20), pady=(10, 5))
        
        name_input = tk.StringVar
        def validate_name_input(inserted_text: str):
            return inserted_text.isalnum()
        validate_cmd = (self.register(validate_name_input), '%S')
        self.name_entry = ttk.Entry(self.name_enter_frame, width=20, font=12, textvariable=name_input, validate='key', validatecommand=validate_cmd)
        self.name_entry.grid(row=1, column=0, padx=(20, 20), pady=(5, 5))
        
        help_label = tk.Label(self.name_enter_frame, text='Press enter to continue', font=root.content_font, background='white')
        help_label.grid(row=2, column=0, padx=(20, 20), pady=(5, 10))
        
        # Highscore frame
        self.hs_frame = tk.Frame(self, background='#FFB600')
        
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
                           command=lambda: root.show_frame(MainMenuFrame))
        
    def on_enable(self):
        self.play_again_button.grid_forget()
        self.hs_frame.grid_forget()
        self.name_enter_frame.grid(row=0, column=0, sticky='s')
        self.name_entry.focus()
        def on_enter_name(event):
            self.root.last_name = self.name_entry.get()
            
            # Save highscore
            if self.root.last_name != '':
                with open(f'highscores{self.root.difficulty}.txt', 'a+') as f:
                    f.write(f'{self.root.last_name},{self.root.last_score}\n')
            
            self.show_highscores()
        self.name_entry.bind("<Return>", on_enter_name)
    
    def show_highscores(self):
        self.name_entry.unbind("<Return>")
        
        self.name_enter_frame.grid_forget()
        self.hs_frame.grid(row=0, column=0, ipady=10)
        self.play_again_button.grid(row=0, column=0, pady=(20, 20), sticky='s')
        
        # Read from highscore file
        scores: list = []
        with open(f'highscores{self.root.difficulty}.txt','a+') as f:
            f.seek(0)
            while True:
                line = f.readline()
                if not line:
                    break
                split_line = line.strip().split(',')
                if len(split_line) == 2 and is_float(split_line[1]):
                    split_line[1] = float(split_line[1])
                    scores.append(tuple(split_line))
                
        # Sort highscores
        scores.sort(key=lambda tup: float(tup[1]))
                
        # Create labels (only first 10)
        score_labels = [(tk.Label(self.hs_frame, text=name, font=self.root.content_font, background='#FFB600'), tk.Label(self.hs_frame, text=f'{time}s', font=self.root.content_font, background='#FFB600')) for name, time in scores[:10]]
        # Grid those labels!
        for i, player_label in enumerate(score_labels):
            name_label, time_label = player_label
            name_label.grid(row=i+1, column=0, padx=(20, 20), pady= (2, 2), sticky='w')
            time_label.grid(row=i+1, column=1, padx=(20, 20), pady= (2, 2), sticky='e')

class EndLoseFrame(gc.GameFrame):
    """Ending page on lose.

    Inherits:
        gc.GameFrame
    """

    def __init__(self, parent, root):
        super().__init__(parent, root)
        self.background_image3 = tk.PhotoImage(file="./assets/You_Lose.png")
        label = tk.Label(self, text="You ded lol",
                         font=root.title_font,
                         image = self.background_image3,
                         compound = "center")
        label.grid(row=0, column=0, sticky="nsew")

        # styling buttons
        style = ttk.Style()
        style.configure("TButton", font=root.button_font)
        style.map("TButton",
                  foreground=[('pressed', 'red'), ('active', 'blue')],
                  background=[('pressed', '!disabled', 'black'),
                              ('active', 'white')])
        button = ttk.Button(self, text="Play Again",
                           command=lambda: root.show_frame(MainMenuFrame))
        button.place(x=400,y=535, anchor = "n")

if __name__ == '__main__':
    width, height = 800, 600
    animation_fps = 60
    frame_list = [MainMenuFrame, CreditsFrame, DifficultyFrame, GameFrame, EndWinFrame, EndLoseFrame]
    
    app = MainApp(width, height, animation_fps, frame_list)
    app.resizable(False, False)
    app.title('Cat me if you can! by 21F01 - Team 1J')
    app.iconbitmap('icon.ico')
    app.mainloop()

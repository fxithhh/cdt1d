from timeit import default_timer as timer
import random
from wordlist import *
from enum import Enum

#Create a class 
class GameScrambled():
    
    diffculty_map: dict = {1: 1, 2: 0.74, 3: 0.5} # Maps the cat running speed to the difficulty
    
    """
    -----------------------------------------------------------------------------------------------------------------------------------------------
    CREATING RANDOMISED WORD LIST
    -----------------------------------------------------------------------------------------------------------------------------------------------
    """
    #Defining all the variables needed and declaring the type of inputs the variable will take
    
    rando_list: list = []
    question_index: int = 0

    """Creating a function to call the wordlist from wordlist.py based on difficulty chosen"""
    def set_current_list(self):
        if self.difficulty == 1:
            return easyword

        elif self.difficulty == 2:
            return medword

        elif self.difficulty == 3:
            return hardword

        else:
            print("Something went wrong")

    """Creating a function to randomise the words inside the current list"""
    def randomize_list(self):
        return random.shuffle(self.current_list)

    """Creating a function to randomise the letters in the word"""
    def randomize(self, word):
        letters = []
        for char in word:
            letters.append(char) #Creating a list of all the letters in the word

        random.shuffle(letters) #Shuffling the letters

        return ''.join(letters) #Return the scrambled words

    #Get the current shuffled word
    def get_current_scrambled_word(self) -> str:
        return self.rando_list[self.question_index]
    
    #Get the actual word
    def get_current_original_word(self) -> str:
        return self.current_list[self.question_index]


    """
    -----------------------------------------------------------------------------------------------------------------------------------------------
    POINT SYSTEM AND WIN TYPES
    -----------------------------------------------------------------------------------------------------------------------------------------------
    """
    
    """Main Variables that will be used"""

    cat_initial: int = 0 #Initial points of the cat

    game_time_start: float = 0.0 #Starting time 
    
    fast_win_points: int = 30 #How many points the user should achieve to get a fast win

    on_win_callback = None

    #Get Mouse Points
    def get_mouse_points(self) -> int:
        return self.mouse_point

    #Get Cat Points
    def get_cat_points(self) -> float:
        return self.get_game_time()*self.diffculty_map[self.difficulty] + self.cat_initial

    #Get difference between mouse and cat points that will determine the end game conditions
    def get_cat_dist_from_mouse(self) -> float:
        return self.mouse_point - self.get_cat_points()

    #Getting the time taken to answer a question for the Mouse Points
    def get_question_time(self) -> float:
        return timer() - self.qn_time_start
    
    #Getting the total time the game has been running for the Cat Points
    def get_game_time(self) -> float:
        return timer() - self.game_time_start


    """Create a function that determines the points based on the time taken to solve the question"""
    def get_answer_point_level(self) -> int: #Returns an int
        c_time = self.get_question_time() #Getting the time taken to solve the question
        
        #Point system
        if c_time < 3:
            return 5
        elif c_time < 6:
            return 4
        elif c_time < 10:
            return 3
        elif c_time < 15:
            return 2
        else:
            return 1


    """Create a class to set up the type of wins"""
    class WinType(Enum):
        LOSE = 0
        WIN = 1
        BIG_WIN = 2


    """
    Create a function that determines which type of win did the user achieve
    Function will return the values from WinType Class
    """
    def on_game_end_condition(self, win: bool, epic_win: bool = False) -> WinType:
        if win:
            if epic_win:
                print("DAYUM you left the cat in the dust!!!")
                if self.on_win_callback:
                    self.on_win_callback(self.WinType.BIG_WIN)
            else:
                print("Winner winner chicken dinner!")
                if self.on_win_callback:
                    self.on_win_callback(self.WinType.WIN)
        else:
            print("Caught by cat!")
            if self.on_win_callback:
                self.on_win_callback(self.WinType.LOSE)



    """Creating a function that checks if the cat has catch up with the mouse"""
    def check_cat_position(self):
        
        #Lose Condition
        if self.get_cat_dist_from_mouse() < 0:
            self.on_game_end_condition(False)

        #Early win condition
        if self.get_cat_dist_from_mouse() >= self.fast_win_points:
            self.on_game_end_condition(True, True)


    """
    -----------------------------------------------------------------------------------------------------------------------------------------------
    GAME FLOW
    -----------------------------------------------------------------------------------------------------------------------------------------------
    """
    
    #Main variables required

    total_questions: int = 10 #Total number of questions asked

    on_question_callback = None

    results = []

    
    """Create a function to give the new question"""
    def next_question(self):
        self.question_index += 1

        #Checking if all the questions have been asked, if all have been asked get the win condition and end the game
        if self.question_index >= len(self.rando_list) or self.question_index >= self.total_questions: 

            #Give the end game condition, if cat_dist_from_mouse <0, return False (Lose), else return True (Win but not BIG_WIN)
            self.on_game_end_condition(self.get_cat_dist_from_mouse() > 0) 
            return
        
        #start the timer the moment the new question is given 
        self.qn_time_start = timer()
        print("Unscramble this:", self.get_current_scrambled_word())

        #Replace the variable on_question_callback with the current scrambled word
        self.on_question_callback(self.get_current_scrambled_word())
    
    
    """
    Create a function to check the answer and award points respectively, 
    the function has to return an int as defined by f()-> int 
        
    Summary for the point system: Skip: -3, Wrong: -1, Correct: Depending on the time
    """
    def check_answer(self, answer, skip: bool = False) -> int: 
        original_word = self.get_current_original_word() #getting the original word
        question_points = 0 #points for this specific question is initially 0
        
        # Check guesses 
        if skip:
            question_points = -3 
            print("Skipped. -3 points.")
        
            self.next_question() # Start next question
        
        else:
            if answer.lower() == original_word.lower(): # Correct answer
                question_points = self.get_answer_point_level() #Getting the amt of points awared based on the time taken
                print(f"You have earned {question_points} points! Time: {self.get_question_time()}s")
                
                self.next_question() # Start next question
            
            else: #Wrong answer 
                question_points = -1 
                print("Wrong answer. -1 point.")
    
                self.next_question() #Start the next question
        
        self.mouse_point += question_points #Collating the total amount of points 
        
        return question_points


    """
    ------------------------------------------------------------------------------------------------------------------------------------------------
    GAME
    ------------------------------------------------------------------------------------------------------------------------------------------------
    """
    def initiate_game(self, difficulty, cat_initial):
        self.difficulty = difficulty #Difficulty chosen by user
        
        # Initialize point values 
        self.mouse_point = 0
        self.cat_initial = cat_initial
        
        # Based on the button chosen, TKinter will return a specific value 1,2 or 3
        self.current_list = self.set_current_list()
        print("Difficulty:", self.difficulty, self.current_list)
        
        # Randomly shuffles the order of words 
        self.randomize_list()
        
        # Creates the list of the scrambled letters for the words
        self.rando_list = [self.randomize(word) for word in self.current_list]
        self.question_index = -1 # Needs to offset the initial addition 
        self.results = []
        
        # Begin game timer
        self.game_time_start = timer()
        
        # Begin the first question
        self.next_question()

if __name__ == "__main__":
    gamestart = GameScrambled()
    gamestart.initiate_game(2)
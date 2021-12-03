from timeit import default_timer as timer
import random
from wordlist import *
from enum import Enum

#Request user input
class GameScrambled():
    
    rando_list: list = []
    question_index: int = 0
    
    game_time_start: float = 0.0
    
    cat_initial: int = 0
    
    fast_win_points: int = 30
    
    total_questions: int = 10
    
    on_win_callback = None
    on_question_callback = None

    results = []
    
    # Maps the cat running speed to the difficulty
    diffculty_map: dict = {1: 1, 2: 0.74, 3: 0.5}
    
    class WinType(Enum):
        LOSE = 0
        WIN = 1
        BIG_WIN = 2
    
    def next_question(self):
        self.question_index += 1
        if self.question_index >= len(self.rando_list) or self.question_index >= self.total_questions:
            self.on_game_end_condition(self.get_cat_dist_from_mouse() > 0)
            return
        
        self.qn_time_start = timer()
        print("Unscramble this:", self.get_current_scrambled_word())
        self.on_question_callback(self.get_current_scrambled_word())
    
    def check_answer(self, answer, skip: bool = False) -> int:
        original_word = self.get_current_original_word()
        question_points = 0
        
        # Check guesses
        if skip:
            question_points = -3
            print("Skipped. -3 points.")
        
            # Start next question
            self.next_question()
        else:
            if answer.lower() == original_word.lower():
                # Correct answer
                question_points = self.get_answer_point_level()
                print(f"You have earned {question_points} points! Time: {self.get_question_time()}s")
                
                # Start next question
                self.next_question()
            else:
                # Wrong answer
                question_points = -1
                print("Wrong answer. -1 point.")
        
        self.mouse_point += question_points
        # self.results.append((answer, self.get_current_original_word()))
        
        return question_points
    
    def get_answer_point_level(self) -> int:
        c_time = self.get_question_time()
        if c_time < 2:
            return 5
        elif c_time < 5:
            return 4
        elif c_time < 9:
            return 3
        elif c_time < 14:
            return 2
        else:
            return 1
    
    def check_cat_position(self):
        # Lose Condition
        if self.get_cat_dist_from_mouse() < 0:
            self.on_game_end_condition(False)

        # Early win condition
        if self.get_cat_dist_from_mouse() >= self.fast_win_points:
            self.on_game_end_condition(True, True)

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

    # call the list from wordlist.py    
    def set_current_list(self):
        if self.difficulty == 1:
            return easyword
        elif self.difficulty == 2:
            return medword
        elif self.difficulty == 3:
            return hardword
        else:
            print("Something went wrong")

    def randomize(self, word):
        letters = []
        for char in word:
            letters.append(char)

        random.shuffle(letters)

        return ''.join(letters)
    
    def get_current_scrambled_word(self) -> str:
        return self.rando_list[self.question_index]
    
    def get_current_original_word(self) -> str:
        return self.current_list[self.question_index]

    def get_mouse_points(self) -> int:
        return self.mouse_point

    def get_cat_points(self) -> float:
        return self.get_game_time()*self.diffculty_map[self.difficulty] + self.cat_initial

    def get_cat_dist_from_mouse(self) -> float:
        return self.mouse_point - self.get_cat_points()

    # TIME TAKEN TO ANSWER EACH QUESTION
    def get_question_time(self) -> float:
        return timer() - self.qn_time_start
    
    def get_game_time(self) -> float:
        return timer() - self.game_time_start

    def initiate_game(self, difficulty, cat_initial):
        self.difficulty = difficulty
        
        # Initialize values
        self.mouse_point = 0
        self.cat_initial = cat_initial
        
        # Input 1,2,3 should be button from tkinter
        self.current_list = self.set_current_list()
        print("Difficulty:", self.difficulty, self.current_list)
        
        # Shuffles order of words
        random.shuffle(self.current_list)
        
        # List of random words
        self.rando_list = [self.randomize(word) for word in self.current_list]
        self.question_index = -1 # needs to offset the initial addition
        self.results = []
        
        # Begin game timer
        self.game_time_start = timer()
        
        # Begin the first question
        self.next_question()

if __name__ == "__main__":
    gamestart = GameScrambled()
    gamestart.initiate_game(2)
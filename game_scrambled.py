from timeit import default_timer as timer
import random
from wordlist import *

#Request user input
class GameScrambled():
    
    rando_list: list = []
    question_index: int = 0
    
    game_time_start: float = 0.0
    
    on_win_callback = None
    
    def next_question(self):
        self.question_index += 1
        if self.question_index >= len(self.rando_list):
            self.on_game_end_condition(self.get_cat_dist_from_mouse() > 0)
            return
        
        self.qn_time_start = timer()
        print("Unscramble this:", self.get_current_scrambled_word())
    
    def check_answer(self, original_word, answer, skip: bool = False):
        c_time = self.get_question_time()
        
        question_points = 0
        
        # Check guesses
        if skip:
            question_points = -3
            print("Skipped. -3 points.")
        else:
            #correct answer
            if answer.lower() == original_word.lower():
                if 0 <= c_time < 4:
                    question_points = 5
                elif 4 <= c_time < 8:
                    question_points = 4
                elif 8 <= c_time < 12:
                    question_points = 3
                elif 12 <= c_time < 16:
                    question_points = 2
                elif 16 <= c_time < 32:
                    question_points = 1
                else:
                    question_points = 0
                print(f"You have earned {question_points} points! Time: {self.time_diff_sec}s")
            else:
                #wrong answer
                question_points = -1
                print("Wrong answer. -1 point.")
        
        self.mouse_point += question_points
        self.results.append((answer, self.get_current_original_word()))
        
        # Start next question
        self.next_question()
    
    def check_cat_position(self):
        self.cat_points = self.get_game_time() * 2 # Every 3 Sec cat_point +1
        
        # Lose Condition
        if self.get_cat_dist_from_mouse() < 0:
            self.on_game_end_condition(False)

        # Win condition 50 pts to win
        if self.get_cat_dist_from_mouse() >= 45:
            self.on_game_end_condition(True, True)

    def on_game_end_condition(self, win: bool, epic_win: bool = False) -> int:
        if win:
            if epic_win:
                print("DAYUM you left the cat in the dust!!!")
                if self.on_win_callback:
                    self.on_win_callback(2)
            else:
                print("Winner winner chicken dinner!")
                if self.on_win_callback:
                    self.on_win_callback(1)
        else:
            print("Caught by cat!")
            if self.on_win_callback:
                self.on_win_callback(0)

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

    def randomize(self,word):
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

    def get_cat_dist_from_mouse(self) -> float:
        return self.mouse_point - self.cat_points

    # TIME TAKEN TO ANSWER EACH QUESTION
    def get_question_time(self) -> float:
        return timer() - self.qn_time_start
    
    def get_game_time(self) -> float:
        return timer() - self.game_time_start

    def initiate_game(self, difficulty):
        self.difficulty = difficulty
        
        # Initialize values
        self.mouse_point = 4
        self.cat_points = 0
        
        # Input 1,2,3 should be button from tkinter
        self.current_list = self.set_current_list()
        print("Difficulty:", self.difficulty, self.current_list)
        
        # Shuffles order of words
        random.shuffle(self.current_list)
        
        # List of random words
        self.rando_list = [self.randomize(word) for word in self.current_list]
        self.question_index = -1 # needs to offset the initial addition
        
        # Begin game timer
        self.game_time_start = timer()
        
        # Begin the first question
        self.next_question()

if __name__ == "__main__":
    gamestart = GameScrambled()
    gamestart.initiate_game(2)
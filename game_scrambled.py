# Timing game events
from timeit import default_timer as current_time

# RNG
import random

# Constant preset values
from enum import Enum

# Better type hinting
from typing import *

# Game word list
from wordlist import *


class GameScrambled():
    """Core game logic class.

    Members:
        difficulty_map (Dict[int, int]): Maps the speed of the cat to the difficulty setting.
        original_list (List[str]): Original word list
        shuffled_list (List[str]): Shuffled word list with shuffled words.
        question_index (int): Current position on the list of words that the player has progressed.

        cat_initial (int): Amount of points the cat starts the game with.
        game_time_start (float): The system time at the moment the game starts.
        fast_win_points (int): The point difference between the player and the cat for an early win.
        on_question_callback (Callable[[str], None]): Callback function that gets invoked when a new question is asked. Passes the new scrambled word as argument.
        on_win_callback (Callable[[WinType], None]): Callback function that gets invoked when a winning condition is triggered (e.g. early win, normal win, loss). Passes the WinType of the round as argument.
    """

    class WinType(Enum):
        """Types of game end conditions.
        """

        LOSE = 0
        WIN = 1
        BIG_WIN = 2

    # Member list
    difficulty_map: Dict[int, int] = {1: 1, 2: 0.74, 3: 0.5} # Maps the cat running speed to the difficulty
    original_list: List[str] = [] # Original word list
    shuffled_list: List[str] = []
    total_questions: int = 10 # Total number of questions per round
    question_index: int = 0

    cat_initial: int = 0 # Amount of points the cat starts the game with.
    game_time_start: float = 0.0 # The system time at the moment the game starts.
    fast_win_points: int = 30 # The point difference between the player and the cat for an early win.
    on_question_callback: Callable[[str], None] = None
    on_win_callback: Callable[[WinType], None] = None

    results = []


    """
    -----------------------------------------------------------------------------------------------------------------------------------------------
    CREATING RANDOMISED WORD LIST
    -----------------------------------------------------------------------------------------------------------------------------------------------
    """

    def get_current_word_list(self) -> List[str]:
        """Sets the word list for the current difficulty.

        Returns:
            List[str]: Word list of the current difficulty.
        """

        if self.difficulty == 1:
            return easyword

        elif self.difficulty == 2:
            return medword

        elif self.difficulty == 3:
            return hardword

        else:
            print("Difficulty setting is invalid.", self.difficulty)

    def shuffle_list(self) -> List[str]:
        """Shuffles the words inside the current list.

        Returns:
            List[str]: Shuffled word list.
        """

        return random.shuffle(self.original_list)

    def shuffle_word(self, word: str) -> str:
        """Shuffle letters in a word.

        Args:
            word (str): Input word.

        Returns:
            str: Shuffled word.
        """

        letters = []
        for char in word:
            letters.append(char) #Creating a list of all the letters in the word

        random.shuffle(letters) #Shuffling the letters

        random_word = ''.join(letters)

        while random_word == word: #Make sure the reshuffled words do not reshuffle to the original word
            random.shuffle(letters)

        return random_word #Return the scrambled words

    def get_current_scrambled_word(self) -> str:
        """Gets the scrambled word for the current question.

        Returns:
            str: Current scrambled word.
        """

        return self.shuffled_list[self.question_index]

    def get_current_original_word(self) -> str:
        """Gets the original, unscrambled word for the current question.

        Returns:
            str: Current original word.
        """
        return self.original_list[self.question_index]


    """
    -----------------------------------------------------------------------------------------------------------------------------------------------
    POINT SYSTEM
    -----------------------------------------------------------------------------------------------------------------------------------------------
    """

    def get_mouse_points(self) -> int:
        """Gets the current mouse (player) points.

        Returns:
            int: Current mouse points.
        """

        return self.mouse_point

    def get_cat_points(self) -> float:
        """Gets the current cat points. Time-based and scales based on difficulty.
        Refer to difficulty_map for scaling.

        Returns:
            float: Current cat points.
        """

        return self.get_game_time()*self.difficulty_map[self.difficulty] + self.cat_initial

    def get_cat_dist_from_mouse(self) -> float:
        """Difference between the cat points and mouse points.

        Returns:
            float: Difference between the cat points and mouse points.
        """

        return self.get_mouse_points() - self.get_cat_points()

    def get_question_time(self) -> float:
        """Gets the current time elapsed on the current question.

        Returns:
            float: Current time elapsed on the current question.
        """

        return current_time() - self.qn_time_start

    def get_game_time(self) -> float:
        """Gets the time elapsed for the current game.

        Returns:
            float: Time elapsed for the current game.
        """
        return current_time() - self.game_time_start

    def get_answer_point_level(self) -> int:
        """Gets the time-based points rewarded for the current question. Depends on when this function is called.

        Rewards in priority:
            5 points if under 2s\n
            4 points if under 5s\n
            3 points if under 9s\n
            2 points if under 15s\n
            1 point otherwise.

        Returns:
            int: Points rewarded.
        """

        # Time taken to solve the question
        c_time = self.get_question_time()

        #Point system
        if c_time < 2:
            return 5
        elif c_time < 5:
            return 4
        elif c_time < 9:
            return 3
        elif c_time < 15:
            return 2
        else:
            return 1

    def on_game_end_condition(self, win: bool, epic_win: bool = False):
        """Triggers the on_win_callback based on the winning condition.

        Args:
            win (bool): Whether it was a win.s
            epic_win (bool, optional): Whether it was an epic win. Defaults to False.
        """

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

    def check_cat_position(self) -> None:
        """ Checks the cat position and whether the cat has caught up with the mouse, or if the mouse has left the cat in the dust. Triggers the game ending condition if it has.
        """

        # Lose Condition
        if self.get_cat_dist_from_mouse() < 0:
            self.on_game_end_condition(False)

        # Early win condition
        if self.get_cat_dist_from_mouse() >= self.fast_win_points:
            self.on_game_end_condition(True, True)


    """
    -----------------------------------------------------------------------------------------------------------------------------------------------
    CORE GAME FLOW
    -----------------------------------------------------------------------------------------------------------------------------------------------
    """


    def next_question(self) -> None:
        """Triggers the next question, or end the game if the total questions asked has been reached.
        """

        self.question_index += 1

        # Checking if all the questions have been asked, if all have been asked get the win condition and end the game
        if self.question_index >= len(self.shuffled_list) or self.question_index >= self.total_questions:

            # Give the end game condition, if cat_dist_from_mouse <0, return False (Lose), else return True (Win but not BIG WIN)
            self.on_game_end_condition(self.get_cat_dist_from_mouse() > 0)
            return

        # Start the timer the moment the new question is given
        self.qn_time_start = current_time()
        print("Unscramble this:", self.get_current_scrambled_word())

        # Replace the variable on_question_callback with the current scrambled word
        if self.on_question_callback:
            self.on_question_callback(self.get_current_scrambled_word())

    def check_answer(self, answer: str, skip: bool = False) -> int:
        """Check the player's answer and award points respectively.

        Summary for the point system: Skip: -3, Wrong: -1, Correct: Depending on the time

        Args:
            answer (str): Player's answer
            skip (bool, optional): Whether the question was skipped. Defaults to False.

        Returns:
            int: Amount of points obtained from the answer. Can be negative (in the case of a skip or wrong answer).
        """

        original_word = self.get_current_original_word() # Get the original (unscrambled) word
        question_points = 0 # Initialize the question points variable

        # Check guesses
        if skip:
            # Skipped

            question_points = -3
            print("Skipped. -3 points.")

            self.next_question() # Start next question

        else:
            if answer.lower() == original_word.lower():
                # Correct answer

                question_points = self.get_answer_point_level() # Get the amt of points awared based on the time taken
                print(f"You have earned {question_points} points! Time: {self.get_question_time()}s")

                self.next_question() # Start next question

            else:
                # Wrong answer

                question_points = -1
                print("Wrong answer. -1 point.")

                self.next_question() # Start the next question

        self.mouse_point += question_points # Collating the total amount of points

        return question_points

    def initiate_game(self, difficulty: int, cat_initial: int) -> None:
        """Start the game round.

        Args:
            difficulty (int): Difficulty for this game round.
            cat_initial (int): Initial points for the cat.
        """

        # Initialize point values
        self.mouse_point = 0
        self.cat_initial = cat_initial

        self.difficulty = difficulty # Difficulty chosen by user
        self.original_list = self.get_current_word_list()
        print("Difficulty:", self.difficulty, self.original_list)

        # Shuffle the order of words
        self.shuffle_list()

        # Creates the list of the scrambled letters for the words
        self.shuffled_list = [self.shuffle_word(word) for word in self.original_list]
        self.question_index = -1 # Offset the initial increment from self.next_question
        self.results = []

        # Record game start time
        self.game_time_start = current_time()

        # Begin the first question
        self.next_question()

if __name__ == "__main__":
    gamestart = GameScrambled()
    gamestart.initiate_game(2, -10)
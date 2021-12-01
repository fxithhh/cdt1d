import time
import random
from wordlist import *
#Request user input
class Gamescrambled():
    def __init__(self,difficulty):
        self.difficulty = difficulty

    def get_answer(self):
        self.user_answer = input("[//] to pass. \nUnscrambled word: ")
        return self.user_answer


    def check_answer(self,scrambled_word, original_word):
        start_time = time.time()
        useranswer = self.get_answer()
        end_time = time.time()
        self.time_diff_sec = end_time - start_time
        #Take too long to guess
        if time_diff_sec >=10:
            point = 0
            print( "Give up/Times up. \n 0 Points.\n Next ones coming")
            return point,(useranswer,original_word)
        #skipped
        if useranswer =="//":
            point = -2
            print("Skipped. \n -2 Points.")
            return point,("Skipped",original_word)
        #correct answer
        if useranswer.lower() == original_word.lower():
            if 0 <= time_diff_sec < 4:
                point = 5
            elif 4 <= time_diff_sec < 8:
                point = 4
            elif 8 <= time_diff_sec < 12:
                point = 3
            elif 12 <= time_diff_sec < 16:
                point = 2
            elif 16 <= time_diff_sec < 32:
                point = 1
            else:
                self.point = 0
            print("You have earned {} points!".format(point))
        #wrong answer
        else:
            print("Wrong answer. Points -3")
            point = -3
        return point,(useranswer,original_word)

    #Call the list from wordlist.py    
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


    def get_mouse_points(self):
        return self.mouse_point

    def get_cat_dist_from_mouse(self):
        return self.cat_dist_from_mouse


    #TIME TAKEN TO ANSWER EACH QUESTION
    def get_time_taken_answer(self):
        return self.time_diff_sec

    def initiate_game(self):
        #Mouse Speed
        self.mouse_point = 4
        #Input 1,2,3 should be button from tkinter
        self.current_list = self.set_current_list()
        #Shuffles order of words
        random.shuffle(self.current_list)
        #list of random words
        self.rando_list = [self.randomize(word)for word in self.current_list]
        #Cat Points start
        global_time_start = time.time()
        self.results = []
        for index,rando_word in enumerate(self.rando_list):
            print("Unscramble this: " + rando_word.lower())
            add_point,add_tuple =self.check_answer(rando_word,self.current_list[index])
            self.mouse_point+=add_point
            #Check their guesses
            self.results.append(add_tuple)
            global_time_end = time.time()
            self.cat_points = (global_time_end - global_time_start)//3 # Every 3 Sec cat_point +1
            self.cat_dist_from_mouse = self.mouse_point - self.cat_points
            #Lose Condition
            if self.cat_points > self.mouse_point:
                print("Caught by cat")
                self.got_win = False
                break

            #Win condition 50 pts to win
            if self.cat_dist_from_mouse>=45:
                print("You left the cat in the dust.")
                self.got_win = True
                break
            self.got_win = None

        
        #Check all the guess and answers
        print("Let's see your answers!")
        for twin_values in self.results:
            print(twin_values)
        if self.got_win == True:
            print("You won!")
        elif self.got_win == False:
            print("You've turned into Ratatoullie")
        else:
            print("Barely got by")

if __name__ == "__main__":
    gamestart = Gamescrambled(1)
    
    gamestart.initiate_game()

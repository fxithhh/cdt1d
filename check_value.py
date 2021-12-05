import time
import random
from tkinter import Entry
from gameclasses import GameFrame
import main as mn
from wordlist import *
#Request user input
def get_answer():
    user_answer = input("[//] to pass. \nUnscrambled word: ")
    # user_answer = mn.GameFrame
    return user_answer


def check_answer(scrambled_word, original_word):
    start_time = time.time()
    useranswer = get_answer()
    end_time = time.time()
    time_diff_sec = end_time - start_time
    #Take too long to guess
    if time_diff_sec >=10:
        point = 0
        timesuptxt = "Give up/Times up. \n 0 Points.\n Next ones coming"
        print(timesuptxt)
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
            point = 0
        print("You have earned {} points!".format(point))
    #wrong answer
    else:
        print("Wrong answer. Man mode for 2 seconds. Points -2")
        point = -2
        time.sleep(2)
    return point,(useranswer,original_word)

#Call the list from wordlist.py
def set_current_list(difficulty):
    if difficulty == 1:
        return easyword
    elif difficulty == 2:
        return medword
    elif difficulty == 3:
        return hardword
    else:
        print("Something went wrong")


def randomize(word):
    letters = []
    for char in word:
        letters.append(char)

    random.shuffle(letters)

    return ''.join(letters)


def initiate_game(current_list):
    #Mouse Speed
    mouse_point = 4
    #Input 1,2,3 should be button from tkinter
    # current_list = set_current_list(int(input("1 or 2 or 3: ")))
    #Shuffles order of words
    random.shuffle(current_list)
    #list of random words
    rando_list = [randomize(word)for word in current_list]
    #Cat Points start
    global_time_start = time.time()
    results = []
    for index,rando_word in enumerate(rando_list):
        print("Unscramble this: " + rando_word.lower())
        add_point,add_tuple =check_answer(rando_word,current_list[index])
        mouse_point+=add_point
        #Check their guesses
        results.append(add_tuple)
        global_time_end = time.time()
        cat_points = (global_time_end - global_time_start)//3 # Every 3 Sec cat_point +1
        cat_dist_from_mouse = mouse_point - cat_points
        #Lose Condition
        if cat_points > mouse_point:
            print("Caught by cat")
            got_win = False
            break

        #Win condition 50 pts to win
        if cat_dist_from_mouse>=45:
            print("You left the cat in the dust.")
            got_win = True
            break
        got_win = None


    #Check all the guess and answers
    print("Let's see your answers!")
    for twin_values in results:
        print(twin_values)
    if got_win == True:
        print("You won!")
    elif got_win == False:
        print("You've turned into Ratatoullie")
    else:
        print("Barely got by")


if __name__ == "__main__":
    initiate_game()

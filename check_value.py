import time
import random
from wordlist import *
#Request user input
def get_answer(scrambled_word):
    user_answer = input(
        "[{}]\n[//] to pass. \nUnscrambled word: ".format(scrambled_word))
    return user_answer


def check_answer(scrambled_word, original_word):
    start_time = time.time()
    useranswer = get_answer(scrambled_word)
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
        print("Wrong answer. You have been stunned for 2 seconds. Points -2")
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


def main():
    #Mouse Speed
    mouse_point = 2
    #Input 1,2,3 should be button from tkinter
    current_list = set_current_list(int(self.root.difficulty))
    
    #list of random words
    rando_list = [randomize(word)for word in current_list]
    #Cat Points start
    global_time_start = time.time()
    results = []
    for index,rando_word in enumerate(rando_list):
        print("Unscramble this: " + rando_word)
        add_point,add_tuple =check_answer(rando_word,current_list[index])
        mouse_point+=add_point
        #Check their guesses
        results.append(add_tuple)
        global_time_end = time.time()
        cat_points = (global_time_end - global_time_start)//4 # Every 4 Sec cat_point +1
        
        #Lose Condition
        if cat_points > mouse_point:
            print("Caught by cat")
            break
    
    #Check all the guess and answers
    for twin_values in results:
        print(twin_values)
    print(mouse_point)

if __name__ == "__main__":
    main()

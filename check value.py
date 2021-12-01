import time
import random
from wordlist import *
def get_answer(scrambled_word):
    user_answer = input("[{}]\n[//] to pass. \nUnscrambled word: ".format(scrambled_word))
    return user_answer

def check_answer(scrambled_word,original_word):
    start_time = time.time()
    useranswer = get_answer(scrambled_word)
    end_time = time.time()
    time_diff_sec = end_time - start_time
    if time_diff_sec >=10 or useranswer == "//":
        point = 0
        timesuptxt = "Give up/Times up. \n 0 Points.\n Next ones coming"
        print(timesuptxt)
        return point,(useranswer,original_word)
    if useranswer.lower() == original_word.lower():
        if 0<=time_diff_sec<4:
            point = 5
        elif 4<=time_diff_sec<8:
            point = 4
        elif 8<=time_diff_sec<12:
            point = 3
        elif 12<=time_diff_sec<16:
            point = 2
        elif 16<=time_diff_sec<32:
            point = 1
        else:
            point = 0
        print("You have earned {} points!".format(point))
    else:
        print("Wrong answer. You have been stunned for 3 seconds. Points -1")
        point = -1
        time.sleep(3)
    return point,(useranswer,original_word)

    
def set_current_list(difficulty):
    if difficulty ==1:
        return easyword
    elif difficulty ==2:
        return medword
    elif difficulty ==3:
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
    total_point = 0
    current_list = set_current_list(int(input("Set 1,2,3 : ")))
    rando_list = [randomize(word)for word in current_list]
    for index,rando_word in enumerate(rando_list):
        print("Unscramble this: " + rando_word)
        add_point,add_tuple =check_answer(rando_word,current_list[index])
        total_point+=add_point
    print(total_point)


main()

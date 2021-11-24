import time

def get_answer():
    user_answer = input("[//] to pass. \nUnscrambled word: ")
    return user_answer

def check_answer(original_word,difficulty_no):
    time_multiplier = 1/(2*difficulty_no)
    start_time = time.time()
    useranswer = get_answer()
    end_time = time.time()
    time_diff_sec = end_time - start_time
    if time_diff_sec >=10 or useranswer == "//":
        point = 0
        timesuptxt = "Give up/Times up. \n 0 Points.\n Next ones coming"
        print(timesuptxt)
        return point,(useranswer,original_word)
    if useranswer == original_word:
        if 0<=time_diff_sec<4*time_multiplier:
            point = 5
        elif 4*time_multiplier<=time_diff_sec<8*time_multiplier:
            point = 4
        elif 8*time_multiplier<=time_diff_sec<12*time_multiplier:
            point = 3
        elif 12*time_multiplier<=time_diff_sec<16*time_multiplier:
            point = 2
        elif 16*time_multiplier<=time_diff_sec<32*time_multiplier:
            point = 1
        else:
            point = 0
        print("You have earned {} points!".format(point))
    else:
        print("Wrong answer. You have been stunned for 3 seconds. Points -1")
        point = -1
        time.sleep(3)
    return point,(useranswer,original_word)


check_answer("Hippo",2)
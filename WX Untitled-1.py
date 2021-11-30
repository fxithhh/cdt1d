import random

Word_list = ["skunk", "hippo",]

for word in Word_list:
    letters = []
    for char in word:
        letters.append(char)
    
    letters_copy = letters[:]
    random.shuffle(letters_copy)
    print(letters_copy)
    answer = input("What is the correct answer? Type // if you want to pass")
    
    if answer == "//":
        print("You passed the question")
        continue

    else:
        if answer == word:
            print("You are correct!")
        else:
            print("You are wrong")

#Get info  from BotD.txt
#if text != number or "run", format info for display
import time
import random

time.sleep(1)
#p = open("BotD.txt", "w")
#p.write("run")
#p.close()
print("Welcome to Bird of the Day!")
while True:
    inp = input("Enter B to view the Bird of the Day\nEnter Q to quit\n")#Enter H to view Bird of the Day history\nEnter A to view about page\nEnter Q to quit\n")

#while True:
    if inp == "B" or inp == "b":
        p = open("BotD.txt", "r")
        text = p.readlines()
        if text[0] != "run" and text[0].isnumeric() == False:
            print(f"Bird name: {text[0]}")
            print(f"Bird image: {text[1]}")
            print(f"Conservation status: {text[2]}")
            print(f"Wiki link: {text[3]}")
            #p.close()
            #break
        p.close()
        time.sleep(3)
    #elif inp == "H" or inp == "h":
    #    print("History page: TODO")
    #elif inp == "A" or inp == "a":
    #    print("About page: TODO")
    elif inp == "Q" or inp == "q":
        break

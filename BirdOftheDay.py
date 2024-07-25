#Get info  from BotD.txt
#if text != number or "run", format info for display
import time
import random
import webbrowser

time.sleep(1)
#p = open("BotD.txt", "w")
#p.write("run")
#p.close()
print("Welcome to Bird of the Day!")
while True:
    inp = input("Enter B to view the Bird of the Day\nEnter W to open the Wikipedia information page about the bird\nEnter Q to quit\n")#Enter H to view Bird of the Day history\nEnter A to view about page\nEnter Q to quit\n")

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
    elif inp == "W" or inp == "w":
        inp2 = input("This will open a new tab in your browser, are you sure you wish to leave the program? Enter 'y' for yes and 'n' for no\n")
        if inp2 == "Y" or inp2 == "y":
            p = open("BotD.txt", "r")
            text = p.readlines()
            if text[0] != "run" and text[0].isnumeric() == False:
                webbrowser.open(text[3],new=2)
            p.close()
    #elif inp == "H" or inp == "h":
    #    print("History page: TODO")
    #elif inp == "A" or inp == "a":
    #    print("About page: TODO")
    elif inp == "Q" or inp == "q":
        break
    print("\n")

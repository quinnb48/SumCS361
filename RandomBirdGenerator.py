#pick a random number between 1 and 10979
#return to GetFromWikiApi via BotD.txt
import time
import random

while True:
    time.sleep(1)
    p = open("BotD.txt", "r")
    text = p.readlines()
    text = text[0]
    print("BotD reads: " + text)
    if text == "run":
        print(text)
        p.close()
        p = open("BotD.txt", "w")
        num = random.randrange(0,10979,1)
        p.write(str(num))
    p.close()

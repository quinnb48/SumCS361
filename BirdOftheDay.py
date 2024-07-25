#Get info  from BotD.txt
#if text != number or "run", format info for display
import time
import random

time.sleep(1)
p = open("BotD.txt", "w")
p.write("run")
p.close()
while True:
    time.sleep(3)
    p = open("BotD.txt", "r")
    text = p.readlines()
    if text[0] != "run" and text[0].isnumeric() == False:
        print(f"Bird name: {text[0]}")
        print(f"Bird image: {text[1]}")
        print(f"Conservation status: {text[2]}")
        print(f"Wiki link: {text[3]}")

    p.close()

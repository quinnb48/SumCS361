#save previous closing date + time somewhere
#on opening, check what date + time it is
#if at least one midnight has passed, ie on different date, send "run" to BotD.txt
#during program, check what date + time is every minute or so
#ID midnight passes, send "run" to BotD.txt
#on ending program, save date + time

from datetime import date
import time

while True:
    t = open("time.txt", "r")
    day = t.readlines()
    day = day[0]

    if day != str(date.today()):
        t.close()
        t = open("time.txt", "w")
        #print("day is " + day)
        #print("date is " + str(date.today()))
        t.write(str(date.today()))
        p = open("BotD.txt", "w")
        p.write("run")
        p.close()
    t.close()
    time.sleep(3)

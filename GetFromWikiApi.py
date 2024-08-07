#Link to get bird extinction info and images:
#https://en.wikipedia.org/w/api.php?action=parse&format=json&page= <   BIRDNAME   > &redirects=1&prop=images%7Ctext&disableeditsection=1&disabletoc=1&formatversion=2

#Take random number from RandomBirdGenerator
#use number to pick specific line from ListOfAllBirds
#Use line as BIRDNAME in API requests, and return name
#search api image result for first bird image link
#search api text result for Least Concern, Conservation Dependent, Near Threatened, Vulnerable, Endangered, Critically Endangered, Extinct in the Wild, and Extinct
#return: bird name, bird image link, bird conservation status (whichever above returns as being in result), current date to BotD.txt


import time
from requests import post, get

def WikiApiGet(name):
    name = name.split(" ")
    name = "%20".join(name)
    name = name.split("\n")
    name = "".join(name)
    url = f'https://en.wikipedia.org/w/api.php?action=parse&format=json&page={name}&redirects=1&prop=images%7Ctext&disableeditsection=1&disabletoc=1&formatversion=2'
    headers = {'User-Agent': 'BirdOfTheDay/1.0 (https://github.com/quinnb48/SumCS361; quinnbehrens@gmail.com)'}
    result = get(url, headers = headers)
    json_result = result.json()
    #print("Result: ")
    #print(json_result)
    return json_result

def WikiApiImageUrlGet(file):
    url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=imageinfo&meta=&titles=File%3A{file}&formatversion=2&iiprop=url"
    headers = {'User-Agent': 'BirdOfTheDay/1.0 (https://github.com/quinnb48/SumCS361; quinnbehrens@gmail.com)'}
    result = get(url, headers = headers)
    json_result = result.json()
    try:
        print(json_result["query"]["pages"][0]["imageinfo"][0]["url"])
        return json_result["query"]["pages"][0]["imageinfo"][0]["url"]
    except:
        return "error getting image"

while True:
    time.sleep(1)
    print("Getting bird num...")
    p = open("BotD.txt", "r")
    num = p.read()
    print(f"Bird num: {num}")
    if(num.isnumeric()):
        num = int(num)
        print("Getting bird name...")
        birds = open('ListOfAllBirds.txt')
        birdName = birds.readlines()
        birdName = birdName[num-1]
        birdInfo = WikiApiGet(birdName)

        birdName = birdName.split("\n")
        birdName = "".join(birdName)

        conStat = ""
        wikiLink = ""
        try:
            if("Least Concern" in birdInfo['parse']['text']):
                conStat = "Least Concern"
            elif("Near Threatened" in birdInfo['parse']['text']):
                conStat = "Near Threatened"
            elif("Vulnerable" in birdInfo['parse']['text']):
                conStat = "Vulnerable"
            elif("Endangered" in birdInfo['parse']['text']):
                conStat = "Endangered"
            elif("Critically Endangered" in birdInfo['parse']['text']):
                conStat = "Critically Endangered"
            elif("Extinct in the Wild" in birdInfo['parse']['text']):
                conStat = "Extinct in the Wild"
            elif("Extinct" in birdInfo['parse']['text']):
                conStat = "Extinct"
            else:
                conStat = "Unknown"

            wikiLink = f"Wiki link: https://en.wikipedia.org/wiki/{birdName}"
        except:
            conStat = "Unknown"
            wikiLink = "Wiki link: Unavailable"

        print(f"Bird name: {birdName}")
        imageLink = ""
        try:
            imageLink = WikiApiImageUrlGet(birdInfo['parse']['images'][0])
            print(f"Image file: {imageLink}")
        except:
            print("Image not available")
            imageLink = "Image not available"
        print(f"Conservation status: {conStat}")
        print(wikiLink)
        i = open("BotD.txt", "w")
        i.write(f"{birdName}\n{imageLink}\n{conStat}\nhttps://en.wikipedia.org/wiki/{birdName}")
        i.close()
    p.close()

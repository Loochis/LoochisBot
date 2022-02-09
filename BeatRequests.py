# HANDLES BEAT SABER REQUESTS

from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chromeOptions = Options()
driver = webdriver.Chrome()
driver.minimize_window()

#driver = webdriver.Firefox()

class BSSong:
    url = ""
    id = ""
    name = ""
    description = ""
    upvotes = 0
    downvotes = 0
    mapper = ""
    coverArt = ""

    def __init__(self, url):
        self.url = url
        urlSplit = url.split('/')
        self.id = urlSplit[len(urlSplit)-1]
        driver.get(url)
        time.sleep(4)
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html.parser")
        self.name = str(soup.find("div", {"class": "card-header"}).contents[0])
        card = soup.find("div", {"class": "card-body"})
        self.coverArt = str(card.findNext().get("src"))
        self.description = '\n'.join([str(x) for x in card.find("div", {"class": "card-text"}).contents[::2]])
        listGroup = soup.find("div", {"class": "list-group"})
        self.mapper = str(listGroup.find("a").findNext().contents[0]).split('(')[0][0:-1]
        listGroupChildren = listGroup.findChildren("div")
        splitVotes = str(listGroupChildren[len(listGroupChildren)-1].findNext().contents[0]).split(" ")
        self.upvotes = int(splitVotes[0])
        self.downvotes = int(splitVotes[2])

class BSReqHandler:
    requests = []
    driver = None

    def __init__(self):
        try:
            open("BSReqs.txt", "x")
        except:
            pass

    def getBeatsaverPage(self, searchTerm):
        # Try getting from URL
        if searchTerm[0:8] == "https://":
            sliced = searchTerm.split('/')
            key = sliced[len(sliced) - 1]
            if key == "":
                return "Invalid URL!"
            driver.get('https://beatsaver.com/maps/' + key)
            time.sleep(1)
            if driver.current_url == 'https://beatsaver.com/maps/' + key:
                return 'https://beatsaver.com/maps/' + key
            else:
                return "Invalid URL!"

        # Try getting from key
        if len(searchTerm) <= 7:
            driver.get('https://beatsaver.com/maps/' + searchTerm)
            time.sleep(1)
            if driver.current_url == 'https://beatsaver.com/maps/' + searchTerm:
                return 'https://beatsaver.com/maps/' + searchTerm

        # Try getting from search term
        driver.get('https://beatsaver.com/?q=' + '%20'.join(searchTerm.split(' ')))
        time.sleep(1)
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html.parser")
        try:
            results = soup.find('main').find('div', {"class": "search-results"}).findChildren('div',
                                                                                              {"class": "beatmap"})
            outStr = "Please choose from these (+BS [code]):```\n"
            for child in results[0:4]:
                codeLine = "[{}]".format(child.find('div', {"class": "additional"}).findNext().contents[0])
                outStr += codeLine + " " * (9 - len(codeLine)) + " | "
                vote = child.find('div', {"class": "percentage"}).contents[0]
                outStr += "👍" + vote + " " * (5 - len(vote)) + " | "
                classes = child.get("class")
                if 'ranked' in classes:
                    outStr += '🏅'
                else:
                    outStr += '⬛'
                if 'curated' in classes:
                    outStr += '✍'
                else:
                    outStr += '⬛'
                outStr += " | "
                outStr += str(child.find('div', {"class": "info"}).findNext().contents[0])
                outStr += "\n"
            outStr += "```"
            return outStr
        except:
            return "Could not find any matching songs..."

    def get_reqs(self):
        reqLs = []
        reqFile = open("BSReqs.txt", "r")
        for line in reqFile:
            reqLs.append(line.strip('\n'))
        reqFile.close()
        self.requests = reqLs

    def add_req(self, song):
        self.get_reqs()
        if song.id + "" + song.name in self.requests:
            return False
        else:
            self.requests.append(song.id + "" + song.name)
            self.save_reqs()
            return True

    def reqsToString(self):
        outFl = ""
        for l in self.requests:
            outFl += l + "\n"
        return outFl

    def save_reqs(self):
        with open("BSReqs.txt", 'w') as file:
            file.write(self.reqsToString())
        file.close()

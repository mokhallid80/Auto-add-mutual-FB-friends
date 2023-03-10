# selenium setup
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Coloring lib
import colorama
from colorama import Fore

# For reading the JSON file
import json

# Time lib
import time

nme = ''
passwrd = ''

min_mutual_friends_count = 1

# Coloring the output
successColor = Fore.GREEN 
dangerColor = Fore.RED
infoColor = Fore.WHITE
actionColor = Fore.BLUE


# reading the JSON file and getting the configs
def getConfigs():
    global nme, passwrd
    try:
        f = open('configs.json')
        data = json.load(f)
        nme = data['email']
        passwrd = data['password']
        min_mutual_friends_count = data['min_mutual_friends']
        print(successColor + "Read the config file Successfully")

        f.close()
    except:
        print(dangerColor + "Couldnt read the config file")
        exit()

# Run the program function
def run():  

    getConfigs()

    driver = webdriver.Firefox()
    driver.get("https://www.facebook.com/friends")	# go to facebook.com

    login(driver)
    seeAllFriends(driver)

# safety delay so that we don't get caught as a BOT
def safityDelay():
    time.delay(1)

# handle the friend request as we check if the condition is met and if so we send a request
def handleFriendRequest(friend, mutualFriendsCount, index):
    if(int(mutualFriendsCount) >= min_mutual_friends_count):
        try:
            confirms = findElems(friend, By.XPATH,"//span[text()='Confirm']")
            confirms[index].click()
            print(actionColor + "added this friend")
        except:
            print(dangerColor + "Couldnt add this friend")

# find the number of the mutual friends
def findMutualFriends(friend):
    res = findElems(friend, By.CLASS_NAME,"xuxw1ft")
    for elem in res:
        if('mutual friend' in elem.get_attribute("innerHTML")):
            return (elem.get_attribute("innerHTML").split(" "))[0]
    return -1

# deal with each frined in the friend list
def handleFriend(friend, count):
        try:
            name = findElem(friend, By.CLASS_NAME,"xuxw1ft").get_attribute("innerHTML")
            mutualFriendsCount = findMutualFriends(friend)

            if(mutualFriendsCount != -1):
                print(infoColor + str(count) + " " +name +" with " + str(mutualFriendsCount) + " mutual friend(s)")
                handleFriendRequest(friend, mutualFriendsCount, count - 1)
            else:
                print(infoColor + str(count) + " " +name +" with " + str(0) +" mutual friend(s)")
            
        except:
            pass

# get all friends in the suggestion list
def seeAllFriends(driver):
    friendsContainer = findElem(driver, By.CLASS_NAME,"x8gbvx8")
    allFriends = findElems(friendsContainer, By.XPATH, "*")


    count = 1
    for friend in allFriends:
        handleFriend(friend, count)
        count += 1

# the normal find elements but wrapped around try and except block
def findElems(source, by, q):
    try:
        return source.find_elements(by, q)
    except:
        print(dangerColor + "Couldnt find the elements.")
        exit()

# the normal find element but wrapped around try and except block
def findElem(source, by, q):
    try:
        return source.find_element(by, q)
    except:
        print(dangerColor + "Couldnt find the element "+ q)
        exit()

# login function
def login(driver):
    try:
        if driver:
            email = findElem(driver, By.NAME, "email")
            email.send_keys(nme)
            email.send_keys(Keys.TAB)


            password = findElem(driver, By.NAME, "pass")
            password.send_keys(passwrd)	


            loginBtn = findElem(driver, By.NAME, "login")
            loginBtn.click()

            print(successColor + "Logged In Successfully")

        else:
            print(dangerColor + "Driver does not exist")
            
    except:
        print(dangerColor + "Couldnt login")



run()
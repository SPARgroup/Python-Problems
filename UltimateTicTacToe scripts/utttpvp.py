import time
import threading as td
import slixmpp as slix
import logging
import os
import requests as req
import msvcrt as ms
import copy
import webbrowser as web

#functions
def askServer(gid, my_jid):
    url = "http://cycada.ml/game/coordinate/coordinate.php"
    data = {"id":gid, "jid":my_jid}

    returned = req.get(url, data)

    if returned == "NEW_GAME":
        #we are P1
        #wait

        return True
    elif returned == "ROOM_FILLED":
        print("This game already has 2 players in it.")
        return False

    else:
        #if returned[-1] == "x":

        #get game state from server
            #if hamari bari
                #play our move
                #message the returned jid(opponent jid)
            #else
                #message opponent
        return returned



def retrieveFile(_filename):
    print("Contacting server...")
    url = "http://cycada.ml/game/" + _filename + ".txt"
    _data = req.get(url)
    if _data.status_code == 200:
        print("File found!")
        return _data.content.decode('utf-8') #convert to string from binary object
    else:
        print("Wrong ID, try relaunching.")
        time.sleep(2)
        return False

def loadgame(_data, _bd,__big, __moves, _turn, __x, __y):
    print("Reading saved game...")
    arr = _data.split("\n")

    for i in range(9):
        _bd[i] = arr[i].split()

    __big = int(arr[9])
    __moves = int(arr[10])
    _turn = bool(int(arr[11]))

    #for player X
    yex = []
    for i in range(12, 21):
        yex = arr[i].split()
        for j in yex:
            __x.ac[i - 12].append(int(j))

    yex = arr[21].split()

    counter = 0
    for j in yex:
        __x.wins[counter] = bool(int(j))
        counter+=1

    yex = arr[22].split()
    counter = 0
    for j in yex:
        __x.moves[counter] = int(j)
        counter+=1

    #for player Y
    for i in range(23, 32):
        yex = arr[i].split()
        for j in yex:
            __y.ac[i - 23].append(int(j))

    yex = arr[32].split()

    counter = 0
    for j in yex:
        __y.wins[counter] = bool(int(j))
        counter+=1

    yex = arr[33].split()
    counter = 0
    for j in yex:
        __y.moves[counter] = int(j)
        counter+=1

    return __big, _turn, __moves

#classes
class receiver(slix.ClientXMPP):
    def __init__(self, jid, password):
        slix.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        pass

class sender(slix.ClientXMPP):
    def __init__(self, jid, password, recipient, msg):
        super().__init__(jid, password)
        self.recipient = recipient
        self.msg = msg

        self.add_event_handler('session_start', self.start)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.send_message(mto=self.recipient, mbody=self.msg, mtype="chat")

    def sendmsg(self, _msg):
        self.send_message(mto=self.recipient, mbody=_msg, mtype="chat")

class player():
    def __init__(self):
        self.ac = [[], [], [], [], [], [], [], [], []]
        self.wins = [False, False, False, False, False, False, False, False, False]
        self.moves = [0,0,0,0,0,0,0,0,0]

#variables
jid = ''

password = ''

opponent_jid = ''

gameid = ''

board = [['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_'],
         ['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_'],
         ['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_'],
         ['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_'],
         ['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_'],
         ['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_'],
         ['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_'],
         ['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_'],
         ['_', '_', '_',
          '_', '_', '_',
          '_', '_', '_']]
x = player()
y = player()
magic = [6, 7, 2,
         1, 5, 9,
         8, 3, 4]
moves = 1
bigscope = 0
turn = True
handler = []

#Intro
print("Ultimate TicTacToe Online\n        v2.1\n[Requires an internet connection to play a saved game]\nCredits: Samarth Singla | Ashmit Chamoli | Rishabh Sharma | Abhivir Singh")
time.sleep(0.5)

#ask user for account
n_1 = input("Do you have a jabber account?(y/n): ")
n_1 = n_1.lower()

#Input reg. details
if n_1[0] == 'y':
    jid = input("\nEnter your User ID: ")
    password = input("Enter Password: ")

else:
    print("\nYou will have to make an XMPP/Jabber account to play the game...\n")
    print("Opening Registration link in 3 seconds...")
    time.sleep(3)
    web.open("https://www.xmpp.jp/signup")
    jid = input("\nEnter your User ID: ")
    password = input("Enter Password: ")

#initialise game
s = input("\nDo you want to continue a saved game?(y/n): ")

if s[0] == 'y' or s[0] == 'Y':
    gameid = input("Enter game ID: ")
    data = retrieveFile(gameid)
    if data != False:
        # print(data)
        handler = loadgame(data, board, bigscope, moves, turn, x, y)
        bigscope = handler[0]
        turn = handler[1]
        moves = handler[2]
        time.sleep(0.3)
    elif not data:
        print("Something went wrong, maybe your entered ID was wrong.")

else:

    gameid = input("\nEnter game ID to enable game saving: ")







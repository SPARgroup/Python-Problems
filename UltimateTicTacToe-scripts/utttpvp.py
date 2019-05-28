import time
import threading as td
import slixmpp as slix
import logging
import os
import requests as req
import msvcrt as ms
import copy
import webbrowser as web
import functions as func

yes = ['yes', 'y', 'yeah', 'ye', 'yeet', 'yup'] # for checking users response
#classes

#receiver class (xmpp derived)
class receiver(slix.ClientXMPP):
    def __init__(self, jid, password):
        slix.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        #do something
        print(msg) # YEAHHHH ITS WORKING BEZOS!


#sender class (xmpp derived)
class sender(slix.ClientXMPP):
    def __init__(self, jid, password, recipient, msg, msgtype):
        super().__init__(jid, password)
        self.recipient = recipient
        self.msg = msg
        self.msgtype = msgtype

        self.add_event_handler('session_start', self.start)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.send_message(mto=self.recipient, mbody=self.msg, mtype=self.msgtype)

    def sendmsg(self, _msg):
        self.send_message(mto=self.recipient, mbody=_msg, mtype="chat")


#players' class, contains data like their account (moves) wins, etc
class player():
    def __init__(self):
        self.ac = [[], [], [], [], [], [], [], [], []]
        self.wins = [False, False, False, False, False, False, False, False, False]
        self.moves = [0,0,0,0,0,0,0,0,0]


#variables
enemyMoves = []

jid = 'spar@xmpp.jp'

password = 'spargroupgaming'

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

#new instance of players (has to be changed to make it online 1v1
x = player()
y = player()

#magic square (win condition check)
magic = [6, 7, 2,
         1, 5, 9,
         8, 3, 4]

#Opponent has moved or not
receivedMove = False # change it to False only when this player HAS ACTUALLY MOVED (optional)

#total moves
moves = 1

#big grid number
bigscope = 0

#what is the turn?
turn = True

#handler to handle data returned during initializing game
handler = []

#Am I X or O
myturn = None

#oops
game_start = False

receiving = True
recv = receiver(jid, password)
recv.connect()
#Thread functions
def start_receiving(enemy_moves):
    while receiving :
        recv.process(timeout=10)

receivingThread = td.Thread(target=start_receiving, args = (enemyMoves,))
receivingThread.start()
def ask_server(gid):

    url = "http://cycada.ml/game/coordinate/coordinate.php"
    data = {"id":gid, "jid":jid}

    returned = req.get(url, data)

    if returned == "NEW_GAME":
        #we are P1, save the state for once
        myturn = True # I am player 1
        save(board, x, y, moves, gameid, bigscope, turn)
        return returned
    elif returned == "ROOM_FILLED":
        print("This game already has 2 players in it.")
        return False

    else:
        dat = returned.split("\n")
        if dat[1] == "SEND_INFO":
            #Send player 1 my Jid (I am player 2)
            my_turn = False
            send = sender(jid, password, dat[0],"normal")
            send.connect()
            print("\nContacting Player...")
            send.process(timeout=5)
            return(dat[0])
        else:
            if dat[1] == "P1":
                myturn = True
            elif dat[1] == "P2":
                myturn = False
            return dat[0]


def returnBitForBool(e):
    if e:
        return "1"
    else:
        return "0"


def stringify(l):
    string = " ".join(str(x) for x in l)
    return string


def prepdata(bd, _x, _y, _moves, f, _big, __turn):
    _a=""
    for i in bd:
        _a += stringify(i) + "\n"

    _a += str(_big) + "\n" + str(_moves) + "\n" + returnBitForBool(__turn) + "\n"

    for i in _x.ac:
        _a += stringify(i) + "\n"

    #Wins array for both players is a boolean array
    yex = []

    for i in _x.wins:
        yex.append(returnBitForBool(i))

    _a += stringify(yex) + "\n"
    _a += stringify(_x.moves) + "\n"

    for i in _y.ac:
        _a += stringify(i) + "\n"

    yay = []

    for i in _y.wins:
        yay.append(returnBitForBool(i))

    _a += stringify(yay) + "\n"
    _a += stringify(_y.moves) + "\n"

    f.write(_a)
    return _a
    f.close()


def loadgame(_data):
    print("Reading saved game...")
    arr = _data.split("\n")

    for i in range(9):
        board[i] = arr[i].split()

    bigscope = int(arr[9])
    moves = int(arr[10])
    turn = bool(int(arr[11]))

    #for player X
    yex = []
    for i in range(12, 21):
        yex = arr[i].split()
        for j in yex:
            x.ac[i - 12].append(int(j))

    yex = arr[21].split()

    counter = 0
    for j in yex:
        x.wins[counter] = bool(int(j))
        counter+=1

    yex = arr[22].split()
    counter = 0
    for j in yex:
        x.moves[counter] = int(j)
        counter+=1

    #for player Y
    for i in range(23, 32):
        yex = arr[i].split()
        for j in yex:
            y.ac[i - 23].append(int(j))

    yex = arr[32].split()

    counter = 0
    for j in yex:
        y.wins[counter] = bool(int(j))
        counter+=1

    yex = arr[33].split()
    counter = 0
    for j in yex:
        y.moves[counter] = int(j)
        counter+=1

    return bigscope, turn, moves


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


def save(board, x, y, moves, _id, bigy, turn):
    filey = open("tasty.txt", "w")
    returnedData = prepdata(board, x, y, moves, filey, bigy, turn)
    url = "http://cycada.ml/game/savegame.php"
    data = {'id' : id,'data' : returnedData}
    status = req.post(url, data)
    if not status:
        print("Something went wrong, our server returned the code: ", status.status_code)


def win(checklist):
    counter = 0
    for i in checklist:
        if i == True:
            counter += 1

    return counter


def display_row(currState, jay, kay):
    print(currState[(3 * jay)], end=" | ")
    print(currState[(3 * jay) + 1], end=" | ")
    print(currState[(3 * jay) + 2], end="")
    if kay != 2:
        print("   I   ", end="") #mid divider


def ultrashow(currState):
    os.system("cls")
    for i in range(3):
        for j in range(3):
            for k in range(3):
                display_row(currState[(3 * i) + k], j, k)

            print("\n")
        if (i != 2):
            for a in range(44):
                print("_", end="")
        print("\n")


def process(s):
    if s == "w":
        return -3
    elif s == "a":
        return -1
    elif s == "d":
        return 1
    elif s == "s":  # s is "s"
        return 3
    else:
        return False


def check(z):
    x = len(z)
    for i in range(0, x - 2):
        for j in range(i + 1, x - 1):
            for k in range(j + 1, x):
                if z[i] + z[j] + z[k] == 15:
                    return True

    return False


def isfilled(l):
    for i in l:
        if i == '_':
            return False

    return True

#Intro
intro = "Ultimate TicTacToe Online\n        v2.1"
func.animatedPrint(intro, 15, 20)
time.sleep(0.5)
print("\n[Requires an internet connection to play a saved game]")
time.sleep(0.2)
credits = "\nCredits: Samarth Singla | Ashmit Chamoli | Rishabh Sharma | Abhivir Singh\n"
func.animatedPrint(credits, 40, 5)
time.sleep(0.5)

#ask user for account
n_1 = func.custom_input("\nDo you have a Jabber/XMPP account? (y/n): ", rate = 10)
n_1 = n_1.lower()

#Input reg. details
if n_1 in yes:
    jid = input("\nEnter your User ID: ")
    password = input("Enter Password: ")

else:
    print("\nYou will have to make an XMPP/Jabber account to play the game...\n")
    print("Opening Registration link in 3 seconds...")
    time.sleep(3)
    web.open("https://www.xmpp.jp/signup")
    jid = func.custom_input("\nEnter your User ID: ")
    password = input("Enter Password: ")

#initialise game
s = input("\nDo you want to continue a saved game?(y/n): ")
s = s.lower()
if s in yes:
    gameid = input("Enter game ID: ")
    data = retrieveFile(gameid)
    if data != False:
        # print(data)
        loadgame(data)
        time.sleep(0.3)
    elif not data:
        print("Something went wrong, maybe your entered ID was wrong.")

else:
    gameid = input("\nEnter game ID to enable game saving: ")


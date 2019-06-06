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


yes = ['yes', 'y', 'yeah', 'ye', 'yeet', 'yup', 'haan', 'bilkul', 'hanji'] # for checking users response
#classes

#Communicator class (xmpp derived)
class communicator(slix.ClientXMPP):

    def __init__(self, jid, password):
        slix.ClientXMPP.__init__(self, jid, password)


        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        #do something
        global receivedMove
        global buffer
        global opponent_jid
        global enemyMoves

        if msg['type'] == 'normal':
            update_game(int(msg['body'].decode('utf-8')))
            enemyMoves.append(msg['body'])


        elif msg['type'] == 'chat':
            #print("\nOpponent says:", msg['body'])
            if msg['body'] == "GAME_START":
                opponent_jid = str(msg['from']).split("/")[0]
                print(msg)
                print(opponent_jid)
                print(f"{opponent_jid} has accepted the challenge. Let the battle begin!")
            buffer.append(msg)


    def sendMessage(self, opponent, msg, mtype):
        self.send_message(mto=opponent, mbody=msg, mtype=mtype)

#players' class, contains data like their account (moves) wins, etc
class player:
    def __init__(self):
        self.ac = [[], [], [], [], [], [], [], [], []]
        self.wins = [False, False, False, False, False, False, False, False, False]
        self.moves = [0,0,0,0,0,0,0,0,0]


#variables

buffer = []


enemyMoves = []

jid = ''

password = ''

opponent_jid = None

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

information = ""
#new instance of players
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

#smalll scope
smallscope = 4

#what is the turn?
turn = True # or None maybe?

#handler to handle data returned during initializing game
handler = []

#Am I X or am I O?
myturn = None

#Shall we?
game_start = False

printed = False

receiving = True

movement = copy.deepcopy(board)

#communicator and it's thread object
#will be set later through the initialize function
comm = None

receivingThread = None

#Thread functions

def debug(err):
    print(f"\n KAALA HIT: {err}")


def start_receiving():
    global enemyMoves
    while receiving :
        comm.process(timeout=1)


def save():
    """Saves the game to server"""
    global gameid
    gameState = prepdata()
    url = "http://cycada.ml/game/savegame.php"
    params = {'id' : gameid,'data' : gameState}
    status = req.post(url, params)
    if status.status_code != 200:
        print("Something went wrong, our server returned the code: ", status.status_code)


def returnBitForBool(e):
    if e:
        return "1"
    else:
        return "0"


def stringify(l):
    string = " ".join(str(x) for x in l)
    return string


def prepdata():
    """Prepares game states into a string for server upload"""
    _a=""
    global board
    global x
    global y
    global moves
    global bigscope
    global turn
    global gameid

    f = open(gameid, 'w')
    for i in board:
        _a += stringify(i) + "\n"

    _a += str(bigscope) + "\n" + str(moves) + "\n" + returnBitForBool(turn) + "\n"

    for i in x.ac:
        _a += stringify(i) + "\n"

    #Wins array for both players is a boolean array
    yex = []

    for i in x.wins:
        yex.append(returnBitForBool(i))

    _a += stringify(yex) + "\n"
    _a += stringify(x.moves) + "\n"

    for i in y.ac:
        _a += stringify(i) + "\n"

    yay = []

    for i in y.wins:
        yay.append(returnBitForBool(i))

    _a += stringify(yay) + "\n"
    _a += stringify(y.moves) + "\n"

    f.write(_a)
    f.close()
    return _a


def loadgame(_data):
    print("Reading saved game...")
    arr = _data.split("\n")
    global bigscope
    global moves
    global turn

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
    """Retrieve file with given game ID"""
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


def win(checklist):
    counter = 0
    for i in checklist:
        if i:
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


def process(moveChar):
    if moveChar == "w":
        return -3
    elif moveChar == "a":
        return -1
    elif moveChar == "d":
        return 1
    elif moveChar == "s":  # s is "s"
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


def ask_server(gid):
    global myturn
    global opponent_jid
    global jid
    url = "http://cycada.ml/game/rooms/coordinate.php"
    data = {"id":gid, "jid":jid}
    returned = req.get(url, data)

    if returned.status_code != 200 :
        func.animatedPrint("There was a problem in our server, please try again later.")
    returned = returned.content.decode('utf-8')

    if returned == "NEW_GAME":
        #we are P1, save the state for once
        myturn = True # I am player 1
        save()
        return returned

    elif returned == "ROOM_FILLED":
        print("This game already has 2 players in it.")
        return False

    else:
        dat = returned.split("#")

        if dat[1] == "SEND_INFO":
            #Send player 1 my Jid (I am player 2)
            myturn = False
            opponent_jid = dat[0]
            print('Have to send message to opponent')
            comm.sendMessage(opponent_jid, "GAME_START", "chat")
            return dat[0]

        else: #the case that the player is revisiting the game after saving it
            if dat[1] == "P1":
                opponent_jid = dat[0]
                myturn = True
            elif dat[1] == "P2":
                opponent_jid = dat[0]
                myturn = False
            return dat[0]


def processResponse(resp):
    #processing the response created by the server
    #includes waiting for player 2 to join game
    global opponent_jid
    global game_start

    if resp == "NEW_GAME" or opponent_jid is None:
        #We can't do anything so wait
        while not receivedMove:
            time.sleep(0.1)
            pass
    elif not resp:
        func.animatedPrint("Sorry, this room is already full, create a new game to play with a friend")
    else:
        #Not a new game, we have got the opponent jid
        opponent_jid = resp
        game_start = True


def start_new_game(gid):
    """Puts empty game file on the server, being player 1 himself."""
    #put empty file on server
    url = 'http://cycada.ml/game/savegame.php'
    empty_state = prepdata()
    dat = {'id':gid, 'data':empty_state}

    response = req.post(url, dat)

    if response.status_code == 200:
        #everything went fine
        pass

    else:
        print("There was a problem with the server, Sorry.")
        exit()


def initialize():
    global comm
    global receivingThread

    comm = communicator(jid, password)
    comm.connect()

    receivingThread = td.Thread(target=start_receiving)
    receivingThread.daemon = True
    receivingThread.start()


def update_game(move):
    """Move is the enemy move received (The small scope, as we already know the bigscope).
    This function updates all the structures of the game according to the move of the
    enemy player"""

    global board
    global x
    global y
    global myturn
    global receivedMove
    global bigscope
    global magic
    global opponent_jid
    global moves

    opponent_turn = not myturn

    if opponent_turn:
        insertVal = "X"
        opponentAcc = x

    else:
        insertVal = "O"
        opponentAcc = y

    board[bigscope][move] = insertVal
    opponentAcc.ac[bigscope].append(magic[move])
    opponentAcc.moves[bigscope] += 1
    moves += 1
    if check(opponentAcc.ac[bigscope]):
        #Opponent has won a block
        opponentAcc.wins[bigscope] = True
        print(f"\nYour opponent {opponent_jid} won the block {bigscope}. Time to show your metal!")

    bigscope = move #set up for local player's move

    receivedMove = True


def send_move():
    pass


def playGame():
    #Globalisation
    global printed
    global buffer
    global enemyMoves
    global jid
    global password
    global opponent_jid
    global gameid
    global board
    global x
    global y
    global magic
    global receivedMove
    global moves
    global bigscope
    global smallscope
    global turn
    global handler
    global myturn
    global receiving
    global movement
    global comm
    global information
    myAccount = None
    insertVal = None

    if myturn:
        insertVal = "X"
        myAccount = x
    elif not myturn:
        insertVal = "O"
        myAccount = y
    else:
        print("KAALA HIT: myturn not set yet.")

    while moves < 81:
        if not printed:
            information = "X : " + str(win(x.wins)) + " O : " + str(win(y.wins)) + "\n"
            information += "X:{} O:{}\n".format(win(x.wins), win(y.wins))
            if turn == myturn:
                information += "Your turn, you are playing in the {} grid.\n\n".format(bigscope + 1)
                information += "Navigate using WASD keys (your pointer starts at the center) :"

            else:
                information += "It's {}'s turn. \n\n".format(opponent_jid.split("@")[0])

            information += "Press 'Q' at any time to save the game.\n\n"

        if turn == myturn:
            printed = False
            smallscope = 4
            movement = copy.deepcopy(board)
            movement[bigscope][smallscope] = '#'
            ultrashow(movement)
            print(information)

            pressedEnter = False
            while not pressedEnter:
                if ms.kbhit():
                    press = ms.getch().decode("utf-8")
                    if press == "\r":
                        pressedEnter = True
                        break
                    elif process(press):
                        movement = copy.deepcopy(board)
                        smallscope = (smallscope + process(press)) % 9

                        movement[bigscope][smallscope] = "#"

                        ultrashow(movement)

                        print(information)
                        #movement = copy.deepcopy(board)
                        time.sleep(0.03)
                    elif press == "q" or press == "Q":
                        save()
                        os.system("cls")
                        print("Saving...")
                        time.sleep(2)
                        exit()

            if board[bigscope][smallscope] != '_':
                print("Wait, ", end="")
                time.sleep(0.5)
                print("That's illegal.")
                moves -= 1
                time.sleep(0.5)

            else:
                board[bigscope][smallscope] = insertVal
                myAccount.ac[bigscope].append(magic[smallscope])
                myAccount.moves[bigscope] += 1
                moves += 1
                if check(myAccount.ac[bigscope]):
                    # Opponent has won a block
                    myAccount.wins[bigscope] = True
                    print(f"\nYou have won the {bigscope} block!")

                comm.sendMessage(opponent_jid, smallscope, "normal")
                turn = not turn


                #do shits
        elif turn != myturn:
            if not printed:
                print(information)
                printed = True



#Do all the init stuff here. Already contains thread launching and stuff.


#Intro
func.play_intro()

#ask user for account
n_1 = func.custom_input("\nDo you have a Jabber/XMPP account? (y/n): ", rate = 20)
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
initialize()
#initialise game
s = func.custom_input("\nDo you want to continue a saved game?(y/n): ")
s = s.lower()
if s in yes:
    gameid = input("Enter game ID: ")
    recvd = ask_server(gameid)
    processResponse(recvd)

    data = retrieveFile(gameid)
    if data:
        loadgame(data)
        time.sleep(0.3)
    elif not data:
        print("Something went wrong, maybe your entered ID was wrong.")

else:
    gameid = input("\nEnter game ID to enable game saving: ")
    #@todo: steps to create new game and stuff
    recvd = ask_server(gameid)
    start_new_game(gameid)
    print(f"\nNew game created! Waiting for opponent to join...")
    processResponse(recvd)


while True:
    if game_start:
        playGame()


input()
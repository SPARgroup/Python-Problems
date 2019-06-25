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
import pygame as pg, pygame

def updater():
    global clock
    global disp
    global takingInput
    global events

    # disp.fill((228, 106, 107))
    # pygame.display.update()

    while True:
        pass

w = 200
h = 200

events = []
# disp = pygame.display.set_mode((w, h))
# takingInput = False
# pygame.display.set_caption("Input Window")
# clock = pygame.time.Clock()
# displayupdater = td.Thread(target=updater, args=())
# displayupdater.daemon = True
# #displayupdater.start()



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
        global challengeAccepted
        global game_start
        global board
        global x
        global y
        global myturn
        global receivedMove
        global bigscope
        global magic
        global opponent_jid
        global moves
        global turn

        #I WAS DOING WHAT WAS NECESSARY
        if msg['type'] == 'normal':
            debug(msg)
            challengeAccepted = True
            print("Entering function")

            move = int(msg['body'])
            print(move)
            ##UPDATE GAME START
            debug("Hello, this is update_game function here.")
            opponent_turn=not myturn

            print("Previous Turn: ",turn)

            if opponent_turn:
                insertVal="X"
                opponentAcc=x

            else:
                insertVal="O"
                opponentAcc=y

            board[bigscope][move]=insertVal
            opponentAcc.ac[bigscope].append(magic[move])
            opponentAcc.moves[bigscope]+=1
            moves+=1
            if check(opponentAcc.ac[bigscope]):
                # Opponent has won a block
                opponentAcc.wins[bigscope]=True
                print(f"\nYour opponent {opponent_jid} won the block {bigscope}. Time to show your metal!")

            bigscope=move  # set up for local player's move

            turn = not turn

            print("Current Turn: ",turn)

            receivedMove = True

            ##UPDATE GAME END

            enemyMoves.append(msg['body'])
            buffer.append(msg)

        elif msg['type'] == 'chat':
            if msg['body'] == "GAME_START":
                challengeAccepted = True
                opponent_jid = str(msg['from']).split("/")[0]
                print(msg)
                print(opponent_jid)
                print(f"{opponent_jid} has accepted the challenge. Let the battle begin!")
                game_start = True
            buffer.append(msg)


    def sendMessage(self, opponent, msg, mtype):
        self.send_message(mto=opponent, mbody=str(msg), mtype=mtype)



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

challengeAccepted = False

receiving = True

movement = copy.deepcopy(board)

running = True
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
    debug(returned.content)

    if returned.status_code != 200 :
        func.animatedPrint("There was a problem in our server, please try again later.")
    returned = returned.content.decode('utf-8')

    if returned == "NEW_GAME":
        #we are P1, save the state for once
        myturn = True #I am player 1
        save()
        return returned

    elif returned == "ROOM_FILLED":
        print("This game already has 2 players in it.")
        return False

    else:
        dat = returned.split("#")
        #Boom
        if dat[1] == "P1":
            myturn = True

        elif dat[1] == "P2":
            myturn = False

        opponent_jid = dat[0]

        comm.sendMessage(opponent_jid, "GAME_START", "chat")

        return None


def processResponse(resp):
    #processing the response created by the server
    #includes waiting for player 2 to join game
    global opponent_jid
    global game_start


    if resp == "NEW_GAME":
        func.animatedPrint("Waiting for opponent to join", 45, 5)

        while not challengeAccepted:
            time.sleep(1)
        game_start = True
        return
    elif resp == "ROOM_FULL":
        func.animatedPrint("This room is already full.", 45, 5)
        time.sleep(3)
        exit()
    elif resp is None:
        game_start = True
        pass


def start_new_game(gid):
    """Puts empty game file on the server, being player 1 himself."""
    #put empty file on server
    url = 'http://cycada.ml/game/savegame.php'
    empty_state = prepdata()
    debug(empty_state)
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
    global turn

    print("Hello, this is update_game function here.")
    opponent_turn = not myturn

    print("Current Turn: ", turn)

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
    turn = not turn
    receivedMove = True


def send_move():
    pass


def keypress(press):
    global movement, information
    global smallscope, bigscope

    movement=copy.deepcopy(board)
    smallscope=(smallscope + process(press)) % 9

    movement[bigscope][smallscope]="#"

    ultrashow(movement)

    print(information)
    time.sleep(0.03)


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
    global events

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
        receivedMove = False

        if not printed:
            information = "X : " + str(win(x.wins)) + " O : " + str(win(y.wins)) + "\n"
            if turn == myturn:
                information += "Your turn, you are playing in the {} grid.\n\n".format(bigscope + 1)
                information += "Press 'Q' at any time to save the game.\n\n"
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

            # #PYGAME
            # takingInput = True
            # while not pressedEnter:
            #     for event in events:
            #         disp.fill((228, 106, 107))
            #         pygame.display.update()
            #         if event.type == pygame.KEYDOWN:
            #             if pygame.key.get_pressed()[pygame.K_RETURN]:
            #                 pressedEnter = True
            #                 break
            #
            #             if pygame.key.get_pressed()[pygame.K_w] or pygame.key.get_pressed()[pygame.K_UP]:
            #                 keypress("w")
            #             elif pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:
            #                 keypress("a")
            #             elif pygame.key.get_pressed()[pygame.K_s] or pygame.key.get_pressed()[pygame.K_DOWN]:
            #                 keypress("s")
            #             elif pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
            #                 keypress("d")
            #             elif pygame.key.get_pressed()[pygame.K_q]:
            #                 save()
            #                 os.system("cls")
            #                 print("Saving...")
            #                 time.sleep(2)
            #                 exit()
            #         elif event.type == pygame.QUIT:
            #             save()
            #             os.system("cls")
            #             print("Saving...")
            #             time.sleep(2)
            #             exit()
            # takingInput = False
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

                bigscope = smallscope
                comm.sendMessage(opponent_jid, str(smallscope), "normal")
                turn = not turn


                #do shits
        elif turn != myturn:

            if not printed:
                ultrashow(board)
                print(information)
                printed = True

            while not receivedMove:
                time.sleep(0.2)
                pass


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

if s in yes or s[0] == "y":
    gameid = input("Enter game ID: ")
    recvd = ask_server(gameid)
    debug(recvd)
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
    debug(recvd)
    start_new_game(gameid)
    print(f"\nNew game created!")
    processResponse(recvd)


while running:
    if game_start:
        playGame()


input()
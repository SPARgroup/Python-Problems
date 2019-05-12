import time
import os
import requests as req


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

    f.close()

def loadgame(_data, _bd, __big, __moves, _turn, __x, __y):
    arr = _data.split("\n")

    for i in range(9):
        _bd[i] = arr[i].split()

    __big = int(arr[9])
#    __moves = int(arr[10])
    _turn = bool(arr[11])

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
    return __big
def retrieveFile(_filename):
    url = "http://cycada.ml/game/" + _filename + ".txt"
    _data = req.get(url)
    if(_data.status_code != 404):
        return _data.content.decode('utf-8') #convert to string from binary object
    else:
        return False


def save(board, x, y, moves, _id, bigy, turn):
    filey = open("tasty.txt","w")
    prepdata(board, x, y, moves, filey, bigy, turn )
    #r = req.post('http://cycada.ml/game/', files={file})

class player():
    def __init__(self):
        self.ac = [[], [], [], [], [], [], [], [], []]
        self.wins = [False, False, False, False, False, False, False, False, False]
        self.moves = [0,0,0,0,0,0,0,0,0]

x = player()
y = player()


#START OF MAIN LOGIC
magic = [6, 7, 2,
         1, 5, 9,
         8, 3, 4]

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
        print("   I   ", end="")

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


moves = 1
bigscope = 0
turn = True


s = input("Do you want to continue saved game?(y/n): ")
if(s == 'y' or s == 'Y'):
    id = input("Enter game ID: ")
    data = retrieveFile(id)
    if data != False:
        # print(data)
        bigscope = loadgame(data, board, bigscope, moves, turn, x, y)
        print(bigscope, "SUPER SAIYYAN \n")
        time.sleep(4)

try:
    while moves <= 81:
        smallscope = 4

        ultrashow(board)

        insertVal = ""

        if turn:
            insertVal="X"
        else:
            insertVal="O"

        print("X :", win(x.wins), "O :", win(y.wins))
        print("\nIt is player",insertVal+"'s turn. You will play in the",bigscope+1,"grid.")
        print("\nNavigate using WASD keys (your pointer starts at the center) :")
        print("\nPress 'Q' to save game and exit.", bigscope, x.ac)
        inp = input()
        if inp == 'q' or inp == 'Q':
            save(board, x, y, moves, id, bigscope, turn)
            os.system("cls")
            print("Saving...")
            time.sleep(2)
            exit()


        for i in inp:
            move = process(i)
            if move == False:
                print("Hold up!")
                time.sleep(0.5)
                smallscope = -1
                break
            else:
                smallscope = (smallscope + move) % 9

          #@todo: check if destination bigscope is already filled
          #@todo: a variable to track how many total wins are there

        if smallscope < 0 or board[bigscope][smallscope] != '_':
            print("Wait.")
            time.sleep(0.5)
            print("That's illegal.")
            moves -= 1
            time.sleep(0.5)
        else:
            board[bigscope][smallscope] = insertVal
            if turn:
                turn = False
                x.moves[bigscope] += 1

                x.ac[bigscope].append(magic[smallscope])

                if x.moves[bigscope] >= 3:

                    if check(x.ac[bigscope]) and y.wins[bigscope] == False:
                        x.wins[bigscope] = True

                if isfilled(board[smallscope]):

                    if (isfilled(board[bigscope])):
                        for checkcounter in range(9):
                            if not(isfilled(board[checkcounter])):
                                bigscope = checkcounter
                                break
                    else:
                        print("They have no space for you in the",smallscope+1,"grid. So you might as well be here itself.")
                        time.sleep(3)
                else:

                    bigscope = smallscope

            else:
                turn = True
                y.moves[bigscope] += 1
                y.ac[bigscope].append(magic[smallscope])

                if y.moves[bigscope] >= 3:

                    if check(y.ac[bigscope]) and x.wins[bigscope] == False:
                        y.wins[bigscope] = True


                if isfilled(board[smallscope]):
                    if (isfilled(board[bigscope])):
                        for checkcounter in range(9):
                            if not (isfilled(board[checkcounter])):
                                bigscope = checkcounter
                                break
                    else:
                        print("They have no space for you in the", smallscope + 1,
                              "grid. So you might as well be here itself.")
                        time.sleep(3)
                else:

                    bigscope = smallscope

        moves += 1



finally:
    print("BYE-BYE")
input()
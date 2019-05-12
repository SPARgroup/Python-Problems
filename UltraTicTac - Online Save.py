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

def stringify(l):
   string = " ".join(str(x) for x in l)
   return string

def prepdata(bd, _x, _y, _moves, f):

    _a=""
    for i in bd:
        _a += stringify(i) + "\n"

    f.write(_a)
    f.close()

def loadgame(_data, _bd):
    arr = _data.split("\n")
    for i in range(9):
        _bd[i] = arr[i].split()


def retrieveFile(_filename):
    params = {'id':_filename}
    url = "http://cycada.ml/game/" + id + ".txt"
    _data = req.get(url, params)
    if(_data.status_code != 404):
        return _data.content.decode('utf-8') #convert to string from binary object
    else:
        return False


def save(board, x, y, moves, file):
    prepdata(board, x, y, moves, file)

class player():
    def __init__(self):
        self.ac = [[], [], [], [], [], [], [], [], []]
        self.wins = [False, False, False, False, False, False, False, False, False]
        self.moves = [0,0,0,0,0,0,0,0,0]

x = player()
y = player()
s = input("Do you want to continue saved game?(y/n): ")

#START OF MAIN LOGIC
if(s == 'y' or s == 'Y'):
    id = input("Enter game ID: ")
    data = retrieveFile(id)
    if data != False:
        # print(data)
        loadgame(data, board)


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

try:
    while moves <= 81:
        smallscope = 4

        ultrashow(board)

        insertVal = ""

        if turn:
            insertVal="X"
        else:
            insertVal="O"

        print("X :", win(x.wins), "Y :", win(y.wins))
        print("\nIt is player",insertVal+"'s turn. You will play in the",bigscope+1,"grid.")
        print("\nNavigate using WASD keys (your pointer starts at the center) :")

        inp = input()

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
        file = open("test.txt","w")
        save(board, x, y, moves, file)
        file.close()

finally:
    file = open("test.txt","w")
    prepdata(board, x, y, moves, file)
    file.close()
input()
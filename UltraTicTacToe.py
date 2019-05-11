import time
import os

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

magic = [6, 7, 2,
         1, 5, 9,
         8, 3, 4]



class player():
    def __init__(self):
        self.ac = [[], [], [], [], [], [], [], [], []]
        self.wins = [False, False, False, False, False, False, False, False, False]
        self.moves = [0,0,0,0,0,0,0,0,0]


x = player()
y = player()


def win(checkList):
    counter = 0
    for i in checkList:
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
    else:
        return True

#@todo: find Python API to use network to store game states at a network location (probably on our site: https://cycada.ml)

moves = 1

bigscope = 0
turn = True

while moves <= 81:
    smallscope = 4

    ultrashow(board)

    insertVal = ""

    if turn:
        insertVal="X"
    else:
        insertVal="O"

    if(win(x.wins) > 0 or win(y.wins) > 0):
        print("X :",win(x.wins),"Y :",win(y.wins))
    else:
        print("Nobody has won any grid to their name yet.")
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
      #@todo: a variable to track how many total wins are there (kinda done)

    if smallscope < 0 or board[bigscope][smallscope] != '_':
        print("Wait.")
        time.sleep(0.5)
        print("That's illegal.")
        moves =- 1
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
                else:
                    continue

            if isfilled(board[smallscope]):

                print("They have no space for you in the",smallscope+1,"grid. So might as well be here itself.")
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
                else:
                    continue

            if isfilled(board[smallscope]):

                print("They have no space for you in the",smallscope+1,"grid. So might as well be here itself.")
                time.sleep(3)

            else:
                bigscope = smallscope

    moves += 1

print("Bro you literally finished the whole game in one go (We haven't made the save game function). Do you life'nt?")
input()
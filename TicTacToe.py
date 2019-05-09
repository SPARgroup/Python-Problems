import os
import msvcrt as ms
import time

# A simple TicTacToe game
def display(currState):
    os.system("cls")
    for i in range(3):
        for j in range(3):
            print(currState[(i * 3) + j], end="")
            if (j + 1) % 3 != 0:
                print(" | ", end="")

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


board = ['_', '_', '_', '_', '_', '_', '_', '_', '_']
#config = ['_', '_', '_', '_', '_', '_', '_', '_', '_']

magic = [6, 7, 2,
         1, 5, 9,
         8, 3, 4]

X = []
Y = []

turn = True
won = False

moves = 1

while moves <= 9 and not won:

    counter = 0  #the starting point is the top-left. Change to 5 to start at center.

    display(board)

    insertVal = ""

    if turn:
        print("Player X")
        insertVal = "X"
    else:
        print("Player O")
        insertVal = "O"

    print("Play Your Move using WASD keys: ")

    x = input()

    for j in x:  #processing keypresses
        move = process(j)
        if move == False:
            print("Hold up!")
            time.sleep(0.5)
            counter = -1
            break
        counter = (counter + move) % 9

    if board[counter] != "_" or counter < 0:
        print("Wait.")
        moves -= 1
        time.sleep(0.5)
        print("That's illegal!")
        time.sleep(1)
    else:
        board[counter] = insertVal
        if turn:
            turn = False
            X.append(magic[counter])
            if moves >= 5:
                if check(X):
                    display(board)
                    print("Outstanding move!")
                    won = True
                    time.sleep(0.4)
                    print("Player X Wins.")
                else:
                    continue

        else:
            turn = True
            Y.append(magic[counter])
            if moves > 5:
                if check(Y):
                    display(board)
                    print("Outstanding move!")
                    won = True
                    time.sleep(0.4)
                    print("Player O Wins.")
                else:
                    continue
    moves += 1
    if moves == 10:
        break

if not won:
  print("Nobody won and its a shame.\n")
inp = ""
while(not(inp == "F" or inp == "f")):
  inp = input("\nPress F and Enter to pay respects. ")

print("Endgame Now")
time.sleep(1)
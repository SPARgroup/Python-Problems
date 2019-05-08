import os
import msvcrt as ms
import time


def display(currState):
    os.system("cls")
    for i in range(3):
        for j in range(3):
            print(currState[(i * 3) + j], end="")
            if (j+1) % 3 != 0:
                print(" | ", end="")

        print("\n")


def process(s):
    if s == "w":
        return -3
    elif s == "a":
        return -1
    elif s == "d":
        return 1
    else:  # s is "s"
        return 3


board = ['_', '_', '_', '_', '_', '_', '_', '_', '_']
config = ['_', '_', '_', '_', '_', '_', '_', '_', '_']

magic = [6, 7, 2, 1, 5, 9, 8, 3, 4]

X = []
Y = []
turn = True
moves = 0
while moves < 9:
    moves += 1
    counter = 0
    display(board)
    insertVal = ""
    if turn:
        print("Player X")
        insertVal = "X"
    else:
        print("Player O")
        insertVal = "O"


    print("Play Your Move using WASD keys: ")
    x = input()  #string for input processing

    for j in x:
        move = process(j)
        counter = (counter + move) % 9


    if board[counter] != "_":
        print("Invalid Move")
        moves -= 1
        time.sleep(1)
    else:
        board[counter] = insertVal
        if turn:
            X.append(magic[counter])
        else:
            Y.append(magic[counter])

        turn = not turn


input()

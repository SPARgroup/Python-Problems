import os
import msvcrt as ms


def display(board):
    os.system("cls")
    for i in range(3):
        for j in range(3):
            print(board[(i * 3) + j], end="")
            if ((j + 1) % 3 != 0):
                print(" ", end="")

        print("\n")


def process(s):
    if s == "w":
        return -3
    elif s == "a":
        return -1
    elif s == "d":
        return 1
    else:
        return 3


board = ['_', '_', '_', '_', '_', '_', '_', '_', '_']

magic = [6, 7, 2, 1, 5, 9, 8, 3, 4]

X = []
Y = []
turn = True
for i in range(9):
    counter = 0
    display(board)
    if (turn):
        print("Player X")
    else:
        print("Player O")

    valid = False

    x = input()
    for i in x:
        move = process(i)
        counter = (counter + move) % 9

    board.insert(counter, " ")

    turn = not (turn)

input()

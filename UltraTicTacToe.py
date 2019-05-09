import time
import os
board = [['_','_','_',
          '_','_','_',
          '_','_','_'],
         ['_','_','_',
          '_','_','_',
          '_','_','_'],
         ['_','_','_',
          '_','_','_',
          '_','_','_'],
         ['_','_','_',
          '_','_','_',
          '_','_','_'],
         ['_','_','_',
          '_','_','_',
          '_','_','_'],
         ['_','_','_',
          '_','_','_',
          '_','_','_'],
         ['_','_','_',
          '_','_','_',
          '_','_','_'],
         ['_','_','_',
          '_','_','_',
          '_','_','_'],
         ['_','_','_',
          '_','_','_',
          '_','_','_']]


def display_row(currState, jay, kay):
    print(currState[(3*jay)], end=" | ")
    print(currState[(3*jay) + 1], end=" | ")
    print(currState[(3*jay) + 2], end="")
    if kay != 2:
        print("   |   ", end = "")


def ultrashow(currState):
    os.system("cls")
    for i in range(3):
        for j in range(3):
            for k in range (3):
                display_row(currState[(3*i) + k],j,k)

            print("\n")
        if(i != 2):
            for a in range(44):
                print("_", end="")
        print("\n")

ultrashow(board)
input()
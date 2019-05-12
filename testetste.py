import os
def stringify(l):
   string = " ".join(str(x) for x in l)
   return string
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



def prepdata(bd,f):

    #prep board
    _a=""
    for i in bd:
        _a += stringify(i) + "\n"

    f.write(_a)


def loadgame(_name, _bd):
    file = open(_name, "r")
    arr = file.read().split("\n")
    # print(arr)
    for i in range(9):
        _bd[i] = arr[i].split()
    file.close()
    
#file = open("test.txt","w")
#prepdata(board, file)
loadgame("test.txt", board)
ultrashow(board)

input()
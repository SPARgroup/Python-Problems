import time
import threading as td
import slixmpp as slix
import logging
import os
import requests as req
import msvcrt as ms
import copy
import webbrowser as web
import functions

enemyMoves = []

jid = 'spar@xmpp.jp'

password = 'spargroupgaming'

opponent_jid = ''

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

#new instance of players (has to be changed to make it online 1v1)
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

#what is the turn?
turn = True

#handler to handle data returned during initializing game
handler = []

#Am I X or O
myturn = None

#oops
game_start = False

receiving = True


def returnBitForBool(e):
    if e:
        return "1"
    else:
        return "0"

def stringify(l):
    string = " ".join(str(x) for x in l)
    return string


def save(board, x, y, moves, _id, bigy, turn):
    filey = open("tasty.txt", "w")
    returnedData = prepdata(board, x, y, moves, filey, bigy, turn)
    url = "http://cycada.ml/game/savegame.php"
    data = {'id' : id,'data' : returnedData}
    status = req.post(url, data)
    if not status:
        print("Something went wrong, our server returned the code: ", status.status_code)

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
    return _a
    f.close()

jid = input("Enter Jid: ")
def ask_server(gid):

    url = "http://cycada.ml/game/coordinate/coordinate.php"
    data = {"id":gid, "jid":jid}

    returned = req.get(url, data)

    if returned == "NEW_GAME":
        #we are P1, save the state for once
        myturn = True # I am player 1
        save(board, x, y, moves, gameid, bigscope, turn)
        return returned
    elif returned == "ROOM_FILLED":
        print("This game already has 2 players in it.")
        return False

    else:
        dat = returned.split("\n")
        if dat[1] == "SEND_INFO":
            #Send player 1 my Jid (I am player 2)
            my_turn = False
            send = sender(jid, password, dat[0],"normal")
            send.connect()
            print("\nContacting Player...")
            send.process(timeout=5)
            return(dat[0])
        else:
            if dat[1] == "P1":
                myturn = True
            elif dat[1] == "P2":
                myturn = False
            return dat[0]


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

buffer = []

enemyMoves = []

jid = 'spar@xmpp.jp'

password = 'spargroupgaming'

opponent_jid = 'spargroup@xmpp.jp'

gameid = ''

comm = None
receiving = True

#Thread functions
def start_receiving():
    global enemyMoves
    global comm
    while receiving :
        comm.process(timeout=1)


class communicator(slix.ClientXMPP):

    def __init__(self, jid, password, opp_jid):
        slix.ClientXMPP.__init__(self, jid, password)
        self.opp_jid = opp_jid

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

        if msg['type'] == 'normal':
            receivedMove = True
            #enemyMoves.append(msg['body'])
        elif msg['type'] == 'chat':
            print("\nOpponent says:", msg['body'])
            if msg.content == "GAME_START":
                opponent_jid = str(msg['from']).split("/")[0]
                print(f"{opponent_jid} has accepted the challenge. Let the battle begin!")
            buffer.append(msg)
        # sender = str(msg['from'])
        # print(type(sender))
        # sender = sender.split("/")[0]
        # print(sender)

    def sendMessage(self, msg, type):
        self.send_message(mto=self.opp_jid, mbody=msg, mtype=type)

def initialize():
    global comm
    global receivingThread

    comm = communicator(jid, password, opponent_jid)
    comm.connect()

    receivingThread = td.Thread(target=start_receiving)
    receivingThread.daemon = True
    receivingThread.start()
initialize()
comm.sendMessage("GAME_START", "chat")
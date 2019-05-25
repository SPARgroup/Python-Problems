import time
import threading as td
import slixmpp as slix
import logging
import os
import requests as req
import msvcrt as ms
import copy
import webbrowser as web

jid = ''
password = ''
opponent_jid = ''

class receiver(slix.ClientXMPP):
    def __init__(self, jid, password):
        slix.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        pass


class sender(slix.ClientXMPP):
    def __init__(self, jid, password, recipient, msg):
        super().__init__(jid, password)
        self.recipient = recipient
        self.msg = msg

        self.add_event_handler('session_start', self.start)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        self.send_message(mto=self.recipient, mbody=self.msg, mtype="chat")

    def sendmsg(self, _msg):
        self.send_message(mto=self.recipient, mbody=_msg, mtype="chat")

#Intro
print("Ultimate TicTacToe Online\n        v2.1\n[Requires an internet connection to play a saved game]\nCredits: Samarth Singla | Ashmit Chamoli | Rishabh Sharma | Abhivir Singh")
time.sleep(0.5)

#ask user for account
n_1 = input("Do you have a jabber account?(y/n): ")
n_1 = n_1.lower()

#Input reg. details
if n_1[0] == 'y':
    jid = input("Enter your User ID: ")
    password = input("Enter Password: ")

else:
    print("Opening Registration link in 2 seconds...")
    time.sleep(2)
    web.open("https://www.xmpp.jp/signup")
    jid = input("Enter your User ID: ")
    password = input("Enter Password: ")

#






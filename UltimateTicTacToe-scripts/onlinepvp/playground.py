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

information = "{}".format("aasdads")
print(information)
import socket as sock
import time
import threading as td
#import slixmpp
import logging
import asyncio
from slixmpp import ClientXMPP


my_jid = "spar@xmpp.jp"
my_pass = "spargroupgaming"

opponent_jid = "spar@xmpp.jp"

class receiver(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def session_start(self):
        print("session started")
        self.send_presence()
        self.get_roster()

    def message(self):
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()


class sender(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(jid, password)

        self.add_event_handler()

logging.basicConfig(level="DEBUG", format='%(levelname)-8s %(message)s')

recv = receiver(my_jid, my_pass)

recv.connect()
recv.process()
input("Press Enter to continue")

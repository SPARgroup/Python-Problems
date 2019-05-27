import socket as sock
import time
import threading as td
import slixmpp as slix
import logging
import asyncio

my_jid = "spargroup@xmpp.jp"
my_pass = "spargroupgaming"

opponent_jid = "spar@xmpp.jp"

#Message handler is working for multiple, sequential messages
class receiver(slix.ClientXMPP):
    def __init__(self, jid, password):
        slix.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("message", self.message)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            msg.reply("Thanks for sending\n%(body)s" % msg).send()
            print(msg['body'])
recv = receiver(my_jid, my_pass)
recv.connect()
# def threader():
#     recv.process()


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

loop = None
async def start_listening():
    pass
# newthread = td.Thread(target=good)
logging.basicConfig(level="DEBUG", format='%(levelname)-8s %(message)s')

# t = td.Thread(target=threader)
# #t.daemon = True #now you can exit the code before this gets finished(it never will)
# t.start()

task = asyncio.ensure_future(start_listening())


input("Press Enter to continue")

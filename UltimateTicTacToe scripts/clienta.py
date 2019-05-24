import socket as sock
import time
import threading as td
import slixmpp as slix



class recvmessageBot(slix.ClientXMPP):
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
            print(msg)

class sendMsgBot(slix.ClientXMPP):
    def __init__(self, jid, password, recipient, msg):
        super().__init__(jid, password)
        self.recipient = recipient
        self.msg = msg

        self.add_event_handler('session_start', self.start)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def bhejo(self):
        self.send_message(mto=self.recipient, mbody=self.msg, mtype="chat")

    def discon(self):
        self.disconnect(self, wait=True)


bot = recvmessageBot("spar@xmpp.jp", "spargroupgaming")
bot2 = sendMsgBot("spar@xmpp.jp", "spargroupgaming", "spar@xmpp.jp", "This is a massage.")
bot.connect()
bot.process()

bot2.connect()
bot2.process()

bot2.bhejo("Hello nigga singh")




# def recievemsg(mySocket):
#     while 1:
#         try:
#             dat, add = mySocket.recvfrom(1024)
#             dat = dat.decode('utf-8')
#             print("\nBheem Says:", dat)
#         except:
#             time.sleep(1)
#             pass
#
#
# target_local = "192.168.88.75"  #set manually, server not set up
# target_port = 0
# me = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
#
# me.bind(("", 0))
#
# print("My Port: ", me.getsockname()[1])
#
# #s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
#
# target_port = int(input("Enter target's port:"))
#
# #s.bind((target_local, target_port))
# t = td.Thread(target=recievemsg, args=(me,))
# t.start()
# while 1:
#     try:
#         msg = input("Enter message for Bheem:").encode("utf-8")
#         me.sendto(msg, (target_local, target_port))
#     except:
#         time.sleep(0.2)
#         pass

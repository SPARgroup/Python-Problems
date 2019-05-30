from slixmpp import ClientXMPP

class sender(ClientXMPP):
    def __init__(self, jid, password, recipient, msg, msgtype):
        ClientXMPP.__init__(self, jid, password)
        self.recipient = recipient
        self.msg = msg
        self.msgtype = msgtype

        self.add_event_handler('session_start', self.start)

        # self.send_presence()
        # self.get_roster()
        # print("DEBUG send_message")
        # self.send_message(mto=self.recipient, mbody=self.msg, mtype=self.msgtype)

    def start(self, event):
        self.send_presence()
        self.get_roster()
        print("DEBUG send_message")
        self.send_message(mto=self.recipient, mbody=self.msg, mtype=self.msgtype)

    def sendmsg(self, _msg):
        self.send_message(mto=self.recipient, mbody=_msg, mtype="chat")

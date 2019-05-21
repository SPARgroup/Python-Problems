import socket as sock
import time
import threading as td


def recievemsg(mySocket):
    while 1:
        try:
            dat, add = mySocket.recvfrom(1024)
            dat = dat.decode('utf-8')
            print("\nBheem Says:", dat)
        except:
            time.sleep(1)
            pass


target_local = "192.168.2.62"  #set manually, server not set up
target_port = 0
me = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)

me.bind(("", 0))

print("My Port: ", me.getsockname()[1])

#s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)

target_port = int(input("Enter target's port:"))

#s.bind((target_local, target_port))
t = td.Thread(target=recievemsg, args=(me,))
t.start()
while 1:
    try:
        msg = input("Enter message for Bheem:").encode("utf-8")
        me.sendto(msg, (target_local, target_port))
    except:
        time.sleep(0.2)
        pass

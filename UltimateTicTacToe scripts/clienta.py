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


target_public = "182.64.168.174"  #set manually, server not set up
target_port = 0
me = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)


me.bind(("192.168.1.9", 0))

print("My Port: ", me.getsockname()[1], "My IP: ", me.getsockname()[0])

target_port = int(input("Enter target's port:"))


t = td.Thread(target=recievemsg, args=(me,))
t.start()

while 1:
    try:
        msg = input("Enter message for Avatar:").encode("utf-8")
        me.sendto(msg, (target_public, target_port))

    except:
        print ("yoyo")
        time.sleep(0.2)
        pass

import socket as sock
import time

target_local = "192.168.88.75"#set manually, server not set up
target_port = 0
me = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)

me.bind(("", 0))

print("My Port: ", me.getsockname()[1])

#s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)

target_port = int(input("Enter target's port:"))

#s.bind((target_local, target_port))

while 1:
    try:
        msg = input("Enter message for Bheem:").encode("utf-8")
        me.sendto(msg, (target_local, target_port))
        data, addr = me.recvfrom(1024)
        data = data.decode("utf-8")
        print("Bheem says:", data)
        time.sleep(2)
    except:
        time.sleep(1)
        pass

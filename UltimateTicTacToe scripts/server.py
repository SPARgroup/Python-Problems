import socket as sock
import threading
import struct
import time
import string

listening_port = 12334
listening_ip = "192.168.2.62"

s = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
s.bind((listening_ip, listening_port))

while 1:
    try:
        data, addr = s.recvfrom(1024)
        s.sendto(data, addr)
        data = data.decode("utf-8")
        print(data, addr)

        time.sleep(3)
    except:
        time.sleep(3)
        pass
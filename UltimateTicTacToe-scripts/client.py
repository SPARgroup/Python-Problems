import socket

HOST = "192.168.2.62"
POT = 0
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
POT = int(input("Enter Host pot: "))



try:
    s.send(b"Hello mr pot.", (HOST, POT))
except:
    print(socket.error)

input()
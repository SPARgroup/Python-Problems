import socket as sock
import time

server_ip = "192.168.2.62"
server_port = 12334

#my_ip = "192.168.2.62"

hellosocket = sock.socket(sock.AF_INET, sock.SOCK_DGRAM)
hellosocket.bind(('', 0))

print(hellosocket.getsockname()[1])

msg = b"Oh Yeah"

hellosocket.sendto(msg, (server_ip, server_port))

data, addr = hellosocket.recvfrom(1024)

print(data.decode("utf-8"), addr)

input()

import socket
import sys
import time

ANY = '0.0.0.0' # socket.gethostbyname('localhost')
S_PORT = 1501
M_ADDR = "224.168.2.9"
M_PORT = 1600

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind((ANY,S_PORT))
sock.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,255)

while 1:
    message = raw_input("Enter message: ")
    sock.sendto(message,(M_ADDR,M_PORT))
    if message == "exit":
        break
sock.close()
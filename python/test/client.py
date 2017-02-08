import socket
import time
import sys

ANY = '0.0.0.0' #socket.gethostbyname('localhost')
M_ADDR = "224.168.2.9"
M_PORT = 1600
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM,socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEPORT,1)
sock.bind((ANY,M_PORT))
sock.setsockopt(socket.IPPROTO_IP,socket.IP_MULTICAST_TTL,255)
status = sock.setsockopt(socket.IPPROTO_IP,socket.IP_ADD_MEMBERSHIP,socket.inet_aton(M_ADDR) + socket.inet_aton(ANY))

while 1:
    data,addr = sock.recvfrom(1024)
    print "Received message from " + str(addr) + " : " + data
    if data == "exit":
        break
sock.close()
import socket

host = ''
port = 80001

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(1)
print 'Listening..'
conn, addr = s.accept()
print 'is up and running.'
print addr, 'connected.'
s.close()
print 'shut down.'
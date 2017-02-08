import socket
import struct
import sys
import time


acknowledge = False
multicast_group = ('224.3.29.71', 10000)

# Create the datagram socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set a timeout so the socket does not block indefinitely when trying
# to receive data.
sock.settimeout(0.2)

# Set the time-to-live for messages to 1 so they do not go past the
# local network segment.
ttl = struct.pack('b', 1)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

for x in range(0, 25):
    message = 'very important data message ' + str(x)
    try:
        # Send data to the multicast group
        print >>sys.stderr, 'sending "%s"' % message
        sent = sock.sendto(message, multicast_group)

        if acknowledge:
                # Look for responses from all recipients
                while True:
                    print >>sys.stderr, 'waiting to receive'
                    try:
                        data, server = sock.recvfrom(16)
                    except socket.timeout:
                        print >>sys.stderr, 'timed out, no more responses'
                        break
                    else:
                        print >>sys.stderr, 'received "%s" from %s' % (data, server)

    finally:
        time.sleep(1) # delays for 1 second before we send another
        # print >>sys.stde

    
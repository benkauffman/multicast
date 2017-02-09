#!/usr/bin/env python

import sys
import socket
import struct
import threading
import pickle

from itertools import product
from optparse import OptionParser
from random import randint as rand
from time import sleep

############################################################################################################

MULTICAST_GROUP = "226.1.1.1"
MULTICAST_PORT = 10000

class Server(object):
    def __init__(self, serv_port):
        self.myport = serv_port
        try:
            print "DEBUG: CREATING SOCKET"
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.socket.bind(("", self.myport))
            self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.settimeout(0.2)
        except socket.error, err:
            print "ERROR: EXCEPTION DURING INITIALIZING SERVER'S SOCKET - %s" % err
            sys.exit(1)
        else:
            print "DEBUG: SOCKET CREATED"
            self.receiver()

    def receiver(self):
        print "DEBUG: WAITING FOR DATA"
        while True:
            try:
                msg, who = self.socket.recvfrom(1024)
            except socket.timeout:
                continue
            except socket.error, err:
                print "ERROR: EXCEPTION DURING RECEIVEING AND READING DATAGRAM - %s" % err
            except KeyboardInterrupt:
                print "DEBUG: KEYBOARD INTERRUPT (CTRL+C)"
                self.__del__()
                return
            else:
                print "MSG: %s \nFROM: %s" % (msg, who)
                self.msg_handle(msg)

    def msg_handle(self, msg):
        msg = int(msg)
        if msg == 88:
            print "DEBUG: RECEIVED CONNECTION REQUEST"
            self.msg_sending("1")
        else:
            print "ERROR: Unknown nr (%s) received" % msg

    def msg_sending(self, msg):
        try:
            print "DEBUG: SENDING - %s" % msg
            self.socket.sendto(msg, (MULTICAST_GROUP, MULTICAST_PORT))
        except socket.error, err:
            print "ERROR: MESSAGE \"%s\" COULDN'T BEEN SENT DUE TO THE: %s." % (msg, err)

    def __del__(self):
        print "DEBUG: CLOSING SOCKET"
        self.socket.close()
        print "DEBUG: SOCKET CLOSED"

############################################################################################################

class Client(object):

############################################################################################################

    class NetworkThread(threading.Thread):

        def __init__(self, parent, serv):
            threading.Thread.__init__(self)
            self.serv = serv
            self.status = 1
            self.parent = parent

            try:
                print "DEBUG: CREATING SOCKET"
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                self.socket.bind(("", MULTICAST_PORT))
#                self.ttl = struct.pack('b', 1)
                self.group = socket.inet_aton(MULTICAST_GROUP)
                self.mreq = struct.pack('=4sl', self.group, socket.INADDR_ANY)
                self.socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, self.mreq)
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                print "DEBUG: TRYING TO CONNECT"
                self.msg_sending( str(88) )
                data, serv = self.socket.recvfrom(1024)
                print str(data) + " from " + str(serv)

            except socket.error, err:
                    print "ERROR: EXCEPTION DURING INITIALIZING SERVER'S SOCKET DUE TO THE: %s" % err
                    sys.exit(1)

        def msg_sending(self, msg):
            try:
                self.socket.sendto(msg, self.serv)
            except socket.error, err:
                print "ERROR: Message \"%s\" COULDN'T BEEN SENT DUE TO THE: %s." % (msg, err)

        def __del__(self): 
            print "DEBUG: CLOSING SOCKET"
            self.socket.close()
            print "DEBUG: SOCKET CLOSED"

############################################################################################################

    def __init__(self, serv):
        self.networking = self.NetworkThread(self, serv)
        self.networking.run()

    def __del__(self):
        print "DEBUG: JOINED - EXITING. HAVE A NICE DAY."

############################################################################################################

if __name__ == "__main__":  
    parser = OptionParser()
    parser.add_option("", "--sp", action="store", type="int", dest="serv_port")
    parser.add_option("", "--sip", action="store", type="string", dest="serv_ip")
    parser.add_option("-c", "", action="store_true", dest="client")
    parser.add_option("-s", "", action="store_true", dest="server")
    options, args = parser.parse_args()
    if not (options.server or options.client):
        print "ERROR: Client/Server not specified. Could not continue..."
        sys.exit(1)
    elif options.server and not options.serv_port:
        print "ERROR: Server's ports not specified. Could not continue..."
        sys.exit(1)
    elif options.client and not (options.serv_port and options.serv_ip):
        print "ERROR: Ports not specified. Could not continue..."
        sys.exit(1)  
    else:
        if options.server:
            serv = Server(options.serv_port)
        else:
            client = Client((options.serv_ip, options.serv_port))
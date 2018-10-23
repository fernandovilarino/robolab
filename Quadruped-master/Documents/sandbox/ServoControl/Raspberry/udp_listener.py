#!/usr/bin/python

import socket
import sys

if len(sys.argv) != 3:
	print 'Error! syntax: server-ip port'
	exit()

UDP_IP = str(sys.argv[1])
UDP_PORT = int(sys.argv[2])

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((UDP_IP, UDP_PORT))
except Exception as e:
	print "Can't create socket :("
	print str(e)
	exit()

while True:
	data, addr = sock.recvfrom(1024)
	print ">>>", data

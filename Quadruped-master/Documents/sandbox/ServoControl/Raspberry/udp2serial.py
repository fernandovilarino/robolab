#!/usr/bin/python

import socket
import serial
import sys
import time



if len(sys.argv) != 3:
	print 'Error! syntax: server-ip port'
	exit()

UDP_IP = str(sys.argv[1])
UDP_PORT = int(sys.argv[2])

try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 32)
	sock.bind((UDP_IP, UDP_PORT))
except Exception as e:
	print "Can't create socket :("
	print e
	exit()

ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
	data, addr = sock.recvfrom(1024)
	ser.write(data)
	print ">>>", data
	time.sleep(0.01)

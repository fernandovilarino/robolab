#!/usr/bin/python

import socket
import serial
import sys
import time

pa = 0

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
	print e
	exit()

ser = serial.Serial('/dev/ttyACM0', 115200)

while True:
	data, addr = sock.recvfrom(9)
	ser.write(data)
	pa += 1
	print 'pa:', pa
	print '<',data
	print '>',ser.readline()
	time.sleep(0.05)

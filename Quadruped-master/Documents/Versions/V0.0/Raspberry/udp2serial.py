#!/usr/bin/python

import socket
import serial
import sys
import time




## =============================================================================
## ============================== Create UDP server ============================
## =============================================================================

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

## =============================================================================
## =============================================================================




## =================== Open serial comunication ===================
ser = serial.Serial('/dev/ttyACM0', 115200)
## ================================================================




## ============================================================================================
## ========================= Send messages to usb when arduinno ready =========================
## ============================================================================================

while True:
	data, addr = sock.recvfrom(255)

	ser.write(data)
	print '<',data

	ser.readline()		# Wait arduino ready
	#print '>',ser.readline()

	time.sleep(0.05)

## ============================================================================================
## ============================================================================================

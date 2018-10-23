#!/usr/bin/python

import socket
import sys
import time
import threading
import serial



class QServer:



	def __init__(self, ip='192.168.4.1', port=8787):
		
		self.IP = ip
		self.PORT = port
		print 'Running on', ip, ':', port
		
		# Client address
		self.client_ip = ""
		self.client_port = 0
		
		
		# State variables	('header':value)
		self.SVar = {
					'w': 0,		# dir
					'r': 0,		# rot
					'q': 0,		# pos
					'v': 1,		# speed
					't': 1,			# steps
					'c': '090090',	# camera pos
					'm': 0,		# mode
					'a': 0		# anti colision
					}
					
		self.prevSVar = self.SVar.copy()
		self.wTo0 = False
		self.rTo0 = False
		
		# Message headers and functions to call when receive it
		self.headers = {
						'p': self.ping,		# Ping
						'w': self.walk,		# Walk
						'r': self.rot,		# rot
						'q': self.setPos,	# wakeup or sleep
						'c': self.setCam,	# camera position
						'a': self.setAc,	# anti colision
						'v': self.setSpeed,	# Speed
						't': self.setSteps	# Steps
						}
		
		
		
		# ----- Create server socket -------------------------------------------------------
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.sock.bind((self.IP, self.PORT))
		except Exception as e:
			print "Can't create socket :("
			print e
			exit()
		# ----------------------------------------------------------------------------------
		
		
		# ----- Open serial comunication ---------------------------------------------------
		self.ser = serial.Serial('/dev/ttyACM0', 115200)
		# ----------------------------------------------------------------------------------
			
			
			
		#   State variable thread lock
		self.varLock = threading.Lock()
		
		#   UDP server thread
		self.thr_udp = threading.Thread(target=self.runServer)
		self.thr_udp.start()
		
		#   Serial comunication thread
		self.thr_ser = threading.Thread(target=self.runSerial)
		self.thr_ser.start()
		
		
		self.thr_udp.join()
		self.thr_ser.join()
		

		
	def runSerial(self):
		wait = False
		
		while True:
			for k in self.SVar.keys():	# Check if some variable has changed
				self.varLock.acquire()
				if self.SVar[k] != self.prevSVar[k]:
					self.prevSVar[k] = self.SVar[k]
					print 'serial',k+str(self.SVar[k])+';'	#ser.write(k+str(self.SVar[k])+';')	# Send changed value
					self.ser.write(k+str(self.SVar[k])+';')
					wait = True

				self.varLock.release()
				if wait:
					print self.ser.readline()  				# Wait for arduino ready
					wait = False
			if self.wTo0:
				self.wTo0 = False
				self.SVar['w'] = 0
			if self.rTo0:
				self.rTo0 = False
				self.SVar['r'] = 0
			time.sleep(0.05)
			

		
		
	# Listen and update state variables
	def runServer(self):
		while True:
		
			data, addr = self.sock.recvfrom(255)

			self.client_ip = addr[0]
			self.client_port = addr[1]
			
			header = data[0]
			body = data[1:]
			
			print header, body
			
			if header in self.headers.keys():	# Call the right method for the received header
				if header == 'w' and self.SVar['w'] != 0 and body == 0:
					self.wTo0 = True
				elif header == 'r' and self.SVar['r'] != 0 and body == 0:
					self.rTo0 = True
				else:
					self.headers[header](body)

			
	
	
	def ping(self, body):
		self.sock.sendto(':D', (self.client_ip, self.client_port))
		
		
	def setPos(self, body):
		self.varLock.acquire()
		self.SVar['q']  = body[0]
		self.varLock.release()
		
		
	def walk(self, body):
		self.varLock.acquire()
		self.SVar['w']  = body[0]
		self.varLock.release()
		
		
	def setCam(self, body):
		self.varLock.acquire()
		self.SVar['c']  = body
		self.varLock.release()
		
	
	def rot(self, body):
		self.varLock.acquire()
		self.SVar['r']  = body
		self.varLock.release()
	
	def setAc(self, body):
		self.varLock.acquire()
		self.SVar['a']  = body
		self.varLock.release()
	
	def setSpeed(self, body):
		self.varLock.acquire()
		self.SVar['v']  = body
		self.varLock.release()
	
	def setSteps(self, body):
		self.varLock.acquire()
		self.SVar['t']  = body
		self.varLock.release()

	
	
	
	

if __name__ == '__main__':

	if len(sys.argv) != 3:
		print 'QServer.py [ServerIp] [Port]'
		qserver = QServer()
	else:
		ip   = str(sys.argv[1])
		port = int(sys.argv[2])
		qserver = QServer(ip, port)
	

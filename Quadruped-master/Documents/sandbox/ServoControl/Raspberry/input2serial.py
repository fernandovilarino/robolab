#!/usr/bin/python

import serial
import time
import math

ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
	ina = raw_input(">>>")
	if(ina.isdigit() and int(ina)>=0 and int(ina)<=180):
		ser.write(ina+';')
	elif(ina == "auto"):
		for i in range(0,180,2):
			ser.write(str(i)+';')
			print '>>>',str(i)+';'
			time.sleep(0.05)
		for i in range(180,0,-2):
			ser.write(str(i)+';')
			print '>>>', str(i)+';'
			time.sleep(0.05)
	elif(ina == "sin"):
		for i in range(0,180):
			ser.write(str(int(180*(math.sin(0.0174533*i))))+';')
			print '>>>', str(int(180*(math.sin(0.0174533*i))))+';'
			time.sleep(0.05)


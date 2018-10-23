from Tkinter import *
import time
import threading
import sys
import socket
import serial



class W1:
	
	def __init__(self):
		self.root = Tk()
		self.root.geometry("350x300")
		
		# LINUX:
		#self.ser = serial.Serial('/dev/ttyACM1', 115200)
		
		# WIN:
		#self.ser = serial.Serial('COM3', 115200)
		
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		
		self.root.bind('<Left>',  self.leftKey)
		self.root.bind('<Right>', self.rightKey)
		self.root.bind('<Up>',    self.upKey)
		self.root.bind('<Down>',  self.downKey)

		self.buttons = {}
		self.labels = {}
		self.scales = {}
		self.spinboxs = {}
		
		self.angV = IntVar()
		self.angH = IntVar()
		
		self.angV.set(90)
		self.angH.set(90)
		
		self.initElements()
		
		self.angV.trace("w", self.update)
		self.angH.trace("w", self.update)

		self.root.focus_set()
		self.root.mainloop()


	def initElements(self):

		# ------ Scales ------
		scaleV = Scale(self.root, variable=self.angV, from_=0, to=180, tickinterval=90, repeatdelay=1)
		scaleV.place(x=0, y=150)
		self.scales['scaleV'] = scaleV
		
		scaleH = Scale(self.root, variable=self.angH, from_=0, to=180, tickinterval=90, repeatdelay=1, orient=HORIZONTAL,length=150)
		scaleH.place(x=170, y=200)
		self.scales['scaleH'] = scaleH

		# ------ Spin Box ------
		spinv = Spinbox(self.root, from_=0, to=180, repeatdelay=1, width=10, textvariable=self.angV)
		spinv.place(x=10, y=260)
		self.spinboxs['spinv'] = spinv
		
		spinh = Spinbox(self.root, from_=0, to=180, repeatdelay=1, width=10, textvariable=self.angH)
		spinh.place(x=175, y=260)
		self.spinboxs['spinh'] = spinh

		# ------ Labels ------
		upl = Label(self.root, text="^ Up Key", fg="grey47")
		upl.place(x=75,y=150)
		self.labels['upl'] = upl
		
		downl = Label(self.root, text="v Down Key", fg="grey47")
		downl.place(x=75,y=235)
		self.labels['downl'] = downl
		
		rl = Label(self.root, text="< Right Key", fg="grey47")
		rl.place(x=170,y=180)
		self.labels['rl'] = rl
		
		ll = Label(self.root, text="Left Key >", fg="grey47")
		ll.place(x=280,y=180)
		self.labels['ll'] = ll

		
		# ------ Canvas ------
		self.canv = Canvas(self.root, bg="gray80", height=130, width=400)
		self.canv.place(x=0, y=0)
		self.arcV = self.canv.create_arc((10,10,110,110), start=90,extent=180, fill="snow")
		self.arcH = self.canv.create_arc((100,50,200,150), start=0,extent=180, fill="snow")
		
		self.RectV = self.canv.create_arc((10,10,110,110), start=90,extent=self.angV.get(), fill="snow", outline="blue")
		self.arcH = self.canv.create_arc((100,50,200,150), start=0, extent=180-self.angH.get(), fill="snow", outline="red")
		


		self.th = threading.Thread(target=self.writeSerial)
		self.th.start()


	def update(self, *args):
		self.canv.delete("all")
		self.arcV = self.canv.create_arc((10,10,110,110), start=90,extent=180, fill="snow")
		self.arcH = self.canv.create_arc((100,50,200,150), start=0,extent=180, fill="snow")

		self.RectV = self.canv.create_arc((10,10,110,110), start=90,extent=self.angV.get(), fill="snow", outline="blue")
		self.arcH = self.canv.create_arc((100,50,200,150), start=0, extent=180-self.angH.get(), fill="snow", outline="red")


	def writeSerial(self):
		antH = 90
		antV = 90

		while (True):
			
			if(antH != self.angH.get() or antV != self.angV.get()):
				antH = self.angH.get()
				antV = self.angV.get()

				msg = ''

				invangH = 180 - antH
				invangV = 180 - antV

				if(invangH < 10):
						msg += '00' + str(invangH)
				elif (invangH < 100):
						msg += '0' + str(invangH)
				else:
						msg += str(invangH)

				if(invangV < 10):
						msg += '00' + str(invangV)
				elif (invangV < 100):
						msg += '0' + str(invangV)
				else:
					msg += str(invangV)

				#self.ser.write('hv'+msg+';')
				#print self.ser.readline()
				print 'cc'+msg+';'
				self.sock.sendto('cc'+msg+';', ('192.168.0.30', 3000))
			
			time.sleep(0.1)



	def leftKey(self, event):
		if (self.angH.get() > 0):
			self.angH.set(self.angH.get() - 1)
		
	def rightKey(self, event):
		if (self.angH.get() < 180):
			self.angH.set(self.angH.get() + 1)

		
	def upKey(self, event):
		if (self.angV.get() > 0):
			self.angV.set(self.angV.get() - 1)

		
	def downKey(self, event):
		if (self.angV.get() < 180):
			self.angV.set(self.angV.get() + 1)




if (__name__ == "__main__"):
		w1 = W1()

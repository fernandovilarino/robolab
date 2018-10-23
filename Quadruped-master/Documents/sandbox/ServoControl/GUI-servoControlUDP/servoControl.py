from Tkinter import *
import time
import threading
import sys
import socket



class W1:
	
	def __init__(self, ip="192.168.0.50", port=4444):
		self.root = Tk()
		self.root.geometry("400x300")
		
		self.servopos = 0
		self.toSend = "0;"

		self.ip = ip
		self.port = int(port)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sendUDP(0)

		self.buttons = {}
		self.labels = {}
		self.scales = {}
		self.spinboxs = {}
		self.initElements()
		
		self.root.mainloop()



	def initElements(self):
		st=threading.Thread(target=self.sender)
		st.start()
		
		# ------ Buttons ------
		self.autorunning = False
		start = Button(self.root, text="start", command=self.auto)
		start.place(x=0, y=30)
		self.buttons['start'] = start

		stop = Button(self.root, text="stop", command=self.stopauto)
		stop.place(x=50, y=30)
		self.buttons['stop'] = stop

		# ------ Scales ------
		var = DoubleVar()
		pos = Scale(self.root, variable=var, from_=0, to=180, tickinterval=90, repeatdelay=1)
		pos.place(x=0, y=100)
		self.scales['pos'] = pos
		t=threading.Thread(target=self.runOnChangePos)
		t.start()

		# ------ Spin Box ------
		spos = Spinbox(self.root, from_=0, to=180, repeatdelay=1, width=10)
		spos.place(x=0, y=230)
		self.spinboxs['pos'] = spos
		t2=threading.Thread(target=self.runOnChangeSpin)
		t2.start()

		# ------ Labels ------
		titletop = Label(self.root, text="Auto")
		titletop.place(x=10,y=10)
		self.labels['titletop'] = titletop

		# ------ Canvas ------
		self.canv = Canvas(self.root, bg="red", height=200, width=200)
		self.canv.place(x=200, y=0)
		self.arc = self.canv.create_arc((10,10,110,110), start=0,extent=0, fill="black")
		self.canv.place(x=200, y=0)



	def runAuto(self):
		while True:
			for i in range(self.servopos, 180):
				self.scales['pos'].set(i)
				if(not self.autorunning):
					return
				time.sleep(0.03)

			for i in range(self.servopos, 0, -1):
				self.scales['pos'].set(i)
				if(not self.autorunning):
					return
				time.sleep(0.03)


	def runOnChangePos(self):
		while True:
			pos = self.scales['pos'].get()
			if(pos != self.servopos):
				self.servopos = pos
				self.spinboxs['pos'].delete(0, len(self.spinboxs['pos'].get()))
				self.spinboxs['pos'].insert(0, str(pos))
				self.canv.delete("all")
				self.arc = self.canv.create_arc((10,10,110,110), start=0,extent=pos, fill="black")
				self.sendUDP(pos)
			time.sleep(0.005)


	def runOnChangeSpin(self):
		while True:
			pos = self.spinboxs['pos'].get()
			if(pos.isdigit() and int(pos) != self.servopos and int(pos)<=180 and int(pos)>=0):
				self.scales['pos'].set(int(pos))
			time.sleep(0.01)


	def auto(self):
		if(self.autorunning == False):
			print 'auto'
			self.autorunning = True
			t=threading.Thread(target=self.runAuto)
			t.start()


	def stopauto(self):
		print 'auto stops'
		self.autorunning = False


	def sendUDP(self,MESSAGE):
		self.toSend = str(MESSAGE)+';'
  		#self.sock.sendto(str(MESSAGE)+';', (self.ip, self.port))

  	def sender(self):
  		a = self.toSend
  		while True:
  			if(self.toSend != a):
  				a = self.toSend
  				self.sock.sendto(self.toSend, (self.ip, self.port))

  			time.sleep(0.05)





if (__name__ == "__main__"):
	if(len(sys.argv) == 3):
		w1 = W1(sys.argv[1], sys.argv[2])
	else:
		w1 = W1()

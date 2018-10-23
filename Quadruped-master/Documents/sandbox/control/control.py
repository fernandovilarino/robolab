from Tkinter import *
from ScrolledText import *
import time
import threading
import sys
import socket
#import serial
from functools import partial


class W1:
	
	def __init__(self, ip='192.168.4.1', port=8787):
	
		self.sender = Sender(ip, port)
		self.connected =  False
		
		self.root = Tk()
		self.root.geometry("1000x500")
		
		self.root.title("Quadruped Controller")
		

		# -------------------------------------------------------------------------	
		
		self.buttons = {}
		self.labels = {}
		self.scales = {}
		self.spinboxs = {}
		self.text = {}
		self.checkbuttons = {}
		
		self.toSend = set()
		
		# -------------------------------------------------------------------------	
		
		self.autoMode = False

		self.speedMax = 10
		self.speedMin = 1
		
		self.stepsMax = 10
		self.stepsMin = 1
		
		self.speed = IntVar()
		self.speed.set(8)
		
		self.anticolision = IntVar()
		self.anticolision.set(0)
		
		self.steps = IntVar()
		self.steps.set(1)

		self.dir = 0
		self.rot = 0
		
		self.camV = IntVar()
		self.camV.set(90)
		self.camH = IntVar()
		self.camH.set(90)
		
		
		self.wTo0 = False
		self.rTo0 = False
		
		# -------------------------------------------------------------------------	
		
		self.initElements()
		
		# -------------------------------------------------------------------------	
		
		self.activeKeys = set()
		self.root.bind_all('<KeyPress>', self.keyPressHandler)
		self.root.bind_all('<KeyRelease>', self.keyReleaseHandler)
		
		# -------------------------------------------------------------------------	
		
		self.speed.trace("w", self.update_sp)
		self.steps.trace("w", self.update_st)
		self.camV.trace("w", self.update_cam)
		self.camH.trace("w", self.update_cam)
		self.anticolision.trace("w", self.update_ac)

		self.root.after(1000, self.handleKeyActions)
		self.root.after(1000, self.send)
		self.root.after(1500, self.checkConn())
		self.root.focus_set()
		self.root.mainloop()



	def initElements(self):

		# ------ Frames ------
	
		movframe = LabelFrame(self.root, text="Movement")
		movframe.place(x=10,y=0)
		c = Label(movframe, text=" ")
		c.pack(padx=300,pady=110)
		
		camframe = LabelFrame(self.root, text="Camera control")
		camframe.place(x=600,y=0)
		c = Label(camframe, text=" ")
		c.pack(padx=190,pady=110)
	
		# ------ Scales ------

		# Speed
		sc_sp = Scale(self.root, variable=self.speed, from_=self.speedMin, to=self.speedMax, repeatdelay=1, showvalue=0, orient=HORIZONTAL)
		sc_sp.place(x=70, y=190)
		self.scales['sc_sp'] = sc_sp
		
		# Steps
		sc_st = Scale(self.root, variable=self.steps, from_=self.stepsMin, to=self.stepsMax, repeatdelay=1, showvalue=0, orient=HORIZONTAL)
		sc_st.place(x=70, y=220)
		self.scales['sc_st'] = sc_st
		
		
		# Cam V
		sc_cv = Scale(self.root, variable=self.camV, from_=0, to=180, repeatdelay=1, showvalue=0, orient=VERTICAL)
		sc_cv.place(x=680, y=70)
		self.scales['sc_cv'] = sc_cv
		
		# Cam H
		sc_ch = Scale(self.root, variable=self.camH, from_=0, to=180, repeatdelay=1, showvalue=0, orient=HORIZONTAL)
		sc_ch.place(x=800, y=190)
		self.scales['sc_ch'] = sc_ch
		

		# ------ Spin Box ------

		# Speed
		sp_sp = Spinbox(self.root, from_=self.speedMin, to=self.speedMax, repeatdelay=1, width=10, textvariable=self.speed)
		sp_sp.place(x=190, y=190)
		self.spinboxs['sp_sp'] = sp_sp
		
		# Steps
		sp_st = Spinbox(self.root, from_=self.stepsMin, to=self.stepsMax, repeatdelay=1, width=10, textvariable=self.steps)
		sp_st.place(x=190, y=220)
		self.spinboxs['sp_st'] = sp_st
		
		# Cam V
		sp_cv = Spinbox(self.root, from_=0, to=180, repeatdelay=1, width=10, textvariable=self.camV)
		sp_cv.place(x=650, y=190)
		self.spinboxs['sp_cv'] = sp_cv
		
		# Cam h
		sp_ch = Spinbox(self.root, from_=0, to=180, repeatdelay=1, width=10, textvariable=self.camH)
		sp_ch.place(x=910, y=190)
		self.spinboxs['sp_ch'] = sp_ch
		

		# ------ Labels ------
		
		# Movement
		ff = Label(self.root, text="forward (w)")
		ff.place(x=193,y=20)
		
		bw = Label(self.root, text="backward (s)")
		bw.place(x=193,y=135)
		
		r = Label(self.root, text="right (d)")
		r.place(x=325,y=102)
		
		l = Label(self.root, text="left (a)")
		l.place(x=82,y=102)

		rr = Label(self.root, text="rotate right (e)")
		rr.place(x=325,y=30)
		
		rl = Label(self.root, text="rotate right (q)")
		rl.place(x=46,y=30)
		
		sp = Label(self.root, text="Speed:", fg="black")
		sp.place(x=20,y=190)
		
		s = Label(self.root, text="Steps:", fg="black")
		s.place(x=20,y=220)
		
		# Camera
		tilt = Label(self.root, text="Tilt", fg="black")
		tilt.place(x=700,y=30)
		
		pan = Label(self.root, text="Pan", fg="black")
		pan.place(x=850,y=30)
		
		up = Label(self.root, text="    Up Key ^", fg="grey47")
		up.place(x=610,y=70)
		
		dw = Label(self.root, text="Down Key v", fg="grey47")
		dw.place(x=610,y=155)
		
		lb_x = Label(self.root, text="< Right Key", fg="grey47")
		lb_x.place(x=750,y=220)
		
		lb_y = Label(self.root, text="Left Key >", fg="grey47")
		lb_y.place(x=889,y=220)
		
		
		# ------ Buttons ------

		self.buttons['fw'] = Button(self.root, text="^", width=5, command=partial(self.setDir, (1)))
		self.buttons['fw'].place(x=200, y=50)
		
		self.buttons['bw'] = Button(self.root, text="v", width=5, command=partial(self.setDir, (3)))
		self.buttons['bw'].place(x=200, y=100)
		
		self.buttons['r'] = Button(self.root, text=">", width=5, command=partial(self.setDir, (2)))
		self.buttons['r'].place(x=270, y=100)
		
		self.buttons['l'] = Button(self.root, text="<", width=5, command=partial(self.setDir, (4)))
		self.buttons['l'].place(x=130, y=100)
		
		self.buttons['rr'] = Button(self.root, text="/->", width=5, command=partial(self.setRot, (1)))
		self.buttons['rr'].place(x=270, y=50)
		
		self.buttons['rl'] = Button(self.root, text="<-\\", width=5, command=partial(self.setRot, (-1)))
		self.buttons['rl'].place(x=130, y=50)
		
		self.buttons['wu'] = Button(self.root, text="wake up ^", width=10, command=self.setWakeup)
		self.buttons['wu'].place(x=500, y=30)
		
		self.buttons['si'] = Button(self.root, text="sleep   v", width=10, command=self.setSleep)
		self.buttons['si'].place(x=500, y=70)
		
		self.buttons['st'] = Button(self.root, text="STOP", borderwidth=4, width=10)
		self.buttons['st'].place(x=500, y=110)
		
		self.buttons['auto'] = Button(self.root, text="Auto", borderwidth=4, width=10, command=self.setAuto, relief="raised")
		self.buttons['auto'].place(x=420, y=180)
		
		self.buttons['man'] = Button(self.root, text="Manual", borderwidth=4, width=10, command=self.setMan, relief="sunken", state=DISABLED)
		self.buttons['man'].place(x=500, y=180)
		
		
		# ------ Checkbuttons ------
		
		self.checkbuttons['anticolision'] = Checkbutton(self.root, text="Anti Colision", variable=self.anticolision)
		self.checkbuttons['anticolision'].place(x = 420, y=220)
		
		# ------ Canvas ------
		
		self.canv = Canvas(self.root, height=120, width=200)
		self.canv.place(x=710, y=60)
		self.arcV = self.canv.create_arc((10,10,110,110), start=90,extent=180, fill="snow")
		self.arcH = self.canv.create_arc((100,50,200,150), start=0,extent=180, fill="snow")
		
		self.RectV = self.canv.create_arc((10,10,110,110), start=90,extent=self.camV.get(), fill="snow", outline="blue")
		self.arcH = self.canv.create_arc((100,50,200,150), start=0, extent=180-self.camH.get(), fill="snow", outline="red")
		
		
		# ------ Text ------
		
		self.text['camIP'] = Text(self.root, width=122, height=1, fg="blue")
		self.text['camIP'].place(x=10,y=270)
		self.text['camIP'].insert(INSERT, "Video Streaming ->  http://192.168.4.1:8082/index.html")
		self.text['camIP'].configure(state=DISABLED)
		
		
		self.text['log'] = ScrolledText(self.root, width=120, height=12, state=DISABLED)
		self.text['log'].place(x=10,y=300)
		
		
		
		if self.sender.ping():
			self.text['log'].configure(state='normal')
			self.text['log'].insert('end', '***Connected')
			self.text['log'].configure(state='disabled')
			self.connected = True
		else:
			self.text['log'].configure(state='normal')
			self.text['log'].insert('end', '***Disonnected')
			self.text['log'].configure(state='disabled')

		
		
		
		
	def setAuto(self):
		self.autoMode = True
		
		self.buttons["auto"].config(relief="sunken")
		self.buttons["auto"].config(state=DISABLED)
		
		self.buttons["man"].config(relief="raised")
		self.buttons["man"].config(state=ACTIVE)
		
		self.buttons["fw"].config(state=DISABLED)
		self.buttons["bw"].config(state=DISABLED)
		self.buttons["r"].config(state=DISABLED)
		self.buttons["l"].config(state=DISABLED)
		self.buttons["rr"].config(state=DISABLED)
		self.buttons["rl"].config(state=DISABLED)
		self.buttons["wu"].config(state=DISABLED)
		self.buttons["si"].config(state=DISABLED)
		self.buttons["st"].config(state=DISABLED)
		
		self.checkbuttons["anticolision"].config(state=DISABLED)
		
		self.send()
		
		
	def setMan(self):
		self.autoMode = False
		
		self.buttons["man"].config(relief="sunken")
		self.buttons["man"].config(state=DISABLED)
		
		self.buttons["auto"].config(relief="raised")
		self.buttons["auto"].config(state=ACTIVE)
		
		self.buttons["fw"].config(state=ACTIVE)
		self.buttons["bw"].config(state=ACTIVE)
		self.buttons["r"].config(state=ACTIVE)
		self.buttons["l"].config(state=ACTIVE)
		self.buttons["rr"].config(state=ACTIVE)
		self.buttons["rl"].config(state=ACTIVE)
		self.buttons["wu"].config(state=ACTIVE)
		self.buttons["si"].config(state=ACTIVE)
		self.buttons["st"].config(state=ACTIVE)
		
		self.checkbuttons["anticolision"].config(state=ACTIVE)
		
		self.send()
		
		
	def update_cam(self, *args):
		self.toSend.add('cam')
		self.canv.delete("all")
		self.arcV = self.canv.create_arc((10,10,110,110), start=90,extent=180, fill="snow")
		self.arcH = self.canv.create_arc((100,50,200,150), start=0,extent=180, fill="snow")

		self.RectV = self.canv.create_arc((10,10,110,110), start=90,extent=self.camV.get(), fill="snow", outline="blue")
		self.arcH = self.canv.create_arc((100,50,200,150), start=0, extent=180-self.camH.get(), fill="snow", outline="red")
		
		self.send()
	
		
	
	def update_sp(self, *args):
		self.toSend.add('sp')
	
	def update_st(self, *args):
		self.toSend.add('st')

	def setDir(self, *args):
		self.dir = args[0]
		self.toSend.add('dir')
		self.wTo0 = True
		
	def setRot(self, *args):
		self.rot = args[0]
		self.toSend.add('rot')
		self.rTo0 = True
		
	def setWakeup(self, *args):
		self.toSend.add('posW')
		
	def setSleep(self, *args):
		self.toSend.add('posS')
	
	def update_ac(self, *args):
		self.toSend.add('ac')
	
	
	
	def send(self):
	
		for u in self.toSend:
			if u == 'sp':
				self.sender.send_speed(self.speed.get())
			elif u == 'st':
				self.sender.send_steps(self.steps.get())
			elif u == 'dir':
				self.sender.send_walk(self.dir)
			elif u == 'rot':
				self.sender.send_rot(self.rot)
			elif u == 'cam':
				self.sender.send_cam(self.camH.get(), self.camV.get())
			elif u == 'posW':
				self.sender.send_wu()
			elif u == 'posS':
				self.sender.send_slp()
			elif u == 'ac':
				self.sender.send_ac(self.anticolision.get())
				
		self.toSend.clear()
	
		if self.wTo0:
			self.dir = 0
			self.toSend.add('dir')
			self.wTo0 = False
		
		if self.rTo0:
			self.rot = 0
			self.toSend.add('rot')
			self.rTo0 = False
	
		self.root.after(500, self.send)
		
		
		
	def checkConn(self):
		self.sender.send_ping()
		ok = self.sender.isAlive()
		if ok and not self.connected:
			self.text['log'].configure(state='normal')
			self.text['log'].insert('end', '\n***Connected')
			self.text['log'].configure(state='disabled')
			self.connected = True
		elif not ok and self.connected:
			self.text['log'].configure(state='normal')
			self.text['log'].insert('end', '\n***Disconnected')
			self.text['log'].configure(state='disabled')
			self.connected = False
			
		self.root.after(5000, self.checkConn)
		
		
	
	# ============================ Keys events ============================
	
	def keyPressHandler(self, event):
		self.activeKeys.add(event.keycode)
		

	def keyReleaseHandler(self, event):
		self.activeKeys.remove(event.keycode)
		
		if event.keycode == 87:		# W key
			self.buttons["fw"].config(relief="raised")
			self.dir = 0
			self.toSend.add('dir')
			return
		
		if event.keycode == 68:		# D key
			self.buttons["r"].config(relief="raised")
			self.dir = 0
			self.toSend.add('dir')
			return
		
		if event.keycode == 83:		# S key
			self.buttons["bw"].config(relief="raised")
			self.dir = 0
			self.toSend.add('dir')
			return
		
		if event.keycode == 65:		# A key
			self.buttons["l"].config(relief="raised")
			self.dir = 0
			self.toSend.add('dir')
			return
		
		if event.keycode == 69:		# E key
			self.buttons["rr"].config(relief="raised")
			self.rot = 0
			self.toSend.add('rot')
			return
		
		if event.keycode == 81:		# Q key
			self.buttons["rl"].config(relief="raised")
			self.rot = 0
			self.toSend.add('rot')
			return
		
	def handleKeyActions(self):
		#print self.activeKeys
		
		for k in self.activeKeys:
			if k == 38:		# Up key
				if (self.camV.get() > 0):
					self.camV.set(self.camV.get() - 5)
				pass
					
			if k == 40:		# Down key
				if (self.camV.get() < 180):
					self.camV.set(self.camV.get() + 5)
				pass
				
			if k == 39:		# Right key
				if (self.camH.get() < 180):
					self.camH.set(self.camH.get() + 5)
				pass
				
			if k == 37:		# Left key
				if (self.camH.get() > 0):
					self.camH.set(self.camH.get() - 5)
				pass
				
			if k == 87:		# W key
				self.setDir(1)
				self.buttons["fw"].config(relief="sunken")
				pass
			
			if k == 68:		# D key
				self.setDir(2)
				self.buttons["r"].config(relief="sunken")
				pass
				
			if k == 83:		# S key
				self.setDir(3)
				self.buttons["bw"].config(relief="sunken")
				pass
			
			if k == 65:		# A key
				self.setDir(4)
				self.buttons["l"].config(relief="sunken")
				pass
			
			if k == 69:		# E key
				self.setRot(1)
				self.buttons["rr"].config(relief="sunken")
				pass
			
			if k == 81:		# Q key
				self.setRot(-1)
				self.buttons["rl"].config(relief="sunken")
				pass
		
		
		self.root.after(80, self.handleKeyActions)
	
	# ====================================================================

	
	
	

	
class Sender:
	
	def __init__(self, ip, port):
		
		self.ip = ip
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.settimeout(2)
		
		self.con = False
		
		self.headers = {
						'ping': 'p',
						'walk': 'w',
						'rot': 'r',
						'speed': 'v',
						'steps': 't',
						'cam': 'c',
						'mode': 'm',
						'pos': 'q',	# Position = sleep or wakeup
						'wakeup': '1',
						'sleep': '0',
						'anticolision': 'a'
						}
		
		self.sock.sendto(self.headers['ping'], (self.ip, self.port))
		try:
			data, addr = self.sock.recvfrom(128)
			print data
		except Exception as e:
			print 'error', e
	
	# -------------- Ping --------------
	def send_ping(self):
		th = threading.Thread(target=self.ping)
		th.start()
	
	def ping(self):
		self.sock.sendto(self.headers['ping'], (self.ip, self.port))
		try:
			data, addr = self.sock.recvfrom(128)
			if self.con == False:
				self.con = True
			return True
		except:
			self.con = False
			return False
	
	def isAlive(self):
		return self.con
	# ---------------------------------
		
	
	# -------------- Walk --------------
	def send_walk(self, dir):
		th = threading.Thread(target=partial(self.walk, (dir)))
		th.start()
		
	def walk(self, dir):
		self.sock.sendto(self.headers['walk']+str(dir), (self.ip, self.port))
	# ---------------------------------
	
	
	# -------------- Rot --------------
	def send_rot(self, rot):
		th = threading.Thread(target=partial(self.rot, (rot)))
		th.start()
		
	def rot(self, rot):
		self.sock.sendto(self.headers['rot']+str(rot), (self.ip, self.port))
	# ---------------------------------
	
	
	# -------------- wakeup --------------
	def send_wu(self):
		th = threading.Thread(target=self.wu)
		th.start()
		
	def wu(self):
		self.sock.sendto(self.headers['pos']+self.headers['wakeup'], (self.ip, self.port))
	# ---------------------------------
	
	
	# -------------- sleep --------------
	def send_slp(self):
		th = threading.Thread(target=self.slp)
		th.start()
		
	def slp(self):
		self.sock.sendto(self.headers['pos']+self.headers['sleep'], (self.ip, self.port))
	# ---------------------------------
	
	
	# -------------- Speed --------------
	def send_speed(self, sp):
		th = threading.Thread(target=partial(self.speed, (sp)))
		th.start()
		
	def speed(self, sp):
		realSp = int((1-(sp/10.0)) * 30 + 10)
		self.sock.sendto(self.headers['speed']+str(realSp), (self.ip, self.port))
	# ---------------------------------
	
	
	# -------------- Steps --------------
	def send_steps(self, st):
		th = threading.Thread(target=partial(self.steps, (st)))
		th.start()
		
	def steps(self, st):
		self.sock.sendto(self.headers['steps']+str(st), (self.ip, self.port))
	# ---------------------------------
	
	
	# -------------- AntiColision --------------
	def send_ac(self, ac):
		th = threading.Thread(target=partial(self.ac, (ac)))
		th.start()
		
	def ac(self, ac):
		self.sock.sendto(self.headers['anticolision']+str(ac), (self.ip, self.port))
	# ---------------------------------
	
	
	# -------------- Cam --------------
	def send_cam(self, x,y):
		th = threading.Thread(target=partial(self.cam, x,y))
		th.start()
		
	def cam(self, x,y):
		msg = ''
		invangH = 180 - x
		invangV = 180 - y
		
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
		
		self.sock.sendto(self.headers['cam']+msg, (self.ip, self.port))
	# ---------------------------------
	
	
	
	
	
	
if (__name__ == "__main__"):

	if len(sys.argv) != 3:
		print 'Control.py [ServerIp] [Port]'
		w1 = W1()
	else:
		ip   = str(sys.argv[1])
		port = int(sys.argv[2])
		w1 = W1(ip, port)

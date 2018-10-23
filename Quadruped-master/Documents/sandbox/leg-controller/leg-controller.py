from Tkinter import *
import time
import threading
import sys
import socket

from functools import partial


class W1:
	
	def __init__(self, mode=0, ip="192.168.4.1", port=30001):
		# mode = 0: only print,  1: serial   2: udp
		
		self.mode = mode
		
		self.root = Tk()
		self.root.geometry("1000x500")
		
		self.root.title("Leg controller")
		
		if(mode == 1):
			# LINUX:
			#self.ser = serial.Serial('/dev/ttyACM1', 115200)
			# WIN:
			self.ser = serial.Serial('COM8', 115200)
		elif (mode == 2):
			self.ip = ip
			self.port = port
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

			
		self.buttons = {}
		self.labels = {}
		self.scales = {}
		self.spinboxs = {}
		
		self.minxz = 03
		self.maxxz = 24
		self.miny = -3
		self.maxy = 15
		
		self.autoUpdateVar = IntVar()
		self.autoUpdateVar.set(0)
		
		self.leg_RFx = IntVar()
		self.leg_RFx.set(15)
		self.leg_RFy = IntVar()
		self.leg_RFy.set(6)
		self.leg_RFz = IntVar()
		self.leg_RFz.set(15)
		
		self.leg_LFx = IntVar()
		self.leg_LFx.set(15)
		self.leg_LFy = IntVar()
		self.leg_LFy.set(6)
		self.leg_LFz = IntVar()
		self.leg_LFz.set(15)
		
		self.leg_LBx = IntVar()
		self.leg_LBx.set(15)
		self.leg_LBy = IntVar()
		self.leg_LBy.set(6)
		self.leg_LBz = IntVar()
		self.leg_LBz.set(15)
		
		self.leg_RBx = IntVar()
		self.leg_RBx.set(15)
		self.leg_RBy = IntVar()
		self.leg_RBy.set(6)
		self.leg_RBz= IntVar()
		self.leg_RBz.set(15)
		
		
		self.initElements()
		
		
		self.leg_LFx.trace("w", self.update_pos)
		self.leg_LFy.trace("w", self.update_pos)
		self.leg_LFz.trace("w", self.update_pos)
		self.leg_RFx.trace("w", self.update_pos)
		self.leg_RFy.trace("w", self.update_pos)
		self.leg_RFz.trace("w", self.update_pos)
		self.leg_LBx.trace("w", self.update_pos)
		self.leg_LBy.trace("w", self.update_pos)
		self.leg_LBz.trace("w", self.update_pos)				
		self.leg_RBx.trace("w", self.update_pos)
		self.leg_RBy.trace("w", self.update_pos)
		self.leg_RBz.trace("w", self.update_pos)
		self.autoUpdateVar.trace("w", self.setAutoU)

		

		self.root.focus_set()
		self.root.mainloop()


	def initElements(self):

	
		# ------ Scales ------
		
		# LF
		sc_lfz = Scale(self.root, variable=self.leg_LFz, to=self.minxz, from_=self.maxxz, repeatdelay=1, showvalue=0)
		sc_lfz.place(x=0, y=70)
		self.scales['sc_lfz'] = sc_lfz
		
		sc_lfx = Scale(self.root, variable=self.leg_LFx, to=self.minxz, from_=self.maxxz, repeatdelay=1, showvalue=0, orient=HORIZONTAL,length=150)
		sc_lfx.place(x=0, y=225)
		self.scales['sc_lfx'] = sc_lfx
		
		sc_lfy = Scale(self.root, variable=self.leg_LFy, to=self.miny, from_=self.maxy, repeatdelay=1, showvalue=0)
		sc_lfy.place(x=170, y=70)
		self.scales['sc_lfy'] = sc_lfy
		
		# RF
		sc_rfz = Scale(self.root, variable=self.leg_RFz, to=self.minxz, from_=self.maxxz, repeatdelay=1, showvalue=0)
		sc_rfz.place(x=680, y=70)
		self.scales['sc_rfz'] = sc_rfz
		
		sc_rfx = Scale(self.root, variable=self.leg_RFx, from_=self.minxz, to=self.maxxz, repeatdelay=1, showvalue=0, orient=HORIZONTAL,length=150)
		sc_rfx.place(x=680, y=225)
		self.scales['sc_rfx'] = sc_rfx
		
		sc_rfy = Scale(self.root, variable=self.leg_RFy, to=self.miny, from_=self.maxy, repeatdelay=1, showvalue=0)
		sc_rfy.place(x=850, y=70)
		self.scales['sc_rfy'] = sc_rfy
		
		# LB
		sc_lbz = Scale(self.root, variable=self.leg_LBz, from_=self.minxz, to=self.maxxz, repeatdelay=1, showvalue=0)
		sc_lbz.place(x=0, y=320)
		self.scales['sc_lbz'] = sc_lbz
		
		sc_lbx = Scale(self.root, variable=self.leg_LBx, to=self.minxz, from_=self.maxxz, repeatdelay=1, showvalue=0, orient=HORIZONTAL,length=150)
		sc_lbx.place(x=0, y=475)
		self.scales['sc_lbx'] = sc_lbx
		
		sc_lby = Scale(self.root, variable=self.leg_LBy, to=self.miny, from_=self.maxy, repeatdelay=1, showvalue=0)
		sc_lby.place(x=170, y=320)
		self.scales['sc_lby'] = sc_lby
		
		# RB
		sc_rbz = Scale(self.root, variable=self.leg_RBz, from_=self.minxz, to=self.maxxz, repeatdelay=1, showvalue=0)
		sc_rbz.place(x=680, y=320)
		self.scales['sc_rbz'] = sc_rbz
		
		sc_rbx = Scale(self.root, variable=self.leg_RBx, from_=self.minxz, to=self.maxxz, repeatdelay=1, showvalue=0, orient=HORIZONTAL,length=150)
		sc_rbx.place(x=680, y=475)
		self.scales['sc_rbx'] = sc_rbx
		
		sc_rby = Scale(self.root, variable=self.leg_RBy, to=self.miny, from_=self.maxy, repeatdelay=1, showvalue=0)
		sc_rby.place(x=850, y=320)
		self.scales['sc_rby'] = sc_rby

		# ------ Spin Box ------
		# LF
		sp_lfz = Spinbox(self.root, from_=self.minxz, to=self.maxxz, repeatdelay=1, width=10, textvariable=self.leg_LFz)
		sp_lfz.place(x=0, y=180)
		self.spinboxs['sp_lfz'] = sp_lfz
		
		sp_lfx = Spinbox(self.root, from_=self.minxz, to=self.maxxz, repeatdelay=1, width=10, textvariable=self.leg_LFx)
		sp_lfx.place(x=170, y=225)
		self.spinboxs['sp_lfx'] = sp_lfx
		
		sp_lfy = Spinbox(self.root, from_=self.minxz, to=self.maxxz, repeatdelay=1, width=10, textvariable=self.leg_LFy)
		sp_lfy.place(x=170, y=180)
		self.spinboxs['sp_lfy'] = sp_lfy
		
		# RF
		sp_rfz = Spinbox(self.root, from_=self.minxz, to=self.maxxz, repeatdelay=1, width=10, textvariable=self.leg_RFz)
		sp_rfz.place(x=680, y=180)
		self.spinboxs['sp_rfz'] = sp_rfz
		
		sp_rfx = Spinbox(self.root, from_=self.minxz, to=self.maxxz, repeatdelay=1, width=10, textvariable=self.leg_RFx)
		sp_rfx.place(x=850, y=225)
		self.spinboxs['sp_rfx'] = sp_rfx
		
		sp_rfy = Spinbox(self.root, from_=self.minxz, to=self.maxxz, repeatdelay=1, width=10, textvariable=self.leg_RFy)
		sp_rfy.place(x=850, y=180)
		self.spinboxs['sp_rfy'] = sp_rfy
		
		# LB
		sp_lbz = Spinbox(self.root, from_=self.minxz, to=self.maxxz, repeatdelay=1, width=10, textvariable=self.leg_LBz)
		sp_lbz.place(x=0, y=430)
		self.spinboxs['sp_lbz'] = sp_lbz
		
		sp_lbx = Spinbox(self.root, from_=self.minxz, to=self.maxxz, repeatdelay=1, width=10, textvariable=self.leg_LBx)
		sp_lbx.place(x=170, y=475)
		self.spinboxs['sp_lbx'] = sp_lbx
		
		sp_lby = Spinbox(self.root, from_=self.minxz, to=self.maxxz, repeatdelay=1, width=10, textvariable=self.leg_LBy)
		sp_lby.place(x=170, y=430)
		self.spinboxs['sp_lby'] = sp_lby
		
		# RB
		sp_rbz = Spinbox(self.root, from_=self.minxz, to=self.maxxz, repeatdelay=1, width=10, textvariable=self.leg_RBz)
		sp_rbz.place(x=680, y=430)
		self.spinboxs['sp_rbz'] = sp_rbz
		
		sp_rbx = Spinbox(self.root, from_=self.minxz, to=self.maxxz, repeatdelay=1, width=10, textvariable=self.leg_RBx)
		sp_rbx.place(x=850, y=475)
		self.spinboxs['sp_rbx'] = sp_rbx
		
		sp_rby = Spinbox(self.root, from_=self.minxz, to=self.maxxz, repeatdelay=1, width=10, textvariable=self.leg_RBy)
		sp_rby.place(x=850, y=430)
		self.spinboxs['sp_rby'] = sp_rby

		# ------ Labels ------
		# LF
		lf = Label(self.root, text="LF", relief=GROOVE, fg="black")
		lf.place(x=10,y=10)
		lf_z = Label(self.root, text="Z:", fg="black")
		lf_z.place(x=0,y=45)
		lf_x = Label(self.root, text="X:", fg="black")
		lf_x.place(x=0,y=205)
		lf_y = Label(self.root, text="Y:", fg="black")
		lf_y.place(x=170,y=45)
		# RF
		rf = Label(self.root, text="RF", relief=GROOVE, fg="black")
		rf.place(x=680,y=10)
		rf_z = Label(self.root, text="Z:", fg="black")
		rf_z.place(x=680,y=45)
		rf_x = Label(self.root, text="X:", fg="black")
		rf_x.place(x=680,y=205)
		rf_y = Label(self.root, text="Y:", fg="black")
		rf_y.place(x=850,y=45)
		# LB
		lb = Label(self.root, text="LB", relief=GROOVE, fg="black")
		lb.place(x=10,y=270)
		lb_z = Label(self.root, text="Z:", fg="black")
		lb_z.place(x=0,y=295)
		lb_x = Label(self.root, text="X:", fg="black")
		lb_x.place(x=0,y=455)
		lb_y = Label(self.root, text="Y:", fg="black")
		lb_y.place(x=170,y=295)
		# RB
		rb = Label(self.root, text="RB", relief=GROOVE, fg="black")
		rb.place(x=680,y=270)
		rb_z = Label(self.root, text="Z:", fg="black")
		rb_z.place(x=680,y=295)
		rb_x = Label(self.root, text="X:", fg="black")
		rb_x.place(x=680,y=455)
		rb_y = Label(self.root, text="Y:", fg="black")
		rb_y.place(x=850,y=295)
		
		
		# ------ Canvas ------
		
		
		self.canv_pos = Canvas(self.root, bg="gray80", height=400, width=400)
		self.canv_pos.place(x=250, y=0)
		
		self.canv_Body = Canvas(self.root, bg="gray50", height=100, width=100)
		self.canv_Body.place(x=400, y=150)
		
		# LF
		x = 150-(self.leg_LFx.get()/float(self.maxxz))*150
		z = 150-(self.leg_LFz.get()/float(self.maxxz))*150
		self.point_lf = self.canv_pos.create_oval(x, z, x+10, z+10, fill="red")
		self.line_lf = self.canv_pos.create_line(150, 150, x+5, z+5, fill="red")
		# RF
		x = 250+(self.leg_RFx.get()/float(self.maxxz))*150
		z = 150-(self.leg_RFz.get()/float(self.maxxz))*150
		self.point_rf = self.canv_pos.create_oval(x, z, x+10, z+10, fill="red")
		self.line_rf = self.canv_pos.create_line(250, 150, x+5, z+5, fill="red")
		# LB
		x = 150-(self.leg_LBx.get()/float(self.maxxz))*150
		z = 250+(self.leg_LBz.get()/float(self.maxxz))*150
		self.point_lb = self.canv_pos.create_oval(x, z, x+10, z+10, fill="red")
		self.line_lb = self.canv_pos.create_line(150, 250, x+5, z+5, fill="red")
		# RB
		x = 250+(self.leg_RBx.get()/float(self.maxxz))*150
		z = 250+(self.leg_RBz.get()/float(self.maxxz))*150
		self.point_rb = self.canv_pos.create_oval(x, z, x+10, z+10, fill="red")
		self.line_rb = self.canv_pos.create_line(250, 250, x+5, z+5, fill="red")
		
		
		
		# ------ Buttons ------
		
		action_with_arg = partial(self.send_pos, (None))
		self.buttons['update'] = Button(self.root, text="update", height=2, width=15, bg="gray80", command=action_with_arg)
		self.buttons['update'].place(x=400, y=450)
		
		self.buttons['autoUpdate'] = Checkbutton(self.root, text="Auto update", variable=self.autoUpdateVar, onvalue=1, offvalue=0)
		self.buttons['autoUpdate'].place(x=400, y=413)


	def update_pos(self, *args):
		possI = [self.leg_RFx.get(),self.leg_RFy.get(),self.leg_RFz.get(),
					self.leg_LFx.get(),self.leg_LFy.get(),self.leg_LFz.get(),
					self.leg_RBx.get(),self.leg_RBy.get(),self.leg_RBz.get(),
					self.leg_LBx.get(),self.leg_LBy.get(),self.leg_LBz.get()]
			
		for i in range(12):
			if not isinstance(possI[i], int):
				self.possI = None
				break
			
		if possI != None:
			#LF
			x = 150-(self.leg_LFx.get()/float(self.maxxz))*150
			z = 150-(self.leg_LFz.get()/float(self.maxxz))*150
			self.canv_pos.coords(self.point_lf, (x,z,x+10,z+10))
			self.canv_pos.coords(self.line_lf, (150, 150, x+5, z+5))
			#RF
			x = 250+(self.leg_RFx.get()/float(self.maxxz))*150
			z = 150-(self.leg_RFz.get()/float(self.maxxz))*150
			self.canv_pos.coords(self.point_rf, (x, z, x+10, z+10))
			self.canv_pos.coords(self.line_rf,(250, 150, x+5, z+5))
			# LB
			x = 150-(self.leg_LBx.get()/float(self.maxxz))*150
			z = 250+(self.leg_LBz.get()/float(self.maxxz))*150
			self.canv_pos.coords(self.point_lb, (x, z, x+10, z+10))
			self.canv_pos.coords(self.line_lb, (150, 250, x+5, z+5))
			# RB
			x = 250+(self.leg_RBx.get()/float(self.maxxz))*150
			z = 250+(self.leg_RBz.get()/float(self.maxxz))*150
			self.canv_pos.coords(self.point_rb, (x, z, x+10, z+10))
			self.canv_pos.coords(self.line_rb, (250, 250, x+5, z+5))
			
			if (self.autoUpdateVar.get() == 1):
				self.send_pos(possI)
		
		
	
	def setAutoU(self, *args):
		if (self.autoUpdateVar.get() == 0):
			self.buttons["update"].config(state="normal")
		else:
			self.buttons["update"].config(state="disabled")
	
	
	def send_pos(self, *args):
		
		if(args[0] == None):
		
			possI = [self.leg_RFx.get(),self.leg_RFy.get(),self.leg_RFz.get(),
					self.leg_LFx.get(),self.leg_LFy.get(),self.leg_LFz.get(),
					self.leg_RBx.get(),self.leg_RBy.get(),self.leg_RBz.get(),
					self.leg_LBx.get(),self.leg_LBy.get(),self.leg_LBz.get()]
		
			for i in range(12):
				if not isinstance(possI[i], int):
					possI = None
					break
		else:
			possI = args[0]
		
		if possI != None:
			
			possS = []
			msg = ""
			for i in range(12):
				ii = possI[i]
				ss = ""
				
				if (ii>=0):
					ss=ss+"+"
				elif (ii<0):
					ss=ss+"-"
				
				if(abs(ii) < 10):
					ss=ss+"0"
				
				ss=ss+str(abs(ii))
				possS.append(ss)
				msg = msg+ss
			
			
			print msg
			if (self.mode == 1):
				self.ser.write("s" + msg + ";")
			elif (self.mode == 2):
				self.sock.sendto('s'+msg+';', (self.ip, self.port))

	

if (__name__ == "__main__"):
	if len(sys.argv) == 1:
		print '"leg-controller.py [serial / udp]"'
		w1 = W1()
	else:

		if (sys.argv[1] == "serial"):
			w1 = W1(1)
		elif (sys.argv[1] == "udp"):
			w1 = W1(2)

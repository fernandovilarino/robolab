from Tkinter import *
import time
import threading


class W1:
	
	def __init__(self):
		self.root = Tk()
		self.root.geometry("400x300")
		self.coord = 10,50,140,110
		
		self.buttons = {}
		self.labels = {}
		self.initElements()
		
		self.root.mainloop()

	def runFill(self):
		for i in range(360):
			print i
			self.canv.delete("all")
			self.arc = self.canv.create_arc(self.coord, start=90,extent=i, fill="black")
			time.sleep(0.02)

	def runChangeS1(self):
		while True:
			pos = self.scale1.get()
			if(pos != self.S1Val):
				self.S1Val = pos
				self.canv.delete("all")
				self.arc = self.canv.create_arc(self.coord, start=90,extent=pos, fill="black")

				print pos
			time.sleep(0.005)


	def initElements(self):
		
		# ------ Buttons ------
		fill = Button(self.root, text="fill", command=self.fill)
		fill.place(x=0, y=50)
		self.buttons['fill'] = fill

		clr = Button(self.root, text="clear", command=self.clr)
		clr.place(x=50, y=50)
		self.buttons['clr'] = clr

		# ------ Scales ------
		self.S1Val = 0
		var = DoubleVar()
		self.scale1 = Scale(self.root, variable=var, from_=0, to=359, tickinterval=90)
		self.scale1.place(x=0, y=100)
		t=threading.Thread(target=self.runChangeS1)
		t.start()

		# ------ Labels ------
		top = Label(self.root, text="top")
		top.place(x=10,y=10)
		self.labels['top'] = top

		# ------ Canvas ------
		self.canv = Canvas(self.root, bg="red", height=200, width=200)
		self.canv.place(x=200, y=0)
		self.arc = self.canv.create_arc(self.coord, start=0,extent=150, fill="white")
		#self.canv.pack()
		self.canv.place(x=200, y=0)
	

	def fill(self):
		print 'fill'
		t=threading.Thread(target=self.runFill)
		t.start()

	def clr(self):
		print 'clear'
		self.canv.delete("all")



		
if __name__ == "__main__":
	w1 = W1()

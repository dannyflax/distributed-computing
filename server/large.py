##
import asyncore
import socket
import Tkinter
import threading
from decimal import Decimal
import time
import math

class simpleapp_tk(Tkinter.Tk):



	def __init__(self,parent):
		Tkinter.Tk.__init__(self,parent)
		self.parent = parent
		self.initialize()

	def initialize(self):
		self.grid()
		self.button = Tkinter.Button(self,text="Click me!",command=self.OnButtonClick)
		self.button.grid(column=1,row=0)
		self.label = Tkinter.Label(self,text="")
		self.label.grid(column=2,row=0)
		self.server = EchoServer('10.186.105.175', 8080)

	def OnButtonClick(self):
		print "Starting server..."
		self.thread1 = threading.Thread(target=self.workerThread1)
		self.thread1.start() 

		self.t2_stop = threading.Event()
		self.thread2 = threading.Thread(target=self.serverCheckThread, args=(1,self.t2_stop))
		self.thread2.start()

		self.button.configure(text = "Calculate", command=self.calculate)


	def workerThread1(self):
		asyncore.loop()

	def serverCheckThread(self,a,t2_stop):
		while not t2_stop.is_set():
			self.label.configure(text="%d connections"%(self.server.connections)) 
			if self.server.calculating:
				self.button.configure(text = "Stop Calculating", command=self.stopCalculating)
			else:
				self.button.configure(text = "Calculate", command=self.calculate)
			time.sleep(1)



	def onClosing(self):
		print "Closing server"
		self.t2_stop.set()
		asyncore.close_all()
		self.destroy()

	def calculate(self):
		print "Beginning calculations..."
		#self.server.startCalculating()
		self.server.distributeCalculations();

	def stopCalculating(self):
		self.server.stopCalculating()


class EchoHandler(asyncore.dispatcher_with_send):
	def __init__(self, sock, server):
		asyncore.dispatcher_with_send.__init__(self,sock)
		self.server = server

	def handle_read(self):
		data = self.recv(4092)
		if self.calculating:
			self.server.handlerFinishedCalculating(self,data)
		
	def handle_close(self):
		self.server.handlerDisconnected(self)
		self.close()


class EchoServer(asyncore.dispatcher):

	def __init__(self, host, port):
		asyncore.dispatcher.__init__(self)
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.set_reuse_addr()
		self.bind((host, port))
		self.listen(5)
		self.seriesRange = 10000						# the "n" argument in the geometric series
		self.connections = 0												# amount of devices connected to server
		self.connectionHandlers = []
		self.calculating = False
		self.calcResult = 0
		self.startTime = time.time()
		self.numberToCheck = 1000001

	def handle_accept(self):
		pair = self.accept()
		if pair is not None:
			sock, addr = pair
			print 'Incoming connection from %s.' % repr(addr)
			handler = EchoHandler(sock,self)
			handler.address = addr
			handler.calculating = False
			handler.closed = False
			self.connectionHandlers.append(handler)
			self.connections = self.connections + 1

	def distributeCalculations(self):
		self.startTime = time.time()
		self.calcResult = 1
		self.calcNumber = 0
		self.calculating = True

		if(True):
			# This distribution gives rotating assignments of n
			if self.connections > 0:
				for x in range(0, len(self.connectionHandlers)):
					self.connectionHandlers[x].send(str(x) + ":" + str(self.connections) + ":" + str(int(math.sqrt(self.numberToCheck)))+"\n")
					self.connectionHandlers[x].calculating = True
			else:
				#Compute
				for x in range(0, self.seriesRange + 1):
					self.calcResult = self.calcResult + 1
				self.calcFinished()

		# This distribution gives consecutive ranges

		# 	increment = self.seriesRange / len(self.connectionHandlers)
		# 	modResult = self.seriesRange % len(self.connectionHandlers)

		# 	distributedCount = 0
		# 	counter = 0

		# 	while(distributedCount < self.seriesRange):
		# 		increase = increment
		# 		if(counter < modResult):
		# 			increase = increase + 1

		# 		lowerHalf = distributedCount
		# 		if(distributedCount != 0):
		# 			lowerHalf = lowerHalf + 1

		# 		self.connectionHandlers[counter].calculating = True
		# 		self.connectionHandlers[counter].send(str(lowerHalf) + ":" + str(distributedCount + increase))
		# 		print str(lowerHalf) + ":" + str(distributedCount + increase)
		# 		distributedCount += increase
		# 		counter = counter + 1
		print "Device tasks assigned..."



	def stopCalculating(self):
		self.calculating = False
		for handler in self.connectionHandlers:
			handler.calculating = False
			handler.send("STOP\n")

	def handlerDisconnected(self,handler):
		self.connectionHandlers.remove(handler)
		self.connections = self.connections - 1

	def handlerFinishedCalculating(self,handler,data):
		self.calcNumber = self.calcNumber + 1
		handler.calculating = False

		try:
			result = Decimal(data)
		except:
			print "Failure to parse device output."
		
		if result == 0:
			self.calcResult = 0
			self.stopCalculating()
			self.calcFinished()

		if self.calcNumber == self.connections:
			self.calcResult = self.numberToCheck
			self.calcFinished()
			
	def calcFinished(self):
		self.calculating = False
		print "Result: "
		print self.calcResult
		print "Time Elapsed: "
		print time.time() - self.startTime

if __name__ == "__main__":
	app = simpleapp_tk(None)
	app.title('my application')
	app.protocol("WM_DELETE_WINDOW", app.onClosing)
	app.mainloop()
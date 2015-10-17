import asyncore
import socket
import Tkinter
import threading
from decimal import Decimal
import time

class App():
	def __init__(self):
		self.initialise()

	def initialise(self):
		self.server = EchoServer('10.186.38.214', 8080)
		self.initialiseThread()
		self.action = False;

	def initialiseThread(self):
		print "Starting server connection..."
		self.thredOne = threading.Thread(target=self.workerThreadOne)
		self.thredOne.start()

		self.t2_stop = threading.Event()
		self.thread2 = threading.Thread(target=self.serverCheckThread, args=(1,self.t2_stop))
		self.thread2.start()

	def workerThreadOne(self):
		asyncore.loop()

	def serverCheckThread(self,a,t2_stop):
		while not t2_stop.is_set():
			if self.server.calculating:
				#print ("Number of connections ",self.server.connections)
				x = raw_input("Stop Calculating ?")
				if(x == 'yes'):
					self.stopCalculating()
			else:
				print ("Number of connections ",(self.server.connections))
				x = raw_input("Start Calculating ?")
				if(x == 'yes'):
					self.calculate()
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

	# DEPRECATED
	def startCalculating(self):
		if(self.connections > 0):
			self.calcNumber = 0
			self.calculating = True
			for handler in self.connectionHandlers:
				handler.calculating = True
				handler.send("hey")
		else:
			self.calcFinished()

	def distributeCalculations(self):

		self.startTime = time.time()
		self.calcResult = 0
		self.calcNumber = 0
		self.calculating = True

		if(True):
			# This distribution gives rotating assignments of n
			if self.connections > 0:
				for x in range(0, len(self.connectionHandlers)):
					self.connectionHandlers[x].send(str(x) + ":" + str(len(self.connectionHandlers)) + ":" + str(self.seriesRange)+"\n")
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

	def handlerDisconnected(self,handler):
		self.connectionHandlers.remove(handler)
		self.connections = self.connections - 1

	def handlerFinishedCalculating(self,handler,data):
		self.calcNumber = self.calcNumber + 1
		handler.calculating = False

		# Check to see if the data is a valid decimal

		try:
			castedData = Decimal(data)
			self.calcResult = self.calcResult + Decimal(data)
		except:
			print "Failure to parse device output."
		
		
		if self.calcNumber == self.connections:
			self.calcFinished()
			
	def calcFinished(self):
		self.calculating = False
		print "Result: "
		print self.calcResult
		print "Time Elapsed: "
		print time.time() - self.startTime

if __name__ == "__main__":
	app = App()

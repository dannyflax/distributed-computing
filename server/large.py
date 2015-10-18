##
import asyncore
import socket
import threading
from decimal import Decimal
import time
import math
import string

class App():

	def __init__(self):
		self.initialize()

	def initialize(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect(("gmail.com",80))
		ip = s.getsockname()[0]
		s.close()
		self.server = EchoServer(ip, 8080)

		self.action = False

		self.initialiseThread()

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
					self.server.numberToCheck = self.server.baseNumber
			else:
				print ("Number of connections ",(self.server.connections))
				x = raw_input("Start Calculating ?")
				if(x == 'yes'):
					self.calculate()
				elif(x == 'quit'):
					self.onClosing()
			time.sleep(1)

	def onClosing(self):
		print "Closing server"
		self.t2_stop.set()
		asyncore.close_all()

	def calculate(self):
		print "Beginning calculations..."
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
			dataChunks = string.split(data,"\n")
			if len(dataChunks) > 2:
				for i in range(0,len(dataChunks)-1):
					self.server.handlerFinishedCalculating(self,dataChunks[i])	
			else:
				self.server.handlerFinishedCalculating(self,dataChunks[0])
		
	def handle_close(self):
		self.server.handlerDisconnected(self)
		self.close()
		self.server.stopCalculating()
		self.server.distributeCalculations()


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
		self.baseNumber = 49573400000
		self.numberToCheck = self.baseNumber

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
		if self.calculating:
			self.server.stopCalculating()
			self.server.distributeCalculations()

	def distributeCalculations(self):
		self.startTime = time.time()
		self.calcResult = 1
		self.calcNumber = 0
		self.calculating = True

		if(True):
			# This distribution gives rotating assignments of n
			if self.connections > 0:
				for x in range(0, self.connections):
					self.connectionHandlers[x].send(str(x+2) + ":" + str(self.connections) + ":" + str(self.numberToCheck)+"\n")
					self.connectionHandlers[x].calculating = True
			else:
				#Compute
				
				while self.calculating:
					isPrime = True

					x = 2
					while isPrime and x <= int(math.sqrt(self.numberToCheck)):
						isPrime = (self.numberToCheck%x != 0)	
						x += 1

					if isPrime:
						print self.numberToCheck
					self.numberToCheck = self.numberToCheck + 1

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
		# print "Device tasks assigned..."



	def stopCalculating(self):
		self.calculating = False
		for handler in self.connectionHandlers:
			handler.calculating = False

	def handlerDisconnected(self,handler):
		print handler
		self.connectionHandlers.remove(handler)
		self.connections = self.connections - 1

	def handlerFinishedCalculating(self,handler,data):
		# print "DATAAA"+data
		

		inputD = string.split(data,":")

		num = inputD[0]
		result = inputD[1]

		if int(num) == self.numberToCheck:
			self.calcNumber = self.calcNumber + 1
			handler.calculating = False

			try:
				result = Decimal(result)
			except:
				print "Failure to parse device output."
			
			if result == 0:
				# print "MOVED ON FROM COMPOSITE"
				self.calcResult = 0
				self.stopCalculating()
				self.calcFinished()
			else:
				if self.calcNumber == self.connections:
					# print "MOVED ON FROM PRIME"
					self.calcResult = self.numberToCheck
					self.calcFinished()
			
	def calcFinished(self):
		self.calculating = False
		if not self.calcResult == 0:
			print "Result: "
			print self.calcResult
			print "Time Elapsed: "
			print time.time() - self.startTime
		
		self.numberToCheck = self.numberToCheck + 1
		self.distributeCalculations()

if __name__ == "__main__":
	app = App()

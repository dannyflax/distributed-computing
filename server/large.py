##
import asyncore
import socket
import Tkinter
import threading
import time

class simpleapp_tk(Tkinter.Tk):



    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()
        self.button = Tkinter.Button(self,text="Click me !",command=self.OnButtonClick)
        self.button.grid(column=1,row=0)
        self.label = Tkinter.Label(self,text="")
        self.label.grid(column=2,row=0)
        self.server = EchoServer('localhost', 8080)

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
        print "gonna calculate eventually"
        #self.server.startCalculating()
        self.server.distributeCalculations();

    def stopCalculating(self):
        self.server.stopCalculating()


class EchoHandler(asyncore.dispatcher_with_send):
    def __init__(self, sock, server):
        asyncore.dispatcher_with_send.__init__(self,sock)
        self.server = server

    def handle_read(self):
        data = self.recv(8192)
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
        self.seriesRange = 100000											# the "n" argument in the geometric series
        self.connections = 0												# amount of devices connected to server
        self.connectionHandlers = []
        self.calculating = False
        self.calcResult = 0

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            print 'Incoming connection from %s' % repr(addr)
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
    	if(self.connections > 0):
    		self.calcNumber = 0
    		self.calculating = True

    		increment = self.seriesRange / len(self.connectionHandlers)
    		modResult = self.seriesRange % len(self.connectionHandlers)

    		distributedCount = 0
    		counter = 0
    		#for(i = 0; distributedCount < self.seriesRange; i++):
    		while(distributedCount < self.seriesRange):
    			increase = increment
    			if(i < modResult):
    				increase = increase + 1
    			self.connectionHandlers(counter).calculating = True
    			self.connectionHandlers(counter).send(str(distributedCount) + ":" + str(distributedCount + increase))
    			distributedCount += increase
    	else:
    		self.calcFinished()



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
        self.calcResult = self.calcResult + int(data)
        if self.calcNumber == self.connections:
            self.calcFinished()
            
    def calcFinished(self):
        self.calculating = False
        print "Result: "
        print self.calcResult

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('my application')
    app.protocol("WM_DELETE_WINDOW", app.onClosing)
    app.mainloop()
   
    


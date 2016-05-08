import time
import sys
import random
import Queue
import multiprocessing as multi



class VirtualMachine(object):

	def __init__(self, iden, messageQueue):
		self.id = iden
		self.messageQueue = messageQueue
		self.m1Q = None
		self.m2Q = None

		self.lClock = 1
		self.messages = []
		self.clockSpeed = None

	def executionLoop(self):

		infiniteLoop = True
		while(infiniteLoop):

			#get starting time
			startTime = time.time()

			#logic in assignment task
			if (self.messages):
				msgFromQ = self.messages.pop(0)
				self.lClock = max(msgFromQ, self.lClock) + 1
				self.logThis("got message. additional messages: " + str(len(self.messages)))
			else:
				num = random.randint(1, 10)
				if(num == 1):
					self.m1Q.put(self.lClock)
					self.logThis("sent message to 1")
				elif (num == 2):
					self.m2Q.put(self.lClock)
					self.logThis("sent message to 2")
				elif (num == 3):
					self.m1Q.put(self.lClock)
					self.m2Q.put(self.lClock)
					self.logThis("sent message to both")
				else:
					self.logThis("internal event")

				self.lClock += 1

			while self.clockSpeed > (time.time() - startTime):
				try:
					timeFromStart = time.time() - startTime
					timeout = self.clockSpeed - timeFromStart
					msgFromQ = self.messageQueue.get(True, timeout)
					self.messages.append(msgFromQ)
				except Queue.Empty:
					break

	def logThis(self, info):
		print self.id + " | time: " + str(time.time()) + ", clockValue:" + str(self.lClock) + "  " + info
        sys.stdout.flush()

if __name__ == "__main__":
	
	#number of VMs
	numVM = 3

	#create network queues
	qArray = [multi.Queue() for x in xrange(numVM)]

	#create virtual machines
	vmArray = [VirtualMachine("vm" + str(x), qArray[x]) for x in xrange(numVM)]

	#connect each machine to the other two. could be done better
	vmArray[0].m1Q = qArray[1]
	vmArray[0].m2Q = qArray[2]

	vmArray[1].m1Q = qArray[0]
	vmArray[1].m2Q = qArray[2]

	vmArray[2].m1Q = qArray[0]
	vmArray[2].m2Q = qArray[1]
	
	#assign random clock speeds from 1-6
	for x in vmArray:
		x.clockSpeed = random.randint(1, 6)
	
	#run things
	pArray = [multi.Process(target = x.executionLoop) for x in vmArray]
	for x in pArray:
		x.start()

	#wait
	time.sleep(60)

	#kill processes
	for x in pArray:
		x.terminate()

	for x in pArray:
		x.join()




from lettuce import *
import json
import jsocket
import logging

convert = lambda s : json.loads(s)

logger = logging.getLogger("jsocket")
logger.setLevel(logging.CRITICAL)

class MyServer(jsocket.ThreadedServer):
	def __init__(self):
		super(MyServer, self).__init__()
		self.timeout = 2.0
		self.isConnected = False 
	
	def _process_message(self, obj):
		""" virtual method """
		if obj != '':
			if obj['message'] == "new connection":
				self.isConnected = True
	
	def isAlive(self):
		return self._isAlive

@step('I start the server')
def startTheServer(step):
	world.jsonserver = MyServer()
	world.jsonserver.start()
	
@step('I stop the server')
def stopTheServer(step):
	world.jsonserver.stop()
	
@step('I close the client')
def stopTheCLient(step):
	world.jsonclient.close()

@step('I connect the client')
def startTheClient(step):
	world.jsonclient = jsocket.JsonClient()
	world.jsonclient.connect()
	
@step('the client sends the object (\{.*\})')
def clientSendsObject(step, obj):
	world.jsonclient.send_obj(convert(obj))
	
@step('the server sends the object (\{.*\})')
def serverSendsObject(step, obj):
	world.jsonserver.send_obj(convert(obj))

@step('the client sees a message (\{.*\})')
def clientMessage(step, obj):
	msg = world.jsonclient.read_obj()
	assert msg == convert(obj), "%d" % convert(obj)

@step('I see a connection')
def checkConnection(step):
	expected = True
	assert world.jsonserver.isConnected == expected, "%d" % False
	
@step('I see a stopped server')
def checkServerStopped(step):
	expected = False
	assert world.jsonserver.isAlive() == expected, "%d" % False
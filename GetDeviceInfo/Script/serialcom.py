import serial
import array
from time import sleep

class SerialConnection():
    def __init__(self, port, baudrate = 38400):#, logger = ""
        self.name = port
		#self.logger = logger
        self.ser = serial.Serial(port=port)
        self.ser.baudrate = baudrate
        self.ser.timeout = None     # wait forever
        
    def __str__(self):
        return "COM:%s" % self.name
        
    def getName(self):
        return self.name

    def clear(self):
        self.ser.flushInput()
        
    def setTesterMode(self, mode):
        #self.logger.warn('SerialConnection.setTesterMode() is not implemented! mode = %s' % mode)
        pass
        
    def setTimeout(self, timeout):
        self.ser.timeout = float(timeout) / 1000.0
        
    def sendBuffer(self, buffer):
		data = array.array('B', buffer).tostring()
		while self.ser.write(data) != len(data):
			data = data[len(data):]
 
 
    def receiveBuffer(self, length = 80):
        """Read the requested number of characters. If a timeout occurs
        Serial.read returns less characters, which we use to identify that
        this has happened. 
        
        In case of timeout we return an empty list (which implies that 
        characters read will be dropped if not enough characters were 
        eceived!)
        """
        data = self.ser.read(length)
        if len(data) != length:
            return []
        return [ord(c) for c in data] 	

    def readline(self):
		return self.ser.readline();
		


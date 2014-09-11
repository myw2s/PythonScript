from serialcom import *

port      = "COM25"
baudrate  = 38400

try:
	serialport = SerialConnection(port , baudrate)
except:
	print "Can not open " + port
	print "Please set COM number in serialConfig.py"
	raw_input()
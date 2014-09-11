from atCmd import *
from serialConfig import serialport
from datetime import datetime
import os

# Definition
SERIAL_TIMEOUT = 5000

# Log file directory
if not os.path.exists("log"):
   os.makedirs("log")
os.chdir("log")

# Log file name
logFileName = "log_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
if os.path.exists(logFileName):
   os.remove(logFileName)

logFile = open(logFileName, "w+")
logFile.write("=======================================================\n")
logFile.write("                      UART Rx Test                     \n")
logFile.write("-------------------------------------------------------\n")
#print '[UART RX Test]'

# Serial port timeout
serialport.setTimeout(SERIAL_TIMEOUT)

# Factory new the controller
print '[Factory New]'
isFN = 0
while(isFN == 0):
	serialport.sendBuffer('ATZ\r\n')
	fnResponse = serialport.readline()
	if fnResponse.startswith('$READY'):
		isFN = 1
	time.sleep(1)
print '[Done]'

#Create network
#sendCommand(serialport, createNwkCmd, channel=0x1A)
#time.sleep(1)

# Enable join
#sendCommand(serialport, joinEnableCmd, time=0xFF)
#isJoinEnabled = 1
#print '[Permit join enabled]'

packetId = 0
lastErrorPacketId = 0

errorCounts = 0

#atCommand='ATE0\r\n'
#atCommand='ATI2\r\n'
atCommand='AT$DNS\r\n'

for packetId in range(0, 1000):
	serialport.sendBuffer(atCommand)
#	print atCommand
	logFile.write(atCommand)

	# Log the echo from the controller
	echo = serialport.readline()
	print echo
	logFile.write(echo)

	response = serialport.readline()
	responseOK = serialport.readline()
	logMessage = '[' + str(packetId) + '] ' + response + responseOK
	print logMessage
	logFile.write(logMessage)

	if (response.startswith('ERROR')):
		errorCounts += 1
		logMessage = '[Error occurs after ' + str(packetId - lastErrorPacketId) + ' packets]\n'
		print logMessage
		lastErrorPacketId = packetId
		logFile.write(logMessage)

## Disable join
#sendCommand(serialport, joinEnableCmd, time=0x00)
#print '[Permit join disabled]'

# Print the test result
print 'Tried: ' + str(packetId + 1) + '\n'
print 'Error Counts: ' + str(errorCounts) + '\n'
logFile.write('Tried: ' + str(packetId + 1) + '\n')
logFile.write('Error Counts: ' + str(errorCounts) + '\n')
logFile.close()

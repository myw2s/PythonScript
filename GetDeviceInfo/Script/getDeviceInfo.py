from atCmd import *
from serialConfig import serialport
from datetime import datetime
import os

# Definition
PERMIT_JOIN_DURATION=0x1E
PERMIT_JOIN_NO_TIME_LIMIT=0xFF
PERMIT_JOIN_STOP=0x00
HA_PROFILE_ID=0x0104
ZLL_PROFILE_ID=0xC05E
DEFAULT_CHANNEL=0x1A

# Elapsed Time
def elapsedTime(start):
   dt = datetime.now() - start
   ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
   return ms

# Read attribute and save to file
def readAttribute(attrId):
	attrResp = sendCommandNoResponsePattern(serialport, remoteAttrReqCmd, shortAddr=int(nwkAddr,base=16), endPoint=int(epList[numOfEP], base=16), clusterId=0000, attrValue=attrId)
	attrStr = attrResp[0]
	startIndex = (attrStr.find('$ATTRRR:'))
	endIndex = (attrStr.find('\r\n'))
	if (startIndex != -1) and (endIndex != -1):
		# Record information
		attrStr = attrStr[(startIndex+12):endIndex]
		attrRespArray = attrStr.split(',')
		return attrRespArray[5]
	return '[Error: ' + attrStr + ']\n'

#Create network
sendCommand(serialport, createNwkCmd, channel=DEFAULT_CHANNEL)
time.sleep(1)

#Enable join
sendCommand(serialport, joinEnableCmd, time=PERMIT_JOIN_DURATION)

#Start time
start = datetime.now()
print '[Permit join enabled]'

#Set serial read timeout
serialport.setTimeout(10000)

# Log file
if not os.path.exists("log"):
   os.makedirs("log")

os.chdir("log")
if os.path.exists("deviceInfo.txt"):
   os.remove("deviceInfo.txt")

logFile = open("deviceInfo.txt", "w+")
logFile.write("=======================================================\n")
logFile.write("[Log created]\n" + datetime.now().strftime("%d %b %Y %H:%M:%S") + "\n")

#Join started
isStarted = 1
isJoined = 0
while(isStarted):
	duration = elapsedTime(start) / 1000 
	if (isJoined == 0) and (duration >= PERMIT_JOIN_DURATION):
		isStarted = 0
	resp = serialport.readline()
	print resp
	if resp:
		# Wait for device join
		if resp.startswith('$NEWDEVU:'):
			s, info = resp.split(':')
			nwkAddr, macAddr = info.split(',')
			acepResp = sendCommandNoResponsePattern(serialport, activeEndpointCmd, shortAddr = int(nwkAddr,base=16))

			# Request to leave
			isJoined = 1

			#Disable join
			sendCommand(serialport, joinEnableCmd, time=PERMIT_JOIN_STOP)
			print '[Permit join disabled]'
			
			# Active endpoint request
			acepStr = acepResp[0]
			startIndex = acepStr.find('$ACEP:')
			endIndex = acepStr.find('\r\n')

			if (startIndex != -1) and (endIndex != -1):
				acepStr = acepStr[(startIndex+6):endIndex]
				epList = acepStr.split(',')
				numOfEP = int(epList[0])
								
				if (numOfEP != 0):
					for numOfEP in range(1, numOfEP+1):
						logFile.write("\n[Endpoint 0x" + str(epList[numOfEP]) + "]\n")
						# Simple descriptor request
						sdrResp = sendCommandNoResponsePattern(serialport, simpleDescriptorCmd, shortAddr = int(nwkAddr,base=16), endPoint = int(epList[numOfEP], base=16))
						# Check simple descriptor response
						numOfResp = len(sdrResp)
						for numOfResp in range(0, numOfResp):
							sdrStr = sdrResp[numOfResp]
							#print sdrStr
							startIndex = (sdrStr.find('$SIMPLEDESC:'))
							endIndex = (sdrStr.find('\r\n'))
							if (startIndex != -1) and (endIndex != -1):
								# Record information
								sdrStr = sdrStr[(startIndex+12):endIndex]
								sdrStrArray = sdrStr.split(',')
								#print sdrStrArray
								# Binding
								profileID = int(sdrStrArray[1], base=16)
								if (profileID == HA_PROFILE_ID) or (profileID == ZLL_PROFILE_ID):
									# HA or ZLL
									numOfOutputCluster = int(sdrStrArray[4], base=16)
									#print numOfOutputCluster
									if (numOfOutputCluster != 0):
										for numOfOutputCluster in range(0, numOfOutputCluster):
											#print sdrStrArray[5 + numOfOutputCluster]
											if (sdrStrArray[5 + numOfOutputCluster] == '0000'):
												# Read basic attribute
												attr = readAttribute(int('0x0004', base=16))
												logFile.write("Manufacturer: " + attr + "\n")
												attr = readAttribute(int('0x0005', base=16))
												logFile.write("Model ID: " + attr + "\n")
												attr = readAttribute(int('0x0006', base=16))
												logFile.write("Date code: " + attr + "\n")
												attr = readAttribute(int('0x4000', base=16))
												logFile.write("Software build: " + attr + "\n")
												attr = readAttribute(int('0x8000', base=16))
												logFile.write("Serial Number: " + attr + "\n")
												attr = readAttribute(int('0x8001', base=16))
												logFile.write("MAC address: " + attr + "\n")
												attr = readAttribute(int('0x8002', base=16))
												logFile.write("Software version: " + attr + "\n")
												attr = readAttribute(int('0x8003', base=16))
												logFile.write("Hardware platform version: " + attr + "\n")
												attr = readAttribute(int('0x8004', base=16))
												logFile.write("Manufacturing date: " + attr + "\n")
												attr = readAttribute(int('0x8005', base=16))
												logFile.write("Manufacturing log: " + attr + "\n")
												attr = readAttribute(int('0x8006', base=16))
												logFile.write("Model name: " + attr + "\n")
										isStarted = 0
#Leave request
if (isJoined == 1):
	sendCommandNoResponsePattern(serialport, leaveNwkCmd, ExtAddr=macAddr)
#Disable join
sendCommand(serialport, joinEnableCmd, time=PERMIT_JOIN_STOP)
print '[Permit join disabled]'
#logFile.write("[Log Ended " + datetime.now().strftime("%d%b%Y %H:%M:%S") + "]\n")
logFile.write("=======================================================\n")
logFile.close()

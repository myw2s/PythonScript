from atCmd import *
from serialConfig import serialport
from datetime import datetime
from zigbeeDevice import *
from defines import *
from util import *

import os
import random

# Log file directory
if not os.path.exists("log"):
   os.makedirs("log")
os.chdir("log")

# Device list file name
if os.path.exists(DEVICE_LIST_FILENAME):
	os.remove(DEVICE_LIST_FILENAME)
devicelistFile = open(DEVICE_LIST_FILENAME, "w+")
	
# Log file name
logFileName = "log_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".txt"
if os.path.exists(logFileName):
   os.remove(logFileName)
   
logFile = open(logFileName, "w+")
logFile.write("=======================================================\n")
logFile.write("                Packet Error Rate Test                 \n")
logFile.write("-------------------------------------------------------\n")
logFile.write("Channel: " + str(DEFAULT_CHANNEL) + "\n")

# Set serial read time-out
serialport.setTimeout(SERIAL_PORT_TIMEOUT_ROUTER)

# Factory new the controller
print '[Factory New]'
isFN = 0
serialport.sendBuffer('ATZ\r\n')
while(isFN == 0):
	fnResponse = serialport.readline()
	if fnResponse.startswith('$READY'):
		isFN = 1
	time.sleep(1)
print '[Done]'

# Create network
sendCommand(serialport, createNwkCmd, channel=DEFAULT_CHANNEL)
time.sleep(1)

# Enable join
sendCommand(serialport, joinEnableCmd, time=PERMIT_JOIN_DURATION)
isJoinEnabled = 1
print '[Permit join enabled]'

# Start time
start = datetime.now()

# JoinedDevices
devices = []
joinedDevice = 0

while(isJoinEnabled):
	# Check if the duration is over the PERMIT_JOIN_DURATION
	duration = elapsedTime(start) / 1000 
	if (duration >= PERMIT_JOIN_DURATION):
		isJoinEnabled = 0

	response = serialport.readline()
	if response:
		# Print response from serial port
		print response
		
		# Wait for device join
		if response.startswith('$NEWDEVU:'):
			# Extract the short and MAC address
			dummy, info = response.split(':')
			shortAddr, macAddr = info.split(',')
			macAddr, dummy = macAddr.split('\r\n')
			
			# Check if already added
			isAlreadyAdded = False
			for index in range(0, zigbeeDevices.totalDevices):
				if (macAddr == devices[index].getMacAddress()):
					isAlreadyAdded = True
					break
			
			# Add to the list
			if (isAlreadyAdded == False):
				newDevice = zigbeeDevices(shortAddr, macAddr)
				if (joinedDevice):
					devicelistFile.write('\n')
				devicelistFile.write(macAddr)
				devicelistFile.flush()
				joinedDevice += 1
				devices.append(newDevice)
				print 'Joined device: ' + str(joinedDevice) + '\n'
				

			# Disable join
			if (joinedDevice == TOTAL_TEST_DEVICES):
				sendCommand(serialport, joinEnableCmd, time=PERMIT_JOIN_STOP)
				isJoinEnabled = 0
				print '[Permit join disabled]'

if (joinedDevice):
	for index in range(0, joinedDevice):
		# Get the short address from list
		shortAddr = devices[index].getShortAddress()

		# Active endpoint request
		response = sendCommandNoResponsePattern(serialport, activeEndpointCmd, shortAddr = int(shortAddr, base=16))
		time.sleep(0.1)
		strACEP = response[0]
		startIndex = strACEP.find('$ACEP:')
		endIndex = strACEP.find('\r\n')

		if (startIndex != -1) and (endIndex != -1):
			strACEP = strACEP[(startIndex + 6) : endIndex]
			strEpList = strACEP.split(',')

			numOfEP = int(strEpList[0])
			if (numOfEP):
				for numOfEP in range(1, numOfEP + 1):
					# Simple descriptor request
					response = sendCommandNoResponsePattern(serialport, simpleDescriptorCmd, shortAddr = int(shortAddr, base=16), endPoint = int(strEpList[numOfEP], base=16))
					time.sleep(0.1)
					# Check simple descriptor response
					numOfResp = len(response)
					for numOfResp in range(0, numOfResp):
						strSimpleDescReq = response[numOfResp]
						startIndex = (strSimpleDescReq.find('$SIMPLEDESC:'))
						endIndex = (strSimpleDescReq.find('\r\n'))
						if (startIndex != -1) and (endIndex != -1):
							# Record information
							strSimpleDescReq = strSimpleDescReq[(startIndex + 12):endIndex]
							strArraySimpleDescReq = strSimpleDescReq.split(',')
							# Profile matching
							profileID = int(strArraySimpleDescReq[1], base=16)
							if (profileID == ZLL_PROFILE_ID):
								# ZLL
								numOfOutputCluster = int(strArraySimpleDescReq[4], base=16)
								if (numOfOutputCluster != 0):
									for numOfOutputCluster in range(0, numOfOutputCluster):
										if (strArraySimpleDescReq[5 + numOfOutputCluster] == '0006'):
											# On/Off control cluster
											devices[index].addSupportedClusterToList('0006')
										elif (strArraySimpleDescReq[5 + numOfOutputCluster] == '0008'):
											# Level control cluster
											devices[index].addSupportedClusterToList('0008')
										elif (strArraySimpleDescReq[5 + numOfOutputCluster] == '0300'):
											# Color control cluster
											devices[index].addSupportedClusterToList('0300')

	# Test
	errorCounts = 0

	targetX = 0
	targetY = 0
	targetLevel = 0
	transitionTime = 0x000A

	logMsg = 'Test started:' + datetime.now().strftime("%H:%M:%S.%f") + '\n'
	logFile.write(logMsg)				
	#for testCounts in range(0, TOTAL_TEST_COUNTS):
	#index = random.randint(0, (joinedDevice - 1))
	count = 0
	for testCounts in range(0, LOOP_COUNTS):
		for index in range(0, joinedDevice):
			shortAddr = devices[index].getShortAddress()
			count += 1
			# if (devices[index].isClusterSupported('0008')):
				# targetLevel = random.randint(0, 255)
				# start = datetime.now()
				# response = sendCommandNoResponsePattern(serialport, moveToLevelCmd, shortAddr = int(shortAddr,base=16), endPoint = int(strEpList[numOfEP], base=16), level = targetLevel, transTime = transitionTime)
				# if (response.startswith('ERROR')):
					# errorCounts += 1
					# response, dummy = response.split('\r\n')
					# logMsg = '%8d: __Device #%2d %8dms' % (count, index + 1, elapsedTime(start)) + '[' + response + ' Level control] __' + str(devices[index].getMacAddress()) + '\n'
					# logFile.write(logMsg)
					# logFile.flush()
				# elif (response.startswith('OK')):
					# response, dummy = response.split('\r\n')
					# logMsg = '%8d: __Device #%2d %8dms' % (count, index + 1, elapsedTime(start)) + '\n'
					# logFile.write(logMsg)
					# logFile.flush()
					
			if (devices[index].isClusterSupported('0300')):
				targetX = random.randint(0, 65535)
				targetY = random.randint(0, 65535)
				start = datetime.now()
				response = sendCommandNoResponsePattern(serialport, moveToColorCmd, shortAddr = int(shortAddr,base=16), endPoint = int(strEpList[numOfEP], base=16), X = targetX, Y = targetY, transTime = transitionTime)
				if (response.startswith('ERROR')):
					errorCounts += 1
					response, dummy = response.split('\r\n')
					logMsg = '%8d: __Device #%2d %8dms' % (count, index + 1, elapsedTime(start)) + '[' + response + ' Color control] __' + str(devices[index].getMacAddress()) + '\n'
					logFile.write(logMsg)
					logFile.flush()
				elif (response.startswith('OK')):
					response, dummy = response.split('\r\n')
					logMsg = '%8d: __Device #%2d %8dms' % (count, index + 1, elapsedTime(start)) + '\n'
					logFile.write(logMsg)
					logFile.flush()

	logMsg = 'Test end: ' + datetime.now().strftime("%H:%M:%S.%f") + '\n' + 'Total trial: ' + str(TOTAL_TEST_COUNTS) + '\n' + 'errorCounts: ' + str(errorCounts)
	logFile.write(logMsg)
	print logMsg

	# Send leave request to joined devices
	for index in range (0, joinedDevice):
		macAddr = devices[index].getMacAddress()
		sendCommandNoResponsePattern(serialport, leaveNwkCmd, ExtAddr=macAddr)
		time.sleep(1)

devicelistFile.close()
# Log file save
logFile.close()

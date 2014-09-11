import sys
import time
import os
from atCmd import *
from serialConfig import serialport


TLResetCmd = {	
	'cmd': "AT$TLR=%(channel)s,%(extAddr)s"}

TLScanCmd = {	
	'cmd': "AT$TLSCAN",
	'respPattern': r"(?P<name>\w+):(?P<channel>\w+),(?P<extAddr>\w+),(?P<a>\w+),(?P<b>\w+),(?P<c>\w+),(?P<d>\w+),(?P<e>\w+),(?P<f>\w+),(?P<g>\w+),(?P<h>\w+),(?P<i>\w+),(?P<j>\w+),(?P<k>\w+)"}
	
#devList = sendCommand(serialport, TLScanCmd)

DEVICE_LIST_FILENAME = 'devicelist.txt'
targetChannel = '14'

if (os.path.exists(DEVICE_LIST_FILENAME) == False):
	sys.exit(0)

lines = [line.rstrip('\n') for line in open(DEVICE_LIST_FILENAME)]
print str(lines)

for i in lines:
	sendCommand(serialport, TLResetCmd, channel = targetChannel, extAddr = i)
	print str(i)
	time.sleep(0.5)
	# sendCommand(serialport, TLResetCmd, targetChannel, extAddr = i)
	# 
	# time.sleep(0.5)
	
# for i in range(0, len(devList)):
	# if (targetChannel == devList[i].group('channel')):
		# sendCommand(serialport, TLResetCmd, channel = devList[i].group('channel'), extAddr = devList[i].group('extAddr'))
		# printMatchObj(devList[i])
		# time.sleep(0.5)

import sys
import time
from atCmd import *
from serialConfig import serialport



TLResetCmd = {	
	'cmd': "AT$TLR=%(channel)s,%(extAddr)s"}

TLScanCmd = {	
	'cmd': "AT$TLSCAN",
	'respPattern': r"(?P<name>\w+):(?P<channel>\w+),(?P<extAddr>\w+),(?P<a>\w+),(?P<b>\w+),(?P<c>\w+),(?P<d>\w+),(?P<e>\w+),(?P<f>\w+),(?P<g>\w+),(?P<h>\w+),(?P<i>\w+),(?P<j>\w+),(?P<k>\w+)"}
	
devList = sendCommand(serialport, TLScanCmd)

targetChannel = '14'
for i in range(0, len(devList)):
	if (targetChannel == devList[i].group('channel')):
		sendCommand(serialport, TLResetCmd, channel = devList[i].group('channel'), extAddr = devList[i].group('extAddr'))
		printMatchObj(devList[i])
		time.sleep(0.5)

import re
import sys
import time
from ctypes import *

#from serialcom import *

#################################################################
# Common parameters
#################################################################
COMMAND_SEPARATOR = '\r\n'

#################################################################
# SmartHome specific commands on the UART interface
#################################################################

createNwkCmd = {
	'cmd': "AT$JNNWK",
	'respPattern': r"(?P<name>\w+):(?P<channel>\w+),(?P<nwkAddr>\w+),(?P<panId>\w+),(?P<exPanId>\w+)"}

joinEnableCmd = {
	'cmd': "AT$JNEN=%(time)02x"}

broadcastMatchCmd = {	
	'cmd': "AT$MATCH=%(clusterId)04x,%(endPoint)02x",
	'respPattern': r"(?P<name>\w+):(?P<shortAddr>\w+),(?P<endPoint>\w+)"}

unicastMatchCmd = {	
	'cmd': "AT$MATCH=%(shortAddr)04x,%(clusterId)04x,%(endPoint)02x",
	'respPattern': r"(?P<name>\w+):(?P<shortAddr>\w+),(?P<endPoint>\w+)"}

getNwkAddrCmd = {
	'cmd': "AT$ADDRREQ=%(extAddr)016x",
	'respPattern': r"(?P<name>\w+):(?P<shortAddr>\w+)"}	
	
getExtAddrCmd = {	
	'cmd': "AT$EXTADDR=%(shortAddr)s",
	'respPattern': r"(?P<name>\w+):(?P<extAddr>\w+)"}

leaveNwkCmd = {
	'cmd': "AT$LVREQ=%(ExtAddr)s"}

bindCmd = {
	'cmd': "AT$BIND=%(action)02x,%(dest)02x,%(localEp)02x,%(extAddr)016x,%(remEp)02x,%(clusterId)04x"} 
	
	
#On/off cluster	
onCmd = {
	'cmd': "AT$ON=%(shortAddr)04x,%(endPoint)02x"}
	
offCmd = {
	'cmd': "AT$OFF=%(shortAddr)04x,%(endPoint)02x"}

toggleCmd = {
	'cmd': "AT$TOGGLE=%(shortAddr)04x,%(endPoint)02x"}	

#Level control cluster
moveToLevelCmd = {	
	'cmd': "AT$MVTOLV=%(shortAddr)04x,%(endPoint)02x,%(level)02x,%(transTime)04x"}	

moveLevelCmd = {	
	'cmd': "AT$MVLV=%(shortAddr)04x,%(endPoint)02x,%(moveMode)02x,%(rate)02x"}	
	
stepLevelCmd = {	
	'cmd': "AT$STEPLV=%(shortAddr)04x,%(endPoint)02x,%(stepMode)02x,%(stepSize)02x,%(transTime)04x"}	

#Color control cluster
moveToHueCmd = {	
	'cmd': "AT$MVTOH=%(shortAddr)04x,%(endPoint)02x,%(hue)02x,%(direction)02x,%(transTime)04x"}	

moveHueCmd = {	
	'cmd': "AT$MVH=%(shortAddr)04x,%(endPoint)02x,%(moveMode)02x,%(rate)02x"}	
	
stepHueCmd = {	
	'cmd': "AT$STEPH=%(shortAddr)04x,%(endPoint)02x,%(stepMode)02x,%(stepSize)02x,%(transTime)04x"}	

moveToSaturationCmd = {	
	'cmd': "AT$MVTOS=%(shortAddr)04x,%(endPoint)02x,%(saturation)02x,%(transTime)04x"}	

moveSaturationCmd = {	
	'cmd': "AT$MVS=%(shortAddr)04x,%(endPoint)02x,%(moveMode)02x,%(rate)02x"}	
	
stepSaturationCmd = {	
	'cmd': "AT$STEPS=%(shortAddr)04x,%(endPoint)02x,%(stepMode)02x,%(stepSize)02x,%(transTime)04x"}	

moveToHueSaturationCmd = {	
	'cmd': "AT$MVTOHS=%(shortAddr)04x,%(endPoint)02x,%(hue)02x,%(saturation)02x,%(transTime)04x"}	
	
moveToColorCmd = {	
	'cmd': "AT$MVTOC=%(shortAddr)04x,%(endPoint)02x,%(X)04x,%(Y)04x,%(transTime)04x"}	

moveColorCmd = {	
	'cmd': "AT$MVC=%(shortAddr)04x,%(endPoint)02x,%(rateX)04x,%(rateY)04x"}	
	
stepColorCmd = {	
	'cmd': "AT$STEPC=%(shortAddr)04x,%(endPoint)02x,%(X)04x,%(Y)04x,%(transTime)04x"}	

#Group cluster
addGroupCmd = {	
	'cmd': "AT$ADDGR=%(shortAddr)04x,%(endPoint)02x,%(groupId)04x",	
	'respPattern': r"(?P<name>\w+):(?P<groupId>\w+)"}
	
removeGroupCmd = {	
	'cmd': "AT$REMGR=%(shortAddr)04x,%(endPoint)02x,%(groupId)04x",	
	'respPattern': r"(?P<name>\w+):(?P<groupId>\w+)"}
	
	
removeAllGroupCmd = {	
	'cmd': "AT$REMAGR=%(shortAddr)04x,%(endPoint)02x"}

activeEndpointCmd = {	
	'cmd': "AT$ACEP=%(shortAddr)04x",	
	'respPattern': r"(?P<name>\w+):(?P<endpoint>\w+)"}
	
#Group commands
grOnCmd = {
	'cmd': "AT$ON=%(groupId)04x"}
	
grOffCmd = {
	'cmd': "AT$OFF=%(groupId)04x"}

grToggleCmd = {
	'cmd': "AT$TOGGLE=%(groupId)04x"}	

grMoveToHueCmd = {	
	'cmd': "AT$MVTOH=%(groupId)04x,%(hue)02x,%(direction)02x,%(transTime)04x"}	

grMoveHueCmd = {	
	'cmd': "AT$MVH=%(groupId)04x,%(moveMode)02x,%(rate)02x"}	
	
grStepHueCmd = {	
	'cmd': "AT$STEPH=%(groupId)04x,%(stepMode)02x,%(stepSize)02x,%(transTime)04x"}	
	
	
def sendCommand(serialport, cmd, **inputs):
	cmdStr = cmd['cmd'] % inputs
	#print inputs
	result = []
	serialport.sendBuffer(cmdStr + COMMAND_SEPARATOR)
	print serialport.readline()
	resp = serialport.readline()
	print resp	
	if resp.startswith('ERROR'):
		return resp
	elif resp.startswith('OK'):
		return resp
	else:
		while(resp.find('OK') == -1):
			result.append(re.search(cmd['respPattern'],resp))
			resp = serialport.readline()	
			print resp			
	return result

def sendCommandToList(serialport, cmd, devList, **inputs):
	for i in range(0, len(devList)):
		inputs['shortAddr'] = int(devList[i].group('shortAddr'), base = 16)
		inputs['endPoint'] = int(devList[i].group('endPoint'), base = 16)
		cmdStr = cmd['cmd'] % inputs
		result = []
		serialport.sendBuffer(cmdStr + COMMAND_SEPARATOR)
		print serialport.readline()
		resp = serialport.readline()
		print resp
		time.sleep(0.2)
		
		if resp.startswith('ERROR'):
			continue
		elif resp.startswith('OK'):
			continue
		else:
			while(resp.find('OK') == -1):
				result.append(re.search(cmd['respPattern'],resp))
				resp = serialport.readline()
				print resp
	return result
	
def sendCommandWithoutResp(serialport, cmd, **inputs):
	cmdStr = cmd['cmd'] % inputs
	result = []
	serialport.sendBuffer(cmdStr + COMMAND_SEPARATOR)
	
def printMatchObj(matchObj):
	print matchObj.group()
	
def printMatchObjList(matchObjList):
	for i in range(0, len(matchObjList)):
		print matchObjList[i].group()
		
class zb_dev_info(Structure):
    _fields_ = [
		("id",   c_ubyte),
        ("ext_addr",   c_ulonglong),
        ("short_addr",      c_uint),
        ("endpoint",   c_ubyte),
        ("cluster_list", c_ulonglong),
    ]
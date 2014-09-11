from datetime import datetime

# Elapsed Time
def elapsedTime(start):
   dt = datetime.now() - start
   ms = (dt.days * 24 * 60 * 60 + dt.seconds) * 1000 + dt.microseconds / 1000.0
   return ms

# # Read attribute and save to file
# def readAttribute(clustId, attrId):
	# attrResp = sendCommandNoResponsePattern(serialport, remoteAttrReqCmd, shortAddr=int(shortAddr, base=16), endPoint=int(strEpList[numOfEP], base=16), clusterId=clustId, attrValue=attrId)
	# attrStr = attrResp[0]
	# startIndex = (attrStr.find('$ATTRRR:'))
	# endIndex = (attrStr.find('\r\n'))
	# if (startIndex != -1) and (endIndex != -1):
		# # Record information
		# attrStr = attrStr[(startIndex+12):endIndex]
		# attrRespArray = attrStr.split(',')
		# return attrRespArray[5]
	# return '[Error: ' + attrStr + ']\n'

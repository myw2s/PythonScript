class zigbeeDevices:

	totalDevices = 0

	def __init__(self, shortAddr, macAddr):
		self.shortAddr = shortAddr
		self.macAddr = macAddr
		self.totalSupportedClusters = 0
		self.clusterSupportList = []
		zigbeeDevices.totalDevices += 1
		
	def getShortAddress(self):
		return self.shortAddr
	
	def getMacAddress(self):
		return self.macAddr
	
	def addSupportedClusterToList(self, clusterId):
		self.totalSupportedClusters += 1
		self.clusterSupportList.append(clusterId)
		print 'Cluster ID [' + str(clusterId) + '] is added'

	def getClusterSuppored(self):
		return self.clusterSupportList
	
	def getTotalSupportedClusters(self):
		return self.totalSupportedClusters
		
	def isClusterSupported(self, clusterId):
		for index in range(0, self.totalSupportedClusters):
			if (self.clusterSupportList[index] == clusterId):
				return True
		return False

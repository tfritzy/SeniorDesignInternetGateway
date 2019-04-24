import TXRX

class Gateway():

    def __init__(self):
        self.id = 0

    def makeResponseData(self, packetData):

        if (len(packetData) != 5):
            return []
        
        packetType = packetData[0]
        if (packetType == TXRX.PacketType.FIND_HOME.value):
            sourceId = self.id
            distanceToHome = 1
            responseData = [TXRX.PacketType.FOUND_HOME.value, sourceId,
                            distanceToHome, -1, -1]
            return responseData

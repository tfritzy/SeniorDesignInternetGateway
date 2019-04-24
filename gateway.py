import TXRX
import time
import urllib.request

class Gateway():

    def __init__(self):
        self.id = 0
        self.txrx = TXRX.TXRX()

    def waitForPacket(self):
        packet = self.txrx.receivePacket()
        return packet

    def transmitPacket(self, packet):
        if (len(packet) != 5):
            return None
        self.txrx.sendPacket(packet[0], packet[1],packet[2],
                        packet[3],packet[4])

    def handlePacket(self, packet):
        print(packet)
        response = self.makeResponseToReceivedPacket(packet)
        if (response == None):
            print("I have no Response to %s" % packet)
        else:
            print("My Response: %s" % response) 
            self.transmitPacket(response)

    def makeResponseToReceivedPacket(self, packetData):

        if (len(packetData) != 5):
            return []
        
        packetType = packetData[0]
        if (packetType == TXRX.PacketType.FIND_HOME.value):
            sourceId = self.id
            distanceToHome = 1
            responseData = [TXRX.PacketType.FOUND_HOME.value, sourceId,
                            distanceToHome, -1, -1]
            return responseData


        elif (packetType == TXRX.PacketType.DATA.value):
            jsonArray = self.makeJSONArrayFromPackets([packetData])
            self.uploadJSONToWebServer(jsonArray)
            responseType = TXRX.PacketType.PACKET_RECEIVED.value;
            sourceId = self.id
            destId = packetData[1]
            responseData = [responseType, sourceId, destId, -1, -1]
            return responseData

    def extractDataFromPacket(self, dataPacket):
        if (dataPacket == None):
            return None
        if (len(dataPacket) != 5):
            return []

        sourceNode = int(dataPacket[1])
        dataValue = float(dataPacket[4])
        if (sourceNode <= 0):
            return None
        if (dataValue < 0):
            return None
        if (sourceNode > 1000):
            return None

        packetData = [int(dataPacket[1]),
                      float(dataPacket[4]),
                      self.getCurrentTime(),
                      self.getCurrentTime()]
        return packetData


    def makeJSONDataElement(self, data):
        if (data == None):
            return None
        if (len(data) != 4):
            return None

        sourceId = data[0]
        value = data[1]
        createdTime = data[2]
        updatedTime = data[3]

        jsonFormat = ("{ \"id\": \"%s\", \"value\": \"%s\", "
        +"\"createdAt\": \"%s\", \"updatedAt\": \"%s\"}") % (str(sourceId),
                                                    str(value),
                                                    str(createdTime),
                                                    str(updatedTime));

        return jsonFormat

    def getJSONFromDataPacket(self, dataPacket):
        data = self.extractDataFromPacket(dataPacket)
        json = self.makeJSONDataElement(data)
        return json

    def makeJSONArrayFromPackets(self, dataPackets):
        jsonElements = ""
        for i in range(len(dataPackets)):
            dataPacket = dataPackets[i]
            jsonElement = self.getJSONFromDataPacket(dataPacket)
            if (jsonElement == None):
                continue
            jsonElements += jsonElement
            if (i < len(dataPackets) - 1):
                jsonElements += ", "
        if (jsonElements == ""):
            return None
        fullJSONBody = "[%s]" % jsonElements
        return fullJSONBody

    
    def getCurrentTime(self):
        return time.strftime('%d-%m-%y %H:%M:%S')

    def uploadJSONToWebServer(self, jsonData):
        jsonDataAsBytes = jsonData.encode('utf-8')
        print(jsonDataAsBytes)
        URL = "http://129.186.5.34:8181/homenodes/3"
        req = urllib.request.Request(URL)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        req.add_header('Content-Length', len(jsonDataAsBytes))
        try:
            response = urllib.request.urlopen(req, jsonDataAsBytes)
            print(response)
        except:
            print("There was a network error!")
        

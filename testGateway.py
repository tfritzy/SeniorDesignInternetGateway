import gateway
import unittest
import TXRX
from TXRX import PacketType
import time
import datetime
import re

class TestGateway(unittest.TestCase):

    def setUp(self):
        self.gw = gateway.Gateway()
        

    def testHandleFindHomePacket(self):
        findPacket = []
        expectedResponse = []
        actualResponse = self.gw.makeResponseToReceivedPacket(findPacket)
        self.assertEqual(
                    expectedResponse,
                    actualResponse)
        
        findPacket = [PacketType.FIND_HOME.value,
                      3, -1, -1, -1]
        expectedResponse = [PacketType.FOUND_HOME.value,
                            0, 1, -1, -1]
        actualResponse = self.gw.makeResponseToReceivedPacket(findPacket)
        self.assertEqual(
                    expectedResponse,
                    actualResponse)

        findPacket = [PacketType.FIND_HOME.value,
                      4, -1, -1, -1]
        expectedResponse = [PacketType.FOUND_HOME.value,
                            0, 1, -1, -1]
        actualResponse = self.gw.makeResponseToReceivedPacket(findPacket)
        self.assertEqual(
                    expectedResponse,
                    actualResponse)

    

    def testHandleDataPacketConfirmation(self):
        dataPacket = []
        expectedResponse = []
        actualResponse = self.gw.makeResponseToReceivedPacket(dataPacket)
        self.assertEqual(
                    expectedResponse,
                    actualResponse)
        
        gatewayId = 0
        sendingNode = 4
        dataPacket = [PacketType.DATA.value, sendingNode, -1, -1, -1]
        expectedResponse = [PacketType.PACKET_RECEIVED.value,
                            gatewayId, sendingNode, -1, -1]
        actualResponse = self.gw.makeResponseToReceivedPacket(dataPacket)
        self.assertEqual(
                    expectedResponse,
                    actualResponse)

        gatewayId = 0
        sendingNode = 17
        dataPacket = [PacketType.DATA.value, sendingNode, -1, -1, -1]
        expectedResponse = [PacketType.PACKET_RECEIVED.value,
                            gatewayId, sendingNode, -1, -1]
        actualResponse = self.gw.makeResponseToReceivedPacket(dataPacket)
        self.assertEqual(
                    expectedResponse,
                    actualResponse)


    def testExtractDataFromDataPacket(self):
        dataPacket = []
        expectedResponse = []
        actualResponse = self.gw.extractDataFromPacket(dataPacket)
        self.assertEqual(
            expectedResponse,
            actualResponse)

        dataPacketType = PacketType.DATA.value
        sourceId = 16
        nextHopId = 0
        lastHopId = 0
        dataValue = 3.5
        dataPacket = [dataPacketType, sourceId,
                      nextHopId, lastHopId, dataValue]
        expectedResponse = [sourceId, dataValue,
                            self.gw.getCurrentTime(),
                            self.gw.getCurrentTime()]
        actualResponse = self.gw.extractDataFromPacket(dataPacket)
        self.assertEqual(
            expectedResponse,
            actualResponse)

        dataPacketType = PacketType.DATA.value
        sourceId = 14
        nextHopId = 0
        lastHopId = 0
        dataValue = 16
        dataPacket = [dataPacketType, sourceId,
                      nextHopId, lastHopId, dataValue]
        expectedResponse = [sourceId, dataValue,
                            self.gw.getCurrentTime(),
                            self.gw.getCurrentTime()]
        actualResponse = self.gw.extractDataFromPacket(dataPacket)
        self.assertEqual(
            expectedResponse,
            actualResponse)

        dataPacketType = PacketType.DATA.value
        sourceId = 18
        nextHopId = 13
        lastHopId = 1
        dataValue = -6
        dataPacket = [dataPacketType, sourceId,
                      nextHopId, lastHopId, dataValue]
        expectedResponse = None
        actualResponse = self.gw.extractDataFromPacket(dataPacket)
        self.assertEqual(
            expectedResponse,
            actualResponse)

        dataPacketType = PacketType.DATA.value
        sourceId = -1
        nextHopId = 13
        lastHopId = 1
        dataValue = -6
        dataPacket = [dataPacketType, sourceId,
                      nextHopId, lastHopId, dataValue]
        expectedResponse = None
        actualResponse = self.gw.extractDataFromPacket(dataPacket)
        self.assertEqual(
            expectedResponse,
            actualResponse)

        dataPacketType = PacketType.DATA.value
        sourceId = 0
        nextHopId = 13
        lastHopId = 1
        dataValue = -6
        dataPacket = [dataPacketType, sourceId,
                      nextHopId, lastHopId, dataValue]
        expectedResponse = None
        actualResponse = self.gw.extractDataFromPacket(dataPacket)
        self.assertEqual(
            expectedResponse,
            actualResponse)

        
        dataPacketType = PacketType.DATA.value
        sourceId = 1001
        nextHopId = 13
        lastHopId = 1
        dataValue = 15
        dataPacket = [dataPacketType, sourceId,
                      nextHopId, lastHopId, dataValue]
        expectedResponse = None
        actualResponse = self.gw.extractDataFromPacket(dataPacket)
        self.assertEqual(
            expectedResponse,
            actualResponse)

        
    def testGetCurrentTime(self):
        time = self.gw.getCurrentTime()
        timeSections = re.findall(r"[\d]+", time)
        self.assertEqual(int(timeSections[0]), datetime.datetime.now().day)
        self.assertEqual(len(timeSections[0]), 2)
        
        self.assertEqual(int(timeSections[1]), datetime.datetime.now().month)
        self.assertEqual(len(timeSections[1]), 2)

        self.assertEqual(int(timeSections[2]), datetime.datetime.now().year - 2000)
        self.assertEqual(len(timeSections[2]), 2)

        self.assertEqual(int(timeSections[3]), datetime.datetime.now().hour)
        self.assertEqual(len(timeSections[3]), 2)

        self.assertEqual(int(timeSections[4]), datetime.datetime.now().minute)
        self.assertEqual(len(timeSections[4]), 2)

        self.assertEqual(int(timeSections[5]), datetime.datetime.now().second)
        self.assertEqual(len(timeSections[5]), 2)

    def testMakeJSONElement(self):
        data = []
        expectedResponse = None
        actualResponse = self.gw.makeJSONDataElement(data)
        self.assertEqual(
            expectedResponse,
            actualResponse)

        sourceId = 4
        dataValue = 14.23
        curTime = self.gw.getCurrentTime()
        data = [sourceId, dataValue, curTime, curTime]
        expectedResponse = ("{ \"id\": %s, \"value:\": %s, "
        +"\"createdAt\": %s, \"updatedAt\": %s}") % (str(sourceId),
                                                    str(dataValue),
                                                    str(curTime),
                                                    str(curTime));
        actualResponse = self.gw.makeJSONDataElement(data)
        self.assertEqual(
            expectedResponse,
            actualResponse)

    def testDataPacketToJSON(self):
        
        # ========== Happy Path ===========
        dataPacketType = PacketType.DATA.value
        sourceId = 18
        nextHopId = 13
        lastHopId = 1
        dataValue = 3.3
        dataPacket = [dataPacketType, sourceId,
                      nextHopId, lastHopId, dataValue]
        expectedResponse = ("{ \"id\": %s, \"value:\": %s, "
        +"\"createdAt\": %s, \"updatedAt\": %s}") % (str(sourceId),
                                                    str(dataValue),
                                                    self.gw.getCurrentTime(),
                                                    self.gw.getCurrentTime());

        actualResponse = self.gw.getJSONFromDataPacket(dataPacket)
        self.assertEqual(
            expectedResponse,
            actualResponse)

        # ========== Invalid Node Id ===========

        dataPacketType = PacketType.DATA.value
        sourceId = -3
        nextHopId = 13
        lastHopId = 1
        dataValue = 3.3
        dataPacket = [dataPacketType, sourceId,
                      nextHopId, lastHopId, dataValue];
        expectedResponse = None
        actualResponse = self.gw.getJSONFromDataPacket(dataPacket)
        self.assertEqual(
            expectedResponse,
            actualResponse)

        # ========== Invalid Data ===========

        sourceId = 16
        nextHopId = 13
        lastHopId = 1
        dataValue = -6
        dataPacket = [dataPacketType, sourceId,
                      nextHopId, lastHopId, dataValue];
        expectedResponse = None
        actualResponse = self.gw.getJSONFromDataPacket(dataPacket)
        self.assertEqual(
            expectedResponse,
            actualResponse)

        # ========== Invalid Node Id ===========

        sourceId = 1001
        nextHopId = 13
        lastHopId = 1
        dataValue = 6
        dataPacket = [dataPacketType, sourceId,
                      nextHopId, lastHopId, dataValue];
        expectedResponse = None
        actualResponse = self.gw.getJSONFromDataPacket(dataPacket)
        self.assertEqual(
            expectedResponse,
            actualResponse)


    def testMakeFullJSONBody(self):

        # ========== One Element Test =============
        dataPacketType = PacketType.DATA.value
        sourceId = 16
        nextHopId = 13
        lastHopId = 1
        dataValue = 6
        dataPackets = [[dataPacketType, sourceId,
                      nextHopId, lastHopId, dataValue]];

        jsonElement = self.gw.getJSONFromDataPacket(dataPackets[0])
        expectedResponse = "[%s]" % jsonElement
        actualResponse = self.gw.makeJSONArrayFromPackets(dataPackets)
        self.assertEqual(
            expectedResponse,
            actualResponse)

        # ========== Two Elements Test =============
        dataPacketType = PacketType.DATA.value
        sourceId = 16
        nextHopId = 13
        lastHopId = 1
        dataValue = 6
        packet1 = [dataPacketType, sourceId,
                      nextHopId, lastHopId, dataValue]
        sourceId = 7
        nextHopId = 0
        lastHopId = 0
        dataValue = 15.3
        packet2 = [dataPacketType, sourceId,
                      nextHopId, lastHopId, dataValue]
        dataPackets = [packet1, packet2];

        jsonElement0 = self.gw.getJSONFromDataPacket(dataPackets[0])
        jsonElement1 = self.gw.getJSONFromDataPacket(dataPackets[1])
        
        expectedResponse = "[%s, %s]" % (jsonElement0, jsonElement1)
        actualResponse = self.gw.makeJSONArrayFromPackets(dataPackets)
        self.assertEqual(
            expectedResponse,
            actualResponse)

        # ========== One Invalid Element Test =============
        dataPacketType = PacketType.DATA.value
        sourceId = 1001 # invalid id
        nextHopId = 13
        lastHopId = 1
        dataValue = 6
        packet1 = [dataPacketType, sourceId,
                      nextHopId, lastHopId, dataValue]
        sourceId = 7
        nextHopId = 0
        lastHopId = 0
        dataValue = 15.3
        packet2 = [dataPacketType, sourceId,
                      nextHopId, lastHopId, dataValue]
        dataPackets = [packet1, packet2];

        jsonElement0 = self.gw.getJSONFromDataPacket(dataPackets[0])
        jsonElement1 = self.gw.getJSONFromDataPacket(dataPackets[1])
        
        expectedResponse = "[%s]" % (jsonElement1)
        actualResponse = self.gw.makeJSONArrayFromPackets(dataPackets)
        self.assertEqual(
            expectedResponse,
            actualResponse)


        # ========== All Invalid Elements Test =============
        dataPacketType = PacketType.DATA.value
        sourceId = 1001 # invalid id
        nextHopId = 13
        lastHopId = 1
        dataValue = 6
        packet1 = [dataPacketType, sourceId,
                      nextHopId, lastHopId, dataValue]
        sourceId = 7
        nextHopId = 0
        lastHopId = 0
        dataValue = -30
        packet2 = [dataPacketType, sourceId,
                      nextHopId, lastHopId, dataValue]
        dataPackets = [packet1, packet2];

        jsonElement0 = self.gw.getJSONFromDataPacket(dataPackets[0])
        jsonElement1 = self.gw.getJSONFromDataPacket(dataPackets[1])
        
        expectedResponse = None
        actualResponse = self.gw.makeJSONArrayFromPackets(dataPackets)
        self.assertEqual(
            expectedResponse,
            actualResponse)



        
                            
        

if __name__ == "__main__":
    unittest.main()

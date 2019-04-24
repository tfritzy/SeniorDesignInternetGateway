import gateway
import unittest
import TXRX
from TXRX import PacketType

class TestGateway(unittest.TestCase):

    def setUp(self):
        self.gw = gateway.Gateway()
        

    def testHandleFindHomePacket(self):
        findPacket = []
        expectedResponse = []
        actualResponse = self.gw.makeResponseData(findPacket)
        self.assertEqual(
                    expectedResponse,
                    actualResponse)
        
        findPacket = [PacketType.FIND_HOME.value,
                      3, -1, -1, -1]
        expectedResponse = [PacketType.FOUND_HOME.value,
                            0, 1, -1, -1]
        actualResponse = self.gw.makeResponseData(findPacket)
        self.assertEqual(
                    expectedResponse,
                    actualResponse)

        findPacket = [PacketType.FIND_HOME.value,
                      4, -1, -1, -1]
        expectedResponse = [PacketType.FOUND_HOME.value,
                            0, 1, -1, -1]
        actualResponse = self.gw.makeResponseData(findPacket)
        self.assertEqual(
                    expectedResponse,
                    actualResponse)

    

    def testHandleDataPacketConfirmation(self):
        gatewayId = 0
        sendingNode = 4
        dataPacket = [PacketType.DATA.value, sendingNode, -1, -1, -1]
        expectedResponse = [PacketType.PACKET_RECEIVED.value,
                            gatewayId, sendingNode, -1, -1]
        actualResponse = self.gw.makeResponseData(dataPacket)
        self.assertEqual(
                    expectedResponse,
                    actualResponse)

        

if __name__ == "__main__":
    unittest.main()

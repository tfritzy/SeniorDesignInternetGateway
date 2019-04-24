import unittest
import TXRX

class TestGateway(unittest.TestCase):

    def setUp(self):
        self.txrx = TXRX.TXRX()

    def testValidatePacket(self):
        self.assertEqual(self.txrx.isValidPacket('asdf'), False)
        self.assertEqual(
            self.txrx.isValidPacket('~||	|	|	^')
            , False)
        self.assertEqual(
            self.txrx.isValidPacket('~|C	|	|	^')
            , False)
        self.assertEqual(
            self.txrx.isValidPacket('~||	||  ^')
            , False)
        self.assertEqual(
            self.txrx.isValidPacket('~a|b|c|e|f^')
            , False)
        self.assertEqual(
            self.txrx.isValidPacket('')
            , False)
        self.assertEqual(
            self.txrx.isValidPacket('~1|2|3|4|5^')
            , True)
        self.assertEqual(
            self.txrx.isValidPacket('~255|255|255|255|255^')
            , False)
        self.assertEqual(
            self.txrx.isValidPacket('~-1|-1|-1|-1|-1^')
            , False)
        self.assertEqual(
            self.txrx.isValidPacket('~4|0|2|-1|-1^')
            , True)
        self.assertEqual(
            self.txrx.isValidPacket('~4|0|2|-1|f^')
            , False)

    def testExtractPacketData(self):
        dataPacket = ''
        expectedData = []
        self.assertEqual(
            self.txrx.extractPacketData(dataPacket),
            expectedData)

        dataPacket = '~a|b|c|'
        expectedData = []
        self.assertEqual(
            self.txrx.extractPacketData(dataPacket),
            expectedData)

        dataPacket = '~a1|2|3|4|E^asdf'
        expectedData = []
        self.assertEqual(
            self.txrx.extractPacketData(dataPacket),
            expectedData)

        dataPacket = '~1|2|3|4|5^'
        expectedData = [1,2,3,4,5]
        self.assertEqual(
            self.txrx.extractPacketData(dataPacket),
            expectedData)

        dataPacket = '~f|f|f|f|f^'
        expectedData = []
        self.assertEqual(
            self.txrx.extractPacketData(dataPacket),
            expectedData)

        

if __name__ == "__main__":
    unittest.main()

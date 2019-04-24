import unittest
import TXRX

class TestGateway(unittest.TestCase):

    def setUp(self):
        self.txrx = TXRX.TXRX()

    def testValidatePacket(self):
        self.assertEqual(self.txrx.isValidPacket('asdf'), False)
        self.assertEqual(
            self.txrx.isValidPacket('S12	3	4	E')
            , True)
        self.assertEqual(
            self.txrx.isValidPacket('S13	3	4	E')
            , False)
        self.assertEqual(
            self.txrx.isValidPacket('S12	34  E')
            , False)
        self.assertEqual(
            self.txrx.isValidPacket('Sa1b2c3d4eE')
            , True)
        self.assertEqual(
            self.txrx.isValidPacket('')
            , False)

    def testExtractPacketData(self):
        dataPacket = ''
        expectedData = []
        self.assertEqual(
            self.txrx.extractPacketData(dataPacket),
            expectedData)

        dataPacket = 'Sa1b2c3'
        expectedData = []
        self.assertEqual(
            self.txrx.extractPacketData(dataPacket),
            expectedData)

        dataPacket = 'Sa1b2c3d4eE9asdf'
        expectedData = []
        self.assertEqual(
            self.txrx.extractPacketData(dataPacket),
            expectedData)

        dataPacket = 'Sa1b2c3d4eE'
        expectedData = [ord('a'), ord('b'),ord('c'),
                        ord('d'), ord('e')]
        self.assertEqual(
            self.txrx.extractPacketData(dataPacket),
            expectedData)

        dataPacket = 'Sf1f2f3f4fE'
        expectedData = [ord('f'), ord('f'),ord('f'),
                        ord('f'), ord('f')]
        self.assertEqual(
            self.txrx.extractPacketData(dataPacket),
            expectedData)

        

if __name__ == "__main__":
    unittest.main()

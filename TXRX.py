import time
import serial
from enum import Enum

class TXRX:
        
        def __init__(self):
                self.ser = serial.Serial(
                port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
                baudrate = 9600)

        def sendPacket(self, packetType, field1, field2, field3, field4):
                packet = 'S%s1%s2%s3%s4%sE' % (packetType, field1, field2,
                                                     field3, field4)
                packet = str.encode(packet)
                self.ser.write(packet)

        def receivePacket(self, timeout=1):
                receiveStartTime = time.time()
                recChar = ''
                
                while(recChar != b'S'):
                        recChar = self.ser.read()
                        if (time.time() > receiveStartTime + timeout):
                                return ''
                packet = recChar
                while(recChar != b'E'):
                        recChar = self.ser.read()
                        packet += recChar
                        if (time.time() > receiveStartTime + timeout):
                                return ''
                packet = packet.decode('utf-8')
                if (not self.isValidPacket(packet)):
                        print("Invalid Packet: {%s}" % packet)
                        return None

                
                packetData = self.extractPacketData(packet)
                
                return packet

        def extractPacketData(self, packet):
                if (not self.isValidPacket(packet)):
                        return []
                packetData = [ord(packet[1]), ord(packet[3]), ord(packet[5]),
                              ord(packet[7]), ord(packet[9])]
                return packetData

        def isValidPacket(self, packet):
                if (len(packet) != 11):
                        return False
                if (packet[0] != 'S' or packet[2] != '1' or packet[4] != '2' or
                    packet[6] != '3' or packet[8] != '4' or packet[10] != 'E'):
                        return False
                return True
        

class PacketType(Enum):
    FIND_HOME = 1
    FOUND_HOME = 2
    DATA = 3
    PACKET_RECEIVED = 4

if (__name__ == "__main__"):
        txrx = TXRX()
        print(PacketType.FIND_HOME.value)
        

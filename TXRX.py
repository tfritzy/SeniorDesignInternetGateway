import time
import serial
from enum import Enum

class TXRX:
        
        def __init__(self):
                self.ser = serial.Serial(
                port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
                baudrate = 9600)

        def sendPacket(self, packetType, field1, field2, field3, field4):
                packet = '~%s|%s|%s|%s|%s^' % (packetType, field1, field2,
                                                     field3, field4)
                packet = str.encode(packet)
                self.ser.write(packet)

        def receivePacket(self, timeout=1):
                receiveStartTime = time.time()
                packet = b''
                recChar = ''
                while (True):

                        recChar = self.ser.read()
                        if (recChar == b'~'):
                            packet = b''
                        packet += recChar
                        print(packet)
                        if (recChar == b'^'):
                                break

                print(packet)
                packet = packet.decode('utf-8')
                print(packet)
                if (not self.isValidPacket(packet)):
                        print("Invalid Packet: {%s}" % packet)
                        return None
                else:
                        print("Valid Packet: {%s}" % packet)

                
                packetData = self.extractPacketData(packet)
                
                return packetData

        def extractPacketData(self, packet):
                if (not self.isValidPacket(packet)):
                        return []
                packetData = []
                packet = packet.replace(r"~", r"")
                packet = packet.replace(r"^", r"")
                seperated = packet.split(r"|")
                for i in range(len(seperated)):
                        packetData.append(int(seperated[i]))

                return packetData

        def isValidPacket(self, packet):
                if (packet == None):
                        return False
                if (len(packet) == 0):
                        return False
                if (packet[0] != '~' or packet[-1] != '^'):
                        return False
                packet = packet.replace(r"~", r"")
                packet = packet.replace(r"^", r"")
                seperated = packet.split(r"|")
                packetType = seperated[0]
                if (not packetType.isdigit() or
                    not (int(packetType) in [1,2,3,4])):
                        return False
                for sep in seperated:
                        if (sep == ""):
                                return False
                        try:
                                int(sep)
                        except:
                                print(sep + " not digit")
                                return False
                                
                
                if (len(seperated) != 5):
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
        

import gateway

if __name__ == "__main__":
    gw = gateway.Gateway()

    while 1:
        packet = gw.waitForPacket()
        if (packet != None):
            print("Received: {%s}" % packet)
            gw.handlePacket(packet)

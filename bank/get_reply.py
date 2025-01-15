import pydivert


# Capture only TCP packets to port 80, i.e. HTTP requests.
# packets will be captured from now on
# Use WinDivert packet buffer
with pydivert.WinDivert("tcp.DstPort == 80 and tcp.PayloadLength > 0") as buffer:
    # Iterate the buffer
    for packet in buffer:
        payload = packet.payload
        if bytes("SUCCESS", "utf-8") in payload:
            print(packet.payload)
        buffer.send(packet)


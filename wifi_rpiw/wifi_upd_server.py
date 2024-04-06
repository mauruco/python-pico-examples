import socket
from time import sleep
import wifi_connect

## how to use
wifi_connect.connect('******', '******')

# Create a new UDP socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to a specific address and port
s.bind(('0.0.0.0', 26760))  # Use your desired port number

while True:
    # Receive up to 1024 bytes from the client
    data, addr = s.recvfrom(1024)
    print('Received:', data, 'from', addr)
    sleep(0.1)
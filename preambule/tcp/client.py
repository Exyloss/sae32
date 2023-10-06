#!/usr/bin/env python3
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 3000))
client.sendall(bytearray([1, 2, 3, 4]))
client.close()

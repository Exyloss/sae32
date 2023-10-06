#!/usr/bin/env python3
import socket
addrPort = ("localhost", 3000)
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.sendto(b"Hello from client", addrPort)
msgServer = client.recv(1024).decode('utf-8')
print("Message du serveur : ", msgServer)
client.close()

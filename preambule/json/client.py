#!/usr/bin/env python3
import socket
import json
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
json_data = {
    "host": "localhost",
    "message": "test du json"
}
client.connect(("localhost", 3000))
client.sendall(json.dumps(json_data).encode())
data = client.recv(1024)
print(data.decode('utf-8'))
client.close()

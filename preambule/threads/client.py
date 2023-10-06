#!/usr/bin/env python3
import socket
import json
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 3000))
mes = ""
while mes != "quit":
    mes = input(">")
    json_data = {
        "host": "localhost",
        "message": mes
    }
    client.sendall(json.dumps(json_data).encode())
    data = client.recv(1024)
    print(data.decode('utf-8'))
client.close()

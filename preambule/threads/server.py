#!/usr/bin/env python3
import socket
import json
import _thread
# initialisation du serveur
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serveur.bind(('', 3000)) # Ecoute sur le port 3000
serveur.listen()

def client_handle(c):
    while True:
        request = client.recv(1024)
        data = request.decode('utf-8')
        data_json = json.loads(data)
        print(data_json['message'])
        print("IP client connecté: ", socket.gethostbyname(socket.gethostname()))
        c.send("message reçu.".encode())
        if data_json['message'] == "quit":
            print("sortie en cours...")
            c.close()
            _thread.exit()
            break

threads = []


while True :
    client, infosclient = serveur.accept()
    _thread.start_new_thread(client_handle, (client,))

serveur.close()

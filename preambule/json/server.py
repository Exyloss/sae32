#!/usr/bin/env python3
import socket
import json
# initialisation du serveur
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serveur.bind(('', 3000)) # Ecoute sur le port 3000
serveur.listen()
while True :
    client, infosclient = serveur.accept()
    request = client.recv(1024)
    data = request.decode('utf-8')
    data_json = json.loads(data)
    print(data_json['message']) #affiche les données du client
    print("IP client connecté: ",socket.gethostbyname(socket.gethostname()))
    client.send("message reçu.".encode())
    client.close()
serveur.close()

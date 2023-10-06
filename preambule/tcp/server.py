#!/usr/bin/env python3
import socket
# initialisation du serveur
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.bind(('localhost', 3000)) # Ecoute sur le port 3000
serveur.listen()
while True :
    client, infosclient = serveur.accept()
    request = client.recv(1024)
    print(request) #affiche les données du client
    print("IP client connecté: ",socket.gethostbyname(socket.gethostname()))
    client.send(b"test")
    client.close()
serveur.close()

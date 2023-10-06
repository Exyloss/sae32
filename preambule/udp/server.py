#!/usr/bin/env python3
import socket
serveur = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# permet de libérer le PORT après un CTRL + C
serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serveur.bind(('localhost', 3000)) # Utilise le port réseau 3000

print("Serveur UDP en écoute sur 3000\n")

while True :
    # utilisation de recvfrom pour récupérer le tuple address
    request, address = serveur.recvfrom(1024)
    print("Message client : ", request.decode("utf-8"))
    print("IP du client connecté : ", address)
    serveur.sendto(b"i am the server", address)

serveur.close()

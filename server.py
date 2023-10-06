#!/usr/bin/env python3
import socket
import json
import _thread
import bdd
# initialisation du serveur
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serveur.bind(('', 3000)) # Ecoute sur le port 3000
serveur.listen()

def client_handle(c):
    while True:
        request = client.recv(1024)
        req_string = request.decode('utf-8')
        req_json = json.loads(req_string) # On convertit la chaine de caractères en json
        print(req_json['data'])
        print("IP client connecté: ", socket.gethostbyname(socket.gethostname()))
        if req_json['op'] == "quit":
            print("sortie en cours...")
            c.close()
            _thread.exit()
            break
        else:
            op = req_json['op']
            data = req_json['data']
            if op == "NEW_PROMO": # Commande d'ajout d'une nouvelle promotion
                bdd.new_promo(data['promo'])
                c.send("message reçu.".encode())
            elif op == "GET_STUDENT_MEAN": # Commande permettant de récupérer la moyenne d'un étudiant
                c.send(str(bdd.get_student_mean(data['etud'])).encode())
            elif op == "GET_PROMO_MEAN": # Commande permettant de récupérer la moyenne d'une promotion
                c.send(str(bdd.get_promo_mean(data['promo'])).encode())
            elif op == "NEW_STUDENT": # Commande d'ajout d'un nouvel étudiant
                promo_id = bdd.get_promo_id(data['promo'])
                if promo_id != -1:
                    data['promo'] = promo_id
                    bdd.new_student(data)
                    c.send("étudiant créé".encode())
                else:
                    c.send("erreur, la promotion renseignée en paramètres n'existe pas.".encode())
            elif op == "NEW_MARK": # Commande d'ajout d'une nouvelle note
                bdd.new_mark(data)
                c.send("note ajoutée avec succés.".encode())
            elif op == "GET_PROMO_BY_NAME": # Commande permettant de lister les promotions en fonction d'un nom
                c.send(str(bdd.get_promo_by_name(data['promo'])).encode())
            elif op == "GET_STUDENTS_BY_PROMO":
                c.send(str(bdd.get_students_by_promo(data['promo'])).encode())


threads = []

while True :
    client, infosclient = serveur.accept()
    _thread.start_new_thread(client_handle, (client,))

serveur.close()

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


def handle_request(op, data):
    if op == "NEW_PROMO": # Commande d'ajout d'une nouvelle promotion
        if "promo" not in data:
            code = 1
            reply = ""
        else:
            code, reply = bdd.new_promo(data['promo'])

    elif op == "GET_STUDENT_MEAN": # Commande permettant de récupérer la moyenne d'un étudiant
        if "etud" not in data:
            code = 1
            reply = ""
        else:
            code, reply = bdd.get_student_mean(data['etud'])

    elif op == "GET_PROMO_MEAN": # Commande permettant de récupérer la moyenne d'une promotion
        if "promo" not in data:
            code = 1
            reply = ""
        else:
            code, reply = bdd.get_promo_mean(data['promo'])

    elif op == "NEW_STUDENT": # Commande d'ajout d'un nouvel étudiant
        if "nom" not in data or prenom not in data or promo not in data:
            code = 1
            reply = ""
        else:
            promo_id = bdd.get_promo_id(data['promo'])
            if promo_id == -1:
                code = 2
                reply = ""
            else:
                data['promo'] = promo_id
                code, reply = bdd.new_student(data)

    elif op == "NEW_MARK": # Commande d'ajout d'une nouvelle note
        if "note" not in data or "coef" not in data:
            code = 1
            reply = ""
        else:
            code, reply = bdd.new_mark(data)

    elif op == "GET_PROMO_BY_NAME": # Commande permettant de lister les promotions en fonction d'un nom
        if "promo" not in data:
            code = 1
            reply = ""
        else:
            code, reply = bdd.get_promo_by_name(data['promo'])

    elif op == "GET_STUDENTS_BY_PROMO":
        if "promo" not in data:
            code = 1
            reply = ""
        else:
            promo_id = bdd.get_promo_id(data['promo'])
            if promo_id == -1:
                code = 2
                reply = ""
            else:
                code, reply = bdd.get_students_by_promo(promo_id)
    else:
        code = 3
        reply = ""
    return (code, reply)


def client_handle(c):
    auth = False
    while True:
        request = json.loads(client.recv(1024))
        print(request['data'])
        print("IP client connecté: ", socket.gethostbyname(socket.gethostname()))
        if request['op'] == "quit":
            print("Sortie en cours...")
            c.close()
            _thread.exit()
            break
        else:
            op = request['op']
            data = request['data']
            if op == "CONNECT":
                auth = bdd.user_auth(data)
                if not auth:
                    reply = "Connexion impossible"
                    code = 4
                else:
                    reply = "Connecté avec succès"
                    code = 0
            elif auth or op.startswith("GET_"):
                code, reply = handle_request(op, data)
            else:
                reply = ""
                code = 5
            c.send(json.dumps((code, reply)).encode())

while True:
    client, infosclient = serveur.accept()
    _thread.start_new_thread(client_handle, (client,))

serveur.close()

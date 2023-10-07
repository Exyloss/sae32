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


def handle_command(op, data, c):
    if op == "NEW_PROMO": # Commande d'ajout d'une nouvelle promotion
        bdd.new_promo(data['promo'])
        c.send("message reçu.".encode())
    elif op == "GET_STUDENT_MEAN": # Commande permettant de récupérer la moyenne d'un étudiant
        mean = bdd.get_student_mean(data['etud'])
        reply = {"reply": mean}
        reply = json.dumps(reply)
        c.send(reply.encode())
    elif op == "GET_PROMO_MEAN": # Commande permettant de récupérer la moyenne d'une promotion
        if data.get("promo") is not None:
            mean = bdd.get_promo_mean(data['promo'])
            reply = {"reply": mean}
            reply = json.dumps(reply)
            c.send(reply.encode())
    elif op == "NEW_STUDENT": # Commande d'ajout d'un nouvel étudiant
        promo_id = bdd.get_promo_id(data['promo'])
        if promo_id != -1:
            data['promo'] = promo_id
            bdd.new_student(data)
            c.send("étudiant créé".encode())
        else:
            c.send("erreur".encode())
    elif op == "NEW_MARK": # Commande d'ajout d'une nouvelle note
        bdd.new_mark(data)
        c.send("note ajoutée avec succés.".encode())
    elif op == "GET_PROMO_BY_NAME": # Commande permettant de lister les promotions en fonction d'un nom
        c.send(str(bdd.get_promo_by_name(data['promo'])).encode())
    elif op == "GET_STUDENTS_BY_PROMO":
        c.send(str(bdd.get_students_by_promo(data['promo'])).encode())


def client_handle(c):
    ids = client.recv(1024).decode("utf-8")
    ids = json.loads(ids)
    auth = bdd.user_auth(ids)
    if not auth:
        c.send("connexion impossible".encode())
        c.close()
        _thread.exit()
    else:
        c.send("connecté".encode())

    while True:
        request = client.recv(1024).decode("utf-8")
        req_json = json.loads(request) # On convertit la chaine de caractères en json
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
            handle_command(op, data, c)

while True:
    client, infosclient = serveur.accept()
    _thread.start_new_thread(client_handle, (client,))

serveur.close()

#!/usr/bin/env python3
import socket
import json
import _thread
import bdd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", "-v", help="Rendre le programme bavard", action="store_true")
args = parser.parse_args()

# initialisation du serveur
serveur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serveur.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serveur.bind(('', 3000)) # Ecoute sur le port 3000
serveur.listen()

COMMANDS = [
    "NEW_PROMO",
    "GET_STUDENT_MEAN",
    "GET_PROMO_MEAN",
    "NEW_STUDENT",
    "NEW_MARK",
    "GET_STUDENTS_BY_PROMO",
    "CONNECT"
]

def handle_request(op, data):
    reply = ""
    code = 1
    if op == "NEW_PROMO": # Commande d'ajout d'une nouvelle promotion
        if "promo" in data:
            code = bdd.new_promo(data['promo'])

    elif op == "GET_STUDENT_MEAN": # Commande permettant de récupérer la moyenne d'un étudiant
        if "etud" in data:
            code, reply = bdd.get_student_mean(data['etud'])

    elif op == "GET_PROMO_MEAN": # Commande permettant de récupérer la moyenne d'une promotion
        if "promo" in data:
            promo_id = bdd.get_promo_id(data['promo'])
            if promo_id == -1:
                code = 2
            else:
                code, reply = bdd.get_promo_mean(promo_id)

    elif op == "NEW_STUDENT": # Commande d'ajout d'un nouvel étudiant
        if "nom" in data and "prenom" in data and "promo" in data :
            promo_id = bdd.get_promo_id(data['promo'])
            if promo_id == -1:
                code = 2
            else:
                data['promo'] = promo_id
                code = bdd.new_student(data)

    elif op == "NEW_MARK": # Commande d'ajout d'une nouvelle note
        if "note" in data and "coef" in data:
            code = bdd.new_mark(data)

    elif op == "GET_PROMO_BY_NAME": # Commande permettant de lister les promotions en fonction d'un nom
        if "promo" in data:
            code, reply = bdd.get_promo_by_name(data['promo'])

    elif op == "GET_STUDENTS_BY_PROMO":
        if "promo" in data:
            promo_id = bdd.get_promo_id(data['promo'])
            if promo_id == -1:
                code = 2
            else:
                code, reply = bdd.get_students_by_promo(promo_id)
    else:
        code = 3
    return (code, reply)


def client_handle(c, infos):
    if args.verbose:
        print(f"{infosclient} s'est connecté.")

    auth = False
    while True:
        try:
            request = client.recv(1024)
        except:
            if args.verbose:
                print(f"Déconnexion violente de {infos}")
            c.close()
            _thread.exit()
        try:
            request = json.loads(request)
        except:
            if args.verbose:
                reply_str = json.dumps((1, ""))
                print(reply_str)
            c.send(reply_str.encode())
            continue

        if args.verbose:
            print(f"de {infos} : {request}")
        if request['op'] == "quit":
            if args.verbose:
                print(f"Déconnexion de {infos}")
            c.send(json.dumps((0, "disconnected")).encode())
            c.close()
            _thread.exit()
            break
        else:
            op = request['op']
            data = request['data']
            if op not in COMMANDS:
                code = 3
                reply = ""
            elif op == "CONNECT":
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
            str_reply = json.dumps((code, reply))
            if args.verbose:
                print("->", str_reply)
            c.send(str_reply.encode())

while True:
    client, infosclient = serveur.accept()
    _thread.start_new_thread(client_handle, (client, infosclient))

serveur.close()

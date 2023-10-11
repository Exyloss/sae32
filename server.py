#!/usr/bin/env python3
import socket
import json
import _thread
import bdd
import argparse

# Paramètre de la commande permettant de rendre le programme verbeux
parser = argparse.ArgumentParser()
parser.add_argument("--verbose",
                    "-v",
                    help="Rendre le programme bavard",
                    action="store_true")
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
    "AUTH"
]

def handle_request(op, data):
    reply = ""
    code = 1
    if op == "NEW_PROMO": # Commande d'ajout d'une nouvelle promotion
        if "promo" in data and isinstance("promo", str):
            promo_id = bdd.get_promo_id(data["promo"])
            if promo_id == -1:
                bdd.new_promo(data['promo'])
                code = 0
            else:
                code = 6

    elif op == "GET_STUDENT_MEAN": # Commande permettant de récupérer la moyenne d'un étudiant
        if "nom" in data and "prenom" in data and "promo" in data:
            student_id = bdd.get_student_id(data)
            if student_id != -1:
                reply = bdd.get_student_mean(student_id)
                code = 0
            else:
                code = 2

    elif op == "GET_PROMO_MEAN": # Commande permettant de récupérer la moyenne d'une promotion
        if "promo" in data:
            promo_id = bdd.get_promo_id(data['promo'])
            if promo_id == -1:
                code = 2
            else:
                reply = bdd.get_promo_mean(promo_id)
                code = 0

    elif op == "NEW_STUDENT": # Commande d'ajout d'un nouvel étudiant
        if "nom" in data and "prenom" in data and "promo" in data:
            etud_id = bdd.get_student_id(data)
            promo_id = bdd.get_promo_id(data["promo"])
            if etud_id == -1:
                data['promo'] = promo_id
                bdd.new_student(data)
                code = 0
            else:
                code = 6

    elif op == "NEW_MARK": # Commande d'ajout d'une nouvelle note
        if "note" in data and "coef" in data and "etud" in data and \
                "nom" in data["etud"] and "prenom" in data["etud"] and "promo" in data["etud"]:
            etud_id = bdd.get_student_id(data["etud"])
            if etud_id != -1:
                data["etud"] = etud_id
                bdd.new_mark(data)
                code = 0
            else:
                code = 2

    elif op == "GET_STUDENTS_BY_PROMO": # Obtenir la liste des étudiants par promotion avec leurs notes
        if "promo" in data:
            promo_id = bdd.get_promo_id(data['promo'])
            if promo_id == -1:
                code = 2
            else:
                reply = bdd.get_students_by_promo(promo_id)
                code = 0
    else:
        code = 3
    return (code, reply)


def client_handle(c, infos):
    if args.verbose:
        print(f"{infosclient} s'est connecté.")

    auth = False
    while True:
        try:
            request = c.recv(1024) # Réception des données du client
        except:
            if args.verbose:
                print(f"Déconnexion de {infos}")
            c.close()
            _thread.exit()
        try:
            request = json.loads(request) # On transforme la chaine de caractères en JSON
            op = request['op'] # Nom de la commande appellée
            data = request['data'] # Données envoyées avec la commande
        except: # S'il y a une erreur dans la lecture du JSON :
            reply_str = json.dumps((1, ""))
            if args.verbose:
                print(reply_str)
            c.send(reply_str.encode())
            continue

        if args.verbose:
            print(f"de {infos} : {request}")

        if request['op'] == "quit":
            if args.verbose:
                print(f"Déconnexion de {infos}")
            c.close()
            _thread.exit()

        else:
            reply = ""
            if op not in COMMANDS: # Si la commande demandée n'existe pas
                code = 3

            elif not isinstance(data, dict):
                code = 2

            elif op == "AUTH": # Si l'utilisateur veut se connecter
                auth = bdd.user_auth(data)
                if not auth: # Si l'authentification échoue
                    reply = "Authentification impossible"
                    code = 4
                else:
                    reply = "Authentifié avec succès"
                    code = 0

            elif auth or op.startswith("GET_"): # Si l'utilisateur est connecté ou que la commande commence par GET
                code, reply = handle_request(op, data) # On traite les données

            else:
                code = 5

            str_reply = json.dumps((code, reply))
            if args.verbose:
                print("->", str_reply)

            c.send(str_reply.encode()) # Envoi de la réponse au format (code, données)

while True:
    client, infosclient = serveur.accept() # On accepte les connexions entrantes
    _thread.start_new_thread(client_handle, (client, infosclient)) # A chaque nouvelle connexion, on ouvre un nouveau thread

serveur.close()

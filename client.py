#!/usr/bin/env python3
import socket
import json
import getpass

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 3000))
mes = ""

ERRORS = [
    "Succès",
    "Requête malformée",
    "Données demandées inexistantes",
    "Commande appellée inexistante",
    "Identifiants incorrects",
    "Vous n'avez pas les privilèges pour effectuer cette requête"
]

while mes != "quit":
    mes = input(">")
    op = mes.split(" ")[0]

    if op == "NEW_STUDENT":
        nom = input("Nom de l'étudiant>")
        prenom = input("Prénom de l'étudiant>")
        promo = input("Promotion de l'étudiant>")
        data = {"nom": nom, "prenom": prenom, "promo": promo}

    elif op == "NEW_PROMO":
        name = " ".join(mes.split(" ")[1:])
        data = {"name": name}

    elif op == "GET_PROMO_MEAN":
        promo = mes.split(" ")[1]
        data = {"promo": promo}

    elif op == "GET_STUDENT_MEAN":
        student = mes.split(" ")[1]
        data = {"etud": student}

    elif op == "NEW_MARK":
        student = int(mes.split(" ")[1])
        note = int(input("note de l'étudiant>"))
        coef = int(input("coefficient de la note>"))
        data = {"etud": student, "note": note, "coef": coef}

    elif op == "GET_PROMO_BY_NAME":
        promo = " ".join(mes.split(" ")[1:])
        data = {"promo": promo}

    elif op == "GET_STUDENTS_BY_NAME":
        data = {"promo": promo}

    elif op == "GET_STUDENTS_BY_PROMO":
        promo = " ".join(mes.split(" ")[1:])
        data = {"promo": promo}
        data = {"promo": int(promo)}

    elif op == "CONNECT":
        user = input("login>")
        passwd = getpass.getpass('passwd>')
        data = {"user": user, "pass": passwd}

    elif op == "quit":
        data = ""

    json_data = {
        "op": op, # Nom de la commande
        "data": data # Données nécessaires
    }
    client.sendall(json.dumps(json_data).encode()) # Envoi des données
    data = json.loads(client.recv(1024).decode('utf-8'))
    if data[0] == 0:
        print("Résultat:")
        print(data[1])
    else:
        print("erreur, code",data[0])
        print(ERRORS[data[0]])
client.close()

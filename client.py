#!/usr/bin/env python3
import socket
import json
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 3000))
mes = ""
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
    elif op == "quit":
        data = ""

    json_data = {
        "op": op, # Nom de la commande
        "data": data # Données nécessaires
    }
    client.sendall(json.dumps(json_data).encode()) # Envoi des données
    data = client.recv(1024) # Réception de la réponse du serveur
    print(data.decode('utf-8'))
client.close()

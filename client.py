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
    "Vous n'avez pas les privilèges pour effectuer cette requête",
    "Les données existent déjà"
]

COMMANDS = [
    ["NEW_PROMO", "Créer une nouvelle promotion"],
    ["NEW_STUDENT", "Ajouter un nouvel étudiant à une promotion"],
    ["NEW_MARK", "Ajouter une nouvelle note à un étudiant"],
    ["GET_STUDENT_MEAN", "Obtenir la moyenne d'un étudiant"],
    ["GET_PROMO_MEAN", "Obtenir la moyenne d'une promotion"],
    ["GET_STUDENTS_BY_PROMO", "Obtenir la liste des étudiants par promotion avce leurs notes"],
    ["AUTH", "S'authentifier"]
]

print("Commandes possibles :")
for i in COMMANDS:
    print(i[0], "->", i[1])
print()


while mes != "quit":
    mes = input(">")
    op = mes.split(" ")[0]

    if op == "NEW_STUDENT":
        nom = input("Nom de l'étudiant>")
        prenom = input("Prénom de l'étudiant>")
        promo = input("Promotion de l'étudiant>")
        data = {"nom": nom, "prenom": prenom, "promo": promo}

    elif op == "NEW_PROMO":
        name = input("Nom de la nouvelle promotion>")
        data = {"promo": name}

    elif op == "GET_PROMO_MEAN":
        promo = input("Nom de la promotion>")
        data = {"promo": promo}

    elif op == "GET_STUDENT_MEAN":
        nom = input("Nom de l'étudiant>")
        prenom = input("Prénom de l'étudiant>")
        promo = input("Promotion de l'étudiant>")
        data = {"nom": nom, "prenom": prenom, "promo": promo}

    elif op == "NEW_MARK":
        nom = input("Nom de l'étudiant>")
        prenom = input("Prénom de l'étudiant>")
        promo = input("Promotion de l'étudiant>")
        note = int(input("note de l'étudiant>"))
        coef = int(input("coefficient de la note>"))
        data = {"etud": {"nom": nom, "prenom": prenom, "promo": promo}, "note": note, "coef": coef}

    elif op == "GET_STUDENTS_BY_PROMO":
        promo = input("Nom de la promotion>")
        data = {"promo": promo}

    elif op == "AUTH":
        user = input("login>")
        passwd = getpass.getpass('passwd>')
        data = {"user": user, "pass": passwd}

    elif op == "quit":
        data = ""
        client.sendall(json.dumps({"op": op, "data": ""}).encode()) # Envoi des données
        quit()

    else:
        print("erreur, commande invalide.")
        continue

    json_data = {
        "op": op, # Nom de la commande
        "data": data # Données nécessaires
    }
    print("->", json_data)
    client.sendall(json.dumps(json_data).encode()) # Envoi des données
    data = json.loads(client.recv(1024).decode('utf-8'))
    if data[0] == 0:
        print("Résultat (Succès):")
        print(data[1])
    else:
        print("erreur, code",data[0])
        print(ERRORS[data[0]])
client.close()

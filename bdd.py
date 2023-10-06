#!/usr/bin/env python3
import sqlite3

def new_promo(name: str):
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    params = (name,)
    cur.execute("INSERT INTO promotions(name) VALUES (?);", params)
    con.commit()
    con.close()

def new_student(data: dict):
    """
    entrée: {nom, prenom, id_promo}
    """
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    params = (data['nom'], data['prenom'], data['promo'],)
    cur.execute("INSERT INTO etudiants(nom, prenom, idPromo) VALUES (?, ?, ?);", params)
    con.commit()
    con.close()

def new_mark(data: dict):
    """
    entrée: {note, coef, idEtud}
    """
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    params = (data['note'], data['coef'], data['etud'],)
    cur.execute("INSERT INTO notes(note, coef, idEtud) VALUES(?, ?, ?)", params)
    con.commit()
    con.close()

def get_promo_id(promo: str)->int:
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    params = (promo,)
    cur.execute("SELECT idPromo FROM promotions WHERE name=?;", params)
    promo_id = cur.fetchall()
    if len(promo_id) == 0:
        return -1
    else:
        return promo_id[0][0]

def get_student_mean(etud: int)->float:
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    params = (etud,)
    cur.execute("SELECT note, coef FROM notes WHERE idEtud=?;", params)
    marks = cur.fetchall()
    n = 0
    d = 0
    for i in marks:
        d += i[1]
        n += i[1]*i[0]
    return n/d

def get_promo_mean(promo: int)->float:
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    params = (promo,)
    cur.execute("SELECT idEtud FROM etudiants WHERE idPromo=?;", params)
    students = cur.fetchall()
    n = 0
    d = len(students)
    for i in students:
        print(i)
        n += get_student_mean(i[0])
    return n/d

def get_promo_by_name(promo: str)->list:
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    promo = f"%{promo}%"
    params = (promo,)
    cur.execute("SELECT * FROM promotions WHERE name LIKE ?", params)
    result = []
    for i in cur.fetchall():
        result.append({"id": i[0], "name": i[1]})
    return result

def get_etud_by_name(etud: dict)->list:
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    params = (nom, prenom)
    cur.execute("SELECT * FROM etudiants WHERE nom LIKE '%?%' AND prenom LIKE '%?%';", params)
    result = []
    for i in cur.fetchall():
        result.append({"id": i[0], "name": i[1]})
    return result

def get_students_by_promo(promo: int)->list:
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    params = (promo,)
    cur.execute("SELECT * FROM etudiants WHERE idPromo=?;", params)
    result = []
    for i in cur.fetchall():
        result.append({"idEtud": i[0], "nom": i[1], "prenom": i[2], "idPromo": i[3]})
    return result

#new_student({"nom": "LE NOOB", "prenom": "Yoan", "promo": 1})
#new_promo("RT1")
#new_mark({"note": 14, "coef": 3, "etud": 1})
#print(get_promo_mean({"promo": 1}))

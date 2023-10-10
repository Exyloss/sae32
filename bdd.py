#!/usr/bin/env python3
import sqlite3

def user_auth(data: dict)->bool:
    """
    entrée : { "user": $username, "pass": $password }
    """
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    params = (data["user"], data["pass"])
    cur.execute("SELECT * FROM users WHERE user=? AND passwd=?;", params)
    result = len(cur.fetchall()) != 0
    con.close()
    return result

def new_promo(name: str):
    """
    entrée : { "name": $promo_name }
    """
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    params = (name,)
    cur.execute("INSERT INTO promotions(name) VALUES (?);", params)
    con.commit()
    con.close()

def new_student(data: dict):
    """
    entrée: { "nom": $nom, "prenom": $prenom, "promo": $idPromo }
    """
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    params = (data['nom'], data['prenom'], data['promo'])
    cur.execute("INSERT INTO etudiants(nom, prenom, idPromo) VALUES (?, ?, ?);", params)
    con.commit()
    con.close()

def new_mark(data: dict):
    """
    entrée: { "note": $note, "coef": $coef}
    """
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    params = (data['note'], data['coef'], data['etud'])
    cur.execute("INSERT INTO notes(note, coef, idEtud) VALUES(?, ?, ?)", params)
    con.commit()
    con.close()

def get_promo_id(promo: str)->int:
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    params = (promo,)
    cur.execute("SELECT idPromo FROM promotions WHERE name=?;", params)
    promo_id = cur.fetchall()
    con.close()
    if len(promo_id) == 0:
        return -1
    else:
        return promo_id[0][0]

def get_student_mean(etud: int)->float:
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    params = (etud,)
    cur.execute("SELECT note, coef FROM notes WHERE idEtud=?;", params)
    n = 0
    d = 0
    for i in cur.fetchall():
        d += i[1]
        n += i[1]*i[0]
    return n/d

def get_promo_mean(promo: int)->float:
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    params = (promo,)
    cur.execute("SELECT idEtud FROM etudiants WHERE idPromo=?;", params)
    n = 0
    d = 0
    for i in cur.fetchall():
        n += get_student_mean(i[0])
        d += 1
    con.close()
    return n/d

def get_students_by_promo(promo: int)->list:
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    params = (promo,)
    cur.execute("SELECT etudiants.idEtud, nom, prenom, note, coef \
                FROM etudiants \
                JOIN notes ON notes.idEtud = etudiants.idEtud WHERE idPromo=?;", params)
    result = []
    for i in cur.fetchall():
        if i[0] not in [j["idEtud"] for j in result]:
            result.append({"idEtud": i[0], "nom": i[1], "prenom": i[2], "notes": [(i[3], i[4])]})
        else:
            k = 0
            while result[k]["idEtud"] != i[0]:
                k += 1
            result[k]["notes"].append((i[3], i[4]))

    con.close()
    return result

def get_student_id(data: dict)->int:
    con = sqlite3.connect("bdd.db")
    cur = con.cursor()
    promo_id = get_promo_id(data["promo"])
    params = (data["nom"], data["prenom"], promo_id)
    cur.execute("SELECT idEtud FROM etudiants WHERE nom=? AND prenom=? AND idPromo=?;", params)
    values = cur.fetchall()
    con.close()
    if len(values) == 0:
        id_etud = -1
    else:
        id_etud = values[0][0]

    return id_etud

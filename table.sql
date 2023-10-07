BEGIN TRANSACTION;

DROP TABLE IF EXISTS promotions;

CREATE TABLE promotions
(
    idPromo	    INTEGER    PRIMARY KEY AUTOINCREMENT,
    name	    TEXT	   NOT NULL
);

DROP TABLE IF EXISTS etudiants;

CREATE TABLE etudiants
(
    idEtud	 INTEGER	PRIMARY KEY AUTOINCREMENT,
    nom	     TEXT	    NOT NULL,
    prenom   TEXT		NOT NULL,
    idPromo	 INTEGER   	NOT NULL,
    FOREIGN KEY(idPromo) REFERENCES promotions(idPromo)
);

DROP TABLE IF EXISTS notes;

CREATE TABLE notes
(
    idNote	INTEGER	PRIMARY KEY AUTOINCREMENT,
    note	INTEGER	NOT NULL,
    coef	INTEGER	NOT NULL,
    idEtud  INTEGER NOT NULL,
    FOREIGN KEY(idEtud) REFERENCES etudiants(idEtud)
);

DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    idUser	INTEGER	PRIMARY KEY AUTOINCREMENT,
    user	INTEGER	NOT NULL,
    passwd	INTEGER	NOT NULL
);


COMMIT;

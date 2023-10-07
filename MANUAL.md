# Structure du format JSON pour chaque type de requête

NEW_PROMO :

```json
{
    "op": "NEW_PROMO",
    "data": {"name": $promo_name}
}
```

NEW_STUDENT :

```json
{
    "op": "NEW_STUDENT",
    "data": {
        "nom": $nom,
        "prenom": $prenom,
        "promo": $idpromo
    }
}
```

GET_STUDENT_MEAN :

```json
{
    "op": "GET_STUDENT_MEAN",
    "data": {
        "etud": $idetud
    }
}
```

GET_PROMO_MEAN :

```json
{
    "op": "GET_STUDENT_MEAN",
    "data": {
        "etud": $idpromo
    }
}
```

NEW_MARK :

```json
{
    "op": "NEW_MARK",
    "data": {
        "note": $note,
        "coef": $coef,
        "etud": $idetud
    }
}
```

CONNECT :

```json
{
    "op": "CONNECT",
    "data": {
        "user": $user,
        "pass": $pass
    }
}
```

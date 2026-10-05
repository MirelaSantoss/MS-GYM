import mysql.connector


def conectar_banco():
    banco = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Lela@2009",
        database="academia"
    )

    return banco
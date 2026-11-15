from werkzeug.security import generate_password_hash, check_password_hash
from app.db import DatabaseConnection

class Usuario:
    def __init__(self, username, password=None, password_hash=None, tipo="aluno", id=None):
        self.id = id
        self.username = username
        self.tipo = tipo
        self.password_hash = password_hash or (
            generate_password_hash(password) if password else None
        )

    def salvar(self):
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT id FROM usuarios WHERE username = ?", (self.username,))
            if db.cursor.fetchone() is not None:
                return False

            sql = "INSERT INTO usuarios (username, password_hash, tipo) VALUES (?, ?, ?)"
            db.cursor.execute(sql, (self.username, self.password_hash, self.tipo))
            self.id = db.cursor.lastrowid
            return True

    @classmethod
    def listar(cls):
        sql = "SELECT id, username, password_hash, tipo FROM usuarios ORDER BY username"
        with DatabaseConnection() as db:
            db.cursor.execute(sql)
            rows = db.cursor.fetchall()
            return [
                cls(id=row['id'], username=row['username'], password_hash=row['password_hash'], tipo=row['tipo'])
                for row in rows
            ]

    @classmethod
    def autenticar(cls, username, password):
        sql = "SELECT id, username, password_hash, tipo FROM usuarios WHERE username = ?"
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (username,))
            row = db.cursor.fetchone()

        if row and check_password_hash(row['password_hash'], password):
            return cls(id=row['id'], username=row['username'], password_hash=row['password_hash'], tipo=row['tipo'])
        return None

    @classmethod
    def buscar_por_id(cls, user_id):
        sql = "SELECT id, username, password_hash, tipo FROM usuarios WHERE id = ?"
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (user_id,))
            row = db.cursor.fetchone()

        if row:
            return cls(id=row['id'], username=row['username'], password_hash=row['password_hash'], tipo=row['tipo'])
        return None

    @classmethod
    def excluir(cls, user_id):
        sql = "DELETE FROM usuarios WHERE id = ?"
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (user_id,))
            return db.cursor.rowcount > 0
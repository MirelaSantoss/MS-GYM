
from werkzeug.security import generate_password_hash, check_password_hash
from app.bd import DatabaseConnection
import sqlite3


class Usuario:
    """Classe responsável pelas operações dos usuários no banco."""

    def __init__(self, usuario, senha=None, tipo=None, id=None):
        self.id = id
        self.usuario = usuario
        self.tipo = tipo

        # Transforma a senha em um hash antes de armazená-la.
        self.senha = generate_password_hash(senha) if senha else None

    def salvar(self):
        """Insere um novo usuário no banco de dados."""

        try:
            with DatabaseConnection() as db:

                # Verifica se o usuário já está cadastrado.
                db.cursor.execute(
                    "SELECT id FROM usuarios WHERE usuario = ?",
                    (self.usuario,)
                )

                if db.cursor.fetchone() is not None:
                    return False

                # Insere o novo usuário.
                db.cursor.execute("""
                    INSERT INTO usuarios (usuario, senha, tipo)
                    VALUES (?, ?, ?)
                """, (self.usuario, self.senha, self.tipo))

                self.id = db.cursor.lastrowid

            return True

        except sqlite3.IntegrityError:
            return False

    @classmethod
    def autenticar(cls, usuario, senha):
        """Verifica se o usuário e a senha estão corretos."""

        with DatabaseConnection() as db:

            db.cursor.execute("""
                SELECT id, usuario, senha, tipo
                FROM usuarios
                WHERE usuario = ?
            """, (usuario,))

            registro = db.cursor.fetchone()

            if registro is None:
                return None

            senha_banco = registro["senha"]

            # Verifica senhas armazenadas no formato hash.
            try:
                senha_correta = check_password_hash(senha_banco, senha)
            except (ValueError, TypeError):
                senha_correta = False

            # Compatibilidade com usuários cadastrados anteriormente
            # que ainda possuem senha em texto simples.
            if not senha_correta and senha_banco == senha:

                nova_senha = generate_password_hash(senha)

                db.cursor.execute("""
                    UPDATE usuarios
                    SET senha = ?
                    WHERE id = ?
                """, (nova_senha, registro["id"]))

                senha_correta = True

            if senha_correta:
                return {
                    "id": registro["id"],
                    "usuario": registro["usuario"],
                    "tipo": registro["tipo"]
                }

            return None

    @classmethod
    def listar(cls):
        """Retorna todos os usuários cadastrados."""

        with DatabaseConnection() as db:

            db.cursor.execute("""
                SELECT id, usuario, tipo
                FROM usuarios
                ORDER BY id DESC
            """)

            registros = db.cursor.fetchall()

            return [dict(registro) for registro in registros]

    @classmethod
    def buscar_por_id(cls, id):
        """Busca um usuário específico pelo seu ID."""

        with DatabaseConnection() as db:

            db.cursor.execute("""
                SELECT id, usuario, tipo
                FROM usuarios
                WHERE id = ?
            """, (id,))

            registro = db.cursor.fetchone()

            return dict(registro) if registro else None

import os
import sqlite3


class Usuario:
    """Modelo Usuario: concentra toda a comunicação com o SQLite."""

    def __init__(self, usuario, senha, tipo, id=None):
        self.id = id
        self.usuario = usuario
        self.senha = senha
        self.tipo = tipo

    @staticmethod
    def conectar():
        """Abre uma conexão com o arquivo database.db."""
        pasta_projeto = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        caminho_banco = os.path.join(pasta_projeto, "database.db")
        conexao = sqlite3.connect(caminho_banco)
        conexao.row_factory = sqlite3.Row
        return conexao

    @classmethod
    def criar_tabela(cls):
        """Cria a tabela caso ela ainda não exista."""
        conexao = cls.conectar()
        conexao.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL
            )
        """)
        conexao.commit()
        conexao.close()

    def salvar(self):
        """Insere este objeto Usuario na tabela."""
        conexao = self.conectar()
        try:
            conexao.execute(
                "INSERT INTO usuarios (usuario, senha, tipo) VALUES (?, ?, ?)",
                (self.usuario, self.senha, self.tipo)
            )
            conexao.commit()
            return True
        except sqlite3.IntegrityError:
            conexao.rollback()
            return False
        finally:
            conexao.close()

    @classmethod
    def listar(cls):
        """Busca todos os usuários cadastrados e devolve uma lista."""
        conexao = cls.conectar()
        registros = conexao.execute(
            "SELECT id, usuario, tipo FROM usuarios ORDER BY id DESC"
        ).fetchall()
        conexao.close()
        return [dict(registro) for registro in registros]

    @classmethod
    def autenticar(cls, usuario, senha):
        """Confere usuário e senha no banco. Retorna os dados ou None."""
        conexao = cls.conectar()
        registro = conexao.execute(
            "SELECT id, usuario, tipo FROM usuarios WHERE usuario = ? AND senha = ?",
            (usuario, senha)
        ).fetchone()
        conexao.close()
        return dict(registro) if registro else None

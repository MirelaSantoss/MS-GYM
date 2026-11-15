
import os
import sqlite3


class DatabaseConnection:
    """Gerencia a conexão com o banco de dados SQLite."""

    def __init__(self):
        # Localiza a pasta principal do projeto.
        pasta_projeto = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        # Define o caminho do banco de dados.
        self.caminho_banco = os.path.join(
            pasta_projeto, "database.db"
        )

    def __enter__(self):
        # Abre a conexão com o banco.
        self.conexao = sqlite3.connect(self.caminho_banco)

        # Permite acessar os registros pelos nomes das colunas.
        self.conexao.row_factory = sqlite3.Row

        # Cria o cursor para executar comandos SQL.
        self.cursor = self.conexao.cursor()

        return self

    def __exit__(self, tipo_erro, erro, traceback):
        # Se não ocorreu erro, confirma as alterações.
        if tipo_erro is None:
            self.conexao.commit()
        else:
            # Se ocorreu erro, desfaz as alterações.
            self.conexao.rollback()

        # Fecha o cursor e a conexão.
        self.cursor.close()
        self.conexao.close()

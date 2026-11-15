import sqlite3
import os

# Define o caminho absoluto para o banco de dados na raiz do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'database.db')

class DatabaseConnection:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Abre a conexão com o SQLite
        self.conn = sqlite3.connect(self.db_path)
        # Configura row_factory para permitir acesso às colunas pelo nome (ex: row['id'])
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        # Ativa restrições de chave estrangeira no SQLite
        self.cursor.execute("PRAGMA foreign_keys = ON")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Se nenhum erro ocorreu dentro do bloco with, faz o commit automático
        if exc_type is None:
            self.conn.commit()
        else:
            # Se ocorreu qualquer exceção, desfaz as alterações (rollback)
            self.conn.rollback()
        # Sempre fecha a conexão para liberar o arquivo
        self.conn.close()
import sqlite3
import os

def inicializar_banco():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "database.db")
    
    print(f"Criando banco de dados em: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            tipo TEXT DEFAULT 'aluno'
        )
    """)

    # Tabela de alunos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            idade INTEGER,
            objetivo TEXT,
            usuario_id INTEGER,
            ultima_mensalidade TEXT,
            proxima_mensalidade TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)

    # Tabela de professores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS professores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            especialidade TEXT,
            telefone TEXT,
            usuario_id INTEGER,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)

    # Tabela de equipamentos da academia (Cadastrados pelo Admin com foto local)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipamentos_academia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            foto_url TEXT NOT NULL,
            descricao TEXT
        )
    """)

    # Tabela de treinos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS treinos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            maquina TEXT NOT NULL,
            foto_url TEXT,
            descricao TEXT,
            series TEXT,
            repeticoes TEXT,
            aluno_id INTEGER,
            usuario_id INTEGER,
            FOREIGN KEY (aluno_id) REFERENCES alunos (id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)

    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

if __name__ == "__main__":
    inicializar_banco()
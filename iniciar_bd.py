
from app.bd import DatabaseConnection


def iniciar_banco():
    """Cria as tabelas necessárias para o MS GYM."""

    with DatabaseConnection() as db:

        # Cria a tabela de usuários, caso ainda não exista.
        db.cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                tipo TEXT NOT NULL
            )
        """)

    print("Banco de dados inicializado com sucesso!")


if __name__ == "__main__":
    iniciar_banco()

from app.database import conectar_banco


def autenticar_usuario(usuario, senha):

    banco = conectar_banco()

    cursor = banco.cursor(dictionary=True)

    sql = """
        SELECT id, usuario, senha, tipo
        FROM usuarios
        WHERE usuario = %s
        AND senha = %s
    """

    cursor.execute(
        sql,
        (usuario, senha)
    )

    usuario_data = cursor.fetchone()

    cursor.close()
    banco.close()

    if not usuario_data:
        return None

    return {
        "id": usuario_data["id"],
        "usuario": usuario_data["usuario"],
        "tipo": usuario_data["tipo"]
    }

# parte do cadastro 

def cadastrar_usuario(usuario, senha, tipo):

    banco = conectar_banco()

    cursor = banco.cursor()

    sql = """
        INSERT INTO usuarios (usuario, senha, tipo)
        VALUES (%s, %s, %s)
    """

    try:

        cursor.execute(
            sql,
            (usuario, senha, tipo)
        )

        banco.commit()

        cursor.close()
        banco.close()

        return True

    except Exception:

        banco.rollback()

        cursor.close()
        banco.close()

        return False
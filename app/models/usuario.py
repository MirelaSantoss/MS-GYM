USUARIOS = {

    "professor": {
        "id": 1,
        "usuario": "professor",
        "senha": "123456",
        "tipo": "professor"
    },

    "aluno": {
        "id": 2,
        "usuario": "aluno",
        "senha": "123456",
        "tipo": "aluno"
    }

}


def autenticar_usuario(usuario, senha):

    usuario_data = USUARIOS.get(usuario)

    # Usuário não existe
    if not usuario_data:
        return None

    # Senha está errada
    if usuario_data["senha"] != senha:
        return None

    # Login correto
    return {
        "id": usuario_data["id"],
        "usuario": usuario_data["usuario"],
        "tipo": usuario_data["tipo"]
    }
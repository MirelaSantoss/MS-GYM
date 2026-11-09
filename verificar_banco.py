from app.models.usuario import Usuario

# Busca os usuários diretamente pelo método da classe
usuarios = Usuario.listar()

print("\n===== USUÁRIOS CADASTRADOS =====")

for usuario in usuarios:
    print(f"ID: {usuario['id']}")
    print(f"Usuário: {usuario['usuario']}")
    print(f"Tipo: {usuario['tipo']}")
    print("-----------------------------")

if not usuarios:
    print("Nenhum usuário cadastrado.")

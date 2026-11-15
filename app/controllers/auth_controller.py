from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.usuario import Usuario
from app.models.aluno import Aluno
from app.models.professor import Professor

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("main.dashboard"))

    erro = None
    if request.method == "POST":
        username = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "")
        
        usuario_autenticado = Usuario.autenticar(username, senha)

        if usuario_autenticado:
            session.clear()
            session["user_id"] = usuario_autenticado.id
            session["username"] = usuario_autenticado.username
            session["tipo"] = usuario_autenticado.tipo  # Garante que o tipo vai pra sessão
            session.permanent = True
            flash("Login realizado com sucesso!", "sucesso")
            return redirect(url_for("main.dashboard"))

        erro = "Usuário ou senha inválidos."
        flash(erro, "erro")

    return render_template("auth/login.html", erro=erro)


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    erro = None
    if request.method == "POST":
        username = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "")
        tipo = request.form.get("tipo", "aluno").strip()  # Pega o tipo selecionado no HTML

        if not username or not senha:
            erro = "Preencha todos os campos obrigatórios."
        else:
            # Passa o tipo correto para o Model de Usuário
            novo_usuario = Usuario(username=username, password=senha, tipo=tipo)
            if novo_usuario.salvar():
                # Se for aluno ou professor, cria também o registro correspondente nas tabelas auxiliares
                if tipo == "aluno":
                    aluno_obj = Aluno(nome=username, idade=18, objetivo="Geral", usuario_id=novo_usuario.id)
                    aluno_obj.salvar()
                elif tipo == "professor":
                    prof_obj = Professor(nome=username, especialidade="Musculação", telefone="0000-0000", usuario_id=novo_usuario.id)
                    # Caso sua classe Professor tenha método salvar, ele será executado aqui
                
                flash("Cadastro realizado com sucesso! Faça o login.", "sucesso")
                return redirect(url_for("auth.login"))
            
            erro = "Esse usuário já existe. Escolha outro nome."
            
        flash(erro, "erro")

    return render_template("auth/cadastro.html", erro=erro)


@auth_bp.post("/logout")
def logout():
    session.clear()
    flash("Sessão encerrada com sucesso.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/usuarios")
def listar_usuarios():
    usuarios = Usuario.listar()
    return render_template("auth/listagem.html", usuarios=usuarios)
from flask import Blueprint, render_template, request, redirect, url_for, session
from app.models.usuario import autenticar_usuario, cadastrar_usuario


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    # Se já estiver autenticado,
    # vai direto para a página inicial.
    if session.get("usuario_id"):

        return redirect(url_for("home.index"))

    erro = None

    if request.method == "POST":

        usuario = request.form.get("usuario","").strip()

        senha = request.form.get("senha","")

        usuario_autenticado = (
            autenticar_usuario(
                usuario,
                senha
            )
        )

        if usuario_autenticado:

            # Limpa uma sessão anterior.
            session.clear()

            # Cria a sessão autenticada.
            session["usuario_id"] = (
                usuario_autenticado["id"]
            )

            session["usuario"] = (
                usuario_autenticado["usuario"]
            )

            session["tipo"] = (
                usuario_autenticado["tipo"]
            )

            session.permanent = True

            return redirect(
                url_for("home.index")
            )

        erro = (
            "Usuário ou senha inválidos."
        )

    return render_template(
        "auth/login.html",
        erro=erro
    )


@auth_bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():

    erro = None

    if request.method == "POST":

        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "")
        tipo = request.form.get("tipo", "")

        cadastro_realizado = cadastrar_usuario(
            usuario,
            senha,
            tipo
        )

        if cadastro_realizado:

            return redirect(
                url_for("auth.login")
            )

        erro = "Esse usuário já existe."

    return render_template(
        "auth/cadastro.html",
        erro=erro
    )


@auth_bp.post("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("auth.login")
    )
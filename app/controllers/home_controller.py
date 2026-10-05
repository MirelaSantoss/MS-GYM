from flask import Blueprint, render_template, session

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def index():

    usuario = session.get("usuario")

    tipo = session.get("tipo")

    return render_template(
        "home/index.html",
        usuario = usuario,
        tipo = tipo
    )
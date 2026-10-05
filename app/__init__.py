from flask import Flask, session, redirect, url_for, request


def create_app():

    app = Flask( __name__, template_folder="views", static_folder="static")

    # Chave usada pelo Flask para proteger a sessão.
    app.config["SECRET_KEY"] = "minha-chave-secreta"


    # ==========================================
    # BLUEPRINTS
    # ==========================================

    from app.controllers.auth_controller import auth_bp
    from app.controllers.home_controller import home_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)


    # ==========================================
    # MIDDLEWARE
    # ==========================================

    @app.before_request
    def verificar_login():

        # Essas páginas não precisam de login.
        paginas_publicas = {
            "auth.login",
            "static"
        }

        if request.endpoint in paginas_publicas:
            return None

        # Verifica se existe usuário na sessão.
        if not session.get("usuario_id"):

            return redirect(
                url_for("auth.login")
            )

        return None


    return app
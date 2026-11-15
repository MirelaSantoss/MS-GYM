from flask import Flask, session, redirect, url_for, request, render_template

def create_app():
    app = Flask(
        __name__,
        template_folder="views",
        static_folder="static"
    )


    app.config["SECRET_KEY"] = "sua-chave-secreta-bem-segura"


    from app.controllers.auth_controller import auth_bp
    from app.controllers.main_controller import main_bp  # Blueprint com Alunos, Professores e Treinos

  
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # Middleware de Autenticação
    @app.before_request
    def verificar_login():
        # Log de entrada em cada requisição
        app.logger.info(f"--> Requisição recebida: {request.method} {request.path}")

        # Páginas e recursos que podem ser acessados sem login
        paginas_publicas = {
            "auth.cadastro",
            "auth.login",
            "static"
        }

        if request.endpoint in paginas_publicas:
            return None

        # Verifica se existe usuário na sessão 
        if not session.get("user_id"):
            app.logger.warning(f"Acesso negado para rota protegida: {request.path}")
            return redirect(url_for("auth.login"))

        return None

    # Tratamento de Erro 404 
    @app.errorhandler(404)
    def pagina_nao_encontrada(erro):
        app.logger.error(f"Erro 404 - Página não encontrada: {request.path}")
        return "<h1>404</h1><p>Página não encontrada no sistema MS-GYM.</p>", 404

    return app
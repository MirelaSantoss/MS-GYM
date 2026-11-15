from functools import wraps
from flask import session, redirect, url_for, flash, g
from app.models.usuario import Usuario

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = session.get('user_id')
        
        # Valida se o ID na sessão realmente existe no banco de dados
        usuario = Usuario.buscar_por_id(user_id) if user_id else None
        
        if not usuario:
            session.clear()
            flash("Por favor, faça o login para acessar esta página.", "erro")
            return redirect(url_for('auth.login'))
        
        # Disponibiliza o objeto Usuario validado na requisição através do objeto g
        g.usuario = usuario
        return f(*args, **kwargs)
        
    return decorated_function
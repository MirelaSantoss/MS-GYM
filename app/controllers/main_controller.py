import os
from werkzeug.utils import secure_filename
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g, current_app
from app.utils.auth_middleware import login_required
from app.models.professor import Professor
from app.models.aluno import Aluno
from app.models.treino import Treino
from app.models.usuario import Usuario
from app.models.equipamento import Equipamento

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required
def dashboard():
    usuario = g.usuario  
    alunos = Aluno.listar_geral()
    professores = Professor.listar_por_usuario(usuario.id) if hasattr(Professor, 'listar_por_usuario') else []
    equipamentos = Equipamento.listar_todos()
    
    aluno_atual = None
    treinos = []
    if usuario.tipo == 'aluno':
        aluno_atual = Aluno.buscar_por_usuario_id(usuario.id)
        if aluno_atual:
            treinos = Treino.listar_por_aluno(aluno_atual.id)
    else:
        # Se for professor ou admin, traz todos os treinos para poder gerenciar
        treinos = Treino.listar_por_usuario(usuario.id) if usuario.tipo == 'professor' else Treino.listar_por_aluno(alunos[0].id) if alunos else []
        # Para o professor ver todos os treinos cadastrados por ele:
        if usuario.tipo == 'professor':
            treinos = []
            for a in alunos:
                treinos.extend(Treino.listar_por_aluno(a.id))

    return render_template(
        'home/index.html', 
        usuario=usuario, 
        alunos=alunos, 
        professores=professores, 
        treinos=treinos, 
        aluno_atual=aluno_atual,
        equipamentos=equipamentos
    )

# --- ROTAS DE EQUIPAMENTOS (ADMIN) ---
@main_bp.route('/equipamentos/novo', methods=['POST'])
@login_required
def cadastrar_equipamento():
    if g.usuario.tipo != 'admin':
        return redirect(url_for('main.dashboard'))

    nome = request.form.get('nome', '').strip()
    descricao = request.form.get('descricao', '').strip()
    foto = request.files.get('foto')

    if not nome or not foto or foto.filename == '':
        flash('Nome e foto são obrigatórios!', 'erro')
        return redirect(url_for('main.dashboard'))

    filename = secure_filename(foto.filename)
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    foto.save(os.path.join(upload_folder, filename))

    eq = Equipamento(nome=nome, foto_url=f"uploads/{filename}", descricao=descricao)
    eq.salvar()
    flash('Equipamento cadastrado com sucesso!', 'sucesso')
    return redirect(url_for('main.dashboard'))

@main_bp.route('/equipamentos/<int:id>/editar', methods=['POST'])
@login_required
def editar_equipamento(id):
    if g.usuario.tipo != 'admin':
        return redirect(url_for('main.dashboard'))

    nome = request.form.get('nome', '').strip()
    descricao = request.form.get('descricao', '').strip()
    foto = request.files.get('foto')

    eq_antigo = Equipamento.buscar_por_id(id)
    foto_url = eq_antigo.foto_url if eq_antigo else ""

    if foto and foto.filename != '':
        filename = secure_filename(foto.filename)
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        foto.save(os.path.join(upload_folder, filename))
        foto_url = f"uploads/{filename}"

    eq = Equipamento(id=id, nome=nome, foto_url=foto_url, descricao=descricao)
    eq.atualizar()
    flash('Equipamento atualizado com sucesso!', 'sucesso')
    return redirect(url_for('main.dashboard'))

@main_bp.route('/equipamentos/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_equipamento(id):
    if g.usuario.tipo != 'admin':
        return redirect(url_for('main.dashboard'))
    Equipamento.excluir(id)
    flash('Equipamento excluído!', 'sucesso')
    return redirect(url_for('main.dashboard'))


# --- ROTAS DE TREINOS (PROFESSOR) ---
@main_bp.route('/treinos/novo', methods=['POST'])
@login_required
def criar_treino():
    if g.usuario.tipo not in ['professor', 'admin']:
        return redirect(url_for('main.dashboard'))

    categoria = request.form.get('categoria', '').strip()
    equipamento_id = request.form.get('equipamento_id')
    descricao = request.form.get('descricao', '').strip()
    series = request.form.get('series', '').strip()
    repeticoes = request.form.get('repeticoes', '').strip()
    aluno_id = request.form.get('aluno_id')
    
    eq = Equipamento.buscar_por_id(int(equipamento_id))
    novo_treino = Treino(
        categoria=categoria, maquina=eq.nome, foto_url=eq.foto_url,
        descricao=descricao or eq.descricao, series=series, repeticoes=repeticoes,
        aluno_id=int(aluno_id), usuario_id=g.usuario.id
    )
    novo_treino.salvar()
    flash('Treino adicionado com sucesso!', 'sucesso')
    return redirect(url_for('main.dashboard'))

@main_bp.route('/treinos/<int:id>/excluir', methods=['POST'])
@login_required
def excluir_treino(id):
    if g.usuario.tipo not in ['professor', 'admin']:
        return redirect(url_for('main.dashboard'))
    Treino.excluir(id, g.usuario.id)
    flash('Treino removido!', 'sucesso')
    return redirect(url_for('main.dashboard'))
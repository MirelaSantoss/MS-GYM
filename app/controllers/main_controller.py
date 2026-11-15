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
        treinos = Treino.listar_por_usuario(usuario.id)

    return render_template(
        'home/index.html', 
        usuario=usuario, 
        alunos=alunos, 
        professores=professores, 
        treinos=treinos, 
        aluno_atual=aluno_atual,
        equipamentos=equipamentos
    )

@main_bp.route('/equipamentos/novo', methods=['POST'])
@login_required
def cadastrar_equipamento():
    if g.usuario.tipo != 'admin':
        flash('Acesso negado.', 'erro')
        return redirect(url_for('main.dashboard'))

    nome = request.form.get('nome', '').strip()
    descricao = request.form.get('descricao', '').strip()
    foto = request.files.get('foto')  # Recebe o arquivo enviado pelo input file

    if not nome or not foto or foto.filename == '':
        flash('Nome e arquivo de foto do equipamento são obrigatórios!', 'erro')
        return redirect(url_for('main.dashboard'))

    # Salva a imagem na pasta static/uploads do projeto
    filename = secure_filename(foto.filename)
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        
    caminho_completo = os.path.join(upload_folder, filename)
    foto.save(caminho_completo)

    # O caminho relativo que será salvo no banco de dados e lido pelo Jinja
    foto_url = f"uploads/{filename}"

    eq = Equipamento(nome=nome, foto_url=foto_url, descricao=descricao)
    eq.salvar()
    flash('Equipamento e foto cadastrados com sucesso!', 'sucesso')
    return redirect(url_for('main.dashboard'))

@main_bp.route('/treinos/novo', methods=['POST'])
@login_required
def criar_treino():
    if g.usuario.tipo not in ['professor', 'admin']:
        flash('Acesso negado.', 'erro')
        return redirect(url_for('main.dashboard'))

    categoria = request.form.get('categoria', '').strip()
    equipamento_id = request.form.get('equipamento_id')
    descricao = request.form.get('descricao', '').strip()
    series = request.form.get('series', '').strip()
    repeticoes = request.form.get('repeticoes', '').strip()
    aluno_id = request.form.get('aluno_id')
    
    if not categoria or not equipamento_id or not aluno_id:
        flash('Categoria, Equipamento e Aluno são obrigatórios!', 'erro')
        return redirect(url_for('main.dashboard'))
        
    # Busca o equipamento selecionado para puxar automaticamente o nome e a foto cadastrada pelo admin
    eq = Equipamento.buscar_por_id(int(equipamento_id))
    if not eq:
        flash('Equipamento inválido.', 'erro')
        return redirect(url_for('main.dashboard'))

    novo_treino = Treino(
        categoria=categoria,
        maquina=eq.nome,
        foto_url=eq.foto_url,
        descricao=descricao or eq.descricao,
        series=series,
        repeticoes=repeticoes,
        aluno_id=int(aluno_id),
        usuario_id=g.usuario.id
    )
    novo_treino.salvar()
    flash('Equipamento adicionado ao treino do aluno com sucesso!', 'sucesso')
    return redirect(url_for('main.dashboard'))

@main_bp.route('/mensalidade/<int:aluno_id>/atualizar', methods=['POST'])
@login_required
def atualizar_mensalidade(aluno_id):
    if g.usuario.tipo != 'admin':
        flash('Acesso negado.', 'erro')
        return redirect(url_for('main.dashboard'))

    ultima = request.form.get('ultima_mensalidade', '').strip()
    proxima = request.form.get('proxima_mensalidade', '').strip()
    Aluno.atualizar_mensalidade(aluno_id, ultima, proxima)
    flash('Mensalidade atualizada com sucesso!', 'sucesso')
    return redirect(url_for('main.dashboard'))
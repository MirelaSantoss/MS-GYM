from app.db import DatabaseConnection

class Professor:
    def __init__(self, nome, especialidade, telefone, usuario_id, id=None):
        self.id = id
        self.nome = nome
        self.especialidade = especialidade
        self.telefone = telefone
        self.usuario_id = usuario_id

    def salvar(self):
        """Cadastra um novo professor vinculado ao usuário logado."""
        sql = """
            INSERT INTO professores (nome, especialidade, telefone, usuario_id)
            VALUES (?, ?, ?, ?)
        """
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (self.nome, self.especialidade, self.telefone, self.usuario_id))
            self.id = db.cursor.lastrowid
            return self.id

    @classmethod
    def listar_por_usuario(cls, usuario_id):
        """Retorna todos os professores cadastrados pelo usuário logado."""
        sql = "SELECT id, nome, especialidade, telefone, usuario_id FROM professores WHERE usuario_id = ? ORDER BY nome"
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (usuario_id,))
            rows = db.cursor.fetchall()
            return [
                cls(id=r['id'], nome=r['nome'], especialidade=r['especialidade'], 
                    telefone=r['telefone'], usuario_id=r['usuario_id'])
                for r in rows
            ]

    @classmethod
    def buscar_por_id(cls, professor_id, usuario_id):
        """Busca um professor específico garantindo que pertence ao usuário logado."""
        sql = "SELECT id, nome, especialidade, telefone, usuario_id FROM professores WHERE id = ? AND usuario_id = ?"
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (professor_id, usuario_id))
            r = db.cursor.fetchone()
            if r:
                return cls(id=r['id'], nome=r['nome'], especialidade=r['especialidade'], 
                           telefone=r['telefone'], usuario_id=r['usuario_id'])
            return None

    def atualizar(self):
        """Atualiza os dados do professor."""
        sql = """
            UPDATE professores 
            SET nome = ?, especialidade = ?, telefone = ?
            WHERE id = ? AND usuario_id = ?
        """
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (self.nome, self.especialidade, self.telefone, self.id, self.usuario_id))
            return db.cursor.rowcount > 0

    @classmethod
    def excluir(cls, professor_id, usuario_id):
        """Remove um professor validando o dono do registro."""
        sql = "DELETE FROM professores WHERE id = ? AND usuario_id = ?"
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (professor_id, usuario_id))
            return db.cursor.rowcount > 0
from app.db import DatabaseConnection

class Aluno:
    def __init__(self, nome, idade, objetivo, usuario_id, ultima_mensalidade=None, proxima_mensalidade=None, id=None):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.objetivo = objetivo
        self.usuario_id = usuario_id
        self.ultima_mensalidade = ultima_mensalidade
        self.proxima_mensalidade = proxima_mensalidade

    def salvar(self):
        sql = """
            INSERT INTO alunos (nome, idade, objetivo, usuario_id, ultima_mensalidade, proxima_mensalidade)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (self.nome, self.idade, self.objetivo, self.usuario_id, self.ultima_mensalidade, self.proxima_mensalidade))
            self.id = db.cursor.lastrowid
            return self.id

    @classmethod
    def listar_geral(cls):
        sql = "SELECT id, nome, idade, objetivo, usuario_id, ultima_mensalidade, proxima_mensalidade FROM alunos ORDER BY nome"
        with DatabaseConnection() as db:
            db.cursor.execute(sql)
            rows = db.cursor.fetchall()
            return [cls(id=r['id'], nome=r['nome'], idade=r['idade'], objetivo=r['objetivo'], 
                        usuario_id=r['usuario_id'], ultima_mensalidade=r['ultima_mensalidade'], 
                        proxima_mensalidade=r['proxima_mensalidade']) for r in rows]

    @classmethod
    def buscar_por_usuario_id(cls, usuario_id):
        sql = "SELECT id, nome, idade, objetivo, usuario_id, ultima_mensalidade, proxima_mensalidade FROM alunos WHERE usuario_id = ?"
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (usuario_id,))
            r = db.cursor.fetchone()
            if r:
                return cls(id=r['id'], nome=r['nome'], idade=r['idade'], objetivo=r['objetivo'], 
                           usuario_id=r['usuario_id'], ultima_mensalidade=r['ultima_mensalidade'], 
                           proxima_mensalidade=r['proxima_mensalidade'])
            return None

    @classmethod
    def atualizar_mensalidade(cls, aluno_id, ultima, proxima):
        sql = "UPDATE alunos SET ultima_mensalidade = ?, proxima_mensalidade = ? WHERE id = ?"
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (ultima, proxima, aluno_id))
            return db.cursor.rowcount > 0
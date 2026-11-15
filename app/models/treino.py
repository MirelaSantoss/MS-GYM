from app.db import DatabaseConnection

class Treino:
    def __init__(self, categoria, maquina, foto_url, descricao, series, repeticoes, aluno_id, usuario_id, id=None):
        self.id = id
        self.categoria = categoria
        self.maquina = maquina
        self.foto_url = foto_url
        self.descricao = descricao
        self.series = series
        self.repeticoes = repeticoes
        self.aluno_id = aluno_id
        self.usuario_id = usuario_id

    def salvar(self):
        sql = """
            INSERT INTO treinos (categoria, maquina, foto_url, descricao, series, repeticoes, aluno_id, usuario_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (
                self.categoria, self.maquina, self.foto_url, 
                self.descricao, self.series, self.repeticoes, 
                self.aluno_id, self.usuario_id
            ))
            self.id = db.cursor.lastrowid
            return self.id

    @classmethod
    def listar_por_aluno(cls, aluno_id):
        sql = "SELECT id, categoria, maquina, foto_url, descricao, series, repeticoes, aluno_id, usuario_id FROM treinos WHERE aluno_id = ?"
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (aluno_id,))
            rows = db.cursor.fetchall()
            return [
                cls(
                    id=r['id'], categoria=r['categoria'], maquina=r['maquina'],
                    foto_url=r['foto_url'], descricao=r['descricao'], series=r['series'],
                    repeticoes=r['repeticoes'], aluno_id=r['aluno_id'], usuario_id=r['usuario_id']
                ) for r in rows
            ]

    @classmethod
    def listar_por_usuario(cls, usuario_id):
        sql = "SELECT id, categoria, maquina, foto_url, descricao, series, repeticoes, aluno_id, usuario_id FROM treinos WHERE usuario_id = ?"
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (usuario_id,))
            rows = db.cursor.fetchall()
            return [
                cls(
                    id=r['id'], categoria=r['categoria'], maquina=r['maquina'],
                    foto_url=r['foto_url'], descricao=r['descricao'], series=r['series'],
                    repeticoes=r['repeticoes'], aluno_id=r['aluno_id'], usuario_id=r['usuario_id']
                ) for r in rows
            ]

    @classmethod
    def excluir(cls, treino_id, usuario_id):
        sql = "DELETE FROM treinos WHERE id = ? AND usuario_id = ?"
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (treino_id, usuario_id))
            return db.cursor.rowcount > 0
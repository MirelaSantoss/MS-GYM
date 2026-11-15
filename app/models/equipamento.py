from app.db import DatabaseConnection

class Equipamento:
    def __init__(self, nome, foto_url, descricao=None, id=None):
        self.id = id
        self.nome = nome
        self.foto_url = foto_url
        self.descricao = descricao

    def salvar(self):
        sql = "INSERT INTO equipamentos_academia (nome, foto_url, descricao) VALUES (?, ?, ?)"
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (self.nome, self.foto_url, self.descricao))
            self.id = db.cursor.lastrowid
            return self.id

    @classmethod
    def listar_todos(cls):
        sql = "SELECT id, nome, foto_url, descricao FROM equipamentos_academia ORDER BY nome"
        with DatabaseConnection() as db:
            db.cursor.execute(sql)
            rows = db.cursor.fetchall()
            return [
                cls(id=r['id'], nome=r['nome'], foto_url=r['foto_url'], descricao=r['descricao'])
                for r in rows
            ]

    @classmethod
    def buscar_por_id(cls, equip_id):
        sql = "SELECT id, nome, foto_url, descricao FROM equipamentos_academia WHERE id = ?"
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (equip_id,))
            r = db.cursor.fetchone()
            if r:
                return cls(id=r['id'], nome=r['nome'], foto_url=r['foto_url'], descricao=r['descricao'])
            return None

    def atualizar(self):
        # Se enviou nova foto, atualiza com a foto; senão, mantém a antiga
        if self.foto_url:
            sql = "UPDATE equipamentos_academia SET nome = ?, foto_url = ?, descricao = ? WHERE id = ?"
            params = (self.nome, self.foto_url, self.descricao, self.id)
        else:
            sql = "UPDATE equipamentos_academia SET nome = ?, descricao = ? WHERE id = ?"
            params = (self.nome, self.descricao, self.id)
            
        with DatabaseConnection() as db:
            db.cursor.execute(sql, params)
            return db.cursor.rowcount > 0

    @classmethod
    def excluir(cls, equip_id):
        sql = "DELETE FROM equipamentos_academia WHERE id = ?"
        with DatabaseConnection() as db:
            db.cursor.execute(sql, (equip_id,))
            return db.cursor.rowcount > 0
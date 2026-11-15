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
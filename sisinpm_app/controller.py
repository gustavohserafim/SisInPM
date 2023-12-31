from sisinpm_app.db import DB
from werkzeug.security import generate_password_hash, check_password_hash


class UserController:
    def __init__(self, user_id):
        self.id = user_id

    def get(self):
        user = DB().run_fr(f"SELECT id, graduacao_id, qra, estagiario FROM usuario WHERE id = {self.id} AND status = 1;")
        user["graduacao"] = self.get_graduacao_text()
        return user

    def get_graduacao_text(self):
        graduacao_id = DB().run_fv(f"SELECT graduacao_id FROM usuario WHERE id = {self.id} ;", "graduacao_id")
        return DB().run_fv(f"SELECT graduacao_abreviada FROM sisinpm.graduacao WHERE id = {graduacao_id};", "graduacao_abreviada")

    @staticmethod
    def get_estagios():
        return DB().run_fa(f"SELECT usuario.id as id, graduacao_id, qra, email, estagiario, graduacao_id, graduacao.graduacao_abreviada FROM usuario, graduacao WHERE status = 1 AND estagiario = 1 AND graduacao.id = graduacao_id;")

    @staticmethod
    def get_policiais():
        return DB().run_fa(f"SELECT usuario.id as id, graduacao_id, qra, email, estagiario, graduacao_id, graduacao.graduacao_abreviada FROM usuario, graduacao WHERE status = 1 AND graduacao.id = graduacao_id ORDER BY graduacao_id;")

    @staticmethod
    def create(email, password, qra, graduacao, is_estagio):
        user = DB().run_fv(f"SELECT id FROM usuario WHERE email = '{email}';", 'id')
        if user:
            return False
        DB().run(f"INSERT INTO usuario (graduacao_id, qra, email, senha, estagiario) VALUES ({graduacao}, '{qra}', '{email}', '{generate_password_hash(password)}', {is_estagio});")
        return True


class AuthController:
    def __init__(self, user_id):
        self.id = user_id

    @staticmethod
    def get_graduacoes():
        tipo_graduacoes = DB().run_fa("SELECT id, tipo_graduacao FROM tipo_graduacao;")
        graduacoes = DB().run_fa("SELECT id, graduacao, graduacao_abreviada, tipo_graduacao_id FROM graduacao;")

        for k, v in enumerate(tipo_graduacoes):
            tipo_graduacoes[k]["graduacoes"] = []
            if v["id"] == 1:
                tipo_graduacoes[k]["graduacoes"] = [g for g in graduacoes if g["tipo_graduacao_id"] == 1]
            elif v["id"] == 2:
                tipo_graduacoes[k]["graduacoes"] = [g for g in graduacoes if g["tipo_graduacao_id"] == 2]
            elif v["id"] == 3:
                tipo_graduacoes[k]["graduacoes"] = [g for g in graduacoes if g["tipo_graduacao_id"] == 3]
            elif v["id"] == 4:
                tipo_graduacoes[k]["graduacoes"] = [g for g in graduacoes if g["tipo_graduacao_id"] == 4]
            elif v["id"] == 5:
                tipo_graduacoes[k]["graduacoes"] = [g for g in graduacoes if g["tipo_graduacao_id"] == 5]
            elif v["id"] == 6:
                tipo_graduacoes[k]["graduacoes"] = [g for g in graduacoes if g["tipo_graduacao_id"] == 6]

        return tipo_graduacoes

    @staticmethod
    def login(email, password):
        user = DB().run_fr(f"SELECT usuario.id as id, graduacao.graduacao_abreviada, usuario.qra, usuario.estagiario, usuario.senha FROM usuario, graduacao WHERE status = 1 AND email = '{email}' AND graduacao.id = usuario.graduacao_id;")

        if user and check_password_hash(user.get("senha"), password):
            user["estagiario"] = bool(user["estagiario"])
            user.pop("senha")
            return user
        return False


class CoreController:
    def __init__(self):
        pass

    @staticmethod
    def avaliar(avaliador_id, avaliado_id, qualidades, novidades, nota, policial_1_id, policial_2_id):
        avaliador = UserController(avaliador_id).get()
        avaliado = UserController(avaliado_id).get()
        policial_1 = UserController(avaliado_id).get()
        policial_2 = policial_2_id if int(policial_2_id) > 0 else "NULL"

        if avaliador and avaliado and policial_1 and policial_2:
            return DB().run(f"INSERT INTO avaliacao (avaliador_id, avaliado_id, nota, qualidades, novidades, policial_presente1_id, policial_presente2_id) VALUES ({avaliador_id}, {avaliado_id}, {nota}, '{qualidades}', '{novidades}', {policial_1_id}, {policial_2})");
        return False

    @staticmethod
    def get_all_avaliacoes():
        return DB().run_fa("SELECT avaliacao.id, usuario.qra, nota, qualidades, novidades, avaliacao.created_at as data_avaliacao FROM avaliacao, usuario WHERE usuario.id = avaliado_id;")

    @staticmethod
    def get_avaliacao(avaliacao_id):
        return DB().run_fr(f"SELECT id, avaliador_id, avaliado_id, nota, qualidades, novidades, policial_presente1_id, policial_presente2_id, created_at FROM sisinpm.avaliacao WHERE id = {avaliacao_id};")
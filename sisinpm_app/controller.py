from sisinpm_app import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserController:
    def __init__(self, user_id):
        self.id = user_id

    @staticmethod
    def create(email, password, qra, graduacao, is_estagio):
        user = db.DB().run_fv(f"SELECT id FROM usuario WHERE email = '{email}';", 'id')
        if user:
            return False
        db.DB().run(f"INSERT INTO usuario (`graduacao_id`,`qra`,`email`,`senha`,`estagiario`) VALUES ({graduacao}, '{qra}', '{email}', '{generate_password_hash(password)}', {is_estagio});")
        return True


class AuthController:
    def __init__(self, user_id):
        self.id = user_id

    @staticmethod
    def get_graduacoes():
        tipo_graduacoes = db.DB().run_fa("SELECT id, tipo_graduacao FROM sisinpm.tipo_graduacao;")
        graduacoes = db.DB().run_fa("SELECT id, graduacao, graduacao_abreviada, tipo_graduacao_id FROM sisinpm.graduacao;")

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
        user = db.DB().run_fr(f"SELECT usuario.id as id, graduacao.graduacao_abreviada, usuario.qra, usuario.estagiario, usuario.senha FROM usuario, graduacao WHERE email = '{email}' AND graduacao.id = usuario.graduacao_id;")

        if user and check_password_hash(user.get("senha"), password):
            user["estagiario"] = bool(user["estagiario"])
            user.pop("senha")
            return user
        return False

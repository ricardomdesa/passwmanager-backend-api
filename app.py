from flask import Flask, request
from flask_restful import Api, Resource
from DB_Manager import init_db, Senhas, Usuarios
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()


@auth.verify_password
def verificaLogin(login, senha):
    if not (login, senha):
        return False
    return Usuarios.query.filter_by(login=login, senha=senha).first()


class ListaSenhas(Resource):
    @auth.login_required
    def get(self):
        try:
            senhas = Senhas.query.all()
            resp = [{'nome': i.nome, 'login': i.login, 'senha': i.senha} for i in senhas]
        except AttributeError:
            resp = {'status': 'Erro'}
        return resp


class AddSenha(Resource):
    def post(self):
        dados = request.json
        try:
            senha = Senhas(nome=dados['nome'], login=dados['login'], senha=dados['senha'])
            senha.save()
            resp = {
                        'nome': dados['nome'],
                        'login': dados['login'],
                        'senha': dados['senha']
                    }
        except AttributeError:
            resp = {'status': 'Erro'}
        return resp


api.add_resource(ListaSenhas, '/senhas')
api.add_resource(AddSenha, '/nova-senha')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
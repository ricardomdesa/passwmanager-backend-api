from flask import Flask, request
from flask_restful import Api, Resource
from DB_Manager import init_db, Senhas, Usuarios, Categoria
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()
currentLogin = ""
cors = CORS(app, resources={r"*": {"/*": "*"}})


# funcao para verificar usuario e senha
@auth.verify_password
def verificaLogin(login, senha):
    if not (login, senha):
        return False
    global currentLogin
    currentLogin = login
    return Usuarios.query.filter_by(login=login, senha=senha).first()


class Senha(Resource):
    # Adiciona uma nova senha, com nome, login, senha, categoria e usuario
    @auth.login_required
    def post(self, userId):
        dados = request.json
        categoriaId = 0
        try:
            cat = Categoria.query.filter_by(nome=dados['categoria']).first()
            if not cat:
                newCat = Categoria(nome=dados['categoria'])
                newCat.save()
                categoriaId = newCat.id
            else:
                categoriaId = cat.id
            user = Usuarios.query.filter_by(id=userId).first()
            if user:
                senha = Senhas(nome=dados['nome'], login=dados['login'],
                               senha=dados['senha'], categoria_id=categoriaId,
                               usuario_id=userId)
                senha.save()
                resp = {
                        'nome': dados['nome'],
                        'login': dados['login'],
                        'senha': dados['senha'],
                        'usuario_id': user.id,
                        'categoria_id': categoriaId
                    }
        except AttributeError:
            resp = {'status': 'Erro post senhas'}
        return resp

    # Lista as senhas cadastradas de acordo com o usuario logado
    @auth.login_required
    def get(self, userId):
        try:
            resp = []
            senhas = Senhas.query.filter_by(usuario_id=userId).all()
            if senhas:
                for i in senhas:
                    categoria = Categoria.query.filter_by(id=i.categoria_id).first().nome
                    resp.append({
                        'nome': i.nome,
                        'login': i.login,
                        'senha': i.senha,
                        'usuario': i.usuario_id,
                        'categoria': categoria
                    })
            else:
                resp = {'status': 'Erro', 'mensagem': 'Usuario nao encontrado'}
        except AttributeError:
            resp = {'status': 'Erro get senhas'}
        return resp


class ModifySenha(Resource):
    # Edita a senha
    @auth.login_required
    def put(self, id):
        dados = request.json
        senha = Senhas.query.filter_by(id=id).first()
        if senha:
            if dados.get('login'):
                senha.login = dados['login']
                senha.save()
                resp = {'status': 'sucesso', 'mensagem': 'Senha alterada'}
            elif dados.get('senha'):
                senha.senha = dados['senha']
                senha.save()
                resp = {'status': 'sucesso', 'mensagem': 'Senha alterada'}
            else:
                resp = {'status': 'erro', 'mensagem': 'Nada a alterar. Verifique o json'}
        else:
            resp = {'status': 'erro', 'mensagem': 'Senha não existe'}
        return resp

    # delete senha
    @auth.login_required
    def delete(self, id):
        try:
            senha = Senhas.query.filter_by(id=id).first()
            senha.delete()
            resp = {'status': 'sucesso', 'mensagem': 'Senha removida'}
        except AttributeError:
            resp = {'status': 'erro', 'mensagem': 'Senha não existe'}
        return resp


class BuscaSenhaPorNome(Resource):
    # Busca senhas por nome
    @auth.login_required
    def get(self, nome):
        usuarioLogado = Usuarios.query.filter_by(login=currentLogin).first()
        senhas = Senhas.query.filter_by(usuario_id=usuarioLogado.id, nome=nome).all()
        resp = []
        for i in senhas:
            userName = Usuarios.query.filter_by(id=i.usuario_id).first().login
            categoria = Categoria.query.filter_by(id=i.categoria_id).first().nome
            resp.append({
                'nome': i.nome,
                'login': i.login,
                'senha': i.senha,
                'usuario': userName,
                'categoria': categoria
            })
        return resp


class BuscaSenhaPorCategoria(Resource):
    # Busca senhas por categoria string
    @auth.login_required
    def get(self, categoria):
        cat = Categoria.query.filter_by(nome=categoria).first()
        if cat:
            usuarioLogado = Usuarios.query.filter_by(login=currentLogin).first()
            senhas = Senhas.query.filter_by(usuario_id=usuarioLogado.id, categoria_id=cat.id).all()
            resp = []
            for i in senhas:
                userName = Usuarios.query.filter_by(id=i.usuario_id).first().login
                categoria = Categoria.query.filter_by(id=i.categoria_id).first().nome
                resp.append({
                    'nome': i.nome,
                    'login': i.login,
                    'senha': i.senha,
                    'usuario': userName,
                    'categoria': categoria
                })
        else:
            resp = {'status': 'erro', 'mensagem': 'Categoria nao encontrada'}
        return resp


class BuscaSenhaPorCategoriaId(Resource):
    # Busca senhas por categoria id
    @auth.login_required
    def get(self, categoriaId):
        cat = Categoria.query.filter_by(id=categoriaId).first()
        if cat:
            usuarioLogado = Usuarios.query.filter_by(login=currentLogin).first()
            senhas = Senhas.query.filter_by(usuario_id=usuarioLogado.id, categoria_id=cat.id).all()
            resp = []
            for i in senhas:
                userName = Usuarios.query.filter_by(id=i.usuario_id).first().login
                categoria = Categoria.query.filter_by(id=i.categoria_id).first().nome
                resp.append({
                    'nome': i.nome,
                    'login': i.login,
                    'senha': i.senha,
                    'usuario': userName,
                    'categoria': categoria
                })
        else:
            resp = {'status': 'erro', 'mensagem': 'Categoria nao encontrada'}
        return resp


class Users(Resource):
    # adiciona um novo usuario
    @auth.login_required
    def post(self):
        dados = request.json
        usuario = Usuarios.query.filter_by(login=dados['login']).first()
        if not usuario:
            novoUsuario = Usuarios(login=dados['login'], senha=dados['senha'])
            novoUsuario.save()
            return {'status': 'sucesso', 'mensagem': 'Usuario adicionado'}
        else:
            return {'status': 'erro', 'mensagem': 'Usuario já existe'}

    # lista os usuarios cadastrados
    @auth.login_required
    def get(self):
        users = Usuarios.query.all()
        return [{'login': i.login, 'senha': i.senha, 'id': i.id} for i in users]


class UsersByLogin(Resource):
    @auth.login_required
    def get(self, login):
        user = Usuarios.query.filter_by(login=login).first()
        if user:
            return {'id': user.id,'login': user.login, 'senha': user.senha}
        else:
            return {'status': 'erro', 'mensagem': 'Usuario não encontrado'}


class ModifyUser(Resource):
    # Edita a senha do usuario
    @auth.login_required
    def put(self, id):
        dados = request.json
        user = Usuarios.query.filter_by(id=id).first()
        if user:
            if dados.get('senha'):
                user.senha = dados['senha']
                user.save()
                resp = {'status': 'sucesso', 'mensagem': 'Senha de usuario alterada'}
            else:
                resp = {'status': 'erro', 'mensagem': 'Nada a alterar. Verifique o json'}
        else:
            resp = {'status': 'erro', 'mensagem': 'Usuario não existe'}
        return resp

    # delete usuario
    @auth.login_required
    def delete(self, id):
        try:
            user = Usuarios.query.filter_by(id=id).first()
            user.delete()
            resp = {'status': 'sucesso', 'mensagem': 'Usuario removido'}
        except AttributeError:
            resp = {'status': 'erro', 'mensagem': 'Usuario não existe'}
        return resp


class UserById(Resource):
    @auth.login_required
    def get(self, id):
        user = Usuarios.query.filter_by(id=id).first()
        if user:
            resp = {'id': user.id, 'login': user.login, 'senha': user.senha}
        else:
            resp = {'status': 'erro', 'mensagem': 'Usuario nao existe'}
        return resp


api.add_resource(Senha, '/senhas/<int:userId>')
api.add_resource(ModifySenha, '/senhas/<int:id>')
api.add_resource(BuscaSenhaPorNome, '/senhas-nome/<string:nome>')
api.add_resource(BuscaSenhaPorCategoria, '/senhas-categoria/<string:categoria>')
api.add_resource(BuscaSenhaPorCategoriaId, '/senhas-categoria/<int:categoriaId>')
api.add_resource(Users, '/users')
api.add_resource(UsersByLogin, '/users/<string:login>')
api.add_resource(UserById, '/users/<int:id>')
api.add_resource(ModifyUser, '/users/<int:id>')


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0')
    #app.run(debug=True)

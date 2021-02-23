import requests, json
from requests.auth import HTTPBasicAuth


class TesteApi():
    url = 'http://localhost:5000/'
    userLogado = 'ricardo'
    senhaUser = 'suplatao1'

    def testeAddUser(self):
        jsonPost = {
            "login": self.userLogado,
            "senha": self.senhaUser
        }

        resp = requests.post(self.url + 'users', json=jsonPost, auth=HTTPBasicAuth('admin', 'suplatao'))
        if not resp:
            print('POST resp vazio')
        else:
            print('POST add user', resp.json())

    def testeModifyUser(self, id):
        jsonPut = {
            "senha": "123ddsds45"
        }
        resp = requests.put(self.url + 'users/' + str(id), json=jsonPut, auth=HTTPBasicAuth(self.userLogado, self.senhaUser))
        if not resp:
            print('PUT change passwd resp vazio')
        else:
            print('PUT change passwd', resp.json())

    def testeDeleteUser(self, id):
        resp = requests.delete(self.url + 'users/' + str(id), auth=HTTPBasicAuth(self.userLogado, self.senhaUser))
        if not resp:
            print('DELETE user resp vazio')
        else:
            print('DELETE user', resp.json())

    def getAllUsers(self):
        resp = requests.get(self.url + 'users', auth=HTTPBasicAuth(self.userLogado, self.senhaUser))
        if not resp:
            print('GET resp vazio')
        else:
            print('GET all users', resp.json())



    ##### Senhas
    def insereSenha(self):
        jsonPost = {
            "nome": "google3",
            "login": "l@gmail.com",
            "senha": "12345",
            "categoria": "email3"
        }
        resp = requests.post(self.url + 'senhas', json=jsonPost, auth=HTTPBasicAuth(self.userLogado, self.senhaUser))
        if not resp:
            print('POST add senha resp vazio')
        else:
            print('POST add senha', resp.json())

    def testeModifySenha(self, id):
        jsonPut = {
            # "senha": "123ddsds45"
            "login": "teste@gmail.com"
        }
        resp = requests.put(self.url + 'senhas/' + str(id), json=jsonPut, auth=HTTPBasicAuth(self.userLogado, self.senhaUser))
        if not resp:
            print('PUT change senhas resp vazio')
        else:
            print('PUT change senhas', resp.json())

    def testeDeleteSenha(self, id):
        resp = requests.delete(self.url + 'senhas/' + str(id), auth=HTTPBasicAuth(self.userLogado, self.senhaUser))
        if not resp:
            print('DELETE senhas resp vazio')
        else:
            print('DELETE senhas', resp.json())

    def getSenhaByName(self, nome):
        resp = requests.get(self.url + 'senhas-nome/' + nome, auth=HTTPBasicAuth(self.userLogado, self.senhaUser))
        if not resp:
            print('GET senha por nome resp vazio')
        else:
            print('GET senha por nome', resp.json())

    def getSenhaByCategoria(self, categoria):
        resp = requests.get(self.url + 'senhas-categoria/' + categoria, auth=HTTPBasicAuth(self.userLogado, self.senhaUser))
        if not resp:
            print('GET senha por nome resp vazio')
        else:
            print('GET senha por nome', resp.json())

    def getSenhaByCategoriaId(self, id):
        resp = requests.get(self.url + 'senhas-categoria/' + str(id), auth=HTTPBasicAuth(self.userLogado, self.senhaUser))
        if not resp:
            print('GET senha por nome resp vazio')
        else:
            print('GET senha por nome', resp.json())

    def getAllSenhas(self):
        resp = requests.get(self.url + 'senhas', auth=HTTPBasicAuth(self.userLogado, self.senhaUser))
        if not resp:
            print('GET todas senhas resp vazio')
        else:
            print('GET todas senhas', resp.json())


# api.add_resource(Senha, '/senhas')
# api.add_resource(BuscaSenhaPorNome, '/senhas-nome/<string:nome>')
# api.add_resource(BuscaSenhaPorCategoria, '/senhas-categoria/<string:categoria>')
# api.add_resource(BuscaSenhaPorCategoriaId, '/senhas-categoria/<int:categoriaId>')
# api.add_resource(Users, '/users')
# api.add_resource(ModifyUser, '/users/<int:id>')

if __name__ == '__main__':
    teste = TesteApi()

    #teste de users
    # teste.testeAddUser()
    # teste.testeModifyUser(4)
    # teste.testeDeleteUser(2)
    teste.getAllUsers()

    # teste de senha
    # teste.insereSenha()
    # teste.testeModifySenha(1)
    # teste.testeDeleteSenha(1)
    # teste.getSenhaByName('google3')
    # teste.getSenhaByCategoria('email2')
    # teste.getSenhaByCategoriaId(1)

    # teste.getAllSenhas()

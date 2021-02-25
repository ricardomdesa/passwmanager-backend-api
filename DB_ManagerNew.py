# from app import app
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

uriSqlite = 'sqlite:///senhas_db3.db'
uriMysql = 'mysql+mysqlconnector://root:Suplatao1@localhost:3306/api_db'
app = Flask(__name__)
app.config['SECRET_KEY'] = "xxxxxxxx"
app.config['SQLALCHEMY_DATABASE_URI'] = uriMysql
db = SQLAlchemy(app)


class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True)
    senha = db.Column(db.String(20))
    senhas = db.relationship("Senhas", cascade="all, delete")

    def __repr__(self):
        return f'<Usuario {self.login}'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Categoria(db.Model):
    __tablename__ = 'categorias'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20))
    senhas = db.relationship("Senhas", cascade="all, delete")

    def __repr__(self):
        return f'<Categoria {self.nome}'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Senhas(db.Model):
    __tablename__ = 'senhas'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    categoria_id = db.Column(db.Integer, db.ForeignKey('categorias.id'))
    nome = db.Column(db.String(40), index=True)
    login = db.Column(db.String(40))
    senha = db.Column(db.String(20))
    usuario = db.relationship("Usuarios")
    categoria = db.relationship("Categoria")

    def __repr__(self):
        return f'<Senhas {self.nome}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


def insereUserInicial():
    user = Usuarios.query.filter_by(login='admin').first()
    if not user:
        userAdmin = Usuarios(login='admin2', senha='suplatao')
        userAdmin.save()


def init_db():
    db.create_all()
    insereUserInicial()


if __name__ == "__main__":
    init_db()
    print(Usuarios.query.all())

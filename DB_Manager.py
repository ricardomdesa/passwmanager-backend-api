from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///senhas_db.db', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Usuarios(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    senha = Column(String(20))
    senhas = relationship("Senhas", cascade="all, delete")


    def __repr__(self):
        return f'<Usuario {self.login}'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Categoria(Base):
    __tablename__ = 'categorias'
    id = Column(Integer, primary_key=True)
    nome = Column(String(20))
    senhas = relationship("Senhas", cascade="all, delete")

    def __repr__(self):
        return f'<Categoria {self.nome}'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Senhas(Base):
    __tablename__ = 'senhas'
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    categoria_id = Column(Integer, ForeignKey('categorias.id'))
    nome = Column(String(40), index=True)
    login = Column(String(40))
    senha = Column(String(20))
    usuario = relationship("Usuarios")
    categoria = relationship("Categoria")

    def __repr__(self):
        return f'<Senhas {self.nome}>'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


def insereUserInicial():
    user = Usuarios.query.filter_by(login='admin').first()
    if not user:
        userAdmin = Usuarios(login='admin', senha='suplatao')
        userAdmin.save()


def init_db():
    Base.metadata.create_all(bind=engine)
    insereUserInicial()


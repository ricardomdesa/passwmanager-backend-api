from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///senhas_db.db', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Senhas(Base):
    __tablename__ = 'senhas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), index=True)
    login = Column(String(40))
    senha = Column(String(20))

    def __repr__(self):
        return f'<Senhas {self.nome}>'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Usuarios(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True)
    senha = Column(String(20))

    def __repr__(self):
        return f'<Usuario {self.login}'

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    user = Usuarios(login='Ricardo', senha='suplatao')
    # user.save()
    # print(Usuarios.query.filter_by(login="Ricardo").first())

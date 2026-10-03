#importando o básico para começar
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer,Boolean, String, Column, Text
from db import db

#classe que contem o modelo da minha table de usuários
class Usuario(db.Model):
    __tablename__ = 'USUARIOS'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    ativo = db.Column(db.Boolean, default=True)

    # Um usuário pode possuir vários cursos
    cursos = db.relationship("Curso", back_populates="usuario")



#classe que contem o modelo da minha table de Cursos
class Curso(db.Model):
    __tablename__ = 'CURSOS'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(
        db.Integer,
        db.ForeignKey("USUARIOS.id"),
        nullable=False    
    )
    titulo = db.Column(db.String, unique=True)
    descricao = db.Column(db.Text,nullable=False)
    plataforma = db.Column(db.String, unique=True)
    progresso = db.Column(db.Integer, default=0)
    status = db.Column(db.Integer, default=1)
    # Curso pertence a um usuário
    usuario = db.relationship("Usuario", back_populates="cursos")



    
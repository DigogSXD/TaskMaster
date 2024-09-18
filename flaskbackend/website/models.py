from . import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):  # Herdando de UserMixin
    id = db.Column(db.Integer, primary_key=True)  # Substituiu id_user por id
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    # Outros campos (se houver)
    

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_projeto = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class Task(db.Model):
    id_task = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # Ex: 'Pré-requisitos', 'Em Produção', 'Concluído'
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))  # Chave estrangeira para Project

    project = db.relationship('Project', backref='tasks')  # Relacionamento inverso com Project

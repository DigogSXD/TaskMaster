from . import db 
from flask_login import UserMixin
from flask_login import login_manager

class Usuario(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    projects = db.relationship('Project', backref='owner')  # Define a relação inversa

class Project(db.Model):
    id_projeto = db.Column(db.Integer, primary_key=True)
    nome_projeto = db.Column(db.String(100), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id_user'))  # Chave estrangeira referenciando Usuario
    
class Task(db.Model):
    id_task = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # Ex: 'Pré-requisitos', 'Em Produção', 'Concluído'
    project_id = db.Column(db.Integer, db.ForeignKey('project.id_projeto'))  # Chave estrangeira para Project

    project = db.relationship('Project', backref='tasks')  # Relacionamento inverso com Project

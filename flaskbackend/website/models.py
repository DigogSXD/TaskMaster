from . import db
from flask_login import UserMixin

# Modelo de Usuário
class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    # Relacionamento com projetos (usando a tabela intermediária)
    projects = db.relationship('Project', secondary='rel_usuario_project', backref='users')


# Modelo de Projeto
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome_projeto = db.Column(db.String(100), nullable=False)
    
    # Você pode manter user_id se quiser identificar o criador do projeto
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    # Relacionamento reverso para facilitar o acesso ao criador
    criador = db.relationship('Usuario', backref='projetos_criados')


# Tabela intermediária entre usuários e projetos
class RelUsuarioProject(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)



class Task(db.Model):
    id_task = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # Ex: 'Pré-requisitos', 'Em Produção', 'Concluído'
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))  # Chave estrangeira para Project

    project = db.relationship('Project', backref='tasks')  # Relacionamento inverso com Project

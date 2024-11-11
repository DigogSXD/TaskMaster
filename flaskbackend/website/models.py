from . import db
from flask_login import UserMixin
from datetime import datetime

# Modelo de Usuário
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    # Relacionamento com projetos (usando a tabela intermediária)
    projects = db.relationship('Project', secondary='rel_usuario_project', backref='users')


# Modelo de Projeto
class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    nome_projeto = db.Column(db.String(100), nullable=False)
    
    # Chave estrangeira para identificar o criador do projeto
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    # Relacionamento reverso para facilitar o acesso ao criador
    criador = db.relationship('Usuario', backref='projetos_criados')


# Tabela intermediária entre usuários e projetos
class RelUsuarioProject(db.Model):
    __tablename__ = 'rel_usuario_project'
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)


# A tabela da Task
class Task(db.Model):
    __tablename__ = 'task'
    id_task = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

    importance = db.Column(db.Integer, nullable=False)
    ease = db.Column(db.Integer, nullable=False)
    priority = db.Column(db.Integer, nullable=False)
    completion_date = db.Column(db.Date, nullable=True)

    comment = db.Column(db.String(500), nullable=True)  # Comentário opcional
    drive_link = db.Column(db.String(500), nullable=True)  # Link opcional

    checklist_items = db.relationship('ChecklistItem', backref='task', cascade='all, delete-orphan')


# Modelo de ChecklistItem
class ChecklistItem(db.Model):
    __tablename__ = 'checklist_item'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id_task'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)


# Modelo de Notification
class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id_task'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_id, content, project_id=None, task_id=None):
        self.user_id = user_id
        self.content = content
        self.project_id = project_id
        self.task_id = task_id

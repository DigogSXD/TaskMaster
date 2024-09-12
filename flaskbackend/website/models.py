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

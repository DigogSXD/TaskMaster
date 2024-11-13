from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager  # Importa o LoginManager
from os import path

db = SQLAlchemy()
DB_NAME = 'taskmaster.db'

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    db.init_app(app)

    
    from .views import views
    from .auth import auth
    from .checklist import checklist_bp
    from .project import project
    from .notificacoes import notificacoes
    from .task import task
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(checklist_bp, url_prefix='/')
    app.register_blueprint(project, url_prefix='/')
    app.register_blueprint(task, url_prefix='/')
    app.register_blueprint(notificacoes, url_prefix='/')

    from .models import Usuario, Project, Task, ChecklistItem, Notification

    create_db(app)

    # Configurando o LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Rota de login se o usuário não estiver autenticado
    login_manager.init_app(app)

    # Função para carregar o usuário a partir do banco de dados
    @login_manager.user_loader
    def load_user(id):
        return Usuario.query.get(int(id))
    
    

    return app

def create_db(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Database Created")


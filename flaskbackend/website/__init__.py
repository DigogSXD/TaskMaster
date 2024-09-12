from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    from .models import Usuario,Project

    create_db(app)
    
    return app


def create_db(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():  # Cria o contexto de aplicação
            db.create_all()
            print("Database Created")

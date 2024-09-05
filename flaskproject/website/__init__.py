from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config['SECRET_KEY'] = 'dev'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth, url_prefix='/auth')

    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados, se não existirem

    return app

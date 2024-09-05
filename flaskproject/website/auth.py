from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return jsonify({'redirect': url_for('auth.task_master')})
        else:
            return jsonify({'redirect': url_for('auth.signup'), 'error': 'Usuário não encontrado'})
    
    return render_template('login.html')

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'error': 'Email ou senha não fornecidos'}), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email já cadastrado'}), 400

        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        print(f'Usuário criado: {new_user.email}')

        return jsonify({'redirect': url_for('auth.task_master')})
    
    return render_template('signup.html')

@auth.route('/taskmaster', methods=['GET'])
def task_master():
    return render_template('taskMaster.html')

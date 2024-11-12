from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from .models import Usuario, Task, Project, RelUsuarioProject, ChecklistItem,Notification
from flask import jsonify, request
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from .models import Usuario, Project

auth = Blueprint('auth',__name__)

@auth.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data.get('emailLogin')
        senha = data.get('passwordLogin')

        # Verifica se os campos foram preenchidos
        if not email or not senha:
            flash("Por favor, preencha todos os campos", category='error')
            return redirect(url_for('auth.login'))  # Retorna para a tela de login

        # Verifica se o usuário existe no banco de dados
        user = Usuario.query.filter_by(email=email).first()

        if not user:
            flash("Usuário inexistente! Faça cadastro antes", category='error')
            return redirect(url_for('auth.signup'))  # Redireciona para a página de cadastro
        else:
            # Verifica se a senha está correta
            if check_password_hash(user.password, senha):
                flash("Login bem sucedido", category='success')

                # Loga o usuário na sessão
                login_user(user)

                return redirect(url_for('project.home'))  # Redireciona para a página principal
            else:
                flash("Senha incorreta", category='error')

    return render_template('login.html')





@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('emailsignup')
        senha = request.form.get('passwordsignup')

        # Debug prints
        print(email)
        print(senha)

        user = Usuario.query.filter_by(email=email).first()

        if user:
            flash("Usuário já cadastrado! Faça Login", category='error')
            return redirect(url_for('auth.login'))

        if len(senha) < 10:
            flash("A senha deve ter pelo menos 10 caracteres", category='error')
            return redirect(url_for('auth.signup'))
        else:
            novo_user = Usuario(email=email, password=generate_password_hash(senha, method='pbkdf2:sha256', salt_length=8))

            db.session.add(novo_user)
            db.session.commit()

            flash("Usuário cadastrado com sucesso", category='success')

            return redirect(url_for('auth.login'))

    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()  # Encerra a sessão do usuário
    return render_template('login.html')



@auth.route('/sobre')
@login_required
def sobre():
    return render_template('sobre.html')


    # Simulação de armazenamento de projetos (dicionário para projetos)
projects = {}


@auth.route('/esqueceu',methods = ['GET','POST'])
def esqueceu():

    email = request.form.get('emailEsqueceu')
    nova_senha = request.form.get('senha1')
    nova_senha2 = request.form.get('senha2')

    if request.method == 'POST':
        
        # Busca o usuário no banco de dados
        user = Usuario.query.filter_by(email=email).first()

        if not user:
            flash("Usuário inexistente! Faça cadastro", category='error')
            return redirect(url_for('auth.signup'))

        # Agora que já verificamos se o usuário existe, podemos acessar seus atributos
        print(user.id) 
        print(user.email)
        print(user.password)

        # Verifica se as senhas são iguais
        if nova_senha != nova_senha2:
            flash("As senhas devem ser iguais")
            return redirect(url_for('auth.esqueceu'))
        
        # Verifica se a nova senha tem no mínimo 10 caracteres
        if len(nova_senha) < 10:
            flash("A nova senha deve ter no mínimo 10 caracteres")
            return redirect(url_for('auth.esqueceu'))
        
        # Atualizar a senha do usuário
        user.password = generate_password_hash(nova_senha, method='pbkdf2:sha256')

        # Commit da nova senha no banco de dados
        try:
            db.session.commit()
            flash("Senha alterada com sucesso!", category='success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash(f"""Erro ao atualizar a senha: {str(e)}. Tente de novo""", category='error')
            return redirect(url_for('auth.esqueceu'))

    return render_template('esqueceu.html')
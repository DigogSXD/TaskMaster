from flask import Blueprint, render_template, request,flash,redirect,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from .models import Usuario ,Project


auth = Blueprint('auth',__name__)

@auth.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data.get('emailLogin')
        senha = data.get('passwordLogin')

        user = Usuario.query.filter_by(email = email).first()

        if not user:
            flash("Usuário inexistente! Faça cadastro antes",category='error')
        else:
            if check_password_hash(user.password,senha):
                flash("Login bem sucedido",category='success')
                return redirect(url_for('auth.home'))
            
    flash("Senha incorreta")      
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

        if len(senha) <= 10:
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
def logout():
    return render_template('login.html')

@auth.route('/home',methods = ['POST','GET'])
def home():
    if request.method == 'POST':
        dados = request.form 
        print(dados)
        
        nome_projeto = dados.get('id')
        projeto = Project.query.filter_by(nome_projeto = nome_projeto ).first()
        if projeto:
            flash("Já existe um projeto com esse nome",category = 'error')
            return redirect(url_for('auth.home'))
        else:
            projeto_novo = Project(nome_projeto = nome_projeto)
            db.session.add(projeto_novo)
            db.session.commit()


    return render_template('taskMaster.html')



@auth.route('/sobre')
def sobre():
    return render_template('sobre.html')
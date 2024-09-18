from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user

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

        print(email)
        print(senha)

        # Verifica se o usuário existe no banco de dados
        user = Usuario.query.filter_by(email=email).first()

        if not user:
            flash("Usuário inexistente! Faça cadastro antes", category='error')
            return redirect(url_for('auth.signup'))
        else:
            # Verifica se a senha está correta
            if check_password_hash(user.password, senha):
                flash("Login bem sucedido", category='success')

                # Loga o usuário na sessão
                login_user(user)

                return redirect(url_for('auth.home'))
            else:
                flash("Senha incorreta", category='error')

    return render_template('login.html')


@auth.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        nome_projeto = request.form.get('projeto')
        print(f"Nome do projeto recebido: {nome_projeto}")  # Debug

        if not nome_projeto:
            flash('O nome do projeto é obrigatório.', category='error')
            return redirect(url_for('auth.home'))
        
        projeto_existente = Project.query.filter_by(nome_projeto=nome_projeto, user_id=current_user.id).first()

        if projeto_existente:
            flash("Já existe um projeto com esse nome", category='error')
        else:
            projeto_novo = Project(nome_projeto=nome_projeto, user_id=current_user.id)
            db.session.add(projeto_novo)
            try:
                db.session.commit()
            except Exception as e:
                print(f"Erro ao salvar no banco de dados: {e}")
                db.session.rollback()
                flash('Erro ao salvar o projeto.', category='error')

        return redirect(url_for('auth.home'))

    projetos = Project.query.filter_by(user_id=current_user.id).all()
    return render_template('taskMaster.html', projects=projetos)


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


@auth.route('/projeto/<int:project_id>', methods=['GET', 'POST'])
@login_required
def gerenciar_projeto(project_id):
    projeto = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        # Salvar as tarefas do projeto (como você já configurou anteriormente)
        # Aqui você pode receber as tarefas do frontend via AJAX e salvar no banco
        pass
    
    # Renderizar a página com o nome do projeto e as tarefas associadas
    return render_template('project_details.html', project_name=projeto.nome_projeto)


@auth.route('/editar_projeto/<int:project_id>', methods=['GET', 'POST'])
@login_required
def editar_projeto(project_id):
    projeto = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        novo_nome = request.form.get('project_name')
        
        if not novo_nome:
            flash('O nome do projeto não pode ser vazio.', category='error')
        else:
            projeto.nome_projeto = novo_nome
            db.session.commit()
            flash('Projeto atualizado com sucesso!', category='success')
            return redirect(url_for('auth.home'))
    
    return render_template('editar_projeto.html', projeto=projeto)


@auth.route('/deletar_projeto/<int:project_id>')
@login_required
def deletar_projeto(project_id):
    projeto = Project.query.get_or_404(project_id)
    
    # Remover o projeto
    db.session.delete(projeto)
    db.session.commit()

    flash('Projeto deletado com sucesso!', category='success')
    return redirect(url_for('auth.home'))



@auth.route('/adicionar_projeto', methods=['POST'])
@login_required
def adicionar_projeto():
    nome_projeto = request.form.get('project_name')
    
    if not nome_projeto:
        flash('O nome do projeto é obrigatório.', category='error')
        return redirect(url_for('auth.home'))

    # Verificar se o projeto já existe
    projeto_existente = Project.query.filter_by(nome_projeto=nome_projeto, user_id=current_user.id).first()
    if projeto_existente:
        flash('Já existe um projeto com esse nome.', category='error')
        return redirect(url_for('auth.home'))
    
    # Criar o novo projeto
    novo_projeto = Project(nome_projeto=nome_projeto, user_id=current_user.id)
    db.session.add(novo_projeto)
    try:
        db.session.commit()
        flash('Projeto criado com sucesso!', category='success')
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao salvar o projeto: {e}")  # Debug
        flash('Erro ao salvar o projeto.', category='error')
        flash('Projeto criado com sucesso!', category='success')
    return redirect(url_for('auth.home'))


@auth.route('/esqueceu',methods = ['GET','POST'])
def esqueceu():

    email = request.form.get('emailEsqueceu')
    nova_senha = request.form.get('senha1')
    nova_senha2 = request.form.get('senha2')

    if request.method == 'POST':
        """
        É aqui que eu tentei inicialmente fazer um teste pra vizualizar td
            Deu certo, mas não consegui fazer em outro arquivo
        
        users = Usuario.query.all()
        
        for i in list(users):
            print(i.id)
            print(i.email)
            print(i.password)
            print("\n\n")
        """
        
        """Aqui estou fazendo a lógica normal da página de esqueceu a senha(não precisa alterar nada, tá funfando)"""
        user = Usuario.query.filter_by(email=email).first()
        
        #Printando no terminal só pra ver se ele consegue 'puxar' os dados do frontend
        print(user.id) 
        print(user.email)
        print(user.password)

        if not user:
            flash("Usuário inexistente! Faça cadastro", category='error')
            return redirect(url_for('auth.signup'))
        else:    
            if nova_senha != nova_senha2:
                flash("As senhas devem ser iguais")
                return redirect(url_for('auth.esqueceu'))
            if len(nova_senha) < 10:
                flash("A nova senha deve ter no mínimo 10 caracteres")
                return redirect(url_for('auth.esqueceu.html'))
            else:
                # Atualizar a senha do usuário
                user.password = generate_password_hash(nova_senha, method='pbkdf2:sha256')

                # Commit da nova senha no banco de dados
                try:
                    db.session.commit()
                    flash("Senha alterada com sucesso!", category='success')
                    return redirect(url_for('auth.login'))
                except Exception as e:
                    db.session.rollback()
                    flash(f"""Erro ao atualizar a senha: {str(e)} 
                          Tente denovo""", category='error')
                    return redirect(url_for('auth.esqueceu'))

    return render_template('esqueceu.html')
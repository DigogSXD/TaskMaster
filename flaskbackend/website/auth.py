from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from .models import Usuario, Task, Project, RelUsuarioProject, ChecklistItem
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

                return redirect(url_for('auth.home'))  # Redireciona para a página principal
            else:
                flash("Senha incorreta", category='error')

    return render_template('login.html')


@auth.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        nome_projeto = request.form.get('projeto')
        
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
                db.session.rollback()
                flash('Erro ao salvar o projeto.', category='error')

        return redirect(url_for('auth.home'))

    # Buscar todos os projetos que o usuário criou OU que foram compartilhados com ele
    projetos_criados = Project.query.filter_by(user_id=current_user.id).all()  # Projetos criados
    projetos_compartilhados = current_user.projects  # Projetos compartilhados via RelUsuarioProject

    # Combinar as listas
    todos_os_projetos = projetos_criados + projetos_compartilhados

    return render_template('taskMaster.html', projects=todos_os_projetos)



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



# Projeto e Task
@auth.route('/projeto/<int:project_id>', methods=['GET', 'POST'])
@login_required
def gerenciar_projeto(project_id):
    projeto = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        task_name = request.form.get('task_name')
        task_status = request.form.get('task_status')
        comment = request.form.get('comment')
        drive_link = request.form.get('drive_link')  # Capturar o link do Google Drive

        # Validação de importância e facilidade
        try:
            importance = int(request.form.get('importance'))
            ease = int(request.form.get('ease'))
        except (TypeError, ValueError):
            flash('Valores de importância e facilidade inválidos.', 'error')
            return redirect(url_for('auth.gerenciar_projeto', project_id=project_id))

        # Verificar se a data de conclusão foi fornecida
        completion_date = request.form.get('completion_date')
        if not completion_date:
            flash('Data de conclusão é obrigatória.', 'error')
            return redirect(url_for('auth.gerenciar_projeto', project_id=project_id))

        # Validação do formato da data de conclusão
        try:
            completion_date = datetime.strptime(completion_date, '%Y-%m-%d').date()
        except ValueError:
            flash('Data de conclusão inválida. Use o formato YYYY-MM-DD.', 'error')
            return redirect(url_for('auth.gerenciar_projeto', project_id=project_id))

        if task_name and task_status and importance and ease:
            priority = importance * ease

            # Criar nova tarefa
            nova_tarefa = Task(description=task_name, status=task_status, project_id=projeto.id,
                               importance=importance, ease=ease, priority=priority,
                               completion_date=completion_date, comment=comment,
                               drive_link=drive_link)  # Armazenar o link do Google Drive
            db.session.add(nova_tarefa)
            db.session.commit()
            flash('Tarefa adicionada com sucesso!', 'success')
        else:
            flash('Todos os campos são obrigatórios.', 'error')

        return redirect(url_for('auth.gerenciar_projeto', project_id=project_id))

    # Obter tarefas por status
    prereq_tasks = Task.query.filter_by(project_id=projeto.id, status='Pré-requisitos').order_by(Task.priority.desc()).all()
    in_prod_tasks = Task.query.filter_by(project_id=projeto.id, status='Em Produção').order_by(Task.priority.desc()).all()
    completed_tasks = Task.query.filter_by(project_id=projeto.id, status='Concluído').order_by(Task.priority.desc()).all()

    return render_template('project_details.html', project=projeto,
                           prereq_tasks=prereq_tasks, in_prod_tasks=in_prod_tasks, 
                           completed_tasks=completed_tasks)

    




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


@auth.route('/deletar_projeto/<int:project_id>', methods=['POST'])
@login_required
def deletar_projeto(project_id):
    projeto = Project.query.get_or_404(project_id)
    
    # Buscar todas as tarefas associadas ao projeto
    tarefas = Task.query.filter_by(project_id=project_id).all()
    
    try:
        # Deletar todas as tarefas associadas ao projeto
        for tarefa in tarefas:
            db.session.delete(tarefa)
        
        # Remover o projeto
        db.session.delete(projeto)
        db.session.commit()
        
        flash('Projeto e todas as tarefas associadas deletados com sucesso!', category='success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao deletar o projeto e as tarefas associadas.', 'error')

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

# Atualizar TAREFA
@auth.route('/atualizar_tarefas', methods=['POST'])
@login_required
def atualizar_tarefas():
    data = request.get_json()
    tasks = data.get('tasks', [])

    for task_data in tasks:
        task_id = task_data.get('id_task')
        new_status = task_data.get('status')
        
        tarefa = Task.query.get(task_id)
        if tarefa:
            tarefa.status = new_status
            db.session.commit()

    return jsonify({'success': True}), 200

# COMPARTILHAR
@auth.route('/compartilhar_projeto/<int:project_id>', methods=['POST'])
@login_required
def compartilhar_projeto(project_id):
    email = request.form.get('emailShare')
    
    if not email:
        flash("Email não recebido.", category="error")
        return redirect(url_for('auth.home'))
    
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        flash("Usuário inexistente", category="error")
        return redirect(url_for('auth.home'))
    
    # Verificar se o relacionamento já existe
    relacao_existente = RelUsuarioProject.query.filter_by(user_id=usuario.id, project_id=project_id).first()

    if relacao_existente:
        flash(f'O usuário {usuario.email} já faz parte deste projeto.', category="info")
        return redirect(url_for('auth.home'))
    else:
        # Criar novo relacionamento
        nova_relacao = RelUsuarioProject(user_id=usuario.id, project_id=project_id)
        db.session.add(nova_relacao)
        db.session.commit()
        flash(f'O usuário {usuario.email} foi adicionado ao projeto com sucesso.', category="success")
        return redirect(url_for('auth.home'))
    
    return render_template('taskMaster.html')

# BOTOES DELETAR TASK

@auth.route('/deletar_tarefa/<int:task_id>/<int:project_id>', methods=['POST'])
@login_required
def deletar_tarefa(task_id, project_id):
    # Buscar a tarefa pelo ID
    tarefa = Task.query.get_or_404(task_id)
    
    try:
        # Deletar a tarefa do banco de dados
        db.session.delete(tarefa)
        db.session.commit()
        flash('Tarefa deletada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao deletar a tarefa.', 'error')

    # Redirecionar para a página do projeto
    return redirect(url_for('auth.gerenciar_projeto', project_id=project_id))






#EDITAR TAREFA
@auth.route('/editar_tarefa/<int:project_id>', methods=['POST'])
@login_required
def editar_tarefa(project_id):
    task_id = request.form.get('task_id')
    task_name = request.form.get('task_name')
    importance = request.form.get('importance')
    ease = request.form.get('ease')

    # Buscar a tarefa no banco de dados
    tarefa = Task.query.get_or_404(task_id)

    # Atualizar os dados da tarefa
    tarefa.description = task_name
    tarefa.importance = importance
    tarefa.ease = ease

    try:
        db.session.commit()
        flash('Tarefa atualizada com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao atualizar a tarefa.', 'error')

    return redirect(url_for('auth.gerenciar_projeto', project_id=project_id))

# CHECKLIST
@auth.route('/checklist/<int:task_id>', methods=['GET'])
@login_required
def checklist(task_id):
    tarefa = Task.query.get_or_404(task_id)
    projeto = Project.query.get_or_404(tarefa.project_id)
    return render_template('checklist.html', tarefa=tarefa, projeto=projeto)


@auth.route('/atualizar_checklist/<int:task_id>/<int:project_id>', methods=['POST'])
@login_required
def atualizar_checklist(task_id, project_id):
    tarefa = Task.query.get_or_404(task_id)
    checklist_items_ids = request.form.getlist('checklist_items')
    print(checklist_items_ids)

    for item in tarefa.checklist_items:
        item.completed = str(item.id) in checklist_items_ids

    db.session.commit()
    flash('Checklist atualizado com sucesso!', 'success')
    return redirect(url_for('auth.checklist', task_id=task_id))


@auth.route('/adicionar_item_checklist/<int:task_id>', methods=['POST'])
@login_required
def adicionar_item_checklist(task_id):
    descricao_item = request.form.get('descricao_item')
    if descricao_item:
        novo_item = ChecklistItem(task_id=task_id, description=descricao_item)
        db.session.add(novo_item)
        db.session.commit()
        flash('Item adicionado com sucesso!', 'success')
    else:
        flash('A descrição do item é obrigatória.', 'error')
    return redirect(url_for('auth.checklist', task_id=task_id))


@auth.route('/excluir_checklist/<int:item_id>/<int:task_id>', methods=['POST'])
@login_required
def excluir_checklist(item_id, task_id):
    item = ChecklistItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item excluído com sucesso!', 'success')
    return redirect(url_for('auth.checklist', task_id=task_id))


@auth.route('/alterar_item_checklist/<int:item_id>/<int:task_id>', methods=['POST'])
@login_required
def alterar_item_checklist(item_id, task_id):
    novo_nome_item = request.form.get('novo_nome_item')
    if novo_nome_item:
        item = ChecklistItem.query.get_or_404(item_id)
        item.description = novo_nome_item
        db.session.commit()
        flash('Nome do item alterado com sucesso!', 'success')
    else:
        flash('O novo nome do item é obrigatório.', 'error')
    return redirect(url_for('auth.checklist', task_id=task_id))
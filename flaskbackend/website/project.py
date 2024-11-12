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

project = Blueprint('project',__name__)


@project.route('/home', methods=['POST', 'GET'])
@login_required
def home():
    if request.method == 'POST':
        nome_projeto = request.form.get('projeto')
        
        if not nome_projeto:
            flash('O nome do projeto é obrigatório.', category='error')
            return redirect(url_for('project.home'))
        
        projeto_existente = Project.query.filter_by(nome_projeto=nome_projeto, user_id=current_user.id).first()

        if projeto_existente:
            flash("Já existe um projeto com esse nome", category='error')
        else:
            projeto_novo = Project(nome_projeto=nome_projeto, user_id=current_user.id)
            db.session.add(projeto_novo)
            try:
                db.session.commit()
                # Adiciona uma notificação
                nova_notificacao = Notification(user_id=current_user.id, content=f'Projeto "{nome_projeto}" foi criado.')
                db.session.add(nova_notificacao)
                db.session.commit()
                flash('Projeto criado com sucesso!', category='success')
            except Exception as e:
                db.session.rollback()
                flash('Erro ao salvar o projeto.', category='error')

        return redirect(url_for('project.home'))

    # Obter todos os projetos do usuário
    projetos_criados = Project.query.filter_by(user_id=current_user.id).all()
    projetos_compartilhados = current_user.projects
    todos_os_projetos = projetos_criados + projetos_compartilhados

    return render_template('taskMaster.html', projects=todos_os_projetos)


@project.route('/projeto/<int:project_id>', methods=['GET', 'POST'])
@login_required
def gerenciar_projeto(project_id):
    projeto = Project.query.get_or_404(project_id)

    if request.method == 'POST':
        task_name = request.form.get('task_name')
        task_status = request.form.get('task_status')
        comment = request.form.get('comment')
        drive_link = request.form.get('drive_link')

        try:
            importance = int(request.form.get('importance'))
            ease = int(request.form.get('ease'))
        except (TypeError, ValueError):
            flash('Valores de importância e facilidade inválidos.', 'error')
            return redirect(url_for('project.gerenciar_projeto', project_id=project_id))

        completion_date = request.form.get('completion_date')
        if not completion_date:
            flash('Data de conclusão é obrigatória.', 'error')
            return redirect(url_for('project.gerenciar_projeto', project_id=project_id))

        try:
            completion_date = datetime.strptime(completion_date, '%Y-%m-%d').date()
        except ValueError:
            flash('Data de conclusão inválida. Use o formato YYYY-MM-DD.', 'error')
            return redirect(url_for('project.gerenciar_projeto', project_id=project_id))

        if task_name and task_status and importance and ease:
            priority = importance * ease
            nova_tarefa = Task(description=task_name, status=task_status, project_id=projeto.id,
                               importance=importance, ease=ease, priority=priority,
                               completion_date=completion_date, comment=comment,
                               drive_link=drive_link)
            db.session.add(nova_tarefa)
            db.session.commit()

            # Adiciona uma notificação
            nova_notificacao = Notification(user_id=current_user.id, content=f'Tarefa "{task_name}" adicionada ao projeto "{projeto.nome_projeto}".')
            db.session.add(nova_notificacao)
            db.session.commit()
            flash('Tarefa adicionada com sucesso!', 'success')
        else:
            flash('Todos os campos são obrigatórios.', 'error')

        return redirect(url_for('project.gerenciar_projeto', project_id=project_id))

    prereq_tasks = Task.query.filter_by(project_id=projeto.id, status='Pré-requisitos').order_by(Task.priority.desc()).all()
    in_prod_tasks = Task.query.filter_by(project_id=projeto.id, status='Em Produção').order_by(Task.priority.desc()).all()
    completed_tasks = Task.query.filter_by(project_id=projeto.id, status='Concluído').order_by(Task.priority.desc()).all()

    return render_template('project_details.html', project=projeto,
                           prereq_tasks=prereq_tasks, in_prod_tasks=in_prod_tasks, 
                           completed_tasks=completed_tasks)

    
@project.route('/editar_projeto/<int:project_id>', methods=['GET', 'POST'])
@login_required
def editar_projeto(project_id):
    projeto = Project.query.get_or_404(project_id)
    
    if request.method == 'POST':
        novo_nome = request.form.get('project_name')
        
        if not novo_nome:
            flash('O nome do projeto não pode ser vazio.', category='error')
        else:
            nome_antigo = projeto.nome_projeto  # Armazenar o nome antigo do projeto
            projeto.nome_projeto = novo_nome
            db.session.commit()
            
            # Adicionar notificação informando a atualização do nome do projeto
            nova_notificacao = Notification(
                user_id=current_user.id,
                content=f'O projeto "{nome_antigo}" foi atualizado para "{novo_nome}".'
            )
            db.session.add(nova_notificacao)
            db.session.commit()
            
            flash('Projeto atualizado com sucesso!', category='success')
            return redirect(url_for('project.home'))
    
    return render_template('editar_projeto.html', projeto=projeto)


@project.route('/deletar_projeto/<int:project_id>', methods=['POST'])
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
        # Adicionar notificação
        nova_notificacao = Notification(user_id=current_user.id, content=f'O projeto "{projeto.nome_projeto}" foi deletado.')
        db.session.add(nova_notificacao)
        db.session.commit()
        db.session.commit()
        
        flash('Projeto e todas as tarefas associadas deletados com sucesso!', category='success')
    except Exception as e:
        db.session.rollback()
        flash('Erro ao deletar o projeto e as tarefas associadas.', 'error')

    return redirect(url_for('project.home'))



@project.route('/adicionar_projeto', methods=['POST'])
@login_required
def adicionar_projeto():
    nome_projeto = request.form.get('project_name')
    
    if not nome_projeto:
        flash('O nome do projeto é obrigatório.', category='error')
        return redirect(url_for('project.home'))

    # Verificar se o projeto já existe
    projeto_existente = Project.query.filter_by(nome_projeto=nome_projeto, user_id=current_user.id).first()
    if projeto_existente:
        flash('Já existe um projeto com esse nome.', category='error')
        return redirect(url_for('project.home'))
    
    # Criar o novo projeto
    novo_projeto = Project(nome_projeto=nome_projeto, user_id=current_user.id)
    db.session.add(novo_projeto)
    try:
        db.session.commit()
        # Adicionar notificação
        nova_notificacao = Notification(user_id=current_user.id, content=f'Projeto "{nome_projeto}" foi criado.', project_id=novo_projeto.id)
        db.session.add(nova_notificacao)
        db.session.commit()
        flash('Projeto criado com sucesso!', category='success')
        flash('Projeto criado com sucesso!', category='success')
    except Exception as e:
        db.session.rollback()
        print(f"Erro ao salvar o projeto: {e}")  # Debug
        flash('Erro ao salvar o projeto.', category='error')
        flash('Projeto criado com sucesso!', category='success')
    return redirect(url_for('project.home'))


@project.route('/compartilhar_projeto/<int:project_id>', methods=['POST'])
@login_required
def compartilhar_projeto(project_id):
    email = request.form.get('emailShare')
    
    if not email:
        flash("Email não recebido.", category="error")
        return redirect(url_for('project.home'))
    
    usuario = Usuario.query.filter_by(email=email).first()

    if not usuario:
        flash("Usuário inexistente", category="error")
        return redirect(url_for('project.home'))
    
    relacao_existente = RelUsuarioProject.query.filter_by(user_id=usuario.id, project_id=project_id).first()

    if relacao_existente:
        flash(f'O usuário {usuario.email} já faz parte deste projeto.', category="info")
    else:
        nova_relacao = RelUsuarioProject(user_id=usuario.id, project_id=project_id)
        db.session.add(nova_relacao)
        db.session.commit()
        
        nova_notificacao = Notification(user_id=usuario.id, content=f'Você foi adicionado ao projeto "{Project.query.get(project_id).nome_projeto}".')
        db.session.add(nova_notificacao)
        db.session.commit()
        
        flash(f'O usuário {usuario.email} foi adicionado ao projeto com sucesso.', category="success")

    return redirect(url_for('project.home'))


@project.route('/notificacoes')
@login_required
def notificacoes():
    notificacoes = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('notificacoes.html', notificacoes=notificacoes)

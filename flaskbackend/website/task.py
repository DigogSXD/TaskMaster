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

task = Blueprint('task',__name__)


# Atualizar TAREFA
@task.route('/atualizar_tarefas', methods=['POST'])
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

            # Adicionar notificação para atualização de status da tarefa
            nova_notificacao = Notification(
                user_id=current_user.id,
                content=f'O status da tarefa "{tarefa.description}" foi atualizado para "{new_status}".',
                task_id=tarefa.id
            )
            db.session.add(nova_notificacao)
            db.session.commit()

    return jsonify({'success': True}), 200



# BOTOES DELETAR TASK
@task.route('/deletar_tarefa/<int:task_id>/<int:project_id>', methods=['POST'])
@login_required
def deletar_tarefa(task_id, project_id):
    # Buscar a tarefa pelo ID
    tarefa = Task.query.get_or_404(task_id)
    
    try:
        # Deletar a tarefa do banco de dados
        db.session.delete(tarefa)
        db.session.commit()
        flash('Tarefa deletada com sucesso!', 'success')
        # Adicionar notificação para exclusão da tarefa
        nova_notificacao = Notification(
            user_id=current_user.id,
            content=f'A tarefa "{tarefa.description}" foi deletada.',
            project_id=project_id,
            task_id=tarefa.id
        )
        db.session.add(nova_notificacao)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('Erro ao deletar a tarefa.', 'error')

    # Redirecionar para a página do projeto
    return redirect(url_for('auth.gerenciar_projeto', project_id=project_id))

#EDITAR TAREFA
@task.route('/editar_tarefa/<int:project_id>', methods=['POST'])
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

         # Adicionar notificação para edição da tarefa
        nova_notificacao = Notification(
            user_id=current_user.id,
            content=f'A tarefa "{task_name}" foi atualizada.',
            project_id=project_id,
            task_id=task_id
        )
        db.session.add(nova_notificacao)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash('Erro ao atualizar a tarefa.', 'error')

    return redirect(url_for('auth.gerenciar_projeto', project_id=project_id))

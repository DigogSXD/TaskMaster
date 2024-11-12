from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from .models import Task, Project, ChecklistItem
from . import db

checklist_bp = Blueprint('checklist_bp', __name__)

# CHECKLIST
@checklist_bp.route('/checklist/<int:task_id>', methods=['GET'])
@login_required
def checklist(task_id):
    tarefa = Task.query.get_or_404(task_id)
    projeto = Project.query.get_or_404(tarefa.project_id)
    return render_template('checklist.html', tarefa=tarefa, projeto=projeto)

@checklist_bp.route('/atualizar_checklist/<int:task_id>/<int:project_id>', methods=['POST'])
@login_required
def atualizar_checklist(task_id, project_id):
    tarefa = Task.query.get_or_404(task_id)
    checklist_items_ids = request.form.getlist('checklist_items')  # Itens marcados

    # Atualiza o campo completed de acordo com a seleção no formulário
    for item in tarefa.checklist_items:
        item.completed = str(item.id) in checklist_items_ids  # Marca como completo se o id estiver em checklist_items_ids

    db.session.commit()  # Salva a atualização de completed no banco de dados
    flash('Checklist atualizado com sucesso!', 'success')
    return redirect(url_for('checklist_bp.checklist', task_id=task_id))

@checklist_bp.route('/adicionar_item_checklist/<int:task_id>', methods=['POST'])
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
    return redirect(url_for('checklist_bp.checklist', task_id=task_id))

@checklist_bp.route('/excluir_checklist/<int:item_id>/<int:task_id>', methods=['POST'])
@login_required
def excluir_checklist(item_id, task_id):
    item = ChecklistItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item excluído com sucesso!', 'success')
    return redirect(url_for('checklist_bp.checklist', task_id=task_id))

@checklist_bp.route('/alterar_item_checklist/<int:item_id>/<int:task_id>', methods=['POST'])
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
    return redirect(url_for('checklist_bp.checklist', task_id=task_id))

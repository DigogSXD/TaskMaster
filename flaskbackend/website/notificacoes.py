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

notificacoes = Blueprint('notificacoes', __name__)

#NOTIFICAÇÕES
@notificacoes.route('/notificacoes')
@login_required
def notifications():
    notificacoes = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('notificacoes.html', notificacoes=notificacoes)

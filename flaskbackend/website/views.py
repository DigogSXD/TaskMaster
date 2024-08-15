from flask import Blueprint ,render_template

views = Blueprint('views',__name__)

@views.route('/')
def login():
    return render_template('login.html')
from flask import Blueprint, render_template, request

auth = Blueprint('auth',__name__)

@auth.route('/',methods=['GET','POST'])
def login():

    return render_template('login.html')
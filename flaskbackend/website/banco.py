from flask import Blueprint, render_template, request,flash,redirect,url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db 
from .models import Usuario ,Project


# Esta bosta, não deu certo

users = Usuario.query.all()

for i in list(users):
    print(i.id_user)
    print(i.email)
    print(i.password)
    print("\n\n")

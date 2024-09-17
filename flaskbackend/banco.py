from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import Usuario, Project
from website import db
from website.models import Usuario, Project

# Fetch all users from the database
users = Usuario.query.all()

# Print each user
for user in users:
    # Fetch all users from the database
    users = Usuario.query.all()

    # Print each user
    for user in users:
        print(user)
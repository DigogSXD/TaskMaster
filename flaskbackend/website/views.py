from flask import Blueprint, render_template, request, flash, redirect, url_for
from . import db 
from .models import Usuario,Project

views = Blueprint('views',__name__)


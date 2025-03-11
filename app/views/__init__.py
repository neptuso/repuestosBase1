from flask import Blueprint, render_template

# Crea un Blueprint para organizar las rutas
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "<h1>¡Bienvenido al sistema de gestión de Re Puestos!</h1>"

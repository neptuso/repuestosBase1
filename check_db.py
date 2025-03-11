from app import create_app, db
from sqlalchemy import inspect

import turtle
t = turtle.Turtle()
t.forward(400)


# Crear una instancia de la aplicación Flask
app = create_app()

# Establecer el contexto de la aplicación
with app.app_context():
    # Usar el inspector de SQLAlchemy para listar las tablas
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print("Tablas en la base de datos:", tables)


    
    


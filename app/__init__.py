from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime



db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///repuestos.db'  # Cambiarás esta línea si usas MySQL más adelante
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'supersecretkey'  # Cambia esto por algo seguro

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Importar y registrar modelos y blueprints **dentro de create_app()**
    from app.models import Cliente, Producto, Venta, Presupuesto, MovimientoStock

    from app.views.clientes import clientes_bp
    app.register_blueprint(clientes_bp)

    from app.views.productos import productos_bp
    app.register_blueprint(productos_bp)

    from app.views.proveedores import proveedores_bp
    app.register_blueprint(proveedores_bp)

    from app.views.main import main_bp
    app.register_blueprint(main_bp)  # Registramos únicamente main_bp

    from app.views.ventas import ventas_bp
    app.register_blueprint(ventas_bp)

    from app.views.reportes import reportes_bp
    app.register_blueprint(reportes_bp)

    return app

if __name__ == "__main__":
    app.run(debug=False)  # Cambiar a False en producción


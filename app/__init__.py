from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

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
    from app.views import main
    from app.views.clientes import clientes_bp  # Importamos el Blueprint de clientes

    app.register_blueprint(main)
    app.register_blueprint(clientes_bp)  # Registramos el Blueprint de clientes

    from app.views.productos import productos_bp
    app.register_blueprint(productos_bp)

    from app.views.proveedores import proveedores_bp
    app.register_blueprint(proveedores_bp)


    return app




from app import db
from datetime import datetime
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

# Modelo para Clientes
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)

# Modelo para Productos
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50))
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'))
    proveedor = db.relationship('Proveedor', backref=db.backref('productos', lazy=True))
    
    def reducir_stock(self,cantidad):
        if cantidad > self.stock:
            raise ValueError("No hay suficiente sotck disponible.")
        self.stock -= cantidad


class Venta(db.Model):
    __tablename__ = 'venta'  # Nombre explícito de la tabla, opcional pero recomendado

    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    fecha_hora = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relación con Producto
    producto = db.relationship('Producto', backref=db.backref('ventas', lazy=True))

    # Relación con Cliente
    cliente = db.relationship('Cliente', backref=db.backref('ventas', lazy=True))

    @property
    def total(self):
        """
        Calcula el total de la venta.
        """
        return self.cantidad * self.precio_unitario

    def __repr__(self):
        """
        Representación legible de la venta.
        """
        return f"<Venta {self.id} - Producto: {self.producto.nombre}, Cliente: {self.cliente.nombre}, Total: {self.total}>"


# Modelo para Presupuestos
class Presupuesto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    total = db.Column(db.Float, nullable=False)
    confirmado = db.Column(db.Boolean, default=False)
    cliente = db.relationship('Cliente', backref=db.backref('presupuestos', lazy=True))

# Modelo para Movimientos de Stock
class MovimientoStock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    tipo = db.Column(db.String(10), nullable=False)  # 'alta' o 'baja'
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    infoadicional = db.Column(db.String(100), nullable=False)
    producto = db.relationship('Producto', backref=db.backref('movimientos', lazy=True))


# Modelo para proveedores
class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    contacto = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    direccion = db.Column(db.Text)




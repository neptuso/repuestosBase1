from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Producto, Venta, Cliente
from app.forms.main import VentaForm

ventas_bp = Blueprint('ventas', __name__)

@ventas_bp.route('/ventas', methods=['GET'])
def listar_ventas():
    ventas = Venta.query.all()
    return render_template('ventas/listar.html', ventas=ventas)

@ventas_bp.route('/ventas/nueva', methods=['GET', 'POST'])
def crear_venta():
    form = VentaForm()

    # Incluye el stock disponible en el menú desplegable de productos
    form.producto_id.choices = [
        (p.id, f"{p.nombre} (Stock: {p.stock})") for p in Producto.query.all()
    ]

    # Carga la lista de clientes
    form.cliente_id.choices = [
        (c.id, c.nombre) for c in Cliente.query.all()
    ]

    if form.validate_on_submit():
        producto = Producto.query.get(form.producto_id.data)
        cliente = Cliente.query.get(form.cliente_id.data)
        if producto and cliente:
            try:
                producto.reducir_stock(form.cantidad.data)  # Actualiza el stock
                nueva_venta = Venta(
                    producto_id=producto.id,
                    cliente_id=cliente.id,
                    cantidad=form.cantidad.data,
                    precio_unitario=producto.precio  # Precio del producto al momento de la venta
                )
                db.session.add(nueva_venta)
                db.session.commit()
                flash('¡Venta registrada con éxito!', 'success')
            except ValueError as e:
                flash(str(e), 'danger')
            return redirect(url_for('ventas.listar_ventas'))
    return render_template('ventas/crear.html', form=form)


from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Producto
from app.forms import ProductoForm

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/productos', methods=['GET'])
def listar_productos():
    productos = Producto.query.all()
    return render_template('productos/listar.html', productos=productos)

@productos_bp.route('/productos/nuevo', methods=['GET', 'POST'])
def crear_producto():
    form = ProductoForm()
    if form.validate_on_submit():
        nuevo_producto = Producto(
            nombre=form.nombre.data,
            categoria=form.categoria.data,
            precio=float(form.precio.data),
            stock=int(form.stock.data)
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        flash('¡Producto creado con éxito!', 'success')
        return redirect(url_for('productos.listar_productos'))
    return render_template('productos/crear.html', form=form)

@productos_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    form = ProductoForm(obj=producto)
    if form.validate_on_submit():
        producto.nombre = form.nombre.data
        producto.categoria = form.categoria.data
        producto.precio = float(form.precio.data)
        producto.stock = int(form.stock.data)
        db.session.commit()
        flash('¡Producto actualizado con éxito!', 'success')
        return redirect(url_for('productos.listar_productos'))
    return render_template('productos/editar.html', form=form, producto=producto)

@productos_bp.route('/productos/eliminar/<int:id>', methods=['POST'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('¡Producto eliminado con éxito!', 'success')
    return redirect(url_for('productos.listar_productos'))

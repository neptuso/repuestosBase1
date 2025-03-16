from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Cliente
from app.forms.main import ClienteForm

clientes_bp = Blueprint('clientes', __name__)

# Listar todos los clientes
@clientes_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes/listar.html', clientes=clientes)

# Crear un cliente nuevo
# Crear un cliente nuevo
@clientes_bp.route('/clientes/nuevo', methods=['GET', 'POST'])
def crear_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        nuevo_cliente = Cliente(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data,
            telefono=form.telefono.data,
            direccion=form.direccion.data
        )
        db.session.add(nuevo_cliente)
        db.session.commit()
        flash('¡Cliente creado con éxito!', 'success')
        return redirect(url_for('clientes.listar_clientes'))
    return render_template('clientes/crear.html', form=form)

# Editar un cliente
@clientes_bp.route('/clientes/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    form = ClienteForm(obj=cliente)
    if form.validate_on_submit():
        cliente.nombre = form.nombre.data
        cliente.apellido = form.apellido.data
        cliente.email = form.email.data
        cliente.telefono = form.telefono.data
        cliente.direccion = form.direccion.data
        db.session.commit()
        flash('¡Cliente actualizado con éxito!', 'success')
        return redirect(url_for('clientes.listar_clientes'))
    return render_template('clientes/editar.html', form=form, cliente=cliente)


# Eliminar un cliente
@clientes_bp.route('/clientes/eliminar/<int:id>', methods=['POST'])
def eliminar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash('¡Cliente eliminado con éxito!', 'success')
    return redirect(url_for('clientes.listar_clientes'))

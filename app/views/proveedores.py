from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Proveedor
from app.forms import ProveedorForm

proveedores_bp = Blueprint('proveedores', __name__)

@proveedores_bp.route('/proveedores', methods=['GET'])
def listar_proveedores():
    proveedores = Proveedor.query.all()
    return render_template('proveedores/listar.html', proveedores=proveedores)

@proveedores_bp.route('/proveedores/nuevo', methods=['GET', 'POST'])
def crear_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        nuevo_proveedor = Proveedor(
            nombre=form.nombre.data,
            contacto=form.contacto.data,
            telefono=form.telefono.data,
            direccion=form.direccion.data
        )
        db.session.add(nuevo_proveedor)
        db.session.commit()
        flash('¡Proveedor creado con éxito!', 'success')
        return redirect(url_for('proveedores.listar_proveedores'))
    return render_template('proveedores/crear.html', form=form)

@proveedores_bp.route('/proveedores/editar/<int:id>', methods=['GET', 'POST'])
def editar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    form = ProveedorForm(obj=proveedor)
    if form.validate_on_submit():
        proveedor.nombre = form.nombre.data
        proveedor.contacto = form.contacto.data
        proveedor.telefono = form.telefono.data
        proveedor.direccion = form.direccion.data
        db.session.commit()
        flash('¡Proveedor actualizado con éxito!', 'success')
        return redirect(url_for('proveedores.listar_proveedores'))
    return render_template('proveedores/editar.html', form=form, proveedor=proveedor)

@proveedores_bp.route('/proveedores/eliminar/<int:id>', methods=['POST'])
def eliminar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
    flash('¡Proveedor eliminado con éxito!', 'success')
    return redirect(url_for('proveedores.listar_proveedores'))

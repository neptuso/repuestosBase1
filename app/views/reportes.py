from flask import Blueprint, render_template, request
from app.forms.main import VentasPorClienteForm
from app.models import Venta, Producto, Cliente
from datetime import datetime, timedelta, timezone
from app import db


hoy = datetime.now(timezone.utc).date()
reportes_bp = Blueprint('reportes', __name__)

@reportes_bp.route('/reportes/diario')
def reporte_diario():
    hoy = datetime.now(timezone.utc).date()
    manana = hoy + timedelta(days=1)
    ventas = Venta.query.filter(Venta.fecha_hora >= hoy, Venta.fecha_hora < manana).all()
    return render_template('reportes/diario.html', ventas=ventas)

@reportes_bp.route('/reportes/mensual')
def reporte_mensual():
    mes_actual = datetime.now(timezone.utc).month
    año_actual = datetime.now(timezone.utc).year
    ventas_por_dia = db.session.query(
        db.func.date(Venta.fecha_hora).label('dia'),
        db.func.sum(Venta.cantidad * Venta.precio_unitario).label('total')
    ).filter(
        db.extract('year', Venta.fecha_hora) == año_actual,
        db.extract('month', Venta.fecha_hora) == mes_actual
    ).group_by(
        db.func.date(Venta.fecha_hora)
    ).all()
    return render_template('reportes/mensual.html', ventas_por_dia=ventas_por_dia)

@reportes_bp.route('/reportes/mas_vendidos')
def productos_mas_vendidos():
    productos = db.session.query(
        Producto.nombre,
        db.func.sum(Venta.cantidad).label('total_cantidad')
    ).join(Venta).group_by(
        Producto.id
    ).order_by(
        db.desc('total_cantidad')
    ).limit(10).all()
    return render_template('reportes/mas_vendidos.html', productos=productos)


@reportes_bp.route('/reportes/ventas_por_cliente', methods=['GET', 'POST'])
def ventas_por_cliente():
    form = VentasPorClienteForm()
    form.cliente_id.choices = [
        (c.id, c.nombre) for c in Cliente.query.all()
    ]
    ventas = []
    if form.validate_on_submit():
        ventas = Venta.query.filter(
            Venta.cliente_id == form.cliente_id.data,
            Venta.fecha_hora >= form.fecha_inicio.data,
            Venta.fecha_hora <= form.fecha_fin.data
        ).all()
    return render_template('reportes/ventas_por_cliente.html', form=form, ventas=ventas)


from flask import Response
from reportlab.pdfgen import canvas
from io import BytesIO

@reportes_bp.route('/reportes/diario/pdf')
def reporte_diario_pdf():
    hoy = datetime.now(timezone.utc).date()
    manana = hoy + timedelta(days=1)
    ventas = Venta.query.filter(Venta.fecha_hora >= hoy, Venta.fecha_hora < manana).all()

    # Generar PDF en memoria
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 800, "Reporte Diario - Ventas")
    y = 750
    for venta in ventas:
        texto = f"{venta.fecha_hora} - {venta.producto.nombre} - Cantidad: {venta.cantidad} - Total: ${venta.total:.2f}"
        pdf.drawString(50, y, texto)
        y -= 20
        if y < 50:  # Nueva página si el espacio se acaba
            pdf.showPage()
            y = 750
    pdf.save()

    buffer.seek(0)
    return Response(buffer, mimetype='application/pdf', headers={"Content-Disposition": "inline; filename=reporte_diario.pdf"})


from io import StringIO
from flask import Response
import csv

@reportes_bp.route('/reportes/diario/csv')
def reporte_diario_csv():
    hoy = datetime.now(timezone.utc).date()
    manana = hoy + timedelta(days=1)
    ventas = Venta.query.filter(Venta.fecha_hora >= hoy, Venta.fecha_hora < manana).all()

    # Crear CSV en memoria
    output = StringIO()  # Cambiar a StringIO
    writer = csv.writer(output)
    writer.writerow(["Fecha", "Producto", "Cantidad", "Total"])  # Cabecera
    for venta in ventas:
        writer.writerow([venta.fecha_hora, venta.producto.nombre, venta.cantidad, f"${venta.total:.2f}"])
    
    # Retornar el CSV como bytes
    output.seek(0)
    return Response(output.getvalue(), mimetype='text/csv', headers={"Content-Disposition": "attachment; filename=reporte_diario.csv"})


# repoprte mensual - genera PDF
@reportes_bp.route('/reportes/mensual/pdf')
def reporte_mensual_pdf():
    mes_actual = datetime.now(timezone.utc).month
    año_actual = datetime.now(timezone.utc).year
    ventas_por_dia = db.session.query(
        db.func.date(Venta.fecha_hora).label('dia'),
        db.func.sum(Venta.cantidad * Venta.precio_unitario).label('total')
    ).filter(
        db.extract('year', Venta.fecha_hora) == año_actual,
        db.extract('month', Venta.fecha_hora) == mes_actual
    ).group_by(
        db.func.date(Venta.fecha_hora)
    ).all()

    # Generar PDF
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 800, "Reporte Mensual - Ventas")
    y = 750
    for venta in ventas_por_dia:
        texto = f"{venta.dia} - Total: ${venta.total:.2f}"
        pdf.drawString(50, y, texto)
        y -= 20
        if y < 50:
            pdf.showPage()
            y = 750
    pdf.save()
    buffer.seek(0)
    return Response(buffer, mimetype='application/pdf', headers={"Content-Disposition": "inline; filename=reporte_mensual.pdf"})


# Reporte mensual para exportar CSV
@reportes_bp.route('/reportes/mensual/csv')
def reporte_mensual_csv():
    mes_actual = datetime.now(timezone.utc).month
    año_actual = datetime.now(timezone.utc).year
    ventas_por_dia = db.session.query(
        db.func.date(Venta.fecha_hora).label('dia'),
        db.func.sum(Venta.cantidad * Venta.precio_unitario).label('total')
    ).filter(
        db.extract('year', Venta.fecha_hora) == año_actual,
        db.extract('month', Venta.fecha_hora) == mes_actual
    ).group_by(
        db.func.date(Venta.fecha_hora)
    ).all()

    # Crear CSV - informe diario
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Día", "Total Ventas"])
    for venta in ventas_por_dia:
        writer.writerow([venta.dia, f"${venta.total:.2f}"])
    output.seek(0)
    return Response(output.getvalue(), mimetype='text/csv', headers={"Content-Disposition": "attachment; filename=reporte_mensual.csv"})


from app.forms.filtros import FiltroVentasForm
@reportes_bp.route('/reportes/filtro', methods=['GET', 'POST'])
def reporte_filtro():
    form = FiltroVentasForm()

    # Opciones dinámicas para productos y clientes
    form.producto_id.choices = [(0, 'Todos')] + [(p.id, p.nombre) for p in Producto.query.all()]
    form.cliente_id.choices = [(0, 'Todos')] + [(c.id, c.nombre) for c in Cliente.query.all()]

    # Filtrado dinámico
    ventas = Venta.query
    if form.validate_on_submit():
        if form.producto_id.data != 0:
            ventas = ventas.filter(Venta.producto_id == form.producto_id.data)
        if form.cliente_id.data != 0:
            ventas = ventas.filter(Venta.cliente_id == form.cliente_id.data)
        if form.fecha_inicio.data:
            ventas = ventas.filter(Venta.fecha_hora >= form.fecha_inicio.data)
        if form.fecha_fin.data:
            ventas = ventas.filter(Venta.fecha_hora <= form.fecha_fin.data)

    ventas = ventas.all()
    return render_template('reportes/filtro.html', form=form, ventas=ventas)

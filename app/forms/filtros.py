from wtforms import SelectField, DateField, SubmitField
from wtforms.validators import Optional
from flask_wtf import FlaskForm

class FiltroVentasForm(FlaskForm):
    producto_id = SelectField('Producto', coerce=int, choices=[], validators=[Optional()])
    cliente_id = SelectField('Cliente', coerce=int, choices=[], validators=[Optional()])
    fecha_inicio = DateField('Fecha Inicio', format='%Y-%m-%d', validators=[Optional()])
    fecha_fin = DateField('Fecha Fin', format='%Y-%m-%d', validators=[Optional()])
    submit = SubmitField('Filtrar')

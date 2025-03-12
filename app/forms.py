from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class ClienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telefono = StringField('Teléfono', validators=[Length(max=20)])
    direccion = TextAreaField('Dirección', validators=[Length(max=200)])
    submit = SubmitField('Guardar')


from wtforms import SelectField

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    categoria = StringField('Categoría', validators=[Length(max=50)])
    precio = StringField('Precio', validators=[DataRequired()])
    stock = StringField('Stock', validators=[DataRequired()])
    proveedor_id = SelectField('Proveedor', coerce=int)
    submit = SubmitField('Guardar')


class ProveedorForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    contacto = StringField('Contacto', validators=[Length(max=100)])
    telefono = StringField('Teléfono', validators=[Length(max=20)])
    direccion = StringField('Dirección')
    submit = SubmitField('Guardar')


from wtforms import SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm

class VentaForm(FlaskForm):
    cliente_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])
    producto_id = SelectField('Producto', coerce=int, validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Registrar Venta')


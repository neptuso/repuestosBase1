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

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    categoria = StringField('Categoría', validators=[Length(max=50)])
    precio = StringField('Precio', validators=[DataRequired()])
    stock = StringField('Stock', validators=[DataRequired()])
    submit = SubmitField('Guardar')

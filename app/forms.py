from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, SubmitField
from wtforms.validators import DataRequired


ESCOLARIDAD = [
    'No estudió', 'Primaria', 'Secundaria', 'Bachillerato', 
    'Universidad o Posgrado', 'Desconocido', 
]

NO_SI = ["No", u"Sí",]

CANTIDAD = ['Ninguno', '1', '2', '3', '4 o más',]


class Atributos(FlaskForm):
    SERV = SelectField(u"Tipo de escuela a la que asiste", choices=[
        'Comunitaria', 'General Pública', 'Privada', 'Indígena'
    ])
    TAM_LOC_PRIM = SelectField(u"Tamaño de la localidad", choices=[
        '1 a 499', '500 a 2499', '2500 a 99999', '100000 o más',
    ])
    SEXO = SelectField(u"Sexo", choices=["Mujer", "Hombre"])
    EDAD_ACC = SelectField(u"Edad", choices=[
        '11 años o menos', '12 años', '13 años', '14 años o más',
    ])
    PAB_4 = SelectField(u"Habitaciones en casa (además de cocina y baños)", choices=[
        '1', '2', '3', '4', u'5 o más'
    ])
    PAB_11 = SelectField(u"Nivel de estudios del padre",
        choices=ESCOLARIDAD)
    PAB_12 = SelectField(u"Nivel de estudio de la madre", 
        choices=ESCOLARIDAD)
    PAB_14 = SelectField(u"Habla una lengua indígena", choices=NO_SI)
    PAB_16 = SelectField(u"Años de asistencia a preescolar", choices=[
        u'No asistió', u'1 año o menos', u'2 años', 
        u'3 años', u'Asistió, años desconocidos', 
    ])
    PAB_22 = SelectField(u"Número de focos en casa (incluidas lámparas)", choices=[
        'Ninguno', 'De 1 a 5', 'De 6 a 10', 'De 11 a 15', 'Más de 15',
    ])
    PAB_24 = SelectField(u"Luz eléctrica", choices=NO_SI)
    PAB_25 = SelectField(u"Agua potable", choices=NO_SI)
    PAB_26 = SelectField(u"Drenaje", choices=NO_SI)
    PAB_29 = SelectField(u"Refrigerador", choices=NO_SI)
    PAB_31 = SelectField(u"Estufa de gas o eléctrica", choices=NO_SI)
    PAB_34 = SelectField(u"Acceso a internet", choices=NO_SI)
    PAB_35 = SelectField(u"Cantidad de computadoras o laptops en casa", choices=CANTIDAD)
    PAB_37 = SelectField(u"Cantidad de automóviles en casa", choices=CANTIDAD)
    PAB_38 = SelectField(u"Cantidad de teléfonos móviles o celulares en casa", choices=CANTIDAD)
    PAB_39 = SelectField(u"Cantidad de tabletas en casa", choices=CANTIDAD)
    PAB_48 = SelectField(u"Cantidad de libros en casa", choices=[
        'Ninguno', 'Entre 1 y 25', 'Entre 26 y 50', 'Entre 51 y 100', 'Más de 100', 
    ])
    PAB_52 = SelectField(u"Asiste a clases de idiomas (inglés u otro)", choices=NO_SI)
    PAB_53 = SelectField(u"Sin contar clases de idiomas, toma clases extra (Matemáticas, Español, etc.)", choices=NO_SI)
    PAB_85 = SelectField(u"Tiempo de traslado de la casa a la escuela", choices=[
        'Máximo 15 minutos', 'De 16 a 30 minutos', 'De 31 minutos a una hora',
        'Entre 1 y 2 horas', 'Más de 2 horas', 
    ])
    submit = SubmitField('Enviar')

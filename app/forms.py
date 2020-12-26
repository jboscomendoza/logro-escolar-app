from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, SubmitField
from wtforms.validators import DataRequired


ESCOLARIDAD = [
    'No estudió', 'Primaria', 'Secundaria', 'Bachillerato', 
    'Universidad o Posgrado', 'Desconocido', 
]

NO_SI = ["No", u"Sí"]

CANTIDAD = [
    'Ninguno', '1', '2', '3', '4 o más',
]


class Atributos(FlaskForm):
    SERV = SelectField(u"Tipo de servicio", choices=[
        'Comunitaria', 'General Pública', 'Privada', 'Indígena'
    ])
    TAM_LOC_PRIM = SelectField(u"Tamaño de la localidad", choices=[
        '1 a 499', '500 a 2499', '2500 a 99999', '100000 o más',
    ])
    SEXO = SelectField(u"Sexo", choices=["Mujer", "Hombre"])
    EDAD_ACC = SelectField(u"Edad", choices=[
        '11 años o menos', '12 años', '14 años o más', '13 años'
    ])
    PAB_4 = SelectField(u"¿Cuántos cuartos se utilizan para dormir en tu casa?", choices=[
        '1', '2', '3', '4', u'5 o más'
    ])
    PAB_11 = SelectField(u"¿Hasta qué nivel estudió tu papá?",
        choices=ESCOLARIDAD)
    PAB_12 = SelectField(u"¿Hasta qué nivel estudió tu mamá?", 
        choices=ESCOLARIDAD)
    PAB_14 = SelectField(u"¿Sabes hablar una lengua indígena?", choices=NO_SI)
    PAB_16 = SelectField(u"¿Cuántos años fuiste a preescolar?", choices=[
        'No fui', u'1 año o menos', u'2 años', 
        u'3 años', u'Asistió, años desconocidos', 
    ])
    PAB_22 = SelectField(u"¿Cuántos focos hay en tu casa (incluidas lámparas)?", choices=[
        'Ninguno', 'De 11 a 15', 'De 6 a 10', 'De 1 a 5', 'Más de 15',
    ])
    PAB_24 = SelectField(u"¿Tienes Luz eléctrica en tu casa?", choices=NO_SI)
    PAB_25 = SelectField(u"¿Tienes Agua potable en tu casa?", choices=NO_SI)
    PAB_26 = SelectField(u"¿Tienes Drenaje en tu casa?", choices=NO_SI)
    PAB_29 = SelectField(u"¿Tienes Refrigerador en tu casa?", choices=NO_SI)
    PAB_31 = SelectField(u"¿Tienes Estufa de gas o estufa eléctrica en tu casa?", choices=NO_SI)
    PAB_34 = SelectField(u"¿Tienes Acceso a internet en tu casa?", choices=NO_SI)
    PAB_35 = SelectField(u"¿Cuántas computadoras o laptops hay en tu casa?", choices=CANTIDAD)
    PAB_37 = SelectField(u"¿Cuántos automóviles hay en tu casa?", choices=CANTIDAD)
    PAB_38 = SelectField(u"¿Cuántos teléfonos móviles o celulares hay en tu casa?", choices=CANTIDAD)
    PAB_39 = SelectField(u"¿Cuántas tablets hay en tu casa?", choices=CANTIDAD)
    PAB_48 = SelectField(u"¿Cuántos libros hay en tu casa?", choices=[
        'Ninguno', 'Entre 1 y 25', 'Entre 26 y 50', 'Entre 51 y 100', 'Más de 100', 
    ])
    PAB_52 = SelectField(u"Además de ir a la escuela, ¿asistes a alguna clase de idiomas (inglés u otro)?", choices=NO_SI)
    PAB_53 = SelectField(u"Sin contar las clases de idiomas, ¿tomas fuera de la escuela alguna clase que te ayude en las materias (Matemáticas, Español, etcétera)?", choices=NO_SI)
    PAB_85 = SelectField(u"¿Cuánto tiempo tardas en llegar de tu casa a la escuela?", choices=[
        'Máximo 15 minutos', 'De 16 a 30 minutos', 'De 31 minutos a una hora',
        'Entre 1 y 2 horas', 'Más de 2 horas', 
    ])
    submit = SubmitField('Enviar')

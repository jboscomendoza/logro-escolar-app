from flask_wtf import FlaskForm
from wtforms import SelectField, RadioField, SubmitField
from wtforms.validators import DataRequired


ESCOLARIDAD = [
    'No estudió', 
    'Primaria completa', 
    'Primaria incompleta', 
    'Secundaria completa',
    'Secundaria incompleta',
    'Preparatoria, bachillerato o carrera técnica', 
    'Carrera universitaria o posgrado (especialidad, maestría o doctorado)'
    'No sé',
    'No tengo',
]
NO_SI = ["No", u"Sí"]
CANTIDAD = [
    '1', '2', '3', '4 o más', 'Ninguno'
]


class Atributos(FlaskForm):
    SERV = RadioField(u"Tipo de servicio", choices=[
        'Comunitaria', 'General Pública', 'Privada', 'Indígena'
    ])
    TAM_LOC_PRIM = RadioField(u"Tamaño de la localidad", choices=[
        '1 a 499', '500 a 2499', '2500 a 99999', '100000 o más', 
        'No identificada'
    ])
    SEXO = RadioField(u"Sexo", choices=["Mujer", "Hombre"])
    EDAD_ACC = RadioField(u"Edad", choices=[
        '11 años o menos', '12 años', '14 años o más', '13 años'
    ])
    PAB_4 = RadioField(u"¿Cuántos cuartos se utilizan para dormir en tu casa?", choices=[
        '1', '2', '3', '4', '5', '6', '7', '8', '9 o más'
    ])
    PAB_11 = RadioField(u"¿Hasta qué nivel estudió tu papá?",
        choices=ESCOLARIDAD)
    PAB_12 = RadioField(u"¿Hasta qué nivel estudió tu mamá?", 
        choices=ESCOLARIDAD)
    PAB_14 = RadioField(u"¿Sabes hablar una lengua indígena?", choices=NO_SI)
    PAB_16 = RadioField(u"¿Cuántos años fuiste a preescolar?", choices=[
        'No fui', '1 año o menos', '2 años', 
        '3 años', 'Sí asistí, pero no sé cuántos años', 
    ])
    PAB_22 = RadioField(u"¿Cuántos focos hay en tu casa (incluidas lámparas)?", choices=[
        'De 11 a 15', 'De 6 a 10', 'De 1 a 5', 'Más de 15', 'Ninguno'
    ])
    PAB_24 = RadioField(u"¿Tienes Luz eléctrica en tu casa?", choices=NO_SI)
    PAB_25 = RadioField(u"¿Tienes Agua potable en tu casa?", choices=NO_SI)
    PAB_26 = RadioField(u"¿Tienes Drenaje en tu casa?", choices=NO_SI)
    PAB_29 = RadioField(u"¿Tienes Refrigerador en tu casa?", choices=NO_SI)
    PAB_31 = RadioField(u"¿Tienes Estufa de gas o estufa eléctrica en tu casa?", choices=NO_SI)
    PAB_34 = RadioField(u"¿Tienes Acceso a internet en tu casa?", choices=NO_SI)
    PAB_35 = RadioField(u"¿Cuántas computadoras o laptops hay en tu casa?", choices=CANTIDAD)
    PAB_37 = RadioField(u"¿Cuántos automóviles hay en tu casa?", choices=CANTIDAD)
    PAB_38 = RadioField(u"¿Cuántos teléfonos móviles o celulares hay en tu casa?", choices=CANTIDAD)
    PAB_39 = RadioField(u"¿Cuántas tablets hay en tu casa?", choices=CANTIDAD)
    PAB_48 = RadioField(u"¿Cuántos libros hay en tu casa?", choices=[
        'Ninguno', 'Entre 1 y 25', 'Entre 26 y 50', 'Entre 51 y 100', 'Más de 100', 
    ])
    PAB_52 = RadioField(u"Además de ir a la escuela, ¿asistes a alguna clase de idiomas (inglés u otro)?", choices=NO_SI)
    PAB_53 = RadioField(u"Sin contar las clases de idiomas, ¿tomas fuera de la escuela alguna clase que te ayude en las materias (Matemáticas, Español, etcétera)?", choices=NO_SI)
    PAB_85 = RadioField(u"¿Cuánto tiempo tardas en llegar de tu casa a la escuela?", choices=[
        'Máximo 15 minutos', 'De 16 a 30 minutos', 'De 31 minutos a una hora',
        'Entre 1 y 2 horas', 'Más de 2 horas', 
    ])
    submit = SubmitField('Enviar')

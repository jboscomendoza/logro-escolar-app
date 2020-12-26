from flask import render_template
from app import app
from app.forms import Atributos

@app.route('/')
@app.route('/index')
def inicio():
    form = Atributos()
    return render_template("index.html", form=form)
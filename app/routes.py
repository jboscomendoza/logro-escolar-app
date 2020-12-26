from flask import render_template, request, redirect, url_for
from app import app
from app.forms import Atributos

@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def inicio():
    form = Atributos()

    if form.validate_on_submit():
        loco = request.form.to_dict()
        return loco
    
    return render_template("index.html", form=form)
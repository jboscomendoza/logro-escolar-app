from flask import render_template, request, redirect, url_for
from app import app
from app.forms import Atributos
from catboost import CatBoostRegressor


modelo_lyc = CatBoostRegressor()
modelo_lyc.load_model("model_lyc.cbm")
modelo_mat = CatBoostRegressor()
modelo_mat.load_model("model_mat.cbm")


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def inicio():
    form = Atributos()

    if form.validate_on_submit():
        data = request.form.to_dict()
        for i in ["csrf_token", "submit"]:
            data.pop(i)
        return redirect(url_for("resultado", atributos=data))
    
    return render_template("index.html", form=form)


@app.route("/resultado/<atributos>", methods=["GET", "POST"])
def resultado(atributos):
    data_atr = eval(atributos)

    nombres = list(data_atr.keys())
    nombres.sort()
    data_list = [data_atr[i] for i in nombres]

    resultado = {}
    resultado["lyc"] = modelo_lyc.predict(data_list)
    resultado["mat"] = modelo_mat.predict(data_list)

    return redirect(url_for("resumen", resultado=resultado))


@app.route("/resumen/<resultado>", methods=["GET"])
def resumen(resultado):
    resultado = eval(resultado)

    return render_template("resumen.html", resultado=resultado)

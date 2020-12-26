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
        return redirect(url_for("resultado", atributos=data))
    
    return render_template("index.html", form=form)

@app.route("/resultado", methods=["GET", "POST"])
def resultado():
    data_atr = eval(request.args["atributos"])
    for i in ["csrf_token", "submit"]:
            data_atr.pop(i)
    data_atr = list(data_atr.values())
    
    resultado = {}
    resultado["lyc"] = modelo_lyc.predict(data_atr)
    resultado["mat"] = modelo_mat.predict(data_atr)
    return redirect(url_for("resumen", resultado=resultado))

@app.route("/resumen/<resultado>", methods=["GET"])
def resumen(resultado):
    resultado = eval(resultado)
    return resultado
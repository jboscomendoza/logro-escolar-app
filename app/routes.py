import numpy as np
import pandas as pd

from flask import render_template, request, redirect, url_for

from app import app
from app.forms import Atributos
from catboost import CatBoostRegressor
from bokeh.plotting import figure
from bokeh.embed import components


modelo_lyc = CatBoostRegressor()
modelo_lyc.load_model("model_lyc.cbm")
modelo_mat = CatBoostRegressor()
modelo_mat.load_model("model_mat.cbm")

cuantiles_lyc = pd.read_csv("cuantiles_lyc.csv")
cuantiles_mat = pd.read_csv("cuantiles_mat.csv")


def comparar_cuantiles(score, asignatura):
    if asignatura == "MAT":
        df = cuantiles_mat
    elif asignatura == "LYC":
        df = cuantiles_lyc
    servicios = df["SERV"].unique()
    
    lista_cuantiles = []
    for serv in servicios:
        for i, row in df[df["SERV"] == serv].iterrows():
            if score >= row[asignatura]:
                cual = {}
                cual["decil"] = row["decil"]
                cual["serv"] = serv
            else:
                break
        lista_cuantiles.append(cual)

    return lista_cuantiles


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


@app.route("/resultado/<atributos>", methods=["GET"])
def resultado(atributos):
    data_atr = eval(atributos)

    nombres = list(data_atr.keys())
    nombres.sort()
    data_list = [data_atr[i] for i in nombres]

    resultado = {}
    resultado["LYC"] = modelo_lyc.predict(data_list)
    resultado["MAT"] = modelo_mat.predict(data_list)

    return redirect(url_for("resumen", resultado=resultado))

@app.route("/resumen/<resultado>", methods=["GET"])
def resumen(resultado):
    resultado = eval(resultado)
    comp_mat = comparar_cuantiles(resultado["MAT"], "MAT")
    comp_lyc = comparar_cuantiles(resultado["LYC"], "LYC")

    x_lyc = list(cuantiles_lyc["decil"])
    y_lyc = list(cuantiles_lyc["LYC"][cuantiles_lyc["SERV"] == "Nacional"])
    plot_lyc = figure(plot_width=400, plot_height=400, title="", toolbar_location="below")
    plot_lyc.line(x_lyc, y_lyc)

    x_mat = list(cuantiles_mat["decil"])
    y_mat = list(cuantiles_mat["MAT"][cuantiles_mat["SERV"] == "Nacional"])
    plot_mat = figure(plot_width=400, plot_height=400, title="", toolbar_location="below")
    plot_mat.line(x_mat, y_mat)

    script_lyc, div_lyc = components(plot_lyc)
    script_mat, div_mat = components(plot_mat)
    
    kwargs = {
        "script_lyc": script_lyc, "div_lyc": div_lyc,
        "script_mat": script_mat, "div_mat": div_mat,
        }
    kwargs['title'] = "Resumen de resultados"

    return render_template("resumen.html", 
        resultado=resultado,
        comp_mat=comp_mat,
        comp_lyc=comp_lyc,
        **kwargs
    )

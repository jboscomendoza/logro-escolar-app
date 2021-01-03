from flask import render_template, request, redirect, url_for
from app import app
from app.forms import Atributos

import numpy as np
import pandas as pd

from catboost import CatBoostRegressor
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CDSView, GroupFilter
from bokeh.embed import components


modelo_lyc = CatBoostRegressor()
modelo_lyc.load_model("model_lyc.cbm")
modelo_mat = CatBoostRegressor()
modelo_mat.load_model("model_mat.cbm")

CUANTILES_LYC = pd.read_csv("CUANTILES_LYC.csv")
CUANTILES_MAT = pd.read_csv("CUANTILES_MAT.csv")

COLORES = ["#000000", "#7d3c98", "#f39c12", "#3498db", "#2ecc71"]


def comparar_cuantiles(score, asignatura):
    if asignatura == "MAT":
        df = CUANTILES_MAT
    elif asignatura == "LYC":
        df = CUANTILES_LYC
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


def crear_plot_dist(asignatura, score_actual):
    if asignatura == "MAT":
        df = CUANTILES_MAT
    elif asignatura == "LYC":
        df = CUANTILES_LYC
    
    plot_dist = figure(plot_width=450, plot_height=500, toolbar_location="below")
    
    for i, j in zip(df["SERV"].unique(), COLORES):
        fuente = ColumnDataSource(df[df["SERV"] == i])
        plot_dist.line("decil", asignatura, source=fuente, color = j, legend_label=i)
    
    plot_dist.ray(
        x=[0], y=[score_actual], length=100, angle=0, 
        line_width=2, color="#e74c3c", legend_label="Puntaje obtenido"
    )

    plot_dist.legend.location = 'top_left'

    return plot_dist


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
    
    plot_lyc = crear_plot_dist("LYC", resultado["LYC"])
    plot_mat = crear_plot_dist("MAT", resultado["MAT"])
    
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

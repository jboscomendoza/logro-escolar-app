from flask import render_template, request, redirect, url_for
from app import app
from app.forms import Atributos, SecForm

import numpy as np
import pandas as pd

from catboost import CatBoostRegressor
from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CDSView, GroupFilter
from bokeh.embed import components


MODELOS = {
    "primaria":{
        "LYC": CatBoostRegressor().load_model("model_lyc.cbm"),
        "MAT": CatBoostRegressor().load_model("model_mat.cbm"),
    },
    "secundaria":{
        "LYC": CatBoostRegressor().load_model("model_sec_lyc.cbm"),
        "MAT": CatBoostRegressor().load_model("model_sec_mat.cbm"),
    }
}

CUANTILES = {
    "primaria":{
        "LYC":pd.read_csv("cuantiles_lyc.csv"),
        "MAT":pd.read_csv("cuantiles_mat.csv"),
    },
    "secundaria":{
        "LYC":pd.read_csv("cuantiles_sec_lyc.csv"),
        "MAT":pd.read_csv("cuantiles_sec_mat.csv"),
    }
}

COLORES = [
    "#000000", "#7d3c98", "#f39c12",
    "#3498db", "#2ecc71", "#f72585"
]


def comparar_cuantiles(score, asignatura, grado):    
    df = CUANTILES[grado][asignatura]
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


def crear_plot_dist(asignatura, score_actual, grado):
    df = CUANTILES[grado][asignatura]
    
    plot_dist = figure(plot_width=450, plot_height=500, toolbar_location="below")
    
    for i, j in zip(df["SERV"].unique(), COLORES):
        fuente = ColumnDataSource(df[df["SERV"] == i])
        plot_dist.line("decil", asignatura, source=fuente, color = j, legend_label=i)
    
    plot_dist.ray(
        x=[0], y=[score_actual], length=100, angle=0, 
        line_width=1.5, color="#e74c3c", line_dash="dashed",
        legend_label="Puntaje obtenido"
    )

    plot_dist.legend.location = 'top_left'

    return plot_dist


@app.route('/', methods=["GET", "POST"])
@app.route('/index/', methods=["GET", "POST"])
def inicio():
    return render_template("index.html")


@app.route('/primaria/', methods=["GET", "POST"])
def primaria():
    form = Atributos()

    if form.validate_on_submit():
        data = request.form.to_dict()
        grado = "primaria"
        for i in ["csrf_token", "submit"]:
            data.pop(i)
        return redirect(url_for("resultado", grado=grado, atributos=data))
    
    return render_template("primaria.html", form=form)


@app.route('/secundaria/', methods=["GET", "POST"])
def secundaria():
    form = SecForm()

    if form.validate_on_submit():
        data = request.form.to_dict()
        grado = "secundaria"
        for i in ["csrf_token", "submit"]:
            data.pop(i)
        return redirect(url_for("resultado", grado=grado, atributos=data))
    
    return render_template("secundaria.html", form=form)


@app.route("/resultado/<grado>/<atributos>", methods=["GET"])
def resultado(grado, atributos):
    data_atr = eval(atributos)

    nombres = list(data_atr.keys())
    nombres.sort()
    data_list = [data_atr[i] for i in nombres]

    resultado = {}
    resultado["LYC"] = MODELOS[grado]["LYC"].predict(data_list)
    resultado["MAT"] = MODELOS[grado]["MAT"].predict(data_list)

    return redirect(url_for("resumen", grado=grado, resultado=resultado))


@app.route("/resumen/<grado>/<resultado>/", methods=["GET"])
def resumen(grado, resultado):
    resultado = eval(resultado)
    comp_mat = comparar_cuantiles(resultado["MAT"], "MAT", grado)
    comp_lyc = comparar_cuantiles(resultado["LYC"], "LYC", grado)
    
    plot_lyc = crear_plot_dist("LYC", resultado["LYC"], grado)
    plot_mat = crear_plot_dist("MAT", resultado["MAT"], grado)
    
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

import numpy as np
import pandas as pd
import re

# Variables relevantes
seleccion = [
    "SERV", "TAM_LOC_PRIM", "SEXO", "EDAD_ACC",
    "PAB_4", "PAB_11", "PAB_12", "PAB_14", "PAB_16", 
    "PAB_22", "PAB_24", "PAB_25", "PAB_26", "PAB_29",
    "PAB_31", "PAB_34", "PAB_35", "PAB_37", "PAB_38", 
    "PAB_39", "PAB_48", "PAB_52", "PAB_53", "PAB_85",
    "PV1MAT", "PV2MAT", "PV3MAT", "PV4MAT", "PV5MAT",
    "PV1LYC", "PV2LYC", "PV3LYC", "PV4LYC", "PV5LYC"
]

vars_mat = ["PV1MAT", "PV2MAT", "PV3MAT", "PV4MAT", "PV5MAT"]
vars_lyc = ["PV1LYC", "PV2LYC", "PV3LYC", "PV4LYC", "PV5LYC"]

# Lectura
p18 = pd.read_spss("Planea06_2018_alumnos.sav", usecols=seleccion)

# Procesamiento
contexto = p18.drop(vars_mat, axis=1)
contexto = contexto.drop(vars_lyc, axis=1)

contexto["MAT"] = p18[vars_mat].mean(axis = 1).round()
contexto["LYC"] = p18[vars_lyc].mean(axis = 1).round()


contexto[["MAT", "LYC"]] = contexto[["MAT", "LYC"]].mask(contexto[["MAT", "LYC"]] >= 800, 800)
contexto[["MAT", "LYC"]] = contexto[["MAT", "LYC"]].mask(contexto[["MAT", "LYC"]] <= 200, 200)

contexto["PAB_4"] = contexto["PAB_4"].replace(["5", "6", "7", "8", "9 o más",], u"5 o más")

contexto[["PAB_11", "PAB_12"]] = contexto[["PAB_11", "PAB_12"]].replace(
    ["No sé", "No tengo papá", "No tengo mamá"], "Desconocido"
    ).replace(
    ["Primaria incompleta", "Primaria completa"], "Primaria"
    ).replace(
    ["Secundaria incompleta", "Secundaria completa"], "Secundaria"
    ).replace(
    ["Preparatoria, bachillerato o carrera técnica", "Carrera universitaria o posgrado (especialidad, maestría o doctorado)"],
    ["Bachillerato", "Universidad o Posgrado"]
    )

contexto["PAB_16"] = contexto["PAB_16"].replace(
    [u"No fui", u"Sí asistí, pero no sé cuántos años"], 
    [u"No asistió", u"Asistió, años desconocidos"]
)
contexto = contexto[contexto["TAM_LOC_PRIM"] != 'No identificada']

perdidos_renglon = contexto.isnull().sum(axis=1) 

contexto = contexto.dropna()

contexto.to_csv("pri.csv", index=False)


scores = contexto[["SERV", "MAT", "LYC"]]
scores_group = scores.groupby("SERV").mean().reset_index()

scores.to_csv("scores.csv", index=False)
scores_group.to_csv("scores_group.csv", index=False)


# Cuantiles
def extraer_cuantiles(df, asignatura):
    #cortes = [i / 100 for i in range(0, 110, 10)]
    cortes = np.arange(0, 1, .01)
    servicios = list(df["SERV"].unique())
    
    lista_cuantiles = []

    cuantiles_nac = df[asignatura].quantile(cortes).reset_index()
    cuantiles_nac["SERV"] = "Nacional"
    lista_cuantiles.append(cuantiles_nac)

    for i in servicios:
        por_serv = df[df["SERV"] == i]
        por_serv = por_serv[asignatura].quantile(cortes).reset_index()
        por_serv["SERV"] = i
        lista_cuantiles.append(por_serv)

    cuantiles_todo = pd.concat(lista_cuantiles)

    cuantiles_todo = cuantiles_todo.rename(columns={"index":"decil"})
    cuantiles_todo["decil"] = np.round(cuantiles_todo["decil"] * 100)
    return cuantiles_todo


cuantiles_mat = extraer_cuantiles(contexto, "MAT")
cuantiles_mat.to_csv("cuantiles_pri_mat.csv", index=False)

cuantiles_lyc = extraer_cuantiles(contexto, "LYC")
cuantiles_lyc.to_csv("cuantiles_pri_lyc.csv", index=False)
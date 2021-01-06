import numpy as np
import pandas as pd
import re

# Variables relevantes
seleccion = [
    "SERV", "TAM_LOC_SEC", "SEXO", "EDAD_ACC",
    "SAB_10", "SAB_11", "SAB_12", "SAB_14", "SAB_16", "SAB_22", 
    "SAB_24", "SAB_25", "SAB_26", "SAB_29", "SAB_31", "SAB_34", 
    "SAB_35", "SAB_38", "SAB_39", "SAB_40", "SAB_48", "SAB_52", 
    "SAB_53", "SAB_85",
    "PV1MAT", "PV2MAT", "PV3MAT", "PV4MAT", "PV5MAT",
    "PV1LYC", "PV2LYC", "PV3LYC", "PV4LYC", "PV5LYC",
]

vars_mat = ["PV1MAT", "PV2MAT", "PV3MAT", "PV4MAT", "PV5MAT"]
vars_lyc = ["PV1LYC", "PV2LYC", "PV3LYC", "PV4LYC", "PV5LYC"]

sec = pd.read_spss("base_Data\Planea09_2017_alumnos.sav", usecols=seleccion)


# Procesamiento
contexto = sec.drop(vars_mat, axis=1)
contexto = contexto.drop(vars_lyc, axis=1)

contexto["MAT"] = sec[vars_mat].mean(axis = 1).round()
contexto["LYC"] = sec[vars_lyc].mean(axis = 1).round()

contexto[["MAT", "LYC"]] = contexto[["MAT", "LYC"]].mask(contexto[["MAT", "LYC"]] >= 800, 800)
contexto[["MAT", "LYC"]] = contexto[["MAT", "LYC"]].mask(contexto[["MAT", "LYC"]] <= 200, 200)

contexto["SAB_10"] = contexto["SAB_10"].replace(
    ["Uno", "Dos", "Tres", "Cuatro", "Cinco", "Seis", "Ocho", "Siete", "Nueve o más"],
    ["1", "2", "3", "4", u"5 o más", u"5 o más", u"5 o más", u"5 o más", u"5 o más"]
)

contexto[["SAB_11", "SAB_12"]] = contexto[["SAB_11", "SAB_12"]].replace(
    ["No sé", "No tengo papá", "No tengo mamá"], "Desconocido"
    ).replace(
    ["Primaria incompleta", "Primaria completa"], "Primaria"
    ).replace(
    ["Secundaria incompleta", "Secundaria completa"], "Secundaria"
    ).replace(
    ["Preparatoria, bachillerato o carrera técnica", "Carrera universitaria o posgrad...(ver cuestionario .pdf)"],
    ["Bachillerato", "Universidad o Posgrado"]
    )

contexto["SAB_48"] = contexto["SAB_48"].replace(["Entre uno y 25"], ["Entre 1 y 25"])

contexto["SAB_16"] = contexto["SAB_16"].replace(
    ["Un año o menos", "Dos años", "Tres años", u"No fui", u"Sí asistí, pero no sé cuántos años"], 
    ["1 año o menos", "2 años", "3 años", u"No asistió", u"Asistió, años desconocidos"]
)

contexto["SAB_22"] = contexto["SAB_22"].replace(
    ["De uno a cinco", "De seis a 10"],
    ["De 1 a 5", "De 6 a 10"]
    )

contexto["SAB_48"] = contexto["SAB_48"].replace(["Entre uno y 25"], ["Entre 1 y 25"])

contexto["SAB_85"] = contexto["SAB_85"].replace(
    ["Entre una y dos horas", "Más de dos horas"],
    ["Entre 1 y 2 horas", "Más de 2 horas"]
)

contexto = contexto[contexto["TAM_LOC_SEC"] != 'No identificada']

perdidos_renglon = contexto.isnull().sum(axis=1) 

contexto = contexto.dropna()

contexto.to_csv("sec.csv", index=False)


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
cuantiles_mat.to_csv("cuantiles_sec_mat.csv", index=False)

cuantiles_lyc = extraer_cuantiles(contexto, "LYC")
cuantiles_lyc.to_csv("cuantiles_sec_lyc.csv", index=False)
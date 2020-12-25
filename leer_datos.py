import numpy as np
import pandas as pd
import re


p18 = pd.read_spss("Planea06_2018_alumnos.sav")


nombres = list(p18.columns)


vars_base = ["NOM_ENT", "SERV", "MARGINC", "TAM_LOC_PRIM", "SEXO", "EDAD_ACC"]
vars_contexto = []
[vars_contexto.append(i) for i in nombres if re.match("PAB_", i)]


score_mat = []
[score_mat.append(i) for i in nombres if re.match("PV.MAT", i)]
score_lyc = []
[score_lyc.append(i) for i in nombres if re.match("PV.LYC", i)]


contexto = pd.concat([p18[vars_base], p18[vars_contexto]], axis=1)
contexto["MAT"] = p18[score_mat].mean(axis = 1).round()
contexto["LYC"] = p18[score_lyc].mean(axis = 1).round()


contexto[["MAT", "LYC"]] = contexto[["MAT", "LYC"]].mask(contexto[["MAT", "LYC"]] >= 800, 800)
contexto[["MAT", "LYC"]] = contexto[["MAT", "LYC"]].mask(contexto[["MAT", "LYC"]] <= 200, 200)


perdidos_renglon = contexto.isnull().sum(axis=1) 
contexto = contexto.dropna()


contexto.to_csv("p18.csv", index=False)
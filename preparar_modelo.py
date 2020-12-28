# Entrenamiento de modelos para Lenguaje y Comunicación y Matemáticas

### Lectura de datos

import pandas as pd
import xgboost as xgb
import numpy as np
from catboost import CatBoostRegressor, CatBoostClassifier, Pool, FeaturesData
from sklearn.model_selection import train_test_split

p18 = pd.read_csv("p18.csv")

p18.head(3)

seleccion = [
    "SERV", "TAM_LOC_PRIM", "SEXO", "EDAD_ACC",
    "PAB_4", "PAB_11", "PAB_12", "PAB_14", "PAB_16", 
    "PAB_22", "PAB_24", "PAB_25", "PAB_26", "PAB_29",
    "PAB_31", "PAB_34", "PAB_35", "PAB_37", "PAB_38", 
    "PAB_39", "PAB_48", "PAB_52", "PAB_53", "PAB_85",
]

y_lyc, y_mat = p18["LYC"], p18["MAT"]

x_data = p18.drop(columns=["LYC", "MAT"])
x_data = x_data[seleccion]
x_data = x_data.fillna("Perdido")

x_data = x_data.reindex(sorted(x_data.columns), axis=1)

### Modelo para Lenguaje y Comunicacion

x_train, x_test, y_lyc_train, y_lyc_test = train_test_split(
    x_data, y_lyc, test_size=0.3, random_state=1986
)

x_train = np.array(x_train)
x_train = FeaturesData(cat_feature_data=x_train)
train_pool = Pool(x_train, y_lyc_train)

x_test = np.array(x_test)
x_test = FeaturesData(cat_feature_data=x_test)
test_lyc_pool = Pool(x_test, y_lyc_test)

model_lyc = CatBoostRegressor(iterations=4500, 
                          depth=4, 
                          learning_rate=.75,
                          min_data_in_leaf=6,
                          loss_function='MAE',
                          task_type="GPU")

model_lyc.fit(train_pool, eval_set=test_lyc_pool,
          early_stopping_rounds=250, plot = True,
          verbose=500)

### Modelo para Matematicas

x_train, x_test, y_mat_train, y_mat_test = train_test_split(
    x_data, y_mat, test_size=0.3, random_state=1986
)

x_train = np.array(x_train)
x_train = FeaturesData(cat_feature_data=x_train)
train_pool = Pool(x_train, y_mat_train)

x_test = np.array(x_test)
x_test = FeaturesData(cat_feature_data=x_test)
test_mat_pool = Pool(x_test, y_mat_test)

model_mat = CatBoostRegressor(iterations=4500, 
                          depth=4, 
                          learning_rate=.75,
                          min_data_in_leaf=6,
                          loss_function='MAE',
                          task_type="GPU")

model_mat.fit(train_pool, eval_set=test_mat_pool,
          early_stopping_rounds=250, plot = True,
          verbose=500)

model_lyc.save_model("model_lyc.cbm")
model_mat.save_model("model_mat.cbm")
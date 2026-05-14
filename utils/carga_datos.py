# utils/carga_datos.py

# Importamos las librerías necesarias

import numpy as np
import pandas as pd
from zipfile import ZipFile
from pathlib import Path


datos = Path(__file__).parent.resolve() / "../datos.zip" # Cargamos el fichero .zip desde el directorio actual.

with ZipFile(datos) as z: # Creamos los dataframes en base a los ficheros del .zip con sus parámetros correspondientes
		with z.open("datNotas.csv") as f: df_notas = pd.read_csv(f, encoding="latin-1", sep=";")
		with z.open("datMatriculas.csv") as f: df_matriculas = pd.read_csv(f, encoding="latin-1", sep=";")
		with z.open("datFaltas.csv") as f: df_faltas = pd.read_csv(f, encoding="latin-1", sep=";")
		with z.open("datMaterias.csv") as f: df_materias = pd.read_csv(f, encoding="latin-1", sep=";")
		with z.open("datUnidades.csv") as f: df_unidades = pd.read_csv(f, encoding="latin-1", sep=";")

# Cargamos solo las columnas necesarias
df_notas = df_notas[["MATRICULA", "ANNO", "CURSO", "EVALUACION", "MATERIA", "CL_MATERIA", "NOTA"]]
df_matriculas = df_matriculas[["MATRICULA", "ETAPA", "ANNO", "ESTUDIOS", "GRUPO", "ESTADOMATRICULA"]]
df_faltas = df_faltas[["EXPEDIENTE", "ANNO", "FECHA_FALTA", "ESTUDIOS", "GRUPO", "MATERIA", "AUSENCIAS", "RETRASOS", "JUSTIFICADAS"]]
df_materias = df_materias[["CODIGO", "DESCRIPCION", "ABREVIATURA"]]
df_unidades = df_unidades[["ANNO", "GRUPO", "ESTUDIO", "CURSO"]] # Opcional. Falta "TUTOR"

# Limpiamos datos

df_notas = df_notas[df_notas["EVALUACION"].isin(["1ª Evaluación", "2ª Evaluación"])] # Solo mostramos las dos primeras evaluaciones

# Creamos un marco para reemplazar las notas categóricas por numéricas.
notas_categoricas = {
    "Insuficiente": 2.5,
    "Insuficiente-1": 1,
    "Suficiente": 5,
    "Apto": 5,
    "Bien": 6.5,
    "Notable": 7.5,
    "Sobresaliente": 9.5,

    "No evaluado": np.nan,
    "Renuncia Convocatoria": np.nan
}

df_notas["NOTA"] = df_notas["NOTA"].replace(notas_categoricas)
df_notas["NOTA"] = pd.to_numeric(df_notas["NOTA"], errors="coerce")

# print(df_notas["NOTA"].value_counts(dropna=True))
# print(df_notas["NOTA"].isna().sum())

# Relacionamos los Datasets por campos comúnes

df_notas_matriculas = pd.merge(df_notas, df_matriculas, on="MATRICULA", how="left")

df_notas_materias = pd.merge(df_notas, df_materias, left_on="MATERIA", right_on="DESCRIPCION", how="left")

df_faltas_matriculas = pd.merge(df_faltas, df_matriculas, on="ESTUDIOS", how="left")

#df_faltas_materias = pd.merge(df_faltas, df_materias, on="")

# En datMaterias, el nombre de la materia se llama DESCRIPCION. En datFaltas, la misma se llama MATERIA.
# He visto, por otro lado, que el CL_MATERIA de datNotas no coincide con el CODIGO de datMaterias
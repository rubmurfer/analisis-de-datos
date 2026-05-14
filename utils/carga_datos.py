# utils/carga_datos.py

# Importamos las librerías necesarias

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

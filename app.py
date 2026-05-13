# Importamos las librerías necesarias
from zipfile import ZipFile
from pathlib import Path
import pandas as pd

from flask import Flask, render_template, redirect

datos = Path(__file__).parent.resolve() / "datos.zip" # Cargamos el fichero .zip desde el directorio actual.

with ZipFile(datos) as z: # Creamos los dataframes en base a los ficheros del .zip con sus parámetros correspondientes
    with z.open("datFaltas.csv") as f: df_faltas = pd.read_csv(f, encoding="latin-1", sep=";")
    with z.open("datMatriculas.csv") as f: df_matriculas = pd.read_csv(f, encoding="latin-1", sep=";")
    with z.open("datNotas.csv") as f: df_notas = pd.read_csv(f, encoding="latin-1", sep=";")
    with z.open("datUnidades.csv") as f: df_unidades = pd.read_csv(f, encoding="latin-1", sep=";")
    with z.open("materias_centro.csv") as f: df_materias_centro = pd.read_csv(f, encoding="latin-1", sep=";")
    with z.open("materias_matriculas.csv") as f: df_materias_matriculas = pd.read_csv(f, encoding="latin-1", sep=",")


print(df_notas)

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("base.html", title="Inicio", msg="Hola")

if __name__ == "__main__":
    app.run(debug=True)
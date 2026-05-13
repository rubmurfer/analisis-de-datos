# app.py

from flask import Flask, render_template, redirect
from utils.carga_datos import df_unidades, df_faltas, df_materias, df_matriculas, df_notas, pd

print(df_faltas)


app = Flask(__name__) # Apartado de Web con Flask

@app.route("/")
def inicio():
    return render_template("base.html", title="Inicio", msg="Hola")

if __name__ == "__main__":
    app.run(debug=True)
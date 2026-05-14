# app.py

from flask import Flask, render_template, redirect
from utils.carga_datos import pd, df_notas_matriculas, df_unidades, df_faltas, df_materias, df_matriculas, df_notas




app = Flask(__name__) # Apartado de Web con Flask

@app.route("/")
def inicio():
    msg = """
    Bienvenido a mi página Web.
    
    Aquí podrás acceder a los datos del centro.
    """
    return render_template("base.html", title="Inicio", msg=msg)

@app.route("/materias")
def materias():
    html = df_notas.sort_values("NOTA").to_html(classes="datos", index=False, border=0)
    return render_template("materias.html", datos=html)




if __name__ == "__main__":
    app.run(debug=True)

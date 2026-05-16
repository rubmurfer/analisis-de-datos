# app.py

from flask import Flask, render_template, redirect
#from utils.carga_datos import pd, df_notas_matriculas, df_unidades, df_faltas, df_materias, df_matriculas, df_notas
from utils.calcular_datos import pd, obtener_rendimiento_materia



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

    columnas = { # Cambiamos los nombres de los datos para hacerlos más visuales en el display de la web
        # df_notas
        "MATRICULA": "Matrícula",
        "ANNO": "Año",
        "CURSO": "Curso",
        "EVALUACION": "Evaluación",
        "MATERIA": "Materia",
        "CL_MATERIA": "Código Materia",
        "NOTA": "Nota",

        # df_matriculas
        "ETAPA": "Etapa",
        "ESTUDIOS": "Estudios",
        "GRUPO": "Grupo",
        "ESTADOMATRICULA": "Estado Matrícula"
        }

    df = obtener_rendimiento_materia(evaluacion="1ª Evaluación").head(100).sort_values("NOTA")
    html = df.to_html(classes="datos", index=True, border=0)
    return render_template("materias.html", datos=html)




if __name__ == "__main__":
    app.run(debug=True)

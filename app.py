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

@app.route("/materias", methods = ["GET"])
def materias(): # Rendimiento por Materia
    # 3 desplegables: Curso, COnvocatoria / Evaluación, Grupo. Nevesitamos varias formularios encadenados. 

    columnas = { # Cambiamos los nombres de los datos para hacerlos más visuales en el display de la web
        # df_notas
        "MATRICULA": "Matrícula",
        "CURSO": "Curso",
        "EVALUACION": "Evaluación",
        "MATERIA": "Materia",
        "NOTA": "Nota",

        # df_matriculas
        "ETAPA": "Etapa",
        "ESTUDIOS": "Estudios",
        "GRUPO": "Grupo"
        }

    # Obtenemos los datos desde la función de calcular_datos.py
    df, resumen = obtener_rendimiento_materia()

    html_datos = df.rename(columns=columnas).head(1000).to_html(classes="datos", index=False, border=0)
    html_resumen = resumen.head(100).to_html(classes="resumen", index=True, border=0)
    return render_template("materias.html", datos=html_datos, resumen=html_resumen)

if __name__ == "__main__":
    app.run(debug=True)

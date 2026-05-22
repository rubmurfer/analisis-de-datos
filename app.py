# app.py

from flask import Flask, render_template, request
from utils.calcular_datos import (
    pd, obtener_rendimiento_materia,
    lista_evaluaciones, lista_grupos, lista_cursos,
    grafica_aprobados
)
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
    # 3 desplegables: Curso, Evaluación, Grupo. Nevesitamos varias formularios encadenados. 

    evaluacion = request.args.get("evaluacion") or None
    curso = request.args.get("curso") or None
    grupo = request.args.get("grupo") or None

    

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
    
    columnas_resumen = {
        "MATERIA":               "Materia",
        "Porcentaje_Aprobados":  "% Aprobados",
        "Porcentaje_Suspensos":  "% Suspensos"
    }

    # Obtenemos los datos desde la función de calcular_datos.py
    df, resumen = obtener_rendimiento_materia(
        evaluacion=evaluacion,
        curso=curso,
        grupo=grupo
    )

    # Generamos la gráfica basada en resumen
    grafica = grafica_aprobados(resumen.sort_values("Porcentaje_Aprobados"))

    html_datos = df.rename(columns=columnas).head(100).to_html(classes="datos", index=False, border=0)
    html_resumen = resumen.rename(columns=columnas_resumen).sort_values("Media", ascending=False).head(100).to_html(classes="resumen", index=True, border=0)
    
    return render_template(
        "materias.html", # La Plantilla HTML de Jinja2
        datos=html_datos,
        resumen=html_resumen,

        # Filtros ["GET"]
        evaluaciones=lista_evaluaciones,
        grupos=lista_grupos,
        cursos=lista_cursos,

        sel_evaluacion=evaluacion,
        sel_curso=curso,
        sel_grupo=grupo,

        grafica=grafica
        )

if __name__ == "__main__":
    app.run(debug=True)

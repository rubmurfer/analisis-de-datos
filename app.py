# app.py

from flask import Flask, render_template, request
from utils.calcular_datos import (
    pd, obtener_rendimiento_materia,
    lista_evaluaciones, lista_grupos, lista_cursos,
    grafica_aprobados
)
app = Flask(__name__) # Apartado de Web con Flask

@app.context_processor # Creamos variables globales para todas las páginas. Podríamos repetir la variable de copy encada web, pero eso sería más repetitivo.
def variables_globales(): 
    return {
        "copy": "2026 · Proyecto de Análisis de Datos Académicos · Rubén Murcia Fernández"
    }

@app.route("/")
def inicio():
    msg = "Bienvenido a mi página Web. Aquí podrás acceder a los datos del centro."

    return render_template(
        "base.html",
        title = "Inicio",
        msg = msg
    )

@app.route("/materias", methods = ["GET"])
def materias(): # Rendimiento por Materia

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
        "MATERIA": "Materia",
        "Porcentaje_Aprobados": "% Aprobados",
        "Porcentaje_Suspensos": "% Suspensos"
    }

    # 3 desplegables: Curso, Evaluación, Grupo. Nevesitamos varias formularios encadenados. 

    evaluacion = request.args.get("evaluacion") or None
    curso = request.args.get("curso") or None
    grupo = request.args.get("grupo") or None

    # Establecemos valores None por defecto
    html_datos = None
    html_resumen = None
    grafica = None

    # Obtenemos los datos desde la función de calcular_datos.py
    df, resumen = obtener_rendimiento_materia(
        evaluacion=evaluacion,
        curso=curso,
        grupo=grupo
    )

    if evaluacion or curso or grupo:
        # Si los tres valores son None, la los valores no se muestras
        # Es decir: lo damos solo se muestran cuando al menos unos de los campos del formulario haya sido elegido

        head_datos_resumen = 50 # Número de filas mostradas por defecto

        # Generamos la gráfica basada en resumen
        grafica = grafica_aprobados(
            resumen.sort_values("Porcentaje_Aprobados")
            .head(head_datos_resumen))

        html_datos = (
            df.rename(columns=columnas)
            .head(head_datos_resumen)
            .to_html(classes="datos", index=False, border=0)
        )
        html_resumen = (
            resumen.rename(columns=columnas_resumen)
            .sort_values("Media", ascending=False)
            .head(head_datos_resumen)
            .to_html(classes="resumen", index=True, border=0))
    
    return render_template(
        "materias.html", # La Plantilla HTML de Jinja2
        title="Materias",
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

@app.route("/grupos", methods = ["GET"])
def grupos():
    return render_template(
        "grupos.html",
        title = "Grupos"
    )

@app.route("/absentismo", methods = ["GET"])
def absentismo():
    return render_template(
        "absentismo.html",
        title = "Absentismo"
    )

if __name__ == "__main__":
    app.run(debug=True)

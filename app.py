# app.py

from flask import Flask, render_template, request
from utils.calcular_datos import (
    pd, obtener_rendimiento_materia, obtener_rendimiento_grupo, obtener_faltas, obtener_resumen_inicio,

    materias_lista_evaluaciones, materias_lista_grupos, materias_lista_cursos,
    grupos_lista_evaluaciones, grupos_lista_cursos, grupos_lista_materias,
    absentismo_lista_grupos, absentismo_lista_estudios, absentismo_lista_materias
)

from utils.crear_graficas import (grafica_materias_aprobados, grafica_grupos, graficas_absentismo)

app = Flask(__name__) # Apartado de Web con Flask

@app.context_processor # Creamos variables globales para todas las páginas. Podríamos repetir la variable de copy encada web, pero eso sería más repetitivo.
def variables_globales(): 
    return {
        "copy": "2026 · Proyecto de Análisis de Datos Académicos · Rubén Murcia Fernández"
    }

head_datos_resumen = 50 # Número de filas mostradas por defecto
@app.route("/")
def inicio():
    msg = "Bienvenido a mi Sitio Web. Aquí podrás acceder a los datos del Centro."

    resumen = obtener_resumen_inicio()

    return render_template(
        "inicio.html",
        title = "Inicio",
        msg = msg,
        resumen = resumen,
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

        # Generamos la gráfica basada en resumen
        grafica = grafica_materias_aprobados(
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
        evaluaciones=materias_lista_evaluaciones,
        grupos=materias_lista_grupos,
        cursos=materias_lista_cursos,

        sel_evaluacion=evaluacion,
        sel_curso=curso,
        sel_grupo=grupo,

        grafica=grafica
        )

@app.route("/grupos", methods = ["GET"])
def grupos(): # Rendimiento por Grupo

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
        "Porcentaje_Aprobados": "% Aprobados",
        "Porcentaje_Suspensos": "% Suspensos"
    }

    evaluacion = request.args.get("evaluacion") or None
    curso = request.args.get("curso") or None
    materia = request.args.get("materia") or None

    # Establecemos valores None por defecto
    html_datos = None
    html_resumen = None
    grafica = None

    df, resumen = obtener_rendimiento_grupo(
        evaluacion=evaluacion,
        curso=curso,
        materia=materia
    )

    if evaluacion or curso or materia:

        html_datos = (
            df.rename(columns=columnas).head(head_datos_resumen)
            .to_html(classes="datos", index=False, border=0)
        )
        html_resumen = (
            resumen.rename(columns=columnas_resumen).head(head_datos_resumen)
            .to_html(classes="resumen grupos", index=True, border=0)
        )

        grafica = grafica_grupos(
            resumen.sort_values("Porcentaje_Aprobados")
            .head(head_datos_resumen))

    return render_template(
        "grupos.html",
        title = "Grupos",
        datos = html_datos,
        resumen=html_resumen,

        evaluaciones=grupos_lista_evaluaciones,
        cursos=grupos_lista_cursos,
        materias=grupos_lista_materias,

        sel_evaluacion=evaluacion,
        sel_curso=curso,
        sel_materia=materia,

        grafica=grafica
    )

@app.route("/absentismo", methods = ["GET"])
def absentismo(): # Faltas, retrasos, etc

    columnas = {
        "EXPEDIENTE":  "Expediente",
        "FECHA_FALTA": "Fecha de Falta",
        "ESTUDIOS":    "Estudios",
        "GRUPO":       "Grupo",
        "MATERIA":     "Materia",
        "AUSENCIAS":   "Ausencias",
        "RETRASOS":    "Retrasos",
        "JUSTIFICADAS":"Justificadas",
        "ETAPA":       "Etapa"
    }

    fecha_inicio = request.args.get("fecha_inicio") or None
    fecha_fin = request.args.get("fecha_fin") or None
    grupo = request.args.get("grupo") or None
    estudios = request.args.get("estudios") or None
    materia = request.args.get("materia") or None

    html_datos = None
    html_resumen_grupo = None
    html_resumen_materia = None
    html_resumen_matricula = None
    
    grafica_grupo = None
    grafica_materia = None
    grafica_temporal = None

    df, resumen_grupo, resumen_materia, resumen_matricula = obtener_faltas(
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        grupo=grupo,
        estudios=estudios,
        materia=materia
    )

    if fecha_inicio or fecha_fin or grupo or estudios or materia:
        html_datos = (
            df.rename(columns=columnas).head(head_datos_resumen)
            .to_html(classes="datos", index=False, border=0)
        )
        html_resumen_grupo = resumen_grupo.head(head_datos_resumen).to_html(classes="resumen", index=True, border=0)
        html_resumen_materia = resumen_materia.head(head_datos_resumen).to_html(classes="resumen", index=True, border=0)
        html_resumen_matricula = resumen_matricula.head(head_datos_resumen).to_html(classes="resumen", index=True, border=0)
        
        grafica_grupo, grafica_materia, grafica_temporal = graficas_absentismo(
            resumen_grupo.head(head_datos_resumen),
            resumen_materia.head(head_datos_resumen),
            df
        )

    return render_template(
        "absentismo.html",
        title = "Absentismo",
        datos=html_datos,
        resumen_grupo=html_resumen_grupo,
        resumen_materia=html_resumen_materia,
        resumen_matricula=html_resumen_matricula,

        grupos=absentismo_lista_grupos,
        estudios=absentismo_lista_estudios,
        materias=absentismo_lista_materias,

        sel_fecha_inicio=fecha_inicio,
        sel_fecha_fin=fecha_fin,
        sel_grupo=grupo,
        sel_estudios=estudios,
        sel_materia=materia,

        grafica_grupo=grafica_grupo,
        grafica_materia=grafica_materia,
        grafica_temporal=grafica_temporal,
    )

if __name__ == "__main__":
    app.run(debug=True)

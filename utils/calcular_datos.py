# utils/calcular_datos.py

from utils.carga_datos import pd, np, df_faltas, df_matriculas, df_notas # df_unidades y df_materias no se usan

# Relacionamos los Datasets por campos comúnes

df_notas_matriculas = pd.merge(df_notas, df_matriculas, on="MATRICULA", how="left")

# Cargamos el dataframe fusionado y limpiamos las columnas redundantes
df_faltas_matriculas = pd.merge(df_faltas, df_matriculas, left_on="EXPEDIENTE", right_on="MATRICULA", how="left")
df_faltas_matriculas = df_faltas_matriculas.drop(columns=["ESTUDIOS_y", "GRUPO_y", "MATRICULA"])
df_faltas_matriculas = df_faltas_matriculas.rename(columns={"ESTUDIOS_x": "ESTUDIOS", "GRUPO_x": "GRUPO"})

#df_faltas_materias = pd.merge(df_faltas, df_materias, on="")

# En datMaterias, el nombre de la materia se llama DESCRIPCION. En datFaltas, la misma se llama MATERIA.
# He visto, por otro lado, que el CL_MATERIA de datNotas no coincide con el CODIGO de datMaterias

# ---------------------------------------------------------------------------------------------------------------

# Creamos listados de los campos a utilizar para mostrar todas las opciones en el formulario HTML

# /materias
materias_lista_evaluaciones = df_notas_matriculas["EVALUACION"].unique().tolist()
materias_lista_cursos = df_notas_matriculas["CURSO"].unique().tolist()
materias_lista_grupos = df_notas_matriculas["GRUPO"].unique().tolist()
#lista_materias = df_notas_matriculas["MATERIA"].unique().tolist()

# /grupos
grupos_lista_evaluaciones = df_notas_matriculas["EVALUACION"].unique().tolist()
grupos_lista_cursos = df_notas_matriculas["CURSO"].unique().tolist()
grupos_lista_materias = df_notas_matriculas["MATERIA"].unique().tolist()

# /absentismo
absentismo_lista_grupos = df_faltas_matriculas["GRUPO"].unique().tolist()
absentismo_lista_estudios = df_faltas_matriculas["ESTUDIOS"].unique().tolist()
absentismo_lista_materias = df_faltas_matriculas["MATERIA"].unique().tolist()


# Establecemos las funciones para obtener el rendimiento.
def obtener_rendimiento_materia(evaluacion=None, curso=None, grupo=None): # Las parámetros de las funcionas son opcionales dentro del formulario web
    df = df_notas_matriculas.copy() # Creamos una copia del Dataframe para tener datos limpios
    
    # Filtros
    if evaluacion is not None: df = df[df["EVALUACION"] == evaluacion]
    if curso is not None: df = df[df["CURSO"] == curso]
    if grupo is not None: df = df[df["GRUPO"] == grupo]

    # Métricas
    resumen = df.groupby("MATERIA").agg( # Mostramos las métricas usando Lambda sobre el campo Nota
        Evaluados=("NOTA", lambda x: x.count()),
        Media=("NOTA", lambda x: (sum(x) / len(x))),
        Aprobados=("NOTA", lambda x: (x >= 5).sum()),
        Suspensos=("NOTA", lambda x: (x < 5).sum()),
        Porcentaje_Aprobados=("NOTA", lambda x: (x >= 5).sum() / x.count() * 100),
        Porcentaje_Suspensos=("NOTA", lambda x: (x < 5).sum() / x.count() * 100)
    ).round(2)

    return df, resumen

def obtener_rendimiento_grupo(evaluacion=None, curso=None, materia=None):
    df = df_notas_matriculas.copy()

    # Filtros
    if evaluacion is not None: df = df[df["EVALUACION"] == evaluacion]
    if curso is not None: df = df[df["CURSO"] == curso]
    if materia is not None: df = df[df["MATERIA"] == materia]

    # Métricas
    peores_materias = df.groupby(["GRUPO", "MATERIA"])["NOTA"].mean().reset_index().sort_values("NOTA").groupby("GRUPO")["MATERIA"].first()
    resumen = df.groupby("GRUPO").agg(
        # Número de alumnos evaluados por grupo, nota media del grupo, % aprobados, % suspensos y materias con peor media.
        Evaluados=("NOTA", lambda x: x.count()),
        Media=("NOTA", lambda x: (sum(x) / len(x))),
        Porcentaje_Aprobados=("NOTA", lambda x: (x >= 5).sum() / x.count() * 100),
        Porcentaje_Suspensos=("NOTA", lambda x: (x < 5).sum() / x.count() * 100),
    ).round(2)
    resumen["Peor Materia"] = peores_materias

    return df, resumen

# En datNotas, NO debemos usar CL_Materia. Solo debemos relacionar Matrícula entre ficheros para ver las asignaturas que tiene cada alumna en base a su curso.

def obtener_faltas(fecha_inicio=None, fecha_fin=None, grupo=None, estudios=None, materia=None):
    df = df_faltas_matriculas.copy()

    # Filtros
    if fecha_inicio is not None: df = df[df["FECHA_FALTA"] >= fecha_inicio]
    if fecha_fin is not None: df = df[df["FECHA_FALTA"] <= fecha_fin]

    if grupo is not None: df = df[df["GRUPO"] == grupo]
    if estudios is not None: df = df[df["ESTUDIOS"] == estudios]
    if materia is not None: df = df[df["MATERIA"] == materia]

    # Métricas # Creamos tres agrupaciones. 
    # Total de ausencias, total de retrasos, justificadas, no justificadas estimadas, faltas por grupo, faltas por materia y faltas por matrícula
    
    resumen_grupo = df.groupby("GRUPO").agg(
        Ausencias=("AUSENCIAS", lambda x: x.sum()),
        Retrasos=("RETRASOS", lambda x: x.sum()),
        Justificadas=("JUSTIFICADAS", lambda x: x.sum())
    )
    resumen_materia = df.groupby("MATERIA").agg(
        Ausencias=("AUSENCIAS", lambda x: x.sum()),
        Retrasos=("RETRASOS", lambda x: x.sum()),
        Justificadas=("JUSTIFICADAS", lambda x: x.sum())
    )
    resumen_matricula = df.groupby("EXPEDIENTE").agg(
        Ausencias=("AUSENCIAS", lambda x: x.sum()),
        Retrasos=("RETRASOS", lambda x: x.sum()),
        Justificadas=("JUSTIFICADAS", lambda x: x.sum())
    )

    # Creamos una variable total para cada agrupación
    resumen_grupo["TOTAL"] = resumen_grupo["Ausencias"] + resumen_grupo["Retrasos"]
    resumen_materia["TOTAL"] = resumen_materia["Ausencias"] + resumen_materia["Retrasos"]
    resumen_matricula["TOTAL"] = resumen_matricula["Ausencias"] + resumen_matricula["Retrasos"]


    return df, resumen_grupo, resumen_materia, resumen_matricula


def obtener_resumen_inicio():
    df = df_notas_matriculas.copy()

    # Creamos las variables que nos darán los datos globales

    total_matriculas = len(df["MATRICULA"].unique()) # Contamos las matrículas únicas con valores útiles
    #total_matriculas = len(df_matriculas["MATRICULA"].unique()) # Aquí contamos el número de matrículas únicas, sin importar los datos que tengan
    total_grupos = len(df["GRUPO"].unique())
    total_materias = len(df["MATERIA"].unique())
    media_global = (df["NOTA"].sum() / len(df["NOTA"])).round(2)
    porcentaje_aprobados = round(len(df[df["NOTA"] >= 5]) / len(df["NOTA"]) * 100, 2)

    # Creamos un dataframe que será usado en la página de Inicio como resumen["total_matriculas"], por ejemplo
    return {
        "total_matriculas": total_matriculas,
        "total_grupos": total_grupos,
        "total_materias": total_materias,
        "media_global": media_global,
        "porcentaje_aprobados": porcentaje_aprobados
    }
# utils/calcular_datos.py

from utils.carga_datos import pd, df_unidades, df_faltas, df_materias, df_matriculas, df_notas

# Relacionamos los Datasets por campos comúnes

df_notas_matriculas = pd.merge(df_notas, df_matriculas, on="MATRICULA", how="left")

df_notas_materias = pd.merge(df_notas, df_materias, left_on="MATERIA", right_on="DESCRIPCION", how="left")

df_faltas_matriculas = pd.merge(df_faltas, df_matriculas, on="ESTUDIOS", how="left")

#df_faltas_materias = pd.merge(df_faltas, df_materias, on="")

# En datMaterias, el nombre de la materia se llama DESCRIPCION. En datFaltas, la misma se llama MATERIA.
# He visto, por otro lado, que el CL_MATERIA de datNotas no coincide con el CODIGO de datMaterias

# ---------------------------------------------------------------------------------------------------------------

# Creamos listados de los campos a utilizar para mostrar todas las opciones en el formulario HTML | En cascada

lista_materias = df_notas_matriculas["MATERIA"].unique().tolist()
lista_evaluaciones = df_notas_matriculas["EVALUACION"].unique().tolist()
lista_grupos = df_notas_matriculas["GRUPO"].unique().tolist()



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


# En datNotas, NO debemos usar CL_Materia. Solo debemos relacionar Matrícula entre ficheros para ver las asignaturas que tiene cada alumna en base a su curso.
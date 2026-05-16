# utils/calcular_datos.py

from utils.carga_datos import pd, df_unidades, df_faltas, df_materias, df_matriculas, df_notas

# Relacionamos los Datasets por campos comúnes

df_notas_matriculas = pd.merge(df_notas, df_matriculas, on="MATRICULA", how="left")

df_notas_materias = pd.merge(df_notas, df_materias, left_on="MATERIA", right_on="DESCRIPCION", how="left")

df_faltas_matriculas = pd.merge(df_faltas, df_matriculas, on="ESTUDIOS", how="left")

#df_faltas_materias = pd.merge(df_faltas, df_materias, on="")

# En datMaterias, el nombre de la materia se llama DESCRIPCION. En datFaltas, la misma se llama MATERIA.
# He visto, por otro lado, que el CL_MATERIA de datNotas no coincide con el CODIGO de datMaterias

# Formateamos algunos datos

df_notas_matriculas = df_notas_matriculas.drop(columns=(["ANNO_y"])).rename(columns={"ANNO_x": "ANNO"}) # Borramos la columa de ANNO para tener solo una


# Establecemos las funciones para obtener el rendimiento.

def obtener_rendimiento_materia(evaluacion=None, curso=None, grupo=None): # Las parámetros de las funcionas son opcionales dentro del formulario web
    df = df_notas_matriculas.copy() # Creamos una copia del Dataframe para tener datos limpios
    
    # Filtros
    if evaluacion is not None: df = df[df["EVALUACION"] == evaluacion]
    if curso is not None: df = df[df["CURSO"] == curso]
    if grupo is not None: df = df[df["GRUPO"] == grupo]

    return df
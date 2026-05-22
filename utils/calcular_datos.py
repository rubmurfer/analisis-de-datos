# utils/calcular_datos.py

from utils.carga_datos import pd, df_unidades, df_faltas, df_materias, df_matriculas, df_notas

# Gráficas de Matplotlib
import matplotlib
matplotlib.use("Agg") # Evitamos que Matplotlibe muestra la gráfica en terminal
import matplotlib.pyplot as plt
import base64, io

# Relacionamos los Datasets por campos comúnes

df_notas_matriculas = pd.merge(df_notas, df_matriculas, on="MATRICULA", how="left")

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

def obtener_faltas(fechas=None, grupo=None, estudios=None, materia=None):
    df = df_faltas_matriculas.copy()

    return df


def grafica_aprobados(resumen):
    materias = resumen.index.tolist()
    p_aprobados = resumen["Porcentaje_Aprobados"].tolist()

    altura = max(6, len(materias) * 0.4) # Calculamos la altura dinámicamente
    figura, ejes = plt.subplots(figsize=(10, altura))

    ejes.barh(materias, p_aprobados, color="#4e8498", edgecolor="none")
    ejes.set_xlabel("% Aprobados", color="#2a3f4a")
    figura.subplots_adjust(left=0.35)

    ejes.set_xlim(0, 100)

    # Estilo

    figura.patch.set_facecolor("#f7fbfd")
    ejes.set_facecolor("#f7fbfd")
    
    ejes.set_title("Materias por porcentaje de aprobados", color="#2a3f4a")
    ejes.tick_params(colors="#2a3f4a")  # color del texto de los ejes

    # Creamos una imagen en RAM y la pasamos a Base64 para inyectarla en HTML
    buf = io.BytesIO()
    figura.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    imagen = base64.b64encode(buf.read()).decode("utf-8")

    plt.close(figura) # LIberamos memoria del servidor
    return imagen
# Gráficas de Matplotlib
import matplotlib
matplotlib.use("Agg") # Evitamos que Matplotlib muestra la gráfica en terminal, lo que daría error.
import matplotlib.pyplot as plt # Importamos pyplot para mostrar las grácias
import io, base64  # Importamos base64 para codificar una imagen png cargado en memoria gracias a io

color_0 = "#f7fbfd"

color_1 = "#4e9898"
color_2 = "#2a3f4a"

color_3 = "#4e8498"
color_4 = "#4e6498"

color_5 = "#faf7f2"

def grafica_materias_aprobados(resumen):
    materias = resumen.index.tolist()
    p_aprobados = resumen["Porcentaje_Aprobados"].tolist()

    altura = max(6, len(materias) * 0.4) # Calculamos la altura dinámicamente
    figura, ejes = plt.subplots(figsize=(10, altura))

    
    barras = ejes.barh(materias, p_aprobados, color=color_1, edgecolor="none")
    ejes.bar_label(barras, fmt="%.1f%%", padding=4, color=color_2) # Mostramos valores numéricos dentro de las barras

    ejes.set_xlabel("% Aprobados", color=color_2)
    figura.subplots_adjust(left=0.35)

    ejes.set_xlim(0, 120)

    # Estilo

    figura.patch.set_facecolor(color_0)
    ejes.set_facecolor(color_0)
    
    ejes.set_title("Materias por porcentaje de aprobados", color=color_2)
    ejes.tick_params(colors=color_2)  # color del texto de los ejes

    # Creamos una imagen en RAM y la pasamos a Base64 para inyectarla en HTML
    buf = io.BytesIO() # Creamos un buffer en memoria.
    figura.savefig(buf, format="png", bbox_inches="tight") # La idea es que la imagen de la gráfica se quede en memoria (sin descargarse localmente)
    buf.seek(0)
    imagen = base64.b64encode(buf.read()).decode("utf-8")

    plt.close(figura)
    return imagen


def grafica_grupos(resumen):
    grupos = resumen.index.tolist()
    medias = resumen["Media"].tolist()
    p_aprobados = resumen["Porcentaje_Aprobados"].tolist()

    altura = max(6, len(medias) * 0.4) # Calculamos la altura dinámicamente
    figura, (ejes1, ejes2) = plt.subplots(1, 2, figsize=(14, altura)) # Creamos dos ejems para mostrar las dos gráficas de manera pareja.

    ejes1.set_xlabel("% Aprobados", color=color_2)
    ejes2.set_xlabel("Medias por grupo", color=color_2)

    barras1 = ejes1.barh(grupos, p_aprobados, color=color_3, edgecolor="none") # Valores en las barras
    barras2 = ejes2.barh(grupos, medias, color=color_4, edgecolor="none")

    ejes1.bar_label(barras1, fmt="%.1f%%", padding=4, color=color_2)
    ejes2.bar_label(barras2, fmt="%.2f", padding=4, color=color_2)

    figura.subplots_adjust(left=0.35)

    ejes1.set_xlim(0, 120)
    ejes2.set_xlim(0, 12)

    # Estilo
    figura.patch.set_facecolor(color_0)
    ejes1.set_facecolor(color_0)
    ejes2.set_facecolor(color_0)
    
    ejes1.set_title("Materias por porcentaje de aprobados", color=color_2)
    ejes2.set_title("Media del alumnado por grupo", color=color_2)
    ejes1.tick_params(colors=color_2) # color del texto de los ejes
    ejes2.tick_params(colors=color_2)

    ejes2.set_yticks([]) # Ocultamos los nombres de los cursos en el segundo eje

    # Imagen
    buf = io.BytesIO()
    figura.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    imagen = base64.b64encode(buf.read()).decode("utf-8")

    plt.close(figura) # Cerramos el proceso para que la gráfica no se acumule tras cada GET.
    return imagen



def grafica_absentismo_grupo(resumen_grupo):
    grupos = resumen_grupo.index.tolist()
    ausencias = resumen_grupo["Ausencias"].tolist()

    altura = max(6, len(grupos) * 0.4)
    figura, ejes = plt.subplots(figsize=(10, altura))


    barras = ejes.barh(grupos, ausencias, color=color_1, edgecolor="none") # Valores en las barras
    ejes.set_xlabel("Ausencias por Grupo", color=color_2)
    ejes.bar_label(barras, fmt="%d", padding=4, color=color_2)
    figura.subplots_adjust(left=0.35)

    figura.patch.set_facecolor(color_5)
    ejes.set_facecolor(color_5)
    ejes.set_title("Ausencias por Grupo", color=color_2)
    ejes.tick_params(colors=color_2)

    buf = io.BytesIO()
    figura.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    imagen = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(figura)

    return imagen

def grafica_absentismo_materia(resumen_materia):
    grupos = resumen_materia.index.tolist()
    ausencias = resumen_materia["Ausencias"].tolist()

    altura = max(6, len(grupos) * 0.4)
    figura, ejes = plt.subplots(figsize=(10, altura))

    barras = ejes.barh(grupos, ausencias, color=color_1, edgecolor="none")
    ejes.set_xlabel("Ausencias por Materia", color=color_2)
    ejes.bar_label(barras, fmt="%d", padding=4, color=color_2) # Valores en las barras
    figura.subplots_adjust(left=0.35)

    figura.patch.set_facecolor(color_5)
    ejes.set_facecolor(color_5)
    ejes.set_title("Ausencias por Materia", color=color_2)
    ejes.tick_params(colors=color_2)

    buf = io.BytesIO()
    figura.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    imagen = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(figura)

    return imagen

def grafica_absentismo_temporal(df):
    por_mes = df.groupby(df["FECHA_FALTA"].dt.to_period("M"))["AUSENCIAS"].sum() # Aquí cortamos los días de todos los meses. No quedamos con algo como yyyy-mm

    meses = [str(m) for m in por_mes.index.tolist()] # Dinñamicamente, pasamos los meses a listas que leerlos con Matplotlib.
    ausencias = por_mes.tolist()

    figura, ejes = plt.subplots(figsize=(12, 4))

    ejes.plot(meses, ausencias, color=color_1, linewidth=2, marker="o")
    ejes.set_xlabel("Mes", color=color_2)
    ejes.set_ylabel("Ausencias", color=color_2)
    ejes.set_title("Evolución de ausencias por mes", color=color_2)
    ejes.tick_params(axis="x", rotation=45, colors=color_2)
    ejes.tick_params(axis="y", colors=color_2)

    figura.patch.set_facecolor(color_5)
    ejes.set_facecolor(color_5)
    figura.tight_layout()

    buf = io.BytesIO()
    figura.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    imagen = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(figura)

    return imagen

# Creamos una función para exportar las cuatro gráficas a la vez.
def graficas_absentismo(resumen_grupo, resumen_materias, df):
    grafica_grupo = grafica_absentismo_grupo(resumen_grupo)
    grafica_materias = grafica_absentismo_materia(resumen_materias)
    grafica_temperal = grafica_absentismo_temporal(df)

    return grafica_grupo, grafica_materias, grafica_temperal
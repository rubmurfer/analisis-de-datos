# Gráficas de Matplotlib
import matplotlib
matplotlib.use("Agg") # Evitamos que Matplotlib muestra la gráfica en terminal, lo que daría error.
import matplotlib.pyplot as plt # Importamos pyplot para mostrar las grácias
import io, base64  # Importamos base64 para codificar una imagen png cargado en memoria gracias a io

def grafica_materias_aprobados(resumen):
    materias = resumen.index.tolist()
    p_aprobados = resumen["Porcentaje_Aprobados"].tolist()

    altura = max(6, len(materias) * 0.4) # Calculamos la altura dinámicamente
    figura, ejes = plt.subplots(figsize=(10, altura))

    ejes.barh(materias, p_aprobados, color="#4e9898", edgecolor="none")
    ejes.set_xlabel("% Aprobados", color="#2a3f4a")
    figura.subplots_adjust(left=0.35)

    ejes.set_xlim(0, 100)

    # Estilo

    figura.patch.set_facecolor("#f7fbfd")
    ejes.set_facecolor("#f7fbfd")
    
    ejes.set_title("Materias por porcentaje de aprobados", color="#2a3f4a")
    ejes.tick_params(colors="#2a3f4a")  # color del texto de los ejes

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

    ejes1.barh(grupos, p_aprobados, color="#4e8498", edgecolor="none")
    ejes2.barh(grupos, medias, color="#4e6498", edgecolor="none")
    ejes1.set_xlabel("% Aprobados", color="#2a3f4a")
    ejes2.set_xlabel("Medias por grupo", color="#2a3f4a")

    figura.subplots_adjust(left=0.35)

    ejes1.set_xlim(0, 100)
    ejes2.set_xlim(0, 10)

    # Estilo
    figura.patch.set_facecolor("#f7fbfd")
    ejes1.set_facecolor("#f7fbfd")
    ejes2.set_facecolor("#f7fbfd")
    
    ejes1.set_title("Materias por porcentaje de aprobados", color="#2a3f4a")
    ejes2.set_title("Media del alumnado por grupo", color="#2a3f4a")
    ejes1.tick_params(colors="#2a3f4a") # color del texto de los ejes
    ejes2.tick_params(colors="#2a3f4a")

    ejes2.set_yticks([]) # Ocultamos los nombres de los cursos en el segundo eje

    # Imagen
    buf = io.BytesIO()
    figura.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    imagen = base64.b64encode(buf.read()).decode("utf-8")

    plt.close(figura) # Cerramos el proceso para que la gráfica no se acumule tras cada GET.
    return imagen
# Gráfico de barras apiladas
import matplotlib.pyplot as plt

def graficar_datos(conteo_dict, titulo="Campos principales"):
    campos = list(conteo_dict.keys())
    llenos = [conteo_dict[c]["lleno"] for c in campos]
    vacios = [conteo_dict[c]["vacio"] for c in campos]

    fig, ax = plt.subplots()
    ax.barh(campos, llenos, color='green', label='Llenos')
    ax.barh(campos, vacios, left=llenos, color='red', label='Vacíos')

    ax.set_xlabel('Cantidad')
    ax.set_title(titulo)
    ax.legend()
    plt.tight_layout()
    plt.show()

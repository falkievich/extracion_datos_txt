import matplotlib.pyplot as plt

def graficar_resultados(encontrados_count, no_encontrados_count, porc_encontrados, porc_no_encontrados):
    categorias = ['Encontrados', 'No encontrados']
    valores_absolutos = [encontrados_count, no_encontrados_count]
    valores_porcentajes = [porc_encontrados, porc_no_encontrados]

    fig, ax1 = plt.subplots(figsize=(8, 6))

    # Posición de las barras
    x = range(len(categorias))

    # Barra de cantidad (eje izquierdo)
    barras1 = ax1.bar(x, valores_absolutos, width=0.4, label='Cantidad', color=['green', 'red'])
    ax1.set_ylabel('Cantidad', color='black')
    ax1.set_ylim(0, max(valores_absolutos) + 5)

    # Eje secundario para porcentaje
    ax2 = ax1.twinx()
    barras2 = ax2.bar([i + 0.4 for i in x], valores_porcentajes, width=0.4, label='Porcentaje', color=['blue', 'orange'])
    ax2.set_ylabel('Porcentaje (%)', color='black')
    ax2.set_ylim(0, 100)

    # Etiquetas sobre las barras
    for i, v in enumerate(valores_absolutos):
        ax1.text(i, v + 0.5, str(v), ha='center', fontweight='bold')
    for i, v in enumerate(valores_porcentajes):
        ax2.text(i + 0.4, v + 1, f"{v:.1f}%", ha='center', fontweight='bold')

    # Títulos y etiquetas
    ax1.set_xticks([i + 0.2 for i in x])
    ax1.set_xticklabels(categorias)
    plt.title('Valores encontrados vs no encontrados\n(cantidad y porcentaje)')

    # Leyenda combinada
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    plt.legend(handles1 + handles2, labels1 + labels2, loc='upper right')

    plt.tight_layout()
    plt.show()

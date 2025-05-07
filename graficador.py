import matplotlib.pyplot as plt

def graficar_resultados(encontrados_count, similares_count, no_encontrados_count,
                        porc_encontrados, porc_similares, porc_no_encontrados):
    categorias = [
        f"{encontrados_count} valores encontrados exactamente\n({porc_encontrados:.1f}%)",
        f"{similares_count} valores con coincidencia aproximada\n({porc_similares:.1f}%)",
        f"{no_encontrados_count} valores no encontrados\n({porc_no_encontrados:.1f}%)"
    ]
    porcentajes = [porc_encontrados, porc_similares, porc_no_encontrados]

    fig, ax = plt.subplots(figsize=(10, 6))
    x = range(len(categorias))

    barras = ax.bar(x, porcentajes, width=0.6)
    ax.set_ylim(0, 100)
    ax.set_ylabel('Porcentaje (%)')
    ax.set_xticks(x)
    # Rotación 0 para etiquetas horizontales
    ax.set_xticklabels(categorias, rotation=0, ha='center')
    ax.set_title('Comparación de valores: exactos, aproximados y no encontrados')

    # Etiquetas de porcentaje sobre cada barra
    for bar, pct in zip(barras, porcentajes):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 1,
                f"{pct:.1f}%", ha='center', fontweight='bold')

    plt.tight_layout()
    plt.show()

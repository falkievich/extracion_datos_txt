"""
Módulo para serializar y exportar los resultados de la comparación a JSON,  
y para formatear y mostrar esos resultados en un widget de texto Tkinter.
"""
import json
from tkinter import filedialog, messagebox

def exportar_resultados(resultado):
    """
    Abre un diálogo para guardar los resultados de la comparación en un archivo JSON.
    Convierte los conjuntos en listas para asegurar la serialización.
    """
    # Preparar datos serializables
    datos_serializables = {}
    for clave, valor in resultado.items():
        if isinstance(valor, set):
            datos_serializables[clave] = list(valor)
        else:
            datos_serializables[clave] = valor

    # Diálogo para elegir ubicación y nombre de archivo
    filepath = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Archivos JSON", "*.json")],
        title="Guardar resultados como"
    )
    if not filepath:
        return  # Usuario canceló

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(datos_serializables, f, ensure_ascii=False, indent=4)
        messagebox.showinfo("Exportación completada", f"Resultados exportados en:\n{filepath}")
    except Exception as e:
        messagebox.showerror("Error al exportar", f"No se pudo exportar los resultados:\n{e}")


def mostrar_resultado_comparacion(text_widget, resultado, graficar_func):
    """
    Pinta en el text_widget los resultados de la comparación y llama al graficador.
    """
    text_widget.delete(1.0, "end")
    text_widget.insert("end", "🔍 Resultados de la comparación:\n\n")

    if resultado["no_encontrados"]:
        text_widget.insert("end", "❌ Valores del datos.txt NO encontrados en ley.pdf:\n")
        for val in sorted(resultado["no_encontrados"]):
            text_widget.insert("end", f"- {val}\n")
        text_widget.insert("end", "\n")
    else:
        text_widget.insert("end", "✅ Todos los valores fueron encontrados en el PDF (sin omisiones).\n\n")

    if resultado["similares"]:
        text_widget.insert("end", "🔶 Valores con coincidencia aproximada en el PDF:\n")
        for campo, (txt_val, pdf_val) in sorted(resultado["similares"].items()):
            text_widget.insert(
                "end",
                f"- {campo}: {txt_val}  →  Como aparece en el PDF: {pdf_val}\n"
            )
        text_widget.insert("end", "\n")

    if resultado["encontrados"]:
        text_widget.insert("end", "✔️ Valores encontrados exactamente en el PDF:\n")
        for val in sorted(resultado["encontrados"]):
            text_widget.insert("end", f"- {val}\n")
        text_widget.insert("end", "\n")

    text_widget.insert("end", "📊 Estadísticas:\n")
    text_widget.insert("end", f"- Total de valores del .txt analizados: {resultado['total']}\n")
    text_widget.insert("end", f"- Valores encontrados exactamente: {resultado['encontrados_count']}\n")
    text_widget.insert("end", f"- Valores con coincidencia aproximada: {resultado['similares_count']}\n")
    text_widget.insert("end", f"- Valores NO encontrados: {resultado['no_encontrados_count']}\n")
    text_widget.insert("end", f"- Porcentaje de coincidencias exactas: {resultado['porc_encontrados']:.1f}%\n")
    text_widget.insert("end", f"- Porcentaje de coincidencias aproximadas: {resultado['porc_similares']:.1f}%\n")
    text_widget.insert("end", f"- Porcentaje de no coincidencias: {resultado['porc_no_encontrados']:.1f}%\n")

    # Llamar al graficador
    graficar_func(
        resultado['encontrados_count'],
        resultado['similares_count'],
        resultado['no_encontrados_count'],
        resultado['porc_encontrados'],
        resultado['porc_similares'],
        resultado['porc_no_encontrados']
    )
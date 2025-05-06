# Punto de entrada (interfaz)
import tkinter as tk
from tkinter import scrolledtext
from comparador import comparar_txt_con_pdf
from graficador import graficar_resultados

def mostrar_resultado_comparacion(text_widget):
    resultado = comparar_txt_con_pdf()

    text_widget.insert(tk.END, "🔍 Resultados de la comparación:\n\n")

    if resultado["no_encontrados"]:
        text_widget.insert(tk.END, "❌ Valores del datos.txt NO encontrados en ley.pdf:\n")
        for val in sorted(resultado["no_encontrados"]):
            text_widget.insert(tk.END, f"- {val}\n")
        text_widget.insert(tk.END, "\n")
    else:
        text_widget.insert(tk.END, "✅ Todos los valores del datos.txt se encontraron en el PDF.\n\n")

    if resultado["encontrados"]:
        text_widget.insert(tk.END, "✔️ Valores encontrados en el PDF:\n")
        for val in sorted(resultado["encontrados"]):
            text_widget.insert(tk.END, f"- {val}\n")
        text_widget.insert(tk.END, "\n")

    text_widget.insert(tk.END, "📊 Estadísticas:\n")
    text_widget.insert(tk.END, f"- Total de valores del .txt analizados: {resultado['total']}\n")
    text_widget.insert(tk.END, f"- Valores encontrados en el PDF: {resultado['encontrados_count']}\n")
    text_widget.insert(tk.END, f"- Valores NO encontrados en el PDF: {resultado['no_encontrados_count']}\n")
    text_widget.insert(tk.END, f"- Porcentaje de coincidencias: {resultado['porc_encontrados']:.1f}%\n")
    text_widget.insert(tk.END, f"- Porcentaje de no coincidencias: {resultado['porc_no_encontrados']:.1f}%\n")

    # Llamada para graficar los resultados
    graficar_resultados(
        resultado['encontrados_count'],
        resultado['no_encontrados_count'],
        resultado['porc_encontrados'],
        resultado['porc_no_encontrados']
    )

def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Comparador de datos contra PDF")
    ventana.geometry("800x600")

    text_widget = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=100, height=35)
    text_widget.pack(padx=10, pady=10)

    mostrar_resultado_comparacion(text_widget)

    ventana.mainloop()

if __name__ == "__main__":
    crear_interfaz()
# Punto de entrada (interfaz)
import tkinter as tk
from tkinter import scrolledtext
from procesador import procesar_datos
from graficador import graficar_datos

def mostrar_resultados(text_widget):
    conteo, campos_principales, campos_materia_estaticos, otros_materia, otros_fuera = procesar_datos()

    secciones = [
        ("=== Estadísticas principales ===", campos_principales),
        ("=== Campos en 'Materia' ===", campos_materia_estaticos)
    ]

    for titulo, campos in secciones:
        text_widget.insert(tk.END, f"{titulo}\n")
        for campo in campos:
            estado = conteo[campo]
            total = estado["lleno"] + estado["vacio"]
            if total == 0:
                continue
            lleno_pct = (estado["lleno"] / total) * 100
            vacio_pct = (estado["vacio"] / total) * 100
            text_widget.insert(tk.END, f"{campo.upper()}: {total} campos - {lleno_pct:.1f}% lleno, {vacio_pct:.1f}% vacío\n")
        text_widget.insert(tk.END, "\n")

    text_widget.insert(tk.END, "=== Otros campos en 'materia' ===\n")
    for campo, estado in otros_materia.items():
        total = estado["lleno"] + estado["vacio"]
        if total == 0:
            continue
        lleno_pct = (estado["lleno"] / total) * 100
        vacio_pct = (estado["vacio"] / total) * 100
        text_widget.insert(tk.END, f"{campo}: {total} campos - {lleno_pct:.1f}% lleno, {vacio_pct:.1f}% vacío\n")

    text_widget.insert(tk.END, "\n=== Otros campos fuera de 'materia' ===\n")
    for campo, estado in otros_fuera.items():
        total = estado["lleno"] + estado["vacio"]
        if total == 0:
            continue
        lleno_pct = (estado["lleno"] / total) * 100
        vacio_pct = (estado["vacio"] / total) * 100
        text_widget.insert(tk.END, f"{campo}: {total} campos - {lleno_pct:.1f}% lleno, {vacio_pct:.1f}% vacío\n")

    # Opcional: Mostrar gráfico con campos principales
    campos_interes = {c: conteo[c] for c in campos_principales + campos_materia_estaticos}
    graficar_datos(campos_interes)

def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Estadísticas de Campos")
    ventana.geometry("700x600")

    text_widget = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, width=80, height=35)
    text_widget.pack(padx=10, pady=10)

    mostrar_resultados(text_widget)

    ventana.mainloop()

if __name__ == "__main__":
    crear_interfaz()

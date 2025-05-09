"""
Interfaz gráfica con Tkinter que ejecuta la comparación de un JSON contra un PDF,  
muestra los resultados y permite exportarlos usando las funciones de exporter.py.
"""
import tkinter as tk
from tkinter import scrolledtext
from comparador import comparar_txt_con_pdf
from graficador import graficar_resultados
from exporter import exportar_resultados, mostrar_resultado_comparacion
from fastapi import FastAPI

#---------------------------------------------------------- Imports routes
from backend.routes.upload_documents_route import router as upload_documents_route

#---------------------------------------------------------- FastAPI
app = FastAPI()

#---------------------------------------------------------- Include routes
app.include_router(upload_documents_route, prefix="/api")

#---------------------------------------------------------- 

def crear_interfaz():
    ventana = tk.Tk()
    ventana.title("Comparador de datos contra PDF")
    ventana.geometry("900x700")  # Tamaño inicial

    # Configurar filas y columnas expandibles
    ventana.grid_rowconfigure(0, weight=1)
    ventana.grid_columnconfigure(0, weight=1)

    # Área de texto expandible
    text_widget = scrolledtext.ScrolledText(ventana, wrap=tk.WORD)
    text_widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Obtener y mostrar resultados
    resultado = comparar_txt_con_pdf()
    mostrar_resultado_comparacion(text_widget, resultado, graficar_resultados)

    # Botón para exportar a JSON, anclado al fondo
    boton_export = tk.Button(
        ventana,
        text="📤 Exportar resultados a JSON",
        command=lambda: exportar_resultados(resultado),
        bg="#0078D7",     # color de fondo azul
        fg="white",       # texto en blanco
        activebackground="#005A9E",
        activeforeground="white"
    )
    boton_export.grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10))

    ventana.mainloop()

if __name__ == "__main__":
    crear_interfaz()

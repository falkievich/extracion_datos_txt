"""
Acá se compara los valores de un archivo JSON (datos.txt) con el contenido textual extraído de un PDF (ley.pdf), determinando qué campos están presentes y cuáles no, y generando estadísticas sobre los valores encontrados y no encontrados.
"""
import unicodedata # Se dejó de usar por ahora, normaliza el texto para eliminar acentos y caracteres especiales
import re # Se usara para buscar patrones en el texto extraído del PDF
import json
from PyPDF2 import PdfReader

def extraer_valores_txt(path_txt='datos.txt'):
    with open(path_txt, 'r', encoding='utf-8-sig') as file: #Se usa utf-8-sig para evitar problemas con BOM
        datos = json.load(file)

    # Normalizar los valores eliminando espacios múltiples y aplicando strip
    def normalizar_valor(val):
        if isinstance(val, str):
            val = re.sub(r'\s+', ' ', val).strip()
        return val

    # Aplicamos la normalización a todos los valores
    for seccion, lista in datos.items():
        if isinstance(lista, list):
            for elemento in lista:
                for clave in list(elemento.keys()):
                    valor_normalizado = normalizar_valor(elemento[clave])
                    print(f"{seccion} - {clave}: {valor_normalizado}")
                    elemento[clave] = valor_normalizado
        elif isinstance(lista, dict):
            for clave in list(lista.keys()):
                valor_normalizado = normalizar_valor(lista[clave])
                print(f"{seccion} - {clave}: {valor_normalizado}")
                lista[clave] = valor_normalizado

    return datos

def extraer_texto_pdf(path_pdf='ley.pdf'):
    reader = PdfReader(path_pdf)
    texto = ''
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            texto += page_text + '\n'

    # Normalizar el texto: eliminar saltos de línea y espacios múltiples
    texto = texto.replace('\n', ' ').replace('\r', ' ')
    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto

def comparar_txt_con_pdf(path_txt='datos.txt', path_pdf='ley.pdf'):
    datos = extraer_valores_txt(path_txt)
    texto_pdf = extraer_texto_pdf(path_pdf)

    print("\nPDF:", texto_pdf)

    encontrados = set()
    no_encontrados = set()

    for seccion, contenido in datos.items():
        if isinstance(contenido, list):
            for elemento in contenido:
                for clave, valor in elemento.items():
                    
                    # Si el valor está vacío, lo marcaremos como no encontrado
                    if valor == "" or valor is None:
                        no_encontrados.add(f"{clave}: {valor}")
                        continue  # No se busca en el PDF, pero se marca como no encontrado
                    
                    # Si el valor es un número, se busca como patrón
                    if isinstance(valor, int):
                        patron = rf"{clave}[:\s]*{valor}"
                    else:
                        patron = re.escape(str(valor))
                    match = re.search(rf'\b{patron}\b', texto_pdf, re.IGNORECASE) # Busca exactamente la palabra entera
                    if match:
                        encontrados.add(f"{clave}: {valor}")
                    else:
                        no_encontrados.add(f"{clave}: {valor}")
        elif isinstance(contenido, dict):
            for clave, valor in contenido.items():
                if isinstance(valor, int):
                    patron = rf"{clave}[:\s]*{valor}"
                else:
                    patron = re.escape(str(valor))
                match = re.search(rf'\b{patron}\b', texto_pdf, re.IGNORECASE) # Busca exactamente la palabra entera
                if match:
                    encontrados.add(f"{clave}: {valor}")
                else:
                    no_encontrados.add(f"{clave}: {valor}")

    total = len(encontrados) + len(no_encontrados)

    return {
        "encontrados": encontrados,
        "no_encontrados": no_encontrados,
        "total": total,
        "encontrados_count": len(encontrados),
        "no_encontrados_count": len(no_encontrados),
        "porc_encontrados": len(encontrados) / total * 100 if total else 0,
        "porc_no_encontrados": len(no_encontrados) / total * 100 if total else 0
    }

"""
Acá se compara los valores de un archivo JSON (datos.txt) con el contenido textual extraído de un PDF (ley.pdf), determinando qué campos están presentes y cuáles no, y generando estadísticas sobre los valores encontrados y no encontrados.
"""
import unicodedata # Se usa para Normalizar los acentos en el texto
import re # Se usara para buscar patrones en el texto extraído del PDF
import json
import fitz  # PyMuPDF se usa en vez de PyPDF2 para extraer texto de PDF

def normalizar_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFKD', texto)
        if not unicodedata.combining(c)
    )

def extraer_valores_txt(path_txt='datos.txt'):
    with open(path_txt, 'r', encoding='utf-8-sig') as file: #Se usa utf-8-sig para evitar problemas con BOM
        datos = json.load(file)

    # Normalizar los valores eliminando espacios múltiples y aplicando strip
    def normalizar_valor(val):
        if isinstance(val, str):
            val = re.sub(r'\s+', ' ', val).strip()
        return val

    # Aplicamos la normalización a todos los valores en listas y diccionarios
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
    
    # Normalizar claves al nivel raíz que no son listas ni diccionarios
    for clave in list(datos.keys()):
        valor = datos[clave]
        if not isinstance(valor, (list, dict)):
            datos[clave] = normalizar_valor(valor)
            print(f"raiz - {clave}: {datos[clave]}")

    return datos

def extraer_texto_pdf(path_pdf='ley.pdf'):
    texto = ''
    with fitz.open(path_pdf) as doc:
        for pagina in doc:
            texto += pagina.get_text()

    # Normalizar el texto: eliminar saltos de línea y espacios múltiples
    texto = texto.replace('\n', ' ').replace('\r', ' ')
    texto = re.sub(r'\s+', ' ', texto).strip()

    return texto

def comparar_txt_con_pdf(path_txt='datos.txt', path_pdf='ley.pdf'):
    datos = extraer_valores_txt(path_txt)
    texto_pdf = extraer_texto_pdf(path_pdf)
    texto_pdf_normalizado = normalizar_acentos(texto_pdf).lower()

    print("\nPDF:", texto_pdf)

    encontrados = set()
    no_encontrados = set()
    similares = {} # diccionario: clave -> (valor_txt, valor_pdf)

    def verificar_valor(clave, valor):
        # Si el valor es Null o vacío, lo consideramos no encontrado
        if valor == "" or valor is None:
            no_encontrados.add(f"{clave}: {valor}")
            return

        patron = re.escape(str(valor))
        valor_normalizado = normalizar_acentos(str(valor)).lower()

        # Búsqueda exacta
        match = re.search(rf'\b{patron}\b', texto_pdf, re.IGNORECASE)
        if match:
            encontrados.add(f"{clave}: {valor}")
        else:
            # Búsqueda aproximada sobre texto normalizado
            match = re.search(rf'\b{re.escape(valor_normalizado)}\b',
            texto_pdf_normalizado, re.IGNORECASE)
            if match:
               # guardo también el fragmento normalizado que se encontró en el PDF
               valor_pdf = match.group().strip()
               similares[clave] = (valor, valor_pdf)
            else:
                no_encontrados.add(f"{clave}: {valor}")

    # Claves en la raíz
    for clave, valor in datos.items():
        if isinstance(valor, (list, dict)):
            continue
        verificar_valor(clave, valor)

    # Claves en listas y diccionarios
    for seccion, contenido in datos.items():
        if isinstance(contenido, list):
            for elemento in contenido:
                for clave, valor in elemento.items():
                    verificar_valor(clave, valor)
        elif isinstance(contenido, dict):
            for clave, valor in contenido.items():
                verificar_valor(clave, valor)

    total = len(encontrados) + len(no_encontrados) + len(similares)

    return {
        "encontrados": encontrados,
        "no_encontrados": no_encontrados,
        "similares": similares,
        "total": total,
        "encontrados_count": len(encontrados),
        "no_encontrados_count": len(no_encontrados),
        "similares_count": len(similares),
        "porc_encontrados": len(encontrados) / total * 100 if total else 0,
        "porc_no_encontrados": len(no_encontrados) / total * 100 if total else 0,
        "porc_similares": len(similares) / total * 100 if total else 0
    }
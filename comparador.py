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
                    #print(f"{seccion} - {clave}: {valor_normalizado}")
                    elemento[clave] = valor_normalizado
        elif isinstance(lista, dict):
            for clave in list(lista.keys()):
                valor_normalizado = normalizar_valor(lista[clave])
                #print(f"{seccion} - {clave}: {valor_normalizado}")
                lista[clave] = valor_normalizado
    
    # Normalizar claves al nivel raíz que no son listas ni diccionarios
    for clave in list(datos.keys()):
        valor = datos[clave]
        if not isinstance(valor, (list, dict)):
            datos[clave] = normalizar_valor(valor)
            #print(f"raiz - {clave}: {datos[clave]}")

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

    #print("\nPDF:", texto_pdf)

    encontrados = set()
    no_encontrados = set()
    similares = {} # diccionario: clave -> (valor_txt, valor_pdf)

    def verificar_valor(clave, valor):
        # Si el valor es Null o vacío, lo consideramos no encontrado
        if valor == "" or valor is None:
            no_encontrados.add(f"{clave}: {valor}")
            return

        txt_str = str(valor)
        valor_normalizado = normalizar_acentos(txt_str).lower()
        patron = re.escape(txt_str)

        # Búsqueda exacta
        match = re.search(rf'\b{patron}\b', texto_pdf, re.IGNORECASE)
        if match:
            encontrados.add(f"{clave}: {valor}")
        else:
            # 1) coincidencia simple en texto normalizado
            match_norm = re.search(rf'\b{re.escape(valor_normalizado)}\b', texto_pdf_normalizado, re.IGNORECASE)
            if match_norm:
                # Construyo patrón que admita acentos y busco en el PDF original
                accent_map = {
                    'a':'[aáàäâãÁÀÄÂÃ]',
                    'e':'[eéèëêÉÈËÊ]',
                    'i':'[iíìïîÍÌÏÎ]',
                    'o':'[oóòöôõÓÒÖÔÕ]',
                    'u':'[uúùüûÚÙÜÛ]',
                    'n':'[nñÑ]'
                }
                def cls(c):
                    return accent_map.get(c.lower(), re.escape(c))

                pat_pdf = ''.join(cls(c) for c in valor_normalizado)
                pat_pdf = rf'\b{pat_pdf}\b'
                m_raw = re.search(pat_pdf, texto_pdf, re.IGNORECASE)
                valor_pdf = m_raw.group().strip() if m_raw else match_norm.group().strip()
                similares[clave] = (valor, valor_pdf)
            else:
                # 2) regla pluralidad: s/es final
                stem = re.sub(r'(es|s)$', '', valor_normalizado)
                pat_plural = rf'\b{stem}(?:es|s)\b'
                if re.search(pat_plural, texto_pdf_normalizado):
                    found = re.search(pat_plural, texto_pdf_normalizado).group().strip()
                    # extraigo versión original con acentos
                    pat_raw = ''.join(cls(c) for c in re.sub(r'(es|s)$', '', valor_normalizado))
                    pat_raw = rf'\b{pat_raw}(?:es|s)\b'
                    m_raw = re.search(pat_raw, texto_pdf, re.IGNORECASE)
                    similares[clave] = (valor, m_raw.group().strip() if m_raw else found)
                else:
                    # 3) regla acentos ción/ciones y ía/ías
                    stem1 = re.sub(r'(ciones|cion|ías|ia)$', '', valor_normalizado)
                    pat_deriv = rf'\b{stem1}(?:ciones|cion|ías|ia)\b'
                    if re.search(pat_deriv, texto_pdf_normalizado):
                        found = re.search(pat_deriv, texto_pdf_normalizado).group().strip()
                        # extraigo la versión original
                        pat_raw = ''.join(cls(c) for c in stem1)
                        pat_raw = rf'\b{pat_raw}(?:ciones|cion|ías|ia)\b'
                        m_raw = re.search(pat_raw, texto_pdf, re.IGNORECASE)
                        similares[clave] = (valor, m_raw.group().strip() if m_raw else found)
                    else:
                        # 4) regla dígitos con separadores
                        digits = re.sub(r'\D', '', txt_str)
                        if digits:
                            pat_dig = r'\b' + r'\D{0,3}'.join(list(digits)) + r'\b' #Corroborar que no rompa nada
                            if re.search(pat_dig, texto_pdf):
                                found = re.search(pat_dig, texto_pdf).group().strip()
                                similares[clave] = (valor, found)
                            else:
                                no_encontrados.add(f"{clave}: {valor}")
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
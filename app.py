import json

# Cargar el archivo
with open('datos.txt', 'r', encoding='latin-1') as file:
    datos = json.load(file)

# Campos principales a evaluar
campos_principales = ["nombre", "apellido"]
campos_materia_estaticos = ["codigo", "descripcion"]

# Contadores
total_registros = len(datos)
conteo = {
    "nombre": {"lleno": 0, "vacio": 0, "total": 0},
    "apellido": {"lleno": 0, "vacio": 0, "total": 0},
    "codigo": {"lleno": 0, "vacio": 0, "total": 0},
    "descripcion": {"lleno": 0, "vacio": 0, "total": 0}
}
otros_campos_materia = {}

# Analizar los datos
for persona in datos:
    for campo in campos_principales:
        if campo in persona:
            conteo[campo]["total"] += 1
            if persona.get(campo):
                conteo[campo]["lleno"] += 1
            else:
                conteo[campo]["vacio"] += 1

    materia = persona.get("materia", {})
    for campo in campos_materia_estaticos:
        if campo in materia:
            conteo[campo]["total"] += 1
            if materia.get(campo):
                conteo[campo]["lleno"] += 1
            else:
                conteo[campo]["vacio"] += 1

    for clave, valor in materia.items():
        if clave not in campos_materia_estaticos:
            if clave not in otros_campos_materia:
                otros_campos_materia[clave] = {"lleno": 0, "vacio": 0, "total": 0}
            otros_campos_materia[clave]["total"] += 1
            if valor:
                otros_campos_materia[clave]["lleno"] += 1
            else:
                otros_campos_materia[clave]["vacio"] += 1

# Mostrar estadísticas principales
print("\n=== Estadísticas principales ===")
for campo, estado in conteo.items():
    if campo in campos_materia_estaticos:
        continue  # Estos campos se imprimirán más adelante como parte de "Materia"

    total = estado["lleno"] + estado["vacio"]
    lleno_pct = (estado["lleno"] / total) * 100
    vacio_pct = (estado["vacio"] / total) * 100
    print(f"{campo.upper()}: Campos Totales {total} - {lleno_pct:.1f}% ({estado['lleno']} campos) lleno, {vacio_pct:.1f}% ({estado['vacio']} campos) vacío")

# Mostrar los campos PRINCIPALES que están dentro de 'materia'
print("\nCampos en 'Materia':")
for campo in campos_materia_estaticos:
    total = conteo[campo]["lleno"] + conteo[campo]["vacio"]
    lleno_pct = (conteo[campo]["lleno"] / total) * 100
    vacio_pct = (conteo[campo]["vacio"] / total) * 100
    print(f"{campo.upper()}: Campos Totales {total} - {lleno_pct:.1f}% ({conteo[campo]['lleno']} campos) lleno, {vacio_pct:.1f}% ({conteo[campo]['vacio']} campos) vacío")

# Mostrar los campos SECUNDARIOS que están dentro de 'materia'
print("\n=== Otros campos en 'materia' ===")
for campo, estado in otros_campos_materia.items():
    total = estado["lleno"] + estado["vacio"]
    lleno_pct = (estado["lleno"] / total) * 100
    vacio_pct = (estado["vacio"] / total) * 100
    print(f"{campo}: Campos Totales {total} - {lleno_pct:.1f}% ({estado['lleno']} campos) lleno, {vacio_pct:.1f}% ({estado['vacio']} campos) vacío")

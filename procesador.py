import json

def procesar_datos(path='datos.txt'):
    with open(path, 'r', encoding='latin-1') as file:
        datos = json.load(file)

    campos_principales = ["nombre", "apellido"]
    campos_materia_estaticos = ["codigo", "descripcion"]

    conteo = {
        "nombre": {"lleno": 0, "vacio": 0, "total": 0},
        "apellido": {"lleno": 0, "vacio": 0, "total": 0},
        "codigo": {"lleno": 0, "vacio": 0, "total": 0},
        "descripcion": {"lleno": 0, "vacio": 0, "total": 0}
    }
    otros_campos_materia = {}
    otros_campos_fuera_materia = {}

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

        for clave, valor in persona.items():
            if clave not in campos_principales and clave != "materia":
                if clave not in otros_campos_fuera_materia:
                    otros_campos_fuera_materia[clave] = {"lleno": 0, "vacio": 0, "total": 0}
                otros_campos_fuera_materia[clave]["total"] += 1
                if valor:
                    otros_campos_fuera_materia[clave]["lleno"] += 1
                else:
                    otros_campos_fuera_materia[clave]["vacio"] += 1

    return conteo, campos_principales, campos_materia_estaticos, otros_campos_materia, otros_campos_fuera_materia

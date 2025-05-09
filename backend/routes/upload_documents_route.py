from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil, os, tempfile
from comparador import comparar_txt_con_pdf


router = APIRouter()

# ---------------------------------------------------------- Post - Subir y procesar archivo .txt o .json y .pdf
@router.post("/upload_files")
async def procesar_archivos(
    file_json_or_txt: UploadFile = File(...),
    file_pdf:         UploadFile = File(...)
):
    # Validaciones...
    tmp_dir = tempfile.gettempdir()

    # Validar extensión del JSON/TXT
    if not file_json_or_txt.filename.lower().endswith((".txt", ".json")):
        raise HTTPException(400, "Debes enviar un .txt o .json en el campo file_json_or_txt")
    
    # Validar extensión del PDF
    if not file_pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(400, "Debes enviar un .pdf en el campo file_pdf")
    
    # Guardar archivos en tmp
    path_txt = os.path.join(tmp_dir, file_json_or_txt.filename)
    with open(path_txt, "wb") as f:
        shutil.copyfileobj(file_json_or_txt.file, f)
    path_pdf = os.path.join(tmp_dir, file_pdf.filename)
    with open(path_pdf, "wb") as f:
        shutil.copyfileobj(file_pdf.file, f)

    # Procesar
    resultado = comparar_txt_con_pdf(path_txt, path_pdf)  # ajusta firma si es necesario

    # Serializar sets a listas
    serializable = {}
    for k, v in resultado.items():
        serializable[k] = list(v) if isinstance(v, set) else v

    return {
        "message": f"Archivos '{file_json_or_txt.filename}' y '{file_pdf.filename}' procesados correctamente",
        "resultados": serializable
    }
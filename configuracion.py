from pathlib import Path

CARPETA_BASE = Path(__file__).resolve().parent
CARPETA_ENTRADA = CARPETA_BASE / "input"
CARPETA_DESCARGAS = CARPETA_BASE / "downloads"
CARPETA_EXTRAIDOS = CARPETA_BASE / "extracted"
CARPETA_SALIDA = CARPETA_BASE / "output"

RUTA_EXCEL_ENTRADA = CARPETA_ENTRADA / "zips.xlsx"
RUTA_BITACORA = CARPETA_SALIDA / "bitacora.xlsx"

COLUMNAS_ENTRADA = ["nombre", "url"]
COLUMNAS_BITACORA = [
    "fecha_hora",
    "nombre",
    "origen",
    "url_zip",
    "archivo_zip",
    "estado_descarga",
    "estado_descompresion",
    "carpeta_extraida",
    "detalle",
]

TIEMPO_ESPERA_SEGUNDOS = 30
AGENTE_USUARIO = "Mozilla/5.0"

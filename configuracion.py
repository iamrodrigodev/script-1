from pathlib import Path

CARPETA_BASE = Path(__file__).resolve().parent
CARPETA_ENTRADA = CARPETA_BASE / "input"
CARPETA_DESCARGAS = CARPETA_BASE / "downloads"
CARPETA_EXTRAIDOS = CARPETA_BASE / "extracted"
CARPETA_SALIDA = CARPETA_BASE / "output"

RUTA_EXCEL_ENTRADA = CARPETA_ENTRADA / "zips.xlsx"
RUTA_BITACORA = CARPETA_SALIDA / "bitacora.xlsx"

URL_PAGINA_ZIPS = "https://samplelib.com/es/sample-zip.html"

COLUMNAS_ENTRADA = ["pagina_origen", "nombre_zip", "url_zip"]
COLUMNAS_BITACORA = [
    "fecha_hora",
    "pagina_origen",
    "nombre_zip",
    "url_zip",
    "ruta_zip_descargado",
    "estado_descarga",
    "ruta_descompresion",
    "estado_descompresion",
    "detalle",
]

TIEMPO_ESPERA_SEGUNDOS = 30
AGENTE_USUARIO = "Mozilla/5.0"

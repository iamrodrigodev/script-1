from pathlib import Path

CARPETA_BASE = Path(__file__).resolve().parent
CARPETA_ENTRADA = CARPETA_BASE / "input"
CARPETA_ENTRADA_GENERADA = CARPETA_ENTRADA / "generado"
CARPETA_DESCARGAS = CARPETA_BASE / "downloads"
CARPETA_EXTRAIDOS = CARPETA_BASE / "extracted"
CARPETA_SALIDA = CARPETA_BASE / "output"

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


def obtener_ruta_excel_entrada(carpeta_origen):
    return CARPETA_ENTRADA_GENERADA / carpeta_origen / "zips.xlsx"


def obtener_ruta_bitacora(carpeta_origen):
    return CARPETA_SALIDA / carpeta_origen / "bitacora.xlsx"

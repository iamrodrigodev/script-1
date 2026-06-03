from pathlib import Path
from zipfile import BadZipFile, ZipFile

from configuracion import CARPETA_EXTRAIDOS


def obtener_carpeta_destino(ruta_zip, carpeta_origen=""):
    nombre_carpeta = Path(ruta_zip).stem
    carpeta_base = (
        CARPETA_EXTRAIDOS / carpeta_origen if carpeta_origen else CARPETA_EXTRAIDOS
    )
    return carpeta_base / nombre_carpeta


def descomprimir_zip(ruta_zip, carpeta_origen=""):
    carpeta_destino = obtener_carpeta_destino(ruta_zip, carpeta_origen)
    carpeta_destino.mkdir(parents=True, exist_ok=True)

    try:
        with ZipFile(ruta_zip, "r") as archivo_zip:
            for archivo in archivo_zip.namelist():
                ruta_destino = (carpeta_destino / archivo).resolve()

                if not str(ruta_destino).startswith(str(carpeta_destino.resolve())):
                    raise ValueError("El zip contiene rutas no permitidas")

            archivo_zip.extractall(carpeta_destino)

        return {
            "carpeta": carpeta_destino,
            "estado": "descomprimido",
            "detalle": "Descompresion completada",
        }
    except BadZipFile:
        return {
            "carpeta": carpeta_destino,
            "estado": "error",
            "detalle": "El archivo descargado no es un zip valido",
        }
    except Exception as error:
        return {
            "carpeta": carpeta_destino,
            "estado": "error",
            "detalle": str(error),
        }

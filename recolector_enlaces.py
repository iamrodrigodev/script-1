from pathlib import Path

from configuracion import obtener_ruta_excel_entrada
from descargador import obtener_enlaces_zip
from gestor_excel import guardar_fuentes_excel
from input.url_pagina_zips import URLS_PAGINAS_ZIPS
from nombres_carpetas import crear_nombre_carpeta_desde_url


def obtener_nombre_desde_url(url):
    nombre = Path(url.split("?")[0]).name
    return nombre if nombre else "archivo.zip"


def crear_fuentes_desde_url(url, enlaces_zip=None):
    if enlaces_zip is None:
        enlaces_zip = obtener_enlaces_zip(url)

    fuentes = []

    for enlace_zip in enlaces_zip:
        fuentes.append({
            "pagina_origen": url,
            "nombre_zip": obtener_nombre_desde_url(enlace_zip),
            "url_zip": enlace_zip,
        })

    return fuentes


def ejecutar():
    if not URLS_PAGINAS_ZIPS:
        print("Configura URLS_PAGINAS_ZIPS en input/url_pagina_zips.py.")
        return

    total_encontrados = 0
    total_guardados = 0

    for url_pagina_zips in URLS_PAGINAS_ZIPS:
        carpeta_origen = crear_nombre_carpeta_desde_url(url_pagina_zips)
        ruta_excel = obtener_ruta_excel_entrada(carpeta_origen)
        fuentes = crear_fuentes_desde_url(url_pagina_zips)
        cantidad_guardada = guardar_fuentes_excel(ruta_excel, fuentes)
        total_encontrados += len(fuentes)
        total_guardados += cantidad_guardada

    print(f"Se encontraron {total_encontrados} enlaces zip.")
    print(f"Se agregaron {total_guardados} enlaces nuevos.")


if __name__ == "__main__":
    ejecutar()

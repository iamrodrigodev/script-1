from pathlib import Path

from configuracion import RUTA_EXCEL_ENTRADA, URL_PAGINA_ZIPS
from descargador import obtener_enlaces_zip
from gestor_excel import guardar_fuentes_excel


def obtener_nombre_desde_url(url):
    nombre = Path(url.split("?")[0]).name
    return nombre if nombre else "archivo.zip"


def crear_fuentes_desde_url(url):
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
    if not URL_PAGINA_ZIPS:
        print("Configura URL_PAGINA_ZIPS en configuracion.py.")
        return

    fuentes = crear_fuentes_desde_url(URL_PAGINA_ZIPS)
    cantidad_guardada = guardar_fuentes_excel(RUTA_EXCEL_ENTRADA, fuentes)
    print(f"Se encontraron {len(fuentes)} enlaces zip.")
    print(f"Se agregaron {cantidad_guardada} enlaces nuevos al Excel: {RUTA_EXCEL_ENTRADA}")


if __name__ == "__main__":
    ejecutar()

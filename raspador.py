from pathlib import Path
from sys import argv

from configuracion import RUTA_EXCEL_ENTRADA
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
            "nombre": obtener_nombre_desde_url(enlace_zip),
            "url": enlace_zip,
        })

    return fuentes


def obtener_url_usuario():
    if len(argv) > 1:
        return argv[1]

    return input("Ingresa la URL a raspar: ").strip()


def ejecutar():
    url = obtener_url_usuario()

    if not url:
        print("No se ingreso ninguna URL.")
        return

    fuentes = crear_fuentes_desde_url(url)
    cantidad_guardada = guardar_fuentes_excel(RUTA_EXCEL_ENTRADA, fuentes)
    print(f"Se encontraron {len(fuentes)} enlaces zip.")
    print(f"Se agregaron {cantidad_guardada} enlaces nuevos al Excel: {RUTA_EXCEL_ENTRADA}")


if __name__ == "__main__":
    ejecutar()

from configuracion import RUTA_BITACORA, RUTA_EXCEL_ENTRADA, URL_PAGINA_ZIPS
from descargador import descargar_archivo_zip, obtener_enlaces_zip
from descompresor import descomprimir_zip
from gestor_excel import (
    crear_excel_entrada_si_no_existe,
    guardar_bitacora,
    guardar_fuentes_excel,
    leer_fuentes_excel,
)
from recolector_enlaces import crear_fuentes_desde_url


def procesar_fuente(fuente):
    registros = []

    try:
        enlaces_zip = obtener_enlaces_zip(fuente["url"])
    except Exception as error:
        return [{
            "nombre": fuente["nombre"],
            "origen": fuente["url"],
            "url_zip": "",
            "archivo_zip": "",
            "estado_descarga": "error",
            "estado_descompresion": "pendiente",
            "carpeta_extraida": "",
            "detalle": str(error),
        }]

    if not enlaces_zip:
        registros.append({
            "nombre": fuente["nombre"],
            "origen": fuente["url"],
            "url_zip": "",
            "archivo_zip": "",
            "estado_descarga": "sin_zips",
            "estado_descompresion": "pendiente",
            "carpeta_extraida": "",
            "detalle": "No se encontraron enlaces zip",
        })
        return registros

    for url_zip in enlaces_zip:
        registro = {
            "nombre": fuente["nombre"],
            "origen": fuente["url"],
            "url_zip": url_zip,
            "archivo_zip": "",
            "estado_descarga": "pendiente",
            "estado_descompresion": "pendiente",
            "carpeta_extraida": "",
            "detalle": "",
        }

        resultado_descarga = descargar_archivo_zip(url_zip)
        registro["archivo_zip"] = str(resultado_descarga["ruta_archivo"])
        registro["estado_descarga"] = resultado_descarga["estado"]
        registro["detalle"] = resultado_descarga["detalle"]

        if resultado_descarga["estado"] == "descargado":
            resultado_descompresion = descomprimir_zip(resultado_descarga["ruta_archivo"])
            registro["estado_descompresion"] = resultado_descompresion["estado"]
            registro["carpeta_extraida"] = str(resultado_descompresion["carpeta"])
            registro["detalle"] = resultado_descompresion["detalle"]

        registros.append(registro)

    return registros


def ejecutar():
    crear_excel_entrada_si_no_existe(RUTA_EXCEL_ENTRADA)

    if URL_PAGINA_ZIPS:
        fuentes_recolectadas = crear_fuentes_desde_url(URL_PAGINA_ZIPS)
        cantidad_guardada = guardar_fuentes_excel(RUTA_EXCEL_ENTRADA, fuentes_recolectadas)
        print(f"Se encontraron {len(fuentes_recolectadas)} enlaces zip.")
        print(f"Se agregaron {cantidad_guardada} enlaces nuevos al Excel.")

    fuentes = leer_fuentes_excel(RUTA_EXCEL_ENTRADA)
    bitacora = []

    for fuente in fuentes:
        bitacora.extend(procesar_fuente(fuente))

    guardar_bitacora(RUTA_BITACORA, bitacora)
    print(f"Proceso terminado. Bitacora generada en: {RUTA_BITACORA}")


if __name__ == "__main__":
    ejecutar()

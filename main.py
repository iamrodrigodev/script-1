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


def crear_registro_base(fuente, url_zip=""):
    return {
        "nombre": fuente["nombre"],
        "origen": fuente["url"],
        "url_zip": url_zip,
        "archivo_zip": "",
        "estado_descarga": "pendiente",
        "estado_descompresion": "pendiente",
        "carpeta_extraida": "",
        "detalle": "",
    }


def crear_registro_error(fuente, detalle):
    registro = crear_registro_base(fuente)
    registro["estado_descarga"] = "error"
    registro["detalle"] = detalle
    return registro


def crear_registro_sin_zips(fuente):
    registro = crear_registro_base(fuente)
    registro["estado_descarga"] = "sin_zips"
    registro["detalle"] = "No se encontraron enlaces zip"
    return registro


def procesar_fuente(fuente):
    registros = []

    try:
        enlaces_zip = obtener_enlaces_zip(fuente["url"])
    except Exception as error:
        return [crear_registro_error(fuente, str(error))]

    if not enlaces_zip:
        return [crear_registro_sin_zips(fuente)]

    for url_zip in enlaces_zip:
        registro = crear_registro_base(fuente, url_zip)
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


def tarea_preparar_excel():
    crear_excel_entrada_si_no_existe(RUTA_EXCEL_ENTRADA)


def tarea_recolectar_enlaces():
    if not URL_PAGINA_ZIPS:
        return

    fuentes_recolectadas = crear_fuentes_desde_url(URL_PAGINA_ZIPS)
    cantidad_guardada = guardar_fuentes_excel(RUTA_EXCEL_ENTRADA, fuentes_recolectadas)
    print(f"Se encontraron {len(fuentes_recolectadas)} enlaces zip.")
    print(f"Se agregaron {cantidad_guardada} enlaces nuevos al Excel.")


def tarea_descargar_y_descomprimir():
    fuentes = leer_fuentes_excel(RUTA_EXCEL_ENTRADA)
    bitacora = []

    for fuente in fuentes:
        bitacora.extend(procesar_fuente(fuente))

    return bitacora


def tarea_guardar_bitacora(bitacora):
    guardar_bitacora(RUTA_BITACORA, bitacora)
    print(f"Proceso terminado. Bitacora generada en: {RUTA_BITACORA}")


def ejecutar_tareas():
    tarea_preparar_excel()
    tarea_recolectar_enlaces()
    bitacora = tarea_descargar_y_descomprimir()
    tarea_guardar_bitacora(bitacora)


if __name__ == "__main__":
    ejecutar_tareas()

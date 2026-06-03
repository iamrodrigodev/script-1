from configuracion import RUTA_BITACORA, RUTA_EXCEL_ENTRADA
from descargador import descargar_archivo_zip, obtener_enlaces_zip
from descompresor import descomprimir_zip
from gestor_excel import (
    crear_excel_entrada_si_no_existe,
    guardar_bitacora,
    guardar_fuentes_excel,
    leer_fuentes_excel,
)
from input.url_pagina_zips import URL_PAGINA_ZIPS
from recolector_enlaces import crear_fuentes_desde_url
from salida_consola import mostrar_linea, mostrar_mensaje, mostrar_tarea, mostrar_titulo


def crear_registro_base(fuente, url_zip=""):
    return {
        "pagina_origen": fuente["pagina_origen"] or fuente["url_zip"],
        "nombre_zip": fuente["nombre_zip"],
        "url_zip": url_zip or fuente["url_zip"],
        "ruta_zip_descargado": "",
        "estado_descarga": "pendiente",
        "ruta_descompresion": "",
        "estado_descompresion": "pendiente",
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
    print("")
    mostrar_linea("Fuente", fuente["nombre_zip"] or fuente["url_zip"])
    mostrar_linea("Pagina origen", fuente["pagina_origen"] or "No registrada")
    mostrar_linea("URL zip", fuente["url_zip"])

    try:
        enlaces_zip = obtener_enlaces_zip(fuente["url_zip"])
    except Exception as error:
        mostrar_linea("Error al obtener enlaces", error)
        return [crear_registro_error(fuente, str(error))]

    if not enlaces_zip:
        mostrar_mensaje("No se encontraron zips en esta fuente.")
        return [crear_registro_sin_zips(fuente)]

    mostrar_linea("Zips encontrados en esta fuente", len(enlaces_zip))

    for url_zip in enlaces_zip:
        mostrar_linea("Descargando", url_zip)
        registro = crear_registro_base(fuente, url_zip)
        resultado_descarga = descargar_archivo_zip(url_zip)
        registro["ruta_zip_descargado"] = str(resultado_descarga["ruta_archivo"])
        registro["estado_descarga"] = resultado_descarga["estado"]
        registro["detalle"] = resultado_descarga["detalle"]

        if resultado_descarga["estado"] == "descargado":
            mostrar_linea("Descomprimiendo", resultado_descarga["ruta_archivo"])
            resultado_descompresion = descomprimir_zip(resultado_descarga["ruta_archivo"])
            registro["estado_descompresion"] = resultado_descompresion["estado"]
            registro["ruta_descompresion"] = str(resultado_descompresion["carpeta"])
            registro["detalle"] = resultado_descompresion["detalle"]

        mostrar_linea(
            "Resultado",
            f"{registro['estado_descarga']} / {registro['estado_descompresion']}",
        )
        registros.append(registro)

    return registros


def tarea_preparar_excel():
    mostrar_tarea(1, "Preparar Excel de entrada")
    crear_excel_entrada_si_no_existe(RUTA_EXCEL_ENTRADA)
    mostrar_linea("Excel generado/acumulado", RUTA_EXCEL_ENTRADA)


def tarea_recolectar_enlaces():
    mostrar_tarea(2, "Recolectar enlaces zip desde la pagina inicial")

    if not URL_PAGINA_ZIPS:
        mostrar_mensaje("No hay URL configurada para recolectar enlaces.")
        return

    mostrar_linea("URL pagina zips", URL_PAGINA_ZIPS)
    fuentes_recolectadas = crear_fuentes_desde_url(URL_PAGINA_ZIPS)
    cantidad_guardada = guardar_fuentes_excel(RUTA_EXCEL_ENTRADA, fuentes_recolectadas)
    mostrar_linea("Enlaces zip encontrados", len(fuentes_recolectadas))
    mostrar_linea("Enlaces nuevos agregados al Excel", cantidad_guardada)


def tarea_descargar_y_descomprimir():
    mostrar_tarea(3, "Descargar y descomprimir zips")
    fuentes = leer_fuentes_excel(RUTA_EXCEL_ENTRADA)
    bitacora = []
    mostrar_linea("Fuentes cargadas desde Excel", len(fuentes))

    for fuente in fuentes:
        bitacora.extend(procesar_fuente(fuente))

    return bitacora


def tarea_guardar_bitacora(bitacora):
    mostrar_tarea(4, "Guardar bitacora final")
    descargados = sum(
        1 for registro in bitacora if registro["estado_descarga"] == "descargado"
    )
    descomprimidos = sum(
        1 for registro in bitacora if registro["estado_descompresion"] == "descomprimido"
    )

    guardar_bitacora(RUTA_BITACORA, bitacora)
    mostrar_linea("Registros procesados", len(bitacora))
    mostrar_linea("Archivos descargados", descargados)
    mostrar_linea("Archivos descomprimidos", descomprimidos)
    mostrar_linea("Bitacora generada", RUTA_BITACORA)


def ejecutar_tareas():
    mostrar_titulo("Proceso automatico de descarga y descompresion de zips")
    tarea_preparar_excel()
    tarea_recolectar_enlaces()
    bitacora = tarea_descargar_y_descomprimir()
    tarea_guardar_bitacora(bitacora)
    mostrar_titulo("Proceso terminado")


if __name__ == "__main__":
    ejecutar_tareas()

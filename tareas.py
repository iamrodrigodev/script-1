from configuracion import obtener_ruta_bitacora, obtener_ruta_excel_entrada
from gestor_excel import (
    crear_excel_entrada_si_no_existe,
    guardar_bitacora,
    guardar_fuentes_excel,
    leer_fuentes_excel,
)
from input.url_pagina_zips import URLS_PAGINAS_ZIPS
from nombres_carpetas import crear_nombre_carpeta_desde_url
from procesador_zips import procesar_fuente
from recolector_enlaces import crear_fuentes_desde_url
from salida_consola import mostrar_linea, mostrar_mensaje, mostrar_tarea, mostrar_titulo
from validador_urls import validar_url_pagina_zips


def tarea_validar_url(url_pagina_zips):
    mostrar_tarea(1, "Validar URL candidata")
    resultado_validacion = validar_url_pagina_zips(url_pagina_zips)
    mostrar_linea("URL valida", "si" if resultado_validacion["es_valida"] else "no")
    mostrar_linea(
        "URL candidata",
        "si" if resultado_validacion["es_candidata"] else "no",
    )
    mostrar_linea("Enlaces zip detectados", len(resultado_validacion["enlaces_zip"]))
    mostrar_linea("Detalle", resultado_validacion["detalle"])
    return resultado_validacion


def tarea_preparar_excel(ruta_excel):
    mostrar_tarea(2, "Preparar Excel de entrada")
    crear_excel_entrada_si_no_existe(ruta_excel)
    mostrar_linea("Excel generado/acumulado", ruta_excel)


def tarea_recolectar_enlaces(url_pagina_zips, ruta_excel, enlaces_zip):
    mostrar_tarea(3, "Recolectar enlaces zip desde la pagina inicial")
    mostrar_linea("URL pagina zips", url_pagina_zips)

    fuentes_recolectadas = crear_fuentes_desde_url(url_pagina_zips, enlaces_zip)
    cantidad_guardada = guardar_fuentes_excel(ruta_excel, fuentes_recolectadas)
    mostrar_linea("Enlaces encontrados en esta pagina", len(fuentes_recolectadas))
    mostrar_linea("Enlaces nuevos agregados", cantidad_guardada)


def tarea_descargar_y_descomprimir(ruta_excel):
    mostrar_tarea(4, "Descargar y descomprimir zips")
    fuentes = leer_fuentes_excel(ruta_excel)
    bitacora = []
    mostrar_linea("Fuentes cargadas desde Excel", len(fuentes))

    for fuente in fuentes:
        bitacora.extend(procesar_fuente(fuente))

    return bitacora


def tarea_guardar_bitacora(bitacora, ruta_bitacora):
    mostrar_tarea(5, "Guardar bitacora final")
    descargados = sum(
        1 for registro in bitacora if registro["estado_descarga"] == "descargado"
    )
    descomprimidos = sum(
        1 for registro in bitacora if registro["estado_descompresion"] == "descomprimido"
    )

    guardar_bitacora(ruta_bitacora, bitacora)
    mostrar_linea("Registros procesados", len(bitacora))
    mostrar_linea("Archivos descargados", descargados)
    mostrar_linea("Archivos descomprimidos", descomprimidos)
    mostrar_linea("Bitacora generada", ruta_bitacora)


def ejecutar_tareas_por_url(indice, url_pagina_zips):
    carpeta_origen = crear_nombre_carpeta_desde_url(url_pagina_zips)
    ruta_excel = obtener_ruta_excel_entrada(carpeta_origen)
    ruta_bitacora = obtener_ruta_bitacora(carpeta_origen)

    mostrar_titulo(f"URL {indice}: {carpeta_origen}")
    mostrar_linea("Pagina origen", url_pagina_zips)
    mostrar_linea("Carpeta de trabajo", carpeta_origen)
    resultado_validacion = tarea_validar_url(url_pagina_zips)

    if not resultado_validacion["es_candidata"]:
        mostrar_mensaje("Se omite esta URL porque no es candidata para descarga.")
        return

    tarea_preparar_excel(ruta_excel)
    tarea_recolectar_enlaces(
        url_pagina_zips,
        ruta_excel,
        resultado_validacion["enlaces_zip"],
    )
    bitacora = tarea_descargar_y_descomprimir(ruta_excel)
    tarea_guardar_bitacora(bitacora, ruta_bitacora)


def ejecutar_tareas():
    mostrar_titulo("Proceso automatico de descarga y descompresion de zips")

    if not URLS_PAGINAS_ZIPS:
        mostrar_mensaje("No hay URLs configuradas para recolectar enlaces.")
        return

    for indice, url_pagina_zips in enumerate(URLS_PAGINAS_ZIPS, start=1):
        ejecutar_tareas_por_url(indice, url_pagina_zips)

    mostrar_titulo("Proceso terminado")

from configuracion import RUTA_BITACORA, RUTA_EXCEL_ENTRADA
from gestor_excel import (
    crear_excel_entrada_si_no_existe,
    guardar_bitacora,
    guardar_fuentes_excel,
    leer_fuentes_excel,
)
from input.url_pagina_zips import URLS_PAGINAS_ZIPS
from procesador_zips import procesar_fuente
from recolector_enlaces import crear_fuentes_desde_url
from salida_consola import mostrar_linea, mostrar_mensaje, mostrar_tarea, mostrar_titulo


def tarea_preparar_excel():
    mostrar_tarea(1, "Preparar Excel de entrada")
    crear_excel_entrada_si_no_existe(RUTA_EXCEL_ENTRADA)
    mostrar_linea("Excel generado/acumulado", RUTA_EXCEL_ENTRADA)


def tarea_recolectar_enlaces():
    mostrar_tarea(2, "Recolectar enlaces zip desde la pagina inicial")

    if not URLS_PAGINAS_ZIPS:
        mostrar_mensaje("No hay URLs configuradas para recolectar enlaces.")
        return

    total_encontrados = 0
    total_guardados = 0

    for indice, url_pagina_zips in enumerate(URLS_PAGINAS_ZIPS, start=1):
        mostrar_linea(f"URL pagina zips {indice}", url_pagina_zips)
        fuentes_recolectadas = crear_fuentes_desde_url(url_pagina_zips)
        cantidad_guardada = guardar_fuentes_excel(
            RUTA_EXCEL_ENTRADA,
            fuentes_recolectadas,
        )
        total_encontrados += len(fuentes_recolectadas)
        total_guardados += cantidad_guardada
        mostrar_linea("Enlaces encontrados en esta pagina", len(fuentes_recolectadas))
        mostrar_linea("Enlaces nuevos agregados", cantidad_guardada)

    mostrar_linea("Total enlaces zip encontrados", total_encontrados)
    mostrar_linea("Total enlaces nuevos agregados al Excel", total_guardados)


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

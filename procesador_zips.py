from descargador import descargar_archivo_zip, obtener_enlaces_zip
from descompresor import descomprimir_zip
from nombres_carpetas import crear_nombre_carpeta_desde_url
from salida_consola import mostrar_linea, mostrar_mensaje


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
    carpeta_origen = crear_nombre_carpeta_desde_url(
        fuente["pagina_origen"] or fuente["url_zip"],
    )
    print("")
    mostrar_linea("Fuente", fuente["nombre_zip"] or fuente["url_zip"])
    mostrar_linea("Pagina origen", fuente["pagina_origen"] or "No registrada")
    mostrar_linea("Carpeta origen", carpeta_origen)
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
        resultado_descarga = descargar_archivo_zip(url_zip, carpeta_origen)
        registro["ruta_zip_descargado"] = str(resultado_descarga["ruta_archivo"])
        registro["estado_descarga"] = resultado_descarga["estado"]
        registro["detalle"] = resultado_descarga["detalle"]

        if resultado_descarga["estado"] == "descargado":
            mostrar_linea("Descomprimiendo", resultado_descarga["ruta_archivo"])
            resultado_descompresion = descomprimir_zip(
                resultado_descarga["ruta_archivo"],
                carpeta_origen,
            )
            registro["estado_descompresion"] = resultado_descompresion["estado"]
            registro["ruta_descompresion"] = str(resultado_descompresion["carpeta"])
            registro["detalle"] = resultado_descompresion["detalle"]

        mostrar_linea(
            "Resultado",
            f"{registro['estado_descarga']} / {registro['estado_descompresion']}",
        )
        registros.append(registro)

    return registros

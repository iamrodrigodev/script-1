from datetime import datetime

from openpyxl import Workbook, load_workbook

from configuracion import COLUMNAS_BITACORA, COLUMNAS_ENTRADA


def crear_excel_entrada_si_no_existe(ruta_excel):
    ruta_excel.parent.mkdir(parents=True, exist_ok=True)

    if not ruta_excel.exists():
        libro = Workbook()
        hoja = libro.active
        hoja.title = "zips"
        hoja.append(COLUMNAS_ENTRADA)
        libro.save(ruta_excel)
        return

    libro = load_workbook(ruta_excel)
    hoja = libro.active
    encabezados = [celda.value for celda in next(hoja.iter_rows(min_row=1, max_row=1))]

    if encabezados == COLUMNAS_ENTRADA:
        return

    fuentes = leer_fuentes_excel(ruta_excel)
    libro = Workbook()
    hoja = libro.active
    hoja.title = "zips"
    hoja.append(COLUMNAS_ENTRADA)

    for fuente in fuentes:
        hoja.append([
            fuente["pagina_origen"],
            fuente["nombre_zip"],
            fuente["url_zip"],
        ])

    libro.save(ruta_excel)


def leer_fuentes_excel(ruta_excel):
    libro = load_workbook(ruta_excel)
    hoja = libro.active
    encabezados = [celda.value for celda in next(hoja.iter_rows(min_row=1, max_row=1))]
    posicion_pagina_origen = (
        encabezados.index("pagina_origen") if "pagina_origen" in encabezados else None
    )
    posicion_nombre_zip = (
        encabezados.index("nombre_zip") if "nombre_zip" in encabezados else None
    )
    posicion_url_zip = encabezados.index("url_zip") if "url_zip" in encabezados else None

    if posicion_url_zip is None:
        posicion_url_zip = encabezados.index("url")

    if posicion_nombre_zip is None and "nombre" in encabezados:
        posicion_nombre_zip = encabezados.index("nombre")

    fuentes = []

    for fila in hoja.iter_rows(min_row=2, values_only=True):
        url_zip = fila[posicion_url_zip]

        if not url_zip:
            continue

        pagina_origen = (
            fila[posicion_pagina_origen] if posicion_pagina_origen is not None else ""
        )
        nombre_zip = fila[posicion_nombre_zip] if posicion_nombre_zip is not None else ""

        fuentes.append({
            "pagina_origen": str(pagina_origen or "").strip(),
            "nombre_zip": str(nombre_zip or "").strip(),
            "url_zip": str(url_zip).strip(),
        })

    return fuentes


def guardar_fuentes_excel(ruta_excel, fuentes):
    crear_excel_entrada_si_no_existe(ruta_excel)
    fuentes_actuales = leer_fuentes_excel(ruta_excel)
    urls_actuales = {fuente["url_zip"] for fuente in fuentes_actuales}
    cantidad_guardada = 0

    libro = load_workbook(ruta_excel)
    hoja = libro.active

    for fuente in fuentes:
        if fuente["url_zip"] in urls_actuales:
            continue

        hoja.append([
            fuente["pagina_origen"],
            fuente["nombre_zip"],
            fuente["url_zip"],
        ])
        urls_actuales.add(fuente["url_zip"])
        cantidad_guardada += 1

    libro.save(ruta_excel)
    return cantidad_guardada


def guardar_bitacora(ruta_excel, registros):
    ruta_excel.parent.mkdir(parents=True, exist_ok=True)
    libro = Workbook()
    hoja = libro.active
    hoja.title = "bitacora"
    hoja.append(COLUMNAS_BITACORA)

    for registro in registros:
        hoja.append([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            registro["pagina_origen"],
            registro["nombre_zip"],
            registro["url_zip"],
            registro["ruta_zip_descargado"],
            registro["estado_descarga"],
            registro["ruta_descompresion"],
            registro["estado_descompresion"],
            registro["detalle"],
        ])

    libro.save(ruta_excel)

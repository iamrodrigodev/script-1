from urllib.parse import urlparse

from descargador import obtener_enlaces_zip


def validar_url_pagina_zips(url):
    if not url or not str(url).strip():
        return {
            "es_valida": False,
            "es_candidata": False,
            "enlaces_zip": [],
            "detalle": "La URL esta vacia",
        }

    url = str(url).strip()
    partes = urlparse(url)

    if partes.scheme not in ["http", "https"]:
        return {
            "es_valida": False,
            "es_candidata": False,
            "enlaces_zip": [],
            "detalle": "La URL debe empezar con http o https",
        }

    if not partes.netloc:
        return {
            "es_valida": False,
            "es_candidata": False,
            "enlaces_zip": [],
            "detalle": "La URL no tiene dominio",
        }

    try:
        enlaces_zip = obtener_enlaces_zip(url)
    except Exception as error:
        return {
            "es_valida": True,
            "es_candidata": False,
            "enlaces_zip": [],
            "detalle": str(error),
        }

    if not enlaces_zip:
        return {
            "es_valida": True,
            "es_candidata": False,
            "enlaces_zip": [],
            "detalle": "No se encontraron enlaces zip",
        }

    return {
        "es_valida": True,
        "es_candidata": True,
        "enlaces_zip": enlaces_zip,
        "detalle": "URL candidata para descarga",
    }

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse
from urllib.request import Request, urlopen

from configuracion import AGENTE_USUARIO, CARPETA_DESCARGAS, TIEMPO_ESPERA_SEGUNDOS

class LectorEnlacesZip(HTMLParser):
    def __init__(self, url_base):
        super().__init__()
        self.url_base = url_base
        self.enlaces = []

    def handle_starttag(self, etiqueta, atributos):
        if etiqueta.lower() != "a":
            return

        atributos_enlace = dict(atributos)
        href = atributos_enlace.get("href", "")

        if es_url_zip(href):
            self.enlaces.append(urljoin(self.url_base, href))


def abrir_url(url):
    solicitud = Request(url, headers={"User-Agent": AGENTE_USUARIO})
    return urlopen(solicitud, timeout=TIEMPO_ESPERA_SEGUNDOS)


def es_url_zip(url):
    ruta = urlparse(url).path.lower()
    return ruta.endswith(".zip")


def obtener_enlaces_zip(url):
    if es_url_zip(url):
        return [url]

    with abrir_url(url) as respuesta:
        contenido = respuesta.read()
        tipo_contenido = respuesta.headers.get("content-type", "").lower()

    if "zip" in tipo_contenido:
        return [url]

    texto = contenido.decode("utf-8", errors="ignore")
    lector = LectorEnlacesZip(url)
    lector.feed(texto)
    return list(dict.fromkeys(lector.enlaces))


def obtener_nombre_archivo(url):
    ruta = unquote(urlparse(url).path)
    nombre = Path(ruta).name
    return nombre if nombre else "archivo.zip"


def descargar_archivo_zip(url):
    CARPETA_DESCARGAS.mkdir(parents=True, exist_ok=True)
    nombre_archivo = obtener_nombre_archivo(url)
    ruta_archivo = CARPETA_DESCARGAS / nombre_archivo

    try:
        with abrir_url(url) as respuesta:
            contenido = respuesta.read()

        ruta_archivo.write_bytes(contenido)

        return {
            "ruta_archivo": ruta_archivo,
            "estado": "descargado",
            "detalle": "Descarga completada",
        }
    except Exception as error:
        return {
            "ruta_archivo": ruta_archivo,
            "estado": "error",
            "detalle": str(error),
        }

import re
from urllib.parse import urlparse


def crear_nombre_carpeta_desde_url(url):
    partes = urlparse(url)
    texto = f"{partes.netloc}{partes.path}"
    texto = texto.lower()
    texto = re.sub(r"\.[a-z0-9]+$", "", texto)
    texto = re.sub(r"[^a-z0-9]+", "-", texto)
    texto = texto.strip("-")
    return texto[:80] if texto else "sin-origen"

ANCHO_SEPARADOR = 70


def mostrar_titulo(texto):
    print("")
    print("=" * ANCHO_SEPARADOR)
    print(texto.upper())
    print("=" * ANCHO_SEPARADOR)


def mostrar_tarea(numero, texto):
    print("")
    print("-" * ANCHO_SEPARADOR)
    print(f"TAREA {numero}: {texto}")
    print("-" * ANCHO_SEPARADOR)


def mostrar_linea(etiqueta, valor):
    print(f"{etiqueta}: {valor}")


def mostrar_mensaje(texto):
    print(f"- {texto}")

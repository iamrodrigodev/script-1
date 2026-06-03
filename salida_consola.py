def mostrar_titulo(texto):
    print("")
    print("=" * 70)
    print(texto.upper())
    print("=" * 70)


def mostrar_tarea(numero, texto):
    print("")
    print("-" * 70)
    print(f"TAREA {numero}: {texto}")
    print("-" * 70)


def mostrar_linea(etiqueta, valor):
    print(f"{etiqueta}: {valor}")


def mostrar_mensaje(texto):
    print(f"- {texto}")

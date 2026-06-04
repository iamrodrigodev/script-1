![Encabezado del proyecto](images/header.png)

# Prototipo de automatización de facturas SUNAT

## Objetivo

Este prototipo automatiza la identificación, descarga y extracción de archivos ZIP asociados a facturas electrónicas.

El proceso recibe una lista de páginas web, valida si contienen enlaces ZIP, registra los archivos encontrados en Excel, descarga los archivos comprimidos y los descomprime en carpetas locales organizadas.

El alcance actual cubre dos fases:

1. Descarga de archivos ZIP mediante web scraping.
2. Extracción de los archivos comprimidos.

El envío de archivos XML por correo electrónico no forma parte de este prototipo.

## Flujo general

```mermaid
flowchart TD
    A["Ejecutar python main.py"] --> B["Leer lista de URLs configuradas"]
    B --> C{"¿Existen URLs?"}
    C -- "No" --> Z["Finalizar sin procesar"]
    C -- "Sí" --> D["Tomar siguiente URL"]

    subgraph URL["Procesamiento independiente por URL"]
        D --> J1["Job 1: Validar URL candidata"]
        J1 --> V{"¿La URL contiene enlaces ZIP?"}
        V -- "No" --> O["Informar motivo y omitir URL"]
        V -- "Sí" --> J2["Job 2: Preparar Excel de entrada"]
        J2 --> J3["Job 3: Registrar enlaces ZIP en Excel"]
        J3 --> J4["Job 4: Descargar y descomprimir ZIPs"]
        J4 --> J5["Job 5: Generar bitácora Excel"]
    end

    O --> S{"¿Quedan URLs?"}
    J5 --> S
    S -- "Sí" --> D
    S -- "No" --> F["Proceso terminado"]
```

Cada URL se procesa de manera independiente. Sus archivos de entrada, descargas, extracciones y bitácoras se almacenan en carpetas separadas para evitar cruces y sobrescrituras.

## Ejecución por jobs

`main.py` inicia el proceso una sola vez. Después, `tareas.py` recorre cada URL configurada y ejecuta cinco jobs en orden.

| Job | Entrada | Acción | Salida |
|---|---|---|---|
| 1. Validar URL | URL configurada | Valida formato, acceso y existencia de enlaces ZIP. | URL candidata o URL omitida. |
| 2. Preparar Excel | Carpeta identificada para la URL | Crea o recupera el Excel acumulado. | `input/<pagina-origen>/zips.xlsx` |
| 3. Registrar enlaces | Enlaces ZIP detectados | Agrega enlaces nuevos sin duplicar registros. | Excel actualizado. |
| 4. Descargar y descomprimir | Registros del Excel | Descarga cada ZIP y extrae su contenido. | Carpetas `downloads/` y `extracted/`. |
| 5. Generar bitácora | Resultado de cada archivo | Registra estados, rutas y errores. | `output/<pagina-origen>/bitacora.xlsx` |

```mermaid
sequenceDiagram
    participant Usuario
    participant Main as main.py
    participant Tareas as tareas.py
    participant Validador as validador_urls.py
    participant Recolector as recolector_enlaces.py
    participant Excel as gestor_excel.py
    participant Procesador as procesador_zips.py
    participant Descargador as descargador.py
    participant Extractor as descompresor.py

    Usuario->>Main: python main.py
    Main->>Tareas: ejecutar_tareas()

    loop Por cada URL configurada
        Tareas->>Validador: validar_url_pagina_zips(url)
        Validador-->>Tareas: candidata y enlaces ZIP

        alt URL no candidata
            Tareas-->>Usuario: Mostrar motivo y omitir URL
        else URL candidata
            Tareas->>Excel: Crear o recuperar zips.xlsx
            Tareas->>Recolector: Crear registros desde enlaces ZIP
            Recolector->>Excel: Guardar enlaces nuevos

            loop Por cada ZIP registrado
                Tareas->>Procesador: procesar_fuente(fuente)
                Procesador->>Descargador: descargar_archivo_zip()
                Descargador-->>Procesador: Estado y ruta del ZIP
                Procesador->>Extractor: descomprimir_zip()
                Extractor-->>Procesador: Estado y ruta extraída
            end

            Tareas->>Excel: Guardar bitácora final
            Tareas-->>Usuario: Mostrar resumen de la URL
        end
    end
```

## Separación de información por URL

Cada URL genera el mismo nombre de carpeta en las distintas etapas:

```mermaid
flowchart LR
    U["URL configurada"] --> N["Nombre de carpeta normalizado"]
    N --> I["input/<pagina-origen>/zips.xlsx"]
    N --> D["downloads/<pagina-origen>/"]
    N --> E["extracted/<pagina-origen>/"]
    N --> B["output/<pagina-origen>/bitacora.xlsx"]
```

Esta separación permite ejecutar varias páginas dentro del mismo proceso sin mezclar facturas, descargas, extracciones o bitácoras.

## Estructura del proyecto

```text
script-1/
├── main.py
├── tareas.py
├── configuracion.py
├── validador_urls.py
├── recolector_enlaces.py
├── descargador.py
├── procesador_zips.py
├── descompresor.py
├── gestor_excel.py
├── nombres_carpetas.py
├── salida_consola.py
├── requirements.txt
├── input/
│   ├── url_pagina_zips.py
│   └── <pagina-origen>/
│       └── zips.xlsx
├── downloads/
│   └── <pagina-origen>/
│       └── archivos.zip
├── extracted/
│   └── <pagina-origen>/
│       └── archivos_descomprimidos/
└── output/
    └── <pagina-origen>/
        └── bitacora.xlsx
```

## Punto de entrada

El proceso completo se inicia ejecutando:

```powershell
python main.py
```

`main.py` funciona únicamente como punto de entrada y delega la ejecución al módulo `tareas.py`.

Las páginas que se procesarán se configuran en `input/url_pagina_zips.py`:

```python
URLS_PAGINAS_ZIPS = [
    "https://pagina-ejemplo.com/facturas",
]
```

## Fase 1: descarga y web scraping

### Validación de URL

Antes de crear carpetas o descargar archivos, `validador_urls.py` verifica:

- que la URL no esté vacía;
- que utilice `http` o `https`;
- que contenga un dominio;
- que la página sea accesible;
- que contenga al menos un enlace ZIP.

Si una URL no es candidata, se informa en consola y se omite su procesamiento.

### Detección de archivos ZIP

`descargador.py` abre el contenido HTML de cada página y utiliza `HTMLParser` para identificar etiquetas de enlace:

```html
<a href="factura.zip">Descargar factura</a>
```

El prototipo selecciona enlaces cuyo atributo `href` termina en `.zip`.

Actualmente no se realizan clics visuales sobre botones ni se ejecuta JavaScript. Para páginas dinámicas que oculten los enlaces detrás de botones, podría incorporarse Selenium o Playwright en una versión posterior.

### Registro de archivos encontrados

`recolector_enlaces.py` convierte los enlaces encontrados en registros con los siguientes atributos:

| Campo | Descripción |
|---|---|
| `pagina_origen` | Página web donde se encontró el archivo. |
| `nombre_zip` | Nombre identificado para el archivo ZIP. |
| `url_zip` | Enlace directo utilizado para descargar el ZIP. |

Los registros se almacenan en:

```text
input/<pagina-origen>/zips.xlsx
```

El Excel es acumulativo y evita registrar dos veces la misma URL ZIP.

### Descarga

`descargador.py` descarga cada archivo encontrado y lo almacena en:

```text
downloads/<pagina-origen>/
```

Cada página posee una carpeta propia derivada de su URL. Por ejemplo:

```text
https://samplelib.com/es/sample-zip.html
```

se convierte en:

```text
samplelib-com-es-sample-zip
```

## Fase 2: extracción de archivos

`descompresor.py` utiliza la librería estándar `zipfile` de Python para abrir y extraer cada ZIP descargado.

Los archivos se extraen en:

```text
extracted/<pagina-origen>/<nombre-zip>/
```

Antes de extraer, el módulo valida que el ZIP no contenga rutas que intenten escribir fuera de la carpeta permitida.

El prototipo conserva todos los archivos incluidos dentro del ZIP. En un escenario SUNAT, estos archivos pueden incluir comprobantes XML y documentos relacionados.

## Bitácora Excel

Al finalizar el procesamiento de una URL, `gestor_excel.py` genera una bitácora independiente:

```text
output/<pagina-origen>/bitacora.xlsx
```

La bitácora contiene:

| Campo | Descripción |
|---|---|
| `fecha_hora` | Fecha y hora del registro. |
| `pagina_origen` | Página desde donde se obtuvo el ZIP. |
| `nombre_zip` | Nombre del archivo procesado. |
| `url_zip` | URL directa de descarga. |
| `ruta_zip_descargado` | Ubicación local del ZIP descargado. |
| `estado_descarga` | Resultado de la descarga. |
| `ruta_descompresion` | Ubicación local de los archivos extraídos. |
| `estado_descompresion` | Resultado de la extracción. |
| `detalle` | Mensaje complementario o descripción del error. |

El uso de Excel permite revisar el prototipo sin depender de una base de datos.

## Módulos técnicos

| Módulo | Responsabilidad |
|---|---|
| `main.py` | Inicia el proceso. |
| `tareas.py` | Orquesta las tareas para cada URL. |
| `configuracion.py` | Define rutas, columnas y parámetros generales. |
| `validador_urls.py` | Valida si una URL puede procesarse. |
| `recolector_enlaces.py` | Convierte enlaces ZIP en registros para Excel. |
| `descargador.py` | Detecta enlaces y descarga archivos ZIP. |
| `procesador_zips.py` | Coordina la descarga y extracción de cada ZIP. |
| `descompresor.py` | Descomprime archivos mediante `zipfile`. |
| `gestor_excel.py` | Crea, lee y actualiza los archivos Excel. |
| `nombres_carpetas.py` | Genera nombres de carpeta a partir de URLs. |
| `salida_consola.py` | Presenta el avance del proceso en consola. |

## Requerimientos

- Python 3.
- `openpyxl` para lectura y escritura de archivos Excel.
- `urllib`, `html.parser` y `zipfile`, incluidos en la librería estándar de Python.

Instalación:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Dependencia actual:

```text
openpyxl>=3.1.0
```

Requests, Selenium o Playwright no son requeridos por la versión actual. Pueden incorporarse si las páginas SUNAT necesitan sesiones autenticadas, navegación dinámica o interacción con botones.

## Ejecución por tareas

Por cada URL configurada se ejecutan las siguientes tareas:

1. Validar si la URL es candidata.
2. Preparar el Excel de enlaces ZIP.
3. Recolectar enlaces ZIP.
4. Descargar y descomprimir los archivos.
5. Generar la bitácora final.

La consola muestra cada URL y cada tarea por separado para facilitar el seguimiento y la demostración del prototipo.

## Consideraciones del prototipo

- Los archivos generados no se versionan en Git.
- Cada URL mantiene carpetas y bitácoras independientes.
- El prototipo procesa enlaces ZIP visibles en el HTML.
- No gestiona autenticación en SUNAT.
- No envía archivos XML por correo electrónico.
- El módulo de envío al cliente final se documentará e implementará por separado.

![Pie del proyecto](images/footer.png)

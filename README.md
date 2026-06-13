# Report Automator

Automatiza la lectura de datos desde archivos CSV o Excel, genera un reporte PDF con métricas y visualización, y realiza un intento de envío por correo electrónico dentro de un flujo configurable y reutilizable.

## Descripción general

**Report Automator** es un proyecto en Python orientado a automatizar una tarea común en entornos de negocio: transformar datos tabulares en un reporte PDF listo para compartir.

El flujo actual del proyecto permite:

1. Leer un archivo de datos (`.csv` o `.xlsx`)
2. Generar un resumen con métricas clave
3. Crear un gráfico cuando existen columnas numéricas
4. Construir un PDF con formato legible para stakeholders
5. Intentar enviar ese PDF por correo electrónico
6. Ejecutar el flujo de forma inmediata o programada

No es solo un script de conversión: modela un pequeño pipeline de automatización con separación de responsabilidades, configuración por entorno y validación manual del comportamiento real.

## Problema que resuelve

En muchos contextos operativos, los datos existen pero el reporte no: alguien debe abrir un archivo, revisar métricas, armar un resumen y compartirlo.

Este proyecto reduce esa fricción al encapsular el proceso en una pipeline reproducible:

- entrada de datos
- procesamiento
- generación de artefacto
- intento de distribución
- ejecución manual o periódica

## Funcionalidades actuales

- Lectura de archivos CSV y Excel
- Generación automática de resumen con:
  - total de registros
  - listado de columnas
  - totales numéricos
  - promedios numéricos
  - top 10 registros
- Generación de gráfico de barras cuando aplica
- Generación de PDF con:
  - encabezado
  - timestamp
  - resumen general
  - visualización opcional
  - tabla top 10
- Intento de envío del reporte por correo
- Ejecución inmediata
- Ejecución programada diaria o semanal
- Configuración mediante variables de entorno
- Tolerancia a datasets sin columnas numéricas

## Arquitectura del proyecto

La solución está organizada en módulos con responsabilidades separadas.

```text
main.py
 ├── data_processor.py   -> carga de datos, resumen, gráfico
 ├── pdf_generator.py    -> construcción del PDF
 ├── email_sender.py     -> validación e intento de envío por email
 └── config.py           -> configuración centralizada por entorno
```

### Responsabilidad de cada archivo

- `main.py`: punto de entrada, orquestación del flujo, CLI y scheduler. 
- `config.py`: carga variables de entorno y centraliza configuración. 
- `data_processor.py`: lectura de archivos, resumen y generación de gráfico. 
- `email_sender.py`: validación de configuración de correo e intento de envío SMTP. 

## Flujo actual

```text
DATA_FILE
   ↓
load_data()
   ↓
generate_summary()
   ↓
generate_chart()
   ↓
build_pdf()
   ↓
send_report()
```

## Estructura del repositorio

```text
report-automator/
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── requirements.txt
├── .gitignore
├── .env.example
├── main.py
├── config.py
├── data_processor.py
├── pdf_generator.py
├── email_sender.py
├── sample_data/
│   └── sales_data.csv
├── output/
│   └── report.pdf
└── test_no_numeric.csv
```

## Stack técnico

El proyecto utiliza las siguientes dependencias principales:

- `pandas` para lectura y procesamiento de datos. 
- `matplotlib` para la generación de gráficos. 
- `reportlab` para construir el PDF. 
- `python-dotenv` para cargar configuración desde variables de entorno. 
- `schedule` para programación diaria o semanal. 
- `openpyxl` para soporte de archivos Excel. 

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/TU-REPOSITORIO.git
cd TU-REPOSITORIO
```

### 2. Crear entorno virtual

#### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Configuración

La configuración del proyecto se maneja por variables de entorno cargadas con `python-dotenv`. 

Crea un archivo `.env` a partir de `.env.example`.

### Variables disponibles

```env
EMAIL_SENDER=
EMAIL_PASSWORD=
EMAIL_RECIPIENTS=
DATA_FILE=sample_data/sales_data.csv
REPORT_TITLE=Reporte Automático
COMPANY_NAME=Mi Empresa
OUTPUT_PDF=output/report.pdf
SCHEDULE_TIME=08:00
```

### Significado de las variables

- `EMAIL_SENDER`: correo del remitente
- `EMAIL_PASSWORD`: contraseña o app password
- `EMAIL_RECIPIENTS`: lista de destinatarios separada por comas
- `DATA_FILE`: ruta del archivo de entrada
- `REPORT_TITLE`: título mostrado en el PDF y asunto del correo
- `COMPANY_NAME`: nombre de empresa mostrado en el encabezado
- `OUTPUT_PDF`: ruta de salida del PDF generado
- `SCHEDULE_TIME`: hora de ejecución programada en formato `HH:MM`

## Uso

### Ejecutar inmediatamente

```bash
python main.py --run-now
```

### Ejecutar con comportamiento por defecto

Si no se pasa ningún argumento, el programa también ejecuta una corrida inmediata. [file:153]

```bash
python main.py
```

### Programar ejecución diaria

```bash
python main.py --schedule daily
```

### Programar ejecución semanal

```bash
python main.py --schedule weekly
```

## Comportamiento validado manualmente

Durante la validación manual del proyecto se confirmaron estos escenarios:

- un dataset numérico genera gráfico y PDF;
- un dataset sin columnas numéricas sigue generando PDF sin romper el flujo
- la generación del PDF no depende del éxito del envío por correo
- la ruta de salida del PDF puede configurarse por entorno en el estado validado del repositorio local;
- el arranque del scheduler funciona en modos diario y semanal;
- un archivo de entrada inexistente produce un error controlado y entendible desde la ejecución principal. 

## Ejemplos de comportamiento

### Caso normal

Con un dataset válido, el flujo puede producir:

- `output/chart.png`
- `output/report.pdf`

Luego, el sistema intenta enviar el PDF por correo.

### Caso sin columnas numéricas

Si el dataset no contiene columnas numéricas:

- el resumen se genera igual;
- el gráfico se omite;
- el PDF se construye igualmente;
- el flujo continúa hasta el intento de envío.

## Decisiones técnicas destacables

Este proyecto fue trabajado con una metodología incremental:

- análisis antes de editar
- cambios pequeños y verificables
- validación manual por bloques
- priorización de robustez antes que complejidad innecesaria

Eso permitió endurecer el flujo sin convertir el proyecto en una solución sobredimensionada para su alcance actual.

## Limitaciones actuales

El proyecto es funcional, pero sigue siendo una solución liviana. Las principales limitaciones actuales son:

- el envío de correo depende de credenciales SMTP válidas
- la observabilidad actual es por consola, no mediante logging estructurado
- la validación del scheduler se realizó en arranque y comportamiento esperado, pero la ejecución productiva a hora real debe comprobarse en el entorno final
- no existen tests automatizados todavía
- la configuración depende mayoritariamente de variables de entorno

## Qué demuestra este proyecto

Desde una perspectiva técnica, este repositorio demuestra:

- diseño modular en Python
- separación de responsabilidades
- automatización de reporting
- generación de artefactos PDF a partir de datos tabulares
- uso práctico de configuración por entorno
- manejo razonable de errores en una pipeline pequeña
- criterio de validación manual antes de publicación

## Posibles mejoras futuras

- incorporar tests automatizados
- agregar logging estructurado
- ampliar la validación de configuración
- mejorar la interfaz de línea de comandos
- soportar otros proveedores o parámetros SMTP
- añadir mayor flexibilidad en configuración de salida y scheduling

## Requisitos

Las dependencias actualmente declaradas son: 

```txt
pandas>=2.2.0
reportlab>=4.0.0
matplotlib>=3.8.0
python-dotenv>=1.0.0
schedule>=1.2.0
openpyxl>=3.1.0
```


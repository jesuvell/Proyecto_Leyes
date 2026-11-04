# 🚀 Modulos de apoyo del portafolio

Esta es una libreria de modulos python comun a todos los proyectos del portafolio.
Contiene modulos para la ingesta, escritura y auditoría automatizada.
Está diseñada bajo principios de arquitectura limpia, patrones de diseño de software y manejo avanzado de archivos.

---

## ✨ Características Principales & Decisiones de Diseño

*   **Arquitectura Orientada a Objetos (Fábricas):** Implementación del patrón *Factory Method* dinámico para instanciar lectores de datos específicos (`ExcelFactory`, `CsvFactory`) según la extensión del archivo, aislando la lógica de negocio de los formatos de origen.
*   **Ingesta Automatizada (Smart Loading):** Detección dinámica y autónoma del archivo más reciente en el directorio de entrada mediante marcas de tiempo del sistema de archivos (`mtime`).
*   **Transaccionalidad en Archivos:** Los archivos procesados se mueven de forma segura mediante operaciones de sistema (`shutil.move`) a un directorio histórico *únicamente* si el pipeline se ejecuta con éxito total (evitando pérdida o duplicación de datos).
*   **Observabilidad Completa (Logging Dinámico):** Sistema de logs en espejo (Consola y Archivo) acoplado al ciclo de vida del script principal (`sys.argv`). Genera trazas cronológicas detalladas por ejecución con formato `[Script]_[YYYYMMDD_HH24MISS].log` para fácil depuración.
*   **Estrategia Solid y Modular:** Separación estricta de responsabilidades en capas aisladas: Extracción (`file_manager`), Limpieza (`df_clean`), Transformación (`df_transformacion_01`) y Orquestación (`pipeline`).

*   **Los modulos de lectura, manejo de archivos y manejo de logs son reutilizables, y fueron diseñados para usarlos en otros proyectos de este mismo portafolio
---

## 🛠️ Stack Tecnológico

*   **Lenguaje:** Python 3.12+
*   **Análisis de Datos:** Pandas
*   **I/O & Sistema de Archivos:** Pathlib, Shutil
*   **Monitoreo:** Logging (Standard Library)

---

## 📂 Estructura del Proyecto

```text
├── utils/
│   ├── __init__.py             # Metodo constructor del proyecto.
│   ├── file_manager.py         # Lógica de detección, carga y movimiento de archivos. 
│   ├── logger_config.py        # Configuración de observabilidad dinámica del proceso de carga.  Se puede reemplazar por Logstash / Grafana Loki/base de datos.
│   ├── dataframe_to_file.py    # Implementación de Fábricas y escritores de archivos de Datos.
│   └── readers.py              # Implementación de Fábricas y Lectores de archivos de Datos.
├── .gitignore                  # Lista de objetos que no se quiere subir a github
└── README.md

---

## ⚙️ Configuración y Ejecución

### 1. Requisitos Previos
Clona el repositorio e instala las dependencias necesarias:
```bash
git clone https://github.com
cd tu-repositorio
pip install pandas openpyxl
```

### 2. Ejecutar el Pipeline
Para inicializar el orquestador y procesar el lote de datos más reciente, ejecuta el script principal:
```bash
No aplica. Estas son invocadas desde los proyectos del portafolio.
```

---

## 📝 Ejemplo de Observabilidad (Logs en Tiempo Real)

Cada ejecución genera automáticamente un diagnóstico limpio y detallado. Ejemplo de salida en consola y archivo `.log`:

```text
2026-09-19 20:20:25,078 [INFO] (file_manager.py:35) - Archivo más reciente detectado automáticamente: 'proyectos_ley_20260918_171249.xlsx'
2026-09-19 20:20:25,120 [INFO] (pipeline.py:27) - --- Fase 1/3: Extracción de datos ---
2026-09-19 20:20:25,845 [INFO] (pipeline.py:29) - Fase 1 Completada. Dimensiones iniciales: (1524, 18)
2026-09-19 20:20:25,850 [INFO] (pipeline.py:32) - --- Fase 2/3: Limpieza de datos ---
2026-09-19 20:20:26,102 [INFO] (file_manager.py:54) - Archivo movido exitosamente a: 'data/procesados/proyectos_ley_20260918_171249.xlsx'
2026-09-19 20:20:26,105 [INFO] (pipeline.py:42) - === [FIN SUCCESSFUL] El Pipeline ha terminado con éxito ===
```

---
💡 **Nota para Reclutadores:** Este proyecto fue construido simulando un ambiente de producción, priorizando la resiliencia al fallo (error handling robusto), el código autodocumentado mediante *type hinting* y la escalabilidad de la arquitectura.


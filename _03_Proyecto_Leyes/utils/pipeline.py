# Importaciones de tus módulos existentes
from _01_Proyecto_Utils.utils.logger_config import setup_logger
from _01_Proyecto_Utils.utils.file_manager import load_most_recent_file
from _01_Proyecto_Utils.utils.dataframe_to_file import export_dataframe
from _03_Proyecto_Leyes.utils.df_clean import limpiar_proyectos
from _03_Proyecto_Leyes.utils.df_transformacion_01 import transformacion_01_proyectos
from pathlib import Path
import pandas as pd

# Inicializamos el logger para el orquestador del pipeline
logger = setup_logger(__name__)

class ETLPipeline:
    #def __init__(self, ruta_datos: Path, ruta_procesados: Path):
    def __init__(self, ruta_datos: Path, ruta_procesados: Path, ruta_temporales: Path, ruta_modelos: Path):
        """
        Inicializa el pipeline con las rutas de entrada y salida de archivos.
        """
        self.ruta_datos = ruta_datos
        self.ruta_procesados = ruta_procesados  # NUEVO: Atributo para almacenar el destino de procesados
        self.ruta_temporales = ruta_temporales  # NUEVO: Atributo para almacenar el destino de temporales
        self.ruta_modelos = ruta_modelos  # NUEVO: Atributo para almacenar el destino de modelos para análisis
        self.df = None

    def run(self) -> pd.DataFrame:
        """
        Ejecuta secuencialmente las fases del Pipeline ETL.
        Interrumpe el flujo de forma segura si ocurre un fallo.
        """
        logger.info("=== [INICIO] Ejecución del Pipeline ETL ===")
        
        try:
            # Fase 1: Extracción (Load) y Movimiento de archivo
            logger.info("--- Fase 1/4: Extracción de datos ---")
            # CAMBIO: Ahora pasa ambos parámetros obligatorios
            self.df = load_most_recent_file(self.ruta_datos, self.ruta_procesados)
            logger.info(f"Fase 1 Completada. Dimensiones iniciales: {self.df.shape}")
            
            # Fase 2: Limpieza (Clean)
            logger.info("--- Fase 2/4: Limpieza de datos ---")
            self.df = limpiar_proyectos(self.df)
            logger.info(f"Fase 2 Completada. Dimensiones post-limpieza: {self.df.shape}")
            
            # Fase 3: Transformación (Transform)
            logger.info("--- Fase 3/4: Transformación de variables ---")
            self.df = transformacion_01_proyectos(self.df)
            logger.info(f"Fase 3 Completada. Columnas finales: {list(self.df.columns)}")
            
            # Fase 4: Exportar Data Frame a archivo parquet (Export)
            logger.info("--- Fase 4/4: Exportación de datos a Parquet ---")
            export_dataframe(
                df=self.df, 
                df_name="proyectos_procesados", 
                location_type="M",  # 'M' para modelos, 'T' para temporales
                file_type="P"       # 'P' para Parquet
            )
            logger.info("Fase 4 Completada. Archivo exportado exitosamente.")
            
            logger.info("=== [FIN SUCCESSFUL] El Pipeline ha terminado con éxito ===")
            return self.df

        except FileNotFoundError as fnf:
            logger.error(f"Fallo en Fase 1: No se encontraron archivos en la ruta proporcionada. {fnf}")
            raise
        except ValueError as ve:
            logger.error(f"Fallo en Fase 2/3: Error de consistencia o validación en los datos. {ve}")
            raise
        except Exception as e:
            logger.exception(f"Fallo crítico inesperado durante la ejecución del Pipeline: {e}")
            raise

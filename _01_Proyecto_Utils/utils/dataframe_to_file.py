from abc import ABC, abstractmethod
from pathlib import Path
import pandas as pd
from _01_Proyecto_Utils.utils.logger_config import setup_logger

# Configuración del Logger
logger = setup_logger(__name__)

# ==========================================
# 1. PRODUCTOS ABSTRACTOS Y CONCRETOS
# ==========================================
class DataExporter(ABC):
    """Producto Abstracto para la exportación de archivos."""
    @abstractmethod
    def export(self, df: pd.DataFrame, path: Path) -> None:
        pass

class CSVExporter(DataExporter):
    """Producto Concreto para CSV."""
    def export(self, df: pd.DataFrame, path: Path) -> None:
        df.to_csv(path, index=False)

class ExcelExporter(DataExporter):
    """Producto Concreto para Excel."""
    def export(self, df: pd.DataFrame, path: Path) -> None:
        df.to_excel(path, index=False)

class ParquetExporter(DataExporter):
    """Producto Concreto para Parquet."""
    def export(self, df: pd.DataFrame, path: Path) -> None:
        df.to_parquet(path, index=False)


# ==========================================
# 2. FÁBRICAS ABSTRACTAS Y CONCRETAS
# ==========================================
class ExporterFactory(ABC):
    """Fábrica Abstracta."""
    @abstractmethod
    def create_exporter(self) -> DataExporter:
        pass

class CSVFactory(ExporterFactory):
    def create_exporter(self) -> DataExporter:
        return CSVExporter()

class ExcelFactory(ExporterFactory):
    def create_exporter(self) -> DataExporter:
        return ExcelExporter()

class ParquetFactory(ExporterFactory):
    def create_exporter(self) -> DataExporter:
        return ParquetExporter()


# ==========================================
# 3. FUNCIÓN PRINCIPAL / CLIENTE
# ==========================================
def export_dataframe(df: pd.DataFrame, df_name: str, location_type: str, file_type: str) -> None:
    """
    Exporta un DataFrame utilizando el patrón Abstract Factory.
    
    :param df: DataFrame de pandas a exportar. Debe tener asignado el atributo 'df.name'.
    :param location_type: 'M' para carpeta modelos, 'T' para carpeta temporales.
    :param file_type: 'C' para CSV, 'X' para Excel, 'P' para Parquet.
    """
    # Mapeo de fábricas y extensiones
    factories = {
        'C': (CSVFactory(), '.csv'),
        'X': (ExcelFactory(), '.xlsx'),
        'P': (ParquetFactory(), '.parquet')
    }
    
    # Raíz del proyecto (directorio donde se encuentra este script)
    root_dir = Path(__file__).resolve().parent.parent
    
    # Mapeo de directorios destino basados en la raíz del proyecto
    directories = {
        'M': root_dir / 'modelos',
        'T': root_dir / 'temporales'
    }
    
    try:
        logger.info(f"Iniciando exportación. Nombre: {df_name}, Tipo: {file_type}, Ubicación: {location_type}")
        
        # 1. Validar y obtener el nombre del DataFrame
        file_name = df_name
        if not file_name:
            raise ValueError("El DataFrame no tiene un nombre asignado en el atributo 'df.name'.")
        
        # 2. Validar tipo de archivo y obtener fábrica junto con su extensión
        if file_type not in factories:
            raise ValueError(f"Tipo de archivo no válido: '{file_type}'. Use 'C', 'X' o 'P'.")
        factory, extension = factories[file_type]
        
        # 3. Validar destino base
        if location_type not in directories:
            raise ValueError(f"Ubicación no válida: '{location_type}'. Use 'M' o 'T'.")
        base_dir = directories[location_type]
        
        # Asegurar que la carpeta destino exista en la raíz del proyecto
        base_dir.mkdir(parents=True, exist_ok=True)
        
        # 4. Construir la ruta final tipo Path (.csv, .xlsx o .parquet)
        final_path = base_dir / f"{file_name}{extension}"
        
        # 5. Instanciar el exportador mediante la fábrica y procesar
        exporter = factory.create_exporter()
        exporter.export(df, final_path)
        
        logger.info(f"Archivo exportado exitosamente en: {final_path}")
        
    except ValueError as ve:
        logger.error(f"Error de validación: {ve}")
        raise
    except Exception as e:
        logger.error(f"Error inesperado al exportar el DataFrame: {e}", exc_info=True)
        raise

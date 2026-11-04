from abc import ABC, abstractmethod
import pandas as pd
from _01_Proyecto_Utils.utils.logger_config import setup_logger

logger = setup_logger(__name__)

class CargaArchivo(ABC):
    @abstractmethod
    def read(self, filepath: str) -> pd.DataFrame:
        pass

class CSVReader(CargaArchivo):
    def read(self, filepath: str) -> pd.DataFrame:
        logger.info(f"Leyendo archivo de texto plano en: {filepath}")
        #return pd.read_csv(filepath, delimiter='\t', keep_default_na=False, skip_blank_lines=False)
        return pd.read_csv(filepath, delimiter=',', keep_default_na=False, skip_blank_lines=False)

class ExcelReader(CargaArchivo):
    def read(self, filepath: str) -> pd.DataFrame:
        logger.info(f"Leyendo archivo Excel en: {filepath}")
        return pd.read_excel(filepath)

class JSONReader(CargaArchivo):
    def read(self, filepath: str) -> pd.DataFrame:
        logger.info(f"Leyendo archivo JSON en: {filepath}")
        return pd.read_json(filepath)

class ParquetReader(CargaArchivo):
    def read(self, filepath: str) -> pd.DataFrame:
        logger.info(f"Leyendo archivo Parquet en: {filepath}")
        return pd.read_parquet(filepath)

class DataFactory(ABC):
    @abstractmethod
    def create_reader(self) -> CargaArchivo:
        pass

class CSVFactory(DataFactory):
    def create_reader(self) -> CargaArchivo: return CSVReader()

class ExcelFactory(DataFactory):
    def create_reader(self) -> CargaArchivo: return ExcelReader()

class JSONFactory(DataFactory):
    def create_reader(self) -> CargaArchivo: return JSONReader()

class ParquetFactory(DataFactory):
    def create_reader(self) -> CargaArchivo: return ParquetReader()

# Diccionario utilitario para mapear la extensión del archivo con su fábrica correspondiente
EXTENSION_MAP = {
    '.csv': CSVFactory(),
    '.tsv': CSVFactory(),
    '.txt': CSVFactory(),
    '.xlsx': ExcelFactory(),
    '.xls': ExcelFactory(),
    '.json': JSONFactory(),
    '.parquet': ParquetFactory()  # Mapeo de la nueva extensión
}

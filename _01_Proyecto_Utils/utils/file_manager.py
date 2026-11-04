import shutil
from pathlib import Path
import pandas as pd
from _01_Proyecto_Utils.utils.logger_config import setup_logger
from _01_Proyecto_Utils.utils.readers import DataFactory, EXTENSION_MAP

logger = setup_logger(__name__)

def load_data(factory: DataFactory, filepath: Path) -> pd.DataFrame:
    """Instancia el lector adecuado a través de la fábrica."""
    reader = factory.create_reader()
    return reader.read(str(filepath))

def load_most_recent_file(directory_path: Path, processed_directory_path: Path) -> pd.DataFrame:
    """
    Busca el archivo más reciente soportado en el directorio, lo procesa,
    y si la carga es exitosa, lo mueve al directorio de procesados.
    """
    logger.info(f"Escaneando directorio para buscar el archivo más reciente: {directory_path}")
    
    if not directory_path.exists() or not directory_path.is_dir():
        raise FileNotFoundError(f"El directorio de entrada no existe o no es válido: {directory_path}")
    
    # Filtrar solo archivos con extensiones soportadas
    archivos_validos = [
        f for f in directory_path.iterdir() 
        if f.is_file() and f.suffix.lower() in EXTENSION_MAP
    ]
    
    if not archivos_validos:
        raise FileNotFoundError(f"No se encontraron archivos válidos soportados en: {directory_path}")
    
    # Encontrar el archivo con la fecha de modificación más alta
    archivo_mas_reciente = max(archivos_validos, key=lambda f: f.stat().st_mtime)
    logger.info(f"Archivo más reciente detectado automáticamente: '{archivo_mas_reciente.name}'")
    
    # Obtener la fábrica correspondiente según la extensión e instanciarla
    extension = archivo_mas_reciente.suffix.lower()
    #factory_class = EXTENSION_MAP[extension]
    #factory = factory_class()
    factory = EXTENSION_MAP[extension]
    
    # Intentar cargar los datos
    df = load_data(factory, archivo_mas_reciente)
    
    # Si la línea anterior no lanza excepción, el archivo se cargó correctamente.
    # Procedemos a moverlo:
    try:
        # Asegurar que el directorio de destino exista (crea carpetas hijas y padres si faltan)
        processed_directory_path.mkdir(parents=True, exist_ok=True)
        
        destino = processed_directory_path / archivo_mas_reciente.name
        
        # Mover el archivo usando shutil (Path.rename puede fallar entre diferentes discos/particiones)
        shutil.move(str(archivo_mas_reciente), str(destino))
        logger.info(f"Archivo movido exitosamente a: '{destino}'")
        
    except Exception as e:
        logger.error(f"El archivo se cargó, pero falló al moverse a procesados: {e}")
        # Opcional: puedes decidir si relanzar el error o permitir que devuelva el DataFrame
        raise e

    return df

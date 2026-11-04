from datetime import datetime
import logging
from pathlib import Path
import sys

def setup_logger(name: str) -> logging.Logger:
    """Configura un logger que duplica las salidas: Consola y Archivo .log dinámico"""
    logger = logging.getLogger(name)
    
    # Evitamos duplicar handlers si la función se llama varias veces en submódulos
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Formato de los mensajes
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] (%(filename)s:%(lineno)d) - %(message)s")
        
        # 1. Handler para Consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # 2. Handler para Archivo Físico Dinámico
        # sys.argv[0] obtiene la ruta completa del script inicial (ej: /ruta/leyes.py)
        script_name = Path(sys.argv[0]).stem  # Extrae solo el nombre sin extensión (ej: 'leyes')
        
        # Generar marca de tiempo en formato YYYYMMDD_HHMISS (ej: 20260919_202403)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Construir nombre final (ej: leyes_20260919_202403.log)
        log_file_name = f"{script_name}_{timestamp}.log"
        log_file_path = Path(log_file_name)
        
        file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    return logger

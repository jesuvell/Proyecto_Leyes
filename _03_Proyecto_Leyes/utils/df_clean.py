import pandas as pd
from _01_Proyecto_Utils.utils.logger_config import setup_logger

logger = setup_logger(__name__)

def limpiar_proyectos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recibe un DataFrame de proyectos de ley, realiza la limpieza de columnas,
    normalización de texto, elimina duplicados y reporta las métricas de registros.
    """
    # Guardamos el número de registros iniciales para la validación
    registros_iniciales = df.shape[0]
    logger.info(f"Iniciando limpieza de datos. Registros iniciales: {registros_iniciales}")

    # Creamos una copia para evitar modificar el DataFrame original (Good Practice)
    dfx = df.copy()

    # 1. Borrado de la columna 'Link del Proyecto' si existe
    if 'Link del Proyecto' in dfx.columns:
        dfx = dfx.drop(columns=['Link del Proyecto'])

    # 2. Renombrado de la lista de columnas
    dfx.columns = [
        'no', 'no_camara', 'No_Senado', 'Fecha_Camara', 'Fecha_Senado', 
        'Proyecto', 'Titulo', 'Objeto_del_proyecto', 'Observaciones', 
        'Tipo_de_Ley', 'Autores', 'Estado_de_Ley', 'Origen_de_Ley', 
        'Comision', 'Legislatura'
    ]

    # 3. Borrado de registros superfluos
    dfx = dfx[dfx['Proyecto'] != 'prueba proyecto de ley']
    dfx = dfx[dfx['Titulo'] != '.. FALLA EN EL APLICATIVO...']

    # 4. Limpieza básica de texto (Minúsculas, tildes, caracteres especiales y espacios múltiples)
    # Tabla de mapeo para reemplazar acentos de forma eficiente en un solo paso
    mapeo_acentos = str.maketrans('áéíóúñ', 'aeioun')
    
    for col in dfx.select_dtypes(include=['object']):
        # Pasamos a minúsculas y quitamos espacios al inicio/final
        dfx[col] = dfx[col].astype(str).str.lower().str.strip()
        
        # Reemplazo rápido de tildes/eñes usando la tabla de mapeo
        dfx[col] = dfx[col].str.translate(mapeo_acentos)
        
        # Limpieza de caracteres y reducción de múltiples espacios a un solo espacio
        dfx[col] = (dfx[col]
                    .str.replace(r'\|', '', regex=True)
                    .str.replace(r';', ',', regex=True)
                    .str.replace(r'\s+', ' ', regex=True))  # \s+ agrupa cualquier cantidad de espacios

    # 5. Eliminación de duplicados
    dfx = dfx.drop_duplicates()

    # 6. Reindexación y conversión de tipo de datos
    dfx = dfx.reset_index(drop=True)  # drop=True evita que el índice viejo se vuelva una columna
    dfx['no_camara'] = dfx['no_camara'].astype(str)

    # Validación final del número de registros
    registros_finales = dfx.shape[0]
    registros_eliminados = registros_iniciales - registros_finales
    
    logger.info(f"Limpieza finalizada exitosamente.")
    logger.info(f"Registros finales: {registros_finales} | Registros eliminados/filtrados: {registros_eliminados}")

    return dfx

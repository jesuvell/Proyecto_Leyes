import pandas as pd
from _01_Proyecto_Utils.utils.logger_config import setup_logger

logger = setup_logger(__name__)

def transformacion_01_proyectos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza la primera fase de transformación y enriquecimiento de variables
    sobre el DataFrame de proyectos de ley, reportando métricas en el log.
    """
    logger.info("Iniciando la transformación de variables (Fase 01)...")
    
    # Trabajamos sobre una copia para no alterar el DataFrame de entrada
    dfx = df.copy()

    # 1. Indicador de presencia de autores
    # Evaluamos si no es nulo, no es string vacío y no contiene solo espacios
    dfx['ind_tiene_Autores'] = dfx['Autores'].apply(
        lambda x: 1 if pd.notna(x) and str(x).strip() != "" else 0
    )

    # 2. Conteo de autores
    # Si es nulo o vacío asignamos 0, de lo contrario contamos por comas
    dfx['no_autores'] = dfx['Autores'].apply(
        lambda x: len(str(x).split(',')) if pd.notna(x) and str(x).strip() != "" else 0
    )

    # 3. Resumen y homologación del Estado de la Ley (Optimizado con mapeo)
    mapeo_estados = {
        'archivado': 'archivado',
        'ley': 'ley',
        'retirado': 'retirado',
        'tramite en comision': 'tramite',
        'tramite en plenaria': 'tramite',
        'tramite en senado': 'tramite',
        'tramite conciliacion': 'tramite',
        'tramite objeciones presidenciales': 'tramite',
        'pendiente ponencia primer debate': 'tramite',
        'pendiente ponencia segundo debate': 'tramite',
        'pendiente por designar ponentes': 'tramite',
        'Acto Legislativo': 'tramite',
        'Acumulado': 'tramite',
        'Debate de Comisión': 'tramite',
        'Debate de plenaria': 'tramite',
        'Revisión corte constitucional': 'tramite',
        'Sanción Presidencial': 'tramite',
        'Solicitud de Audiencia Pública': 'tramite'
    }
    
    # Aplicamos el mapeo rápido y llenamos los no encontrados con 'otros'
    dfx['Estado_Ley_2'] = dfx['Estado_de_Ley'].map(mapeo_estados).fillna('otros')

    # 4. Creación de variables indicadoras (Flags binarios)
    dfx['Ind_Observaciones'] = dfx['Observaciones'].notna().astype(int)
    dfx['Ind_No_Senado'] = dfx['No_Senado'].notna().astype(int)
    
    # 5. Cálculo del indicador compuesto de Senado
    dfx['Ind_Fecha_Senado'] = dfx['Fecha_Senado'].notna().astype(int) * 2
    dfx['Ind_Senado'] = dfx['Ind_No_Senado'] + dfx['Ind_Fecha_Senado']

    # --- Generación de métricas para el Logger ---
    Total_registros = len(dfx)
    con_autores = dfx['ind_tiene_Autores'].sum()
    distribucion_estados = dfx['Estado_Ley_2'].value_counts().to_dict()
    promedio_autores = round(dfx['no_autores'].mean(), 2)

    logger.info("Transformación Fase 01 completada exitosamente.")
    logger.info(f"Métricas calculadas para {Total_registros} registros:")
    logger.info(f"  - Proyectos con autores identificados: {con_autores}")
    logger.info(f"  - Promedio de autores por proyecto: {promedio_autores}")
    logger.info(f"  - Resumen de estados homologados (Estado_Ley_2): {distribucion_estados}")

    return dfx

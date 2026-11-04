from pathlib import Path
from _01_Proyecto_Utils.utils.logger_config import setup_logger
from _03_Proyecto_Leyes.utils.pipeline import ETLPipeline  # Importamos nuestro nuevo pipeline

logger = setup_logger(__name__)

def run():
    # Definición de rutas utilizando Pathlib
    raiz_proyecto = Path(__file__).resolve().parent
    #print(f"\n--- raiz_proyecto ---\n{raiz_proyecto}")
    p_archivo = raiz_proyecto / "_03_Proyecto_Leyes/datos"
    #print(f"\n--- p_archivo ---\n{p_archivo}")
    p_procesado = p_archivo / "procesados"
    #print(f"\n--- p_procesado ---\n{p_procesado}")
    p_temporales = raiz_proyecto / "_03_Proyecto_Leyes/temporales"
    #print(f"\n--- p_temporales ---\n{p_temporales}")
    p_modelos = raiz_proyecto / "_03_Proyecto_Leyes/modelos"
    #print(f"\n--- p_modelos ---\n{p_modelos}")

    # Instanciamos y ejecutamos el Pipeline
    try:
        pipeline = ETLPipeline(ruta_datos=p_archivo, ruta_procesados=p_procesado, ruta_temporales=p_temporales, ruta_modelos=p_modelos)
        df_final = pipeline.run()
        
        # Opcional: Imprimir una muestra corta para verificar en consola
        print("\n--- Vista previa del Dataset final listo para analítica ---")
        print(df_final[['no_camara', 'Estado_Ley_2', 'ind_tiene_Autores', 'no_autores']].head())
        
    except Exception:
        logger.critical("El Pipeline ETL falló. Revisa los mensajes anteriores para identificar la fase del error.")

if __name__ == "__main__":
    run()

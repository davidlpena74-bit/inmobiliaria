import sys
import json
import os

# Añadir el directorio actual al path para importar módulos locales
sys.path.append(os.getcwd())

from scripts.scraper_coldwellbanker import scrape_coldwell_banker
from supabase_utils import insert_propiedad

def deploy(url):
    print(f"--- Iniciando extracción de: {url} ---")
    try:
        data = scrape_coldwell_banker(url)
        if not data:
            print("Error: No se pudo extraer información del inmueble.")
            return

        print(f"Extracción exitosa: {data['titulo']}")
        print(f"Referencia: {data['referencia']}")
        print(f"Agente asignado: {data['agente']}")
        print(f"Imágenes encontradas: {len(data['imagenes_url'])}")

        # Forzar que la propiedad sea pública para la web
        data["publicar_web"] = True
        data["estado_publicacion"] = "Activo"

        print("--- Subiendo a Supabase ---")
        response = insert_propiedad(data)
        
        if response:
            print("--- ¡Éxito! Propiedad integrada correctamente ---")
            print(f"URL Local sugerida: http://localhost:8000/inmueble.html?ref={data['referencia']}")
        else:
            print("Error al insertar en la base de datos.")

    except Exception as e:
        print(f"Error durante la implementación: {e}")

if __name__ == "__main__":
    target = "https://www.coldwellbanker.es/en/javea-xabia/cap-marti-el-tossalet-pinomar/exclusive-renovated-villa-with-panoramic-views-and-absolute-privacy-in-javea"
    if len(sys.argv) > 1:
        target = sys.argv[1]
    
    deploy(target)

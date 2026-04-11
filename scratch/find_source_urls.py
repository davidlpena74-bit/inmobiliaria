import sys
import os

# Añadir el directorio raíz al path
sys.path.append(os.getcwd())

import config
from supabase_utils import SupabaseClient

def get_missing_desc_sources():
    client = SupabaseClient()
    try:
        # Buscar propiedades sin descripción
        res = client.client.table("inm_propiedades").select("id, referencia, url, caracteristicas").or_("descripcion.is.null, descripcion.eq.").execute()
        data = res.data
        
        print(f"Propiedades sin descripción: {len(data)}")
        for r in data:
            ref = r.get('referencia')
            url = r.get('url')
            caract = r.get('caracteristicas', {})
            
            # Buscar la URL original de weperti.com
            # En el scraper anterior vimos que se guarda como 'url' o en 'caracteristicas'
            orig_url = None
            if isinstance(caract, dict):
                orig_url = caract.get('original_url') or caract.get('url')
            
            # Si no está en caracteristicas, ver si el campo 'url' de la DB es de weperti.com
            if not orig_url and url and "weperti.com" in url:
                orig_url = url
            
            print(f"Ref: {ref} | Source URL: {orig_url}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_missing_desc_sources()
